import torch
from torch import nn
from torchvision import models
from torchvision import transforms
from torch.nn import functional as F

from .evaluator_backend import EvaluatorBackend


class ResNet18(EvaluatorBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dev = "cuda:0"
        self._model = models.resnet18()
        self._model.fc = torch.nn.Linear(512, 1)
        self._model.load_state_dict(torch.load(str(self.trained_model),
                                               map_location='cpu'))
        self._model.eval()
        self._model.to(self.dev)

        self.img_size = 256


        try:
            self._style_model = nn.Linear(512, 1)
            # self._style_model = nn.Sequential(nn.Linear(512, 1), nn.Sigmoid())
            pth = '.'.join(str(self.trained_model).split('.')[:-1]) + '-latent.pt'
            print(f'latent model: {pth}')
            self._style_model.load_state_dict(torch.load(pth, map_location='cpu'))
            self._style_model.eval()
            self._style_model.to(self.dev)
            self._latent_model_available = True
        except:
            self._latent_model_available = False
            print('no latent model available')

        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        self.normalize = transforms.Normalize(mean, std)
        self.multiplier = 1.
        # self.multiplier = 0.25

        for mod in self._model.modules():
            if hasattr(mod, 'inplace'):
                mod.inplace = False

    def rate_image_batch(self, image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        torch.cuda.empty_cache()
        if enable_grad:
            image_batch = F.interpolate(image_batch, size=self.img_size)
            return self._model(self.normalize(image_batch))
        else:
            with torch.no_grad():
                image_batch = F.interpolate(image_batch, size=self.img_size)
                return torch.tanh(self.multiplier * self._model(self.normalize(image_batch)))

    def rate_style_batch(self, style_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        if not self._latent_model_available:
            return None
        if enable_grad:
            return self._style_model(style_batch)
        else:
            with torch.no_grad():
                return self._style_model(style_batch)