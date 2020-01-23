from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import datasets, transforms
from torchvision.transforms.functional import pad as TorchPad, to_tensor


class Resize2(object):
    '''
    Resize object along LONGER border (tarnsforms.Resize works along smaller border)
    '''

    def __init__(self, new_max_size, interpolation=Image.NEAREST):
        self.new_max_size = new_max_size
        self.interpolation = interpolation

    def __call__(self, img):
        old_size = img.size[:2]
        ratio = float(self.new_max_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        return img.resize(new_size, resample=self.interpolation)


class SquarePad(object):
    '''
    Square img by extending smaller border to longer border size and filling empty space
    '''

    def __init__(self, sqr_size, padding_mode="reflect"):
        self.sqr_size = sqr_size
        self.padding_mode = padding_mode

    def __call__(self, img):
        old_size = img.size[:2]
        pad_size = [0, 0]
        pad_size.extend([self.sqr_size - x for x in old_size])
        return TorchPad(img, tuple(pad_size), padding_mode=self.padding_mode)



MAX_SIZE = 500
color_mean = [0.485, 0.456, 0.406]
color_std = [0.229, 0.224, 0.225]

transformations = transforms.Compose([
        Resize2(MAX_SIZE),
        SquarePad(MAX_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(color_mean, color_std)
    ])


def preprocess_image(image):
    image = transformations(image).float()
    shp = image.shape
    image = image.reshape([1, shp[0], shp[1], shp[2]])
    image.requires_grad = True
    return image


def predict_single_image(file):
    classes = ['blank', 'non_blank']
    X = preprocess_image(file)
    device = torch.device("cpu")
    model = torch.load("model.pkl", map_location=device)
    model.eval()
    out = model(X)
    out = F.softmax(out, dim=1)
    _, pred = torch.max(out, 1)
    label = str(classes[int(pred)])
    return label

