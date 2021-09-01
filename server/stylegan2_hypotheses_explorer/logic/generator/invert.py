import torch
from torchvision import models, transforms
from tqdm import tqdm


def crop_resize(img, size=256, dev='cuda:0'):
    img = transforms.ToPILImage()(img)
    w, h = img.size
    wh = min(w, h)
    img = transforms.CenterCrop(wh)(img)
    img = img.resize((size, size))
    return transforms.ToTensor()(img).to(dev)


def invert_image(
        img,
        SG,
        opt_noise=False,
        n_steps=100,
        dev='cuda:0',
        lr=0.01,
        init='mean',
        mse_lambda=1.,
        vgg_lambda=1.,
        use_scheduler=True,
):
    if init == 'mean':
        w_avg = SG.mapping.w_avg
        style = torch.tensor(w_avg, device=dev)[None].reshape(1, 1, -1)
        style.requires_grad_(True)
    elif init == 'rand':
        z = torch.randn(1, SG.z_dim).cuda()
        with torch.no_grad():
            style = SG.mapping(z, None)[:, :1, :]

        style.requires_grad_(True)
    if opt_noise:
        named_buffers = dict(
            (name, buf) for name, buf in SG.synthesis.named_buffers()
            if 'noise_const' in name
        )
        params = [style]
        for buf in named_buffers.values():
            buf = torch.randn_like(buf)
            buf.requires_grad = True
            params.append(buf)
        optim = torch.optim.Adam(params, lr=lr)
        if use_scheduler:
            scheduler = torch.optim.lr_scheduler.OneCycleLR(
                optim, max_lr=lr, total_steps=n_steps)

    else:
        optim = torch.optim.Adam([style], lr=lr)
        if use_scheduler:
            scheduler = torch.optim.lr_scheduler.OneCycleLR(
                optim, max_lr=lr, total_steps=n_steps)

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

    img = crop_resize(img, size=256, dev=dev)
    mse_L = -1
    vgg_L = -1
    pbar = tqdm(range(n_steps))
    for step in pbar:
        optim.zero_grad()
        gen_img = generate_truncated(SG, style.repeat(
            1, SG.num_ws, 1), noise_mode='const')
        gen_img = transforms.Resize(256)(gen_img)

        difference = 0.
        if mse_lambda > 0:
            mse_L = mse_loss(gen_img, img)
            difference += mse_lambda * mse_L
            # difference += mse_lambda * mse_loss(gen_img, img)
        if vgg_lambda > 0:
            vgg_L = vgg_loss(gen_img, img, eval_model, out1, out2, out3, out4)
            difference += vgg_lambda * vgg_L
        pbar.set_description(
            f'current loss: {difference.item():.5f} -- mse: {mse_L:.5f}; vgg: {vgg_L:.5f}')
        difference.backward()
        optim.step()

        if use_scheduler:
            scheduler.step()

    hook1.remove()
    hook2.remove()
    hook3.remove()
    hook4.remove()

    style = style.detach().cpu()
    return style


def normalize_buffers(buffers):
    for buf in buffers.values():
        buf -= buf.mean()
        buf /= (buf**2).mean()**0.5


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


def generate_truncated(SG, style, noise_mode='const'):
    gen_image = SG.synthesis(style, noise_mode=noise_mode)
    gen_image = (0.5 * gen_image + 0.5).clamp(0, 1)
    return gen_image
