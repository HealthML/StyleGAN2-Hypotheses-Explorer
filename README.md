# StyleGAN2 Hypotheses Explorer

![Build](https://github.com/martingraf4/StyleGAN2-Hypotheses-Explorer/workflows/Export/badge.svg?branch=master)

This repository implements the StyleGAN2 Hypotheses Explorer, a framework to interactively explore an image classifier's decision boundary. 


## Setup

1. [Setup the server](server/README.md#Setup).
2. [Setup the client](client/README.md#Setup).

## Run

1. [Start the server](server/README.md#Run).
2. [Start the client](client/README.md#Run).

## Export

The StyleGAN2 Hypotheses Explorer can be exported into a format which only requires a file server (at the moment it can only be served from the root directory of a domain. See [here](client/README.md#Export-to-Subdirectory) on how to configure serving from a subdirectory manually).

1. Configure the export process by creating an `export_settings.json` file as described [here](server/README.md#Export).
2. Activate the `stylegan2_hypotheses_explorer` environment via `conda activate stylegan2_hypotheses_explorer`.
3. Run `python export.py path/to/export_settings.json`.

After running the export script the exported version (including client and server) can be found in the directory specified in the `export_settings.json`.
