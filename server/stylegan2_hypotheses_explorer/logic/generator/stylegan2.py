import json
from functools import cached_property
from shutil import rmtree
from typing import Dict, List, Tuple, Union

import numpy as np
import torch
from PIL import Image
import stylegan2_pytorch
from stylegan2_pytorch import stylegan2_pytorch as sg2
from .invert_def import invert_image, crop_resize, tfm


import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import pickle
from tqdm import tqdm

from ...models import Generator as GeneratorModel
from ...models import GeneratorSettings, StyleConfiguration
from ..evaluator import EvaluatorBackendT
from ..paths import GENERATOR_SETTINGS_SCHEMA_PATH
from ..util import load, load_and_validate
from .generator_backend import GeneratorBackend

from .projection import project

INTELLIGENT_STYLE_GEN_ITERATIONS = 25
PROJECTION_STEPS = 1000
# RESIZE_IMAGES = False
RESIZE_IMAGES = 256


class StyleGAN2Official(GeneratorBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.width != self.height:
            raise ValueError(
                "Output resolution for StyleGAN2 must be square")

        self._img_size = self.width
        self._psi = 0.85
        self._model = None
        self._load_generator()
        self._load_or_generate_styles() 

    @property
    def computed_layer_count(self):
        return self.model.number_of_layers - self.model.settings.reduce_number_of_layers_by

    def _load_or_generate_styles(self) -> List[List[torch.Tensor]]:
        try:
            if self._generated_styles_are_valid():
                self.styles = torch.load(
                    str(self.styles_cache_path)).to(self.dev)
        except Exception:
            pass
        self.generate_new_styles(self.model)

    def _move_style(self, style, lam=1.):
        print('in move style')
        alpha = self._optimizer()._style_model.weight.data
        alpha = style.norm() * alpha / alpha.norm()
        print(f'alpha norm: {alpha.norm():.2f}, style norm: {style.norm():.2f}')
        labels = self._optimizer().rate_style_batch(style[None], enable_grad=False)
        print(f'labels:', labels.item())
        if labels.item() > 0:
            lam = -lam
        print(lam)
        return style + lam*alpha

    def _generate_styles(self, amount: int):
        style_images = self._styles_from_images()
        if style_images is not None:
            z = torch.randn(amount,
                                self._model.z_dim).to(self.dev)
            with torch.no_grad():
                styles = self._model.mapping(z, None)
            w_avg = self._model.mapping.w_avg
            styles = w_avg + self._psi * (styles - w_avg)

            if self.model.settings.optimize_styles is not None:
                ws = []
                for target_img in style_images[:amount]:
                    t = torch.from_numpy(np.array(target_img)).permute(2, 0, 1)
                    w = self._project(t).to(self.dev).detach()
                    ws.append(w)
                    ws.append(self._move_style(w, lam=0.15))
            else:
                ws = []
                for target_img in style_images[:amount]:
                    t = torch.from_numpy(np.array(target_img)).permute(2, 0, 1)
                    w = self._project(t).to(self.dev).detach()
                    ws.append(w)
            if amount > len(ws):
                styles = torch.cat([torch.cat(ws), styles[:(amount-len(ws)), 0, :]])
            else:
                styles = torch.cat(ws)
                
            return styles.view(amount, 1, -1)
        else:
            z = torch.randn(amount,
                                self._model.z_dim).to(self.dev)
            with torch.no_grad():
                styles = self._model.mapping(z, (torch.rand(len(z), 10)>0.5).float().cuda())
            w_avg = self._model.mapping.w_avg
            styles = w_avg + self._psi * (styles - w_avg)
            return styles[:, :1, :]

    def generate_new_styles(self, model: GeneratorModel):
        self.model = model
        rmtree(str(self.cache_path))
        num_styles = self.model.settings.num_gen_styles_per_layer
        if not self.model.settings.use_same_styles_for_all_layers:
            num_styles *= self.computed_layer_count
        gen_styles = self._generate_styles(num_styles)

        if self.model.settings.use_same_styles_for_all_layers:
            self.styles = [gen_styles for _ in range(
                self.computed_layer_count)]
        else:
            self.styles = [gen_styles[self.model.settings.num_gen_styles_per_layer * layer:
                                      self.model.settings.num_gen_styles_per_layer * (layer + 1)]
                           for layer in range(self.computed_layer_count)]
        self.settings_cache_path.write_text(json.dumps(self.model.settings.to_dict(),
                                                       indent=4))
        torch.save(self.styles, str(self.styles_cache_path))
    
    def _style_configuration_to_style(self, style_configuration: StyleConfiguration) -> List[torch.Tensor]:
        if style_configuration.single_style is not None:
            style = style_configuration.single_style
            return [self.styles[style.layer][style.id]
                    for _ in range(self.model.number_of_layers)]
        else:
            num_backend_layers_per_layer = self.model.number_of_layers // self.computed_layer_count
            styles_with_one_layer_more = self.model.number_of_layers % self.computed_layer_count
            layer = 0

            combined_style = []
            for layer_style in style_configuration.style_array:
                style1 = self.styles[layer][int(layer_style.style1)]
                style = style1
                if layer_style.style2 is not None and layer_style.proportion_style1 is not None:
                    proportion_style1 = layer_style.proportion_style1
                    proportion_style2 = 1 - proportion_style1
                    style2 = self.styles[layer][int(layer_style.style2)]
                    style = style1 * proportion_style1 + style2 * proportion_style2

                num_backend_layers = num_backend_layers_per_layer
                if layer < styles_with_one_layer_more:
                    num_backend_layers += 1
                layer += 1

                combined_style.extend(style for _ in range(num_backend_layers))
            return combined_style

    def _generate_images(self, styles: List[torch.Tensor], with_grad=False, reload=False) -> torch.Tensor:
        torch.cuda.empty_cache()
        try:
            if with_grad:
                gen_images = torch.cat([self._model.synthesis(s[None], noise_mode='const') for s in styles])
                gen_images = (0.5 * gen_images + 0.5).clamp(0, 1)
            else:
                with torch.no_grad():
                    gen_images = torch.cat([self._model.synthesis(s[None], noise_mode='const') for s in styles])
                gen_images = (0.5 * gen_images + 0.5).clamp(0, 1)
        except RuntimeError:
            self._load_generator()
            if not reload:
                return self._generate_images(styles, with_grad, reload=True)
            else:
                raise RuntimeError('reload failed')
        torch.cuda.empty_cache()

        return gen_images

    def generate_images(self, styles: List[StyleConfiguration]) -> torch.Tensor:
        torch.cuda.empty_cache()
        styles = [torch.cat(self._style_configuration_to_style(style))
                  for style in styles]
        styles = torch.stack(styles)
        gen_images = self._generate_images(styles, with_grad=False)
        if RESIZE_IMAGES:
            gen_images = F.interpolate(gen_images, size=(RESIZE_IMAGES, RESIZE_IMAGES), mode='area')
        return gen_images

    def _load_generator(self):
        del self._model
        torch.cuda.empty_cache()
        with open(self.trained_model, 'rb') as f:
            self._model = pickle.load(f)['G_ema'].to(self.dev)
        torch.cuda.empty_cache()

    def _project(self, target: torch.Tensor):
        torch.cuda.empty_cache()
        w = project(target=target, model=self._model, device=self.dev, steps=PROJECTION_STEPS)
        self._load_generator()
        return w

class StyleGAN2(GeneratorBackend):
    '''currently buggy'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.width != self.height:
            raise ValueError(
                "Output resolution for StyleGAN2 must be square")

        self._img_size = self.width
        self._psi = 0.75
        self._moving_average = True
        self._model = sg2.ModelLoader(base_dir=self.trained_model, name='default').model
        self._load_or_generate_styles()

    @property
    def computed_layer_count(self):
        return self.model.number_of_layers - self.model.settings.reduce_number_of_layers_by

    def generate_new_styles(self, model: GeneratorModel):
        self.model = model
        rmtree(str(self.cache_path))
        num_styles = self.model.settings.num_gen_styles_per_layer
        if not self.model.settings.use_same_styles_for_all_layers:
            num_styles *= self.computed_layer_count
        gen_styles = self._generate_styles(self._optimizer(),
                                           self._styles_from_images(),
                                           num_styles)

        if self.model.settings.use_same_styles_for_all_layers:
            self.styles = [gen_styles for _ in range(
                self.computed_layer_count)]
        else:
            print('not using same style for all layers?')
            raise NotImplementedError()
            self.styles = [gen_styles[self.model.settings.num_gen_styles_per_layer * layer:
                                      self.model.settings.num_gen_styles_per_layer * (layer + 1)]
                           for layer in range(self.computed_layer_count)]
        self.settings_cache_path.write_text(json.dumps(self.model.settings.to_dict(),
                                                       indent=4))
        torch.save(self.styles, str(self.styles_cache_path))

    def generate_images(self, styles: List[StyleConfiguration]) -> torch.Tensor:
        noises = [self._style_configuration_to_style(style)[1]
                  for style in styles]
        styles = [self._style_configuration_to_style(style)[0]
                  for style in styles]
        styles = [(torch.cat(batch, 0), 1) for batch in zip(*styles)]
        noises = [(torch.stack(batch, 0), 1) for batch in zip(*noises)]
        with torch.no_grad():
            gen_images = self._generate_images(styles, noises)
        return gen_images

    ########################################

    def _generate_styles(self, optimizer: Union[None, EvaluatorBackendT], styles_from_images: Union[None, List[Image.Image]], amount: int):
        if styles_from_images:
            styles = self._get_styles_from_images(styles_from_images, amount)
        else:
            styles = self._randomly_create_styles(amount)
        styles = [styles[0].to(self.dev), styles[1].to(self.dev)]
        if optimizer is not None:
            self._optimize_styles(styles, optimizer)
        return styles

    def _get_styles_from_images(self, images: List[Image.Image], amount: int) -> torch.Tensor:
        styles = []
        noises = []
        for img in images:
            _, style, noise = invert_image(
                tfm(crop_resize(img)),
                self._model,
                n_steps=10000,
                save_gif=False,
                opt_noise=False,
                normalize=False,
                reg_noise=0.,
                lr=0.05,
                noise_lr=0.0,
                )
            styles.append(style)
            noises.append(noise)
        styles = torch.cat(styles)
        noises = torch.cat(noises)
        if len(images) < amount:
            more_styles = self._randomly_create_styles(amount - len(images))
            styles = torch.cat([styles, more_styles[0].cuda()])
            noises = torch.cat([noises, more_styles[1].cuda()])
        # self.__noises = noises
        print(styles.shape)
        print(noises.shape)
        return [styles, noises]

    def _randomly_create_styles(self, amount: int) -> torch.Tensor:
        style_noise = torch.randn(amount, self._model.GAN.G.latent_dim).to(self.dev)
        style = self._model.GAN.SE(style_noise).view(amount, 1, -1)
        noise = sg2.image_noise(amount, self._img_size, self.dev)
        print('random styles:', style.shape)
        return [style, noise]
        # style_noise = torch.randn(amount, 1, self._model.GAN.G.latent_dim)
        # return torch.randn(amount,
        #                    1,
        #                    self._model.GAN.G.latent_dim)

    def _load_or_generate_styles(self) -> List[List[torch.Tensor]]:
        try:
            if self._generated_styles_are_valid():
                self.styles = torch.load(
                    str(self.styles_cache_path)).to(self.dev)
        except Exception:
            pass
        self.generate_new_styles(self.model)

    @cached_property
    def _settings_schema(self) -> Dict:
        return load(GENERATOR_SETTINGS_SCHEMA_PATH)

    def _generated_styles_are_valid(self) -> bool:
        try:
            gen_settings_dict = load_and_validate(self.settings_cache_path,
                                                  self._settings_schema)
            gen_settings = GeneratorSettings.from_dict(gen_settings_dict)
            return self.model.settings == gen_settings
        except Exception:
            return False

    ########################################

    def _style_configuration_to_style(self, style_configuration: StyleConfiguration) -> List[torch.Tensor]:
        if style_configuration.single_style is not None:
            style = style_configuration.single_style
            # print(len(self.styles))
            # print(self.styles[0])
            # print(self.styles[1])
            # print(self.styles[2])
            comb_style = [self.styles[style.layer][0][style.id]
                    for _ in range(self.model.number_of_layers)]
            comb_noise = [self.styles[style.layer][1][style.id]
                    for _ in range(self.model.number_of_layers)]
            return [comb_style, comb_noise]
        else:
            num_backend_layers_per_layer = self.model.number_of_layers // self.computed_layer_count
            styles_with_one_layer_more = self.model.number_of_layers % self.computed_layer_count
            layer = 0

            combined_style = []
            combined_noise = []
            for layer_style in style_configuration.style_array:
                style1 = self.styles[layer][0][int(layer_style.style1)]
                noise1 = self.styles[layer][1][int(layer_style.style1)]
                style = style1
                noise = noise1
                if layer_style.style2 is not None and layer_style.proportion_style1 is not None:
                    proportion_style1 = layer_style.proportion_style1
                    proportion_style2 = 1 - proportion_style1
                    style2 = self.styles[layer][0][int(layer_style.style2)]
                    noise2 = self.styles[layer][1][int(layer_style.style2)]
                    style = style1 * proportion_style1 + style2 * proportion_style2
                    noise = noise1 * proportion_style1 + noise2 * proportion_style2

                num_backend_layers = num_backend_layers_per_layer
                if layer < styles_with_one_layer_more:
                    num_backend_layers += 1
                layer += 1

                combined_style.extend(style for _ in range(num_backend_layers))
                combined_noise.extend(noise for _ in range(num_backend_layers))
            return [combined_style, combined_noise]

    ###################################

    def _generate_images(self, styles: List[Tuple[torch.Tensor, int]], noises) -> torch.Tensor:
        print('generate images:')
        print(type(styles), type(noises))
        print(len(styles), len(noises))
        noise = sg2.image_noise(len(styles[0][0]), self._img_size, self.dev)
        print(noise.shape)
        # print(self.__noises.shape)
        # noise = self.__noises[:1].repeat(len(styles[0][0]), 1, 1, 1)
        # print(self.__noises.shape, len(styles))
        # noise = self.__noises[0][None].repeat(len(styles[0][0]), 1, 1, 1)
        # noise = self.__noises[0]
        imgs = generate_truncated(self._model, styles, noise, noises, trunc_psi=1., batch_size=self.batch_size)

        # imgs = generate_truncated(self._model,
        #                           self._model.GAN.SE if self._moving_average else self._model.GAN.S,
        #                           self._model.GAN.GE if self._moving_average else self._model.GAN.G,
        #                           styles,
        #                           noise,
        #                           trunc_psi=1,
        # )
        #                         #   self._psi)
        return imgs

    def _optimize_styles(self, styles: torch.Tensor, evaluator: EvaluatorBackendT):
        optim = torch.optim.Adam([styles],
                                 lr=0.009,
                                 eps=1e-7,
                                 weight_decay=0.0001)
        to_evaluator_size = torch.nn.Upsample(
            size=(evaluator.height, evaluator.width),
            mode="bilinear", align_corners=False)
        for _ in range(INTELLIGENT_STYLE_GEN_ITERATIONS):
            optim.zero_grad()
            images = self._generate_images([(styles.squeeze(1), 7)])
            images = to_evaluator_size(images)
            ratings = evaluator.rate_image_batch(images, True)
            ratings = ratings * torch.sign(ratings) * -1
            ratings.sum().backward()
            optim.step()

###############################################################

# Copied from StyleGAN2 source version 1.2.5
# Using generate_truncated directly does not produce a gradient


def exists(val):
    return val is not None


def noise(n, latent_dim, device):
    return torch.randn(n, latent_dim).cuda(device)


def evaluate_in_chunks(max_batch_size, model, *args):
    split_args = list(
        zip(*list(map(lambda x: x.split(max_batch_size, dim=0), args))))
    chunked_outputs = [model(*i) for i in split_args]
    if len(chunked_outputs) == 1:
        return chunked_outputs[0]
    return torch.cat(chunked_outputs, dim=0)


def styles_def_to_tensor(styles_def):
    return torch.cat([t[:, None, :].expand(-1, n, -1) for t, n in styles_def], dim=1)


def generate_truncated(SG, style, noi, noises, trunc_psi=1., batch_size=4):
    # w_space = []
    # for tensor in style:
    #     av_torch = torch.from_numpy(SG.av).cuda(SG.rank)
    #     if trunc_psi < 1:
    #         tmp = trunc_psi * (tensor - av_torch) + av_torch
    #     else:
    #         tmp = tensor
    #     w_space.append((tmp, 1))

    if not exists(SG.av):
        z = noise(2000, 512, device=SG.rank)
        samples = evaluate_in_chunks(batch_size, SG.GAN.SE, z).cpu().numpy()
        SG.av = np.mean(samples, axis=0)
        SG.av = np.expand_dims(SG.av, axis=0)
    w_space = []
    noise_vec = torch.zeros_like(noises[0][0])
    full = 0
    for (tensor, num_layers), (tt, nl) in zip(style, noises):
        # print(tensor.shape, num_layers, tt.shape, nl)
        av_torch = torch.from_numpy(SG.av).cuda(SG.rank)
        if trunc_psi < 1:
            tmp = trunc_psi * (tensor - av_torch) + av_torch
        else:
            tmp = tensor
        w_space.append((tmp, num_layers))
        # print(tt[0,0].flatten())
        noise_vec += nl * tt
        full += nl
    noise_vec /= full
    # print(noise_vec[0,0].flatten())
    # print(noi[0,0].flatten())
    
    w_styles = sg2.styles_def_to_tensor(w_space)
    generated_images = sg2.evaluate_in_chunks(batch_size, SG.GAN.GE, w_styles, noi)
    # generated_images = sg2.evaluate_in_chunks(batch_size, SG.GAN.GE, w_styles, noi)
    return generated_images.clamp(0., 1.)


# def generate_truncated(self, S, G, style, noi, trunc_psi=0.75, num_image_tiles=8):
#     latent_dim = G.latent_dim

#     if not exists(self.av):
#         z = noise(2000, latent_dim, device=self.rank)
#         samples = evaluate_in_chunks(self.batch_size, S, z).cpu().numpy()
#         self.av = np.mean(samples, axis=0)
#         self.av = np.expand_dims(self.av, axis=0)

#     w_space = []
#     for tensor, num_layers in style:
#         tmp = S(tensor)
#         av_torch = torch.from_numpy(self.av).cuda(self.rank)
#         tmp = trunc_psi * (tmp - av_torch) + av_torch
#         w_space.append((tmp, num_layers))

#     w_styles = styles_def_to_tensor(w_space)
#     generated_images = evaluate_in_chunks(self.batch_size, G, w_styles, noi)
#     return generated_images.clamp_(0., 1.)
