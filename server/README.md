# StyleGAN2 Hypotheses Explorer Server

## Setup

1. This server can only be run on systems with a NVIDIA GPU.
2. Install [Anaconda](https://www.anaconda.com)
3. Create a new virtual environment with the name `stylegan2_hypotheses_explorer` and install the requirements with `conda env create -f env.yml` (you might need to change the pytorch and `cudatoolkit` versions, depending on your setup).
4. Add all generators and evaluators you want to use to the [`models.json`](models.json) file.
   1. The schema for this file is defined [here](schemas/models_schema.json).
   2. The file contains a few example entries. Make sure to remove them before running the server.
   3. Add the real models under `server/resources/generators/DIRNAME/FILENAME.pkl` and `server/resources/evaluators/DIRNAME/FILENAME.pth`
   4. If your evaluator model is not a ResNet18, you need to create a new subclass of `EvaluatorBackend`, similar to `server/stylegan2_hypotheses_explorer/logic/evaluator/resnet18.py`
5. To use the original NVIDIA implementation of the StyleGAN2 (recommended, but uses more restrictive license), clone [this repository](https://github.com/NVlabs/stylegan2-ada-pytorch/) and include it in your `PYTHONPATH` variable (e.g. via `export PYTHONPATH=$PYTHONPATH:/path/to/repo/`)


**Note: in the current version, only the [official NVIDIA implementation](https://github.com/NVlabs/stylegan2-ada-pytorch/) of StyleGAN2 is supported; the inofficial version in `stylegan2_pytorch` may be buggy or not work at all**

### Example

To run the Smiling Detector Experiment, you can download the official StyleGAN2 model from [here](https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl), put it under `server/resources/generators/ffhq/ffhq.pkl` and just keep the original entry in the models file.
The smile detection network is already included in this repo.
Note that the [original NVIDIA implementation](#setup) of the StyleGAN2 is required for this.

If you decide to upload and reconstruct images, the reconstruction will usually take a couple of minutes.

### FairFace Networks
In the paper we also investigate the [FairFace](https://github.com/dchen236/FairFace/) network. To setup, download [their trained models](https://drive.google.com/drive/folders/1B2gAnEpJ6oC9sMkcwS8v5Wk8PtHycHOV), use the `res34_fair_align_multi_720190809.pt` file, and follow the instructions above regarding file location and `models.json`.

## Run

1. Activate the `stylegan2_hypotheses_explorer` environment via `conda activate stylegan2_hypotheses_explorer`
2. Execute `python3 -m stylegan2_hypotheses_explorer` from the `server` directory

Afterwards the API can be reached at `http://localhost:8080/api/v2`.

## Export

1. Activate the `stylegan2_hypotheses_explorer` environment via `conda activate stylegan2_hypotheses_explorer`.
2. Execute `python3 -m stylegan2_hypotheses_explorer --export path/to/export_settings.json` from the `server` directory.
   1. The schema for the `export_settings.json` file can be found [here](schemas/export_schema.json).
   2. An example `export_settings.json` matching the example [`models.json`](models.json) file can be found [here](export_settings.json).

Afterwards the API can be served with a file server (like `nginx` or the node `http-server`) from the exported directory.
