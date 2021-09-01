import torch
import torch.nn as nn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
from torch.nn import functional as F

from .evaluator_backend import EvaluatorBackend

class FairFace(EvaluatorBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dev = "cuda:0"
        self._model = load_model(path=str(self.trained_model), mode=7, dev=self.dev)

        self.multiplier = 0.25

        self.normalize = transforms.Compose([
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    def rate_image_batch(self, image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        torch.cuda.empty_cache()
        image_batch = F.interpolate(image_batch, size=224)
        if enable_grad:
            return self._model(self.normalize(image_batch))[:, self.output_unit]
        else:
            with torch.no_grad():
                output = torch.tanh(self.multiplier * self._model(self.normalize(image_batch))[:, self.output_unit])
                return output[:, None]

    def rate_style_batch(self, style_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        raise NotImplementedError()
        # if enable_grad:
        #     return self._style_model(style_batch)
        # else:
        #     with torch.no_grad():
        #         return self._style_model(style_batch)

class FairFaceAgeBrackets(FairFace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_unit = 7

    def rate_image_batch(self, image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        torch.cuda.empty_cache()
        image_batch = F.interpolate(image_batch, size=224)
        if enable_grad:
            age_preds = self._model(self.normalize(image_batch))[:, 9:18]
            age_preds = F.softmax(age_preds, dim=1)
            const = torch.tensor([1., 6., 15., 25., 35., 45., 55., 65., 75.])
            age_preds = (age_preds * const).sum(1)
            return age_preds
        else:
            with torch.no_grad():
                age_preds = self._model(self.normalize(image_batch))[:, 9:18]
                age_preds = F.softmax(age_preds, dim=1)
                return age_preds.argmax(1, keepdim=True)

class FairFaceAge(FairFace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_unit = 7

    def rate_image_batch(self, image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        torch.cuda.empty_cache()
        image_batch = F.interpolate(image_batch, size=224)
        if enable_grad:
            age_preds = self._model(self.normalize(image_batch))[:, 9:18]
            age_preds = F.softmax(age_preds, dim=1)
            const = torch.tensor([1., 6., 15., 25., 35., 45., 55., 65., 75.])
            age_preds = (age_preds * const).sum(1)
            return age_preds
        else:
            with torch.no_grad():
                age_preds = self._model(self.normalize(image_batch))[:, 9:18]
                age_preds = F.softmax(age_preds, dim=1)
                const = torch.tensor([1., 6., 15., 25., 35., 45., 55., 65., 75.]).cuda()
                age_preds = (age_preds * const).sum(1)
                return age_preds[:, None]


        # else:
        #     with torch
        # if enable_grad:
        #     return self._model(self.normalize(image_batch))[:, self.output_unit]
        # else:
        #     with torch.no_grad():
        #         output = torch.tanh(self.multiplier * self._model(self.normalize(image_batch))[:, self.output_unit])
        #         return output[:, None]

        # decoded[preds==0] = '0-2'
        # decoded[preds==1] = '3-9'
        # decoded[preds==2] = '10-19'
        # decoded[preds==3] = '20-29'
        # decoded[preds==4] = '30-39'
        # decoded[preds==5] = '40-49'
        # decoded[preds==6] = '50-59'
        # decoded[preds==7] = '60-69'
        # decoded[preds==8] = '70+'
class FairFaceGender(FairFace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_unit = 7

def load_model(path, mode=7, dev="cuda:0"):
    if mode == 7:
        model_fair = torchvision.models.resnet34(pretrained=True)
        model_fair.fc = nn.Linear(model_fair.fc.in_features, 18)
        model_fair.load_state_dict(torch.load(path))
        # model_fair.load_state_dict(torch.load('fair_face_models/fairface_alldata_20191111.pt'))
        model_fair = model_fair.to(dev)
        model_fair.eval()
    elif mode == 4:
        model_fair = torchvision.models.resnet34(pretrained=True)
        model_fair.fc = nn.Linear(model_fair.fc.in_features, 18)
        model_fair.load_state_dict(torch.load('fair_face_models/fairface_alldata_4race_20191111.pt'))
        model_fair = model_fair.to(dev)
        model_fair.eval()
    return model_fair

def pred(model, image, mode=7, dev='cuda:0'):

    image = trans(image)
    image = image.view(1, 3, 224, 224)  # reshape image to match model dimensions (1 batch size)
    image = image.to(dev)

    # fair
    outputs = model(image)
    outputs = outputs.cpu().detach().numpy()
    outputs = np.squeeze(outputs)

    if mode == 7:
        race_outputs = outputs[:7]
        gender_outputs = outputs[7:9]
        age_outputs = outputs[9:18]
        race_score = np.exp(race_outputs) / np.sum(np.exp(race_outputs))
        gender_score = np.exp(gender_outputs) / np.sum(np.exp(gender_outputs))
        age_score = np.exp(age_outputs) / np.sum(np.exp(age_outputs))

        race_pred = np.argmax(race_score)
        gender_pred = np.argmax(gender_score)
        age_pred = np.argmax(age_score)
        return race_pred, gender_pred, age_pred
    elif mode == 4:


        # fair 4 class
        race_outputs = outputs[:4]
        race_score = np.exp(race_outputs) / np.sum(np.exp(race_outputs))
        race_pred = np.argmax(race_score)
        return race_pred

def decode_output(preds, tp='race'):
    decoded = np.zeros(len(preds), dtype='U25')
    if tp == 'race':
        decoded[preds==0] = 'White'
        decoded[preds==1] = 'Black'
        decoded[preds==2] = 'Latino Hispanic'
        decoded[preds==3] = 'East Asian'
        decoded[preds==4] = 'Southeast Asian'
        decoded[preds==5] = 'Indian'
        decoded[preds==6] = 'Middle Eastern'
    if tp == 'race4':
        decoded[preds==0] = 'White'
        decoded[preds==1] = 'Black'
        decoded[preds==2] = 'Asian'
        decoded[preds==3] = 'Indian'
    if tp == 'gender':
        decoded[preds==0] = 'Male'
        decoded[preds==1] = 'Female'
    if tp == 'age':
        decoded[preds==0] = '0-2'
        decoded[preds==1] = '3-9'
        decoded[preds==2] = '10-19'
        decoded[preds==3] = '20-29'
        decoded[preds==4] = '30-39'
        decoded[preds==5] = '40-49'
        decoded[preds==6] = '50-59'
        decoded[preds==7] = '60-69'
        decoded[preds==8] = '70+'
    return decoded


