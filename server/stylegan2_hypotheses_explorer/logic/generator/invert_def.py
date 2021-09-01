import numpy as np
from tqdm import tqdm

import click

import PIL
from PIL import ImageDraw
import stylegan2_pytorch as sg2

import torch
from torchvision import models
from torchvision import transforms

def crop_resize(img, size=256):
    w, h = img.size
    wh = min(w, h)
    img = transforms.CenterCrop(wh)(img)
    img = img.resize((size, size))
    return img

def tfm(img, size=256):
    return transforms.ToTensor()(img).cuda()

def invert_image(
        img,
        SG,
        opt_noise=True,
        n_steps=100,
        latent_dim=512,
        dev='cuda:0',
        lr=0.05,
        init='mean',
        mse_lambda=1.,
        vgg_lambda=0.,
        use_scheduler=False,
        normalize=True,
        reg_noise=0.,
        noise_lr=0.05,
        ):
    get_av(SG, latent_dim)
    if init == 'mean':
        style = torch.tensor(SG.av, device=dev)[None]
        style.requires_grad_(True)
        # style = torch.tensor([SG.av for _ in range(7)], device=dev, requires_grad=True)
    elif init == 'rand':
        style_noise = torch.randn(1, 512).cuda()
        style = SG.GAN.SE(style_noise)
        style.requires_grad_(True)
    noise = sg2.stylegan2_pytorch.image_noise(1, img.shape[-1], dev)
    if opt_noise:
        noise.requires_grad_(True)
        optim = torch.optim.Adam(
            [
                {'params': style, 'lr': lr}, 
                {'params': noise, 'lr': noise_lr},
                ],
                lr=lr,
                )
        if use_scheduler:
            scheduler = torch.optim.lr_scheduler.OneCycleLR(optim, max_lr=lr, total_steps=n_steps)


    else:
        optim = torch.optim.Adam([style], lr=lr)


    if vgg_lambda > 0:
        eval_model = models.vgg16(pretrained=True).cuda().eval()
        out1 = []
        hook1 = eval_model.features[0].register_forward_hook(
                lambda mod, inp, out: out1.append(out))
        out2 = []
        hook2 = eval_model.features[2].register_forward_hook(
                lambda mod, inp, out: out2.append(out))
        out3 = []
        hook3 = eval_model.features[14].register_forward_hook(
                lambda mod, inp, out: out3.append(out))
        out4 = []
        hook4 = eval_model.features[21].register_forward_hook(
                lambda mod, inp, out: out4.append(out))

    mse_L = -1
    vgg_L = -1
    pbar = tqdm(range(n_steps))
    for step in pbar:
        optim.zero_grad()
        gen_img = generate_truncated(
                SG,
                style.repeat(7, 1, 1),
                noise,
                psi=1,
                latent_dim=latent_dim,
                )

        difference = 0.
        if mse_lambda > 0:
            mse_L = mse_loss(gen_img, img)
            difference += mse_lambda * mse_L
        if vgg_lambda > 0:
            vgg_L = vgg_loss(gen_img, img, eval_model, out1, out2, out3, out4)
            difference += vgg_lambda * vgg_L
        if reg_noise > 0:
            difference += reg_noise * (noise**2).mean()
        pbar.set_description(
                f'current loss: {difference.item():.5f} -- mse: {mse_L:.5f}; vgg: {vgg_L:.5f}'
                )
        difference.backward()
        optim.step()
        if normalize:
            with torch.no_grad():
                normalize_noise(noise)
        if use_scheduler:
            scheduler.step()

    if vgg_lambda > 0:
        hook1.remove()
        hook2.remove()
        hook3.remove()
        hook4.remove()

    style = style.detach()
    noise = noise.detach()
    return to_pil(gen_img), style, noise

def normalize_noise(noise):
    noise -= noise.mean()
    noise /= (noise**2).mean()**0.5

def to_pil(img):
    return transforms.ToPILImage()(img.detach().cpu()[0])

def mse_loss(I1, I2):
    return ((I1 - I2)**2).mean()

def vgg_loss(I1, I2, model, out1, out2, out3, out4):
    tfm = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    _ = model(tfm(I1))
    O11 = out1.pop()
    O12 = out2.pop()
    O13 = out3.pop()
    O14 = out4.pop()
    _ = model(tfm(I2.unsqueeze(0)))
    O21 = out1.pop()
    O22 = out2.pop()
    O23 = out3.pop()
    O24 = out4.pop()
    diff = (
            ((O11 - O21)**2).mean()
         + ((O12 - O22)**2).mean()
         + ((O13 - O23)**2).mean()
         + ((O14 - O24)**2).mean()
         )
    return diff

def get_av(SG, latent_dim=512):
    z = sg2.stylegan2_pytorch.noise(2000, latent_dim, device=SG.rank)
    samples = sg2.stylegan2_pytorch.evaluate_in_chunks(SG.batch_size, SG.GAN.SE, z).cpu().numpy()
    SG.av = np.mean(samples, axis=0)
    SG.av = np.expand_dims(SG.av, axis=0)

def generate_truncated(SG, style, noise, psi=1., latent_dim=512):
    w_space = []
    for tensor in style:
        av_torch = torch.from_numpy(SG.av).cuda(SG.rank)
        tmp = psi * (tensor - av_torch) + av_torch
        w_space.append((tmp, 1))

    w_styles = sg2.stylegan2_pytorch.styles_def_to_tensor(w_space)
    generated_images = sg2.stylegan2_pytorch.evaluate_in_chunks(
            SG.batch_size, SG.GAN.GE, w_styles, noise)
    return generated_images.clamp_(0., 1.)