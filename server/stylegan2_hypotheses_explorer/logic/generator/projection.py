try:
    from projector import project as project_nv
    from torch.nn import functional as F
    NV_PROJECTOR_AVAILABLE = True
    print('Using NVIDIA projection implementation')
except ImportError:
    from .invert import invert_image
    NV_PROJECTOR_AVAILABLE = False
    print('Using default projection implementation')


if NV_PROJECTOR_AVAILABLE:
    def project(target, model, device, steps):
        if target.shape[-2:] != (model.img_resolution, model.img_resolution):
            target = F.interpolate(target.view(1, *target.shape), size=model.img_resolution)[0]
        w = project_nv(
            target=target,
            G=model,
            device=device,
            num_steps=steps,
            w_avg_samples=1500,
            initial_learning_rate=0.1,
            initial_noise_factor=0.05,
            lr_rampdown_length=0.25,
            lr_rampup_length=0.05,
            noise_ramp_length=0.75,
            regularize_noise_weight=1e5,
            verbose=True,
            )[-1, :1, :].cpu()
        return w
else:
    def project(target, model, device, steps):
        w = invert_image(
            img=target,
            SG=model,
            opt_noise=True,
            n_steps=steps,
            dev=device,
            lr=0.1,
            init='mean',
            mse_lambda=1.,
            vgg_lambda=1.,
            use_scheduler=True,
        )
        return w
