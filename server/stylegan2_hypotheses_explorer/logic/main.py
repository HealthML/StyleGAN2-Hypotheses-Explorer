from pathlib import Path

import connexion
from flask_cors import CORS

from ..encoder import JSONEncoder
from .exporter import Exporter
from .model_loader import ModelLoader
from .paths import (API_DIRECTORY_PATH, EXPORT_SCHEMA_PATH, SCHEMAS_PATH,
                    resolve_path)
from .util import load_and_validate

ONLINE_STEP_SIZE = 0.01


class Main:
    def run(self, port=8080):
        ModelLoader(
            step_size=ONLINE_STEP_SIZE,
            offline_mode=False
        ).load_models()
        app = connexion.App(__name__, specification_dir=API_DIRECTORY_PATH)
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', arguments={
            'title': 'StyleGAN2 Interactive Webclient API'},
            pythonic_params=True)
        CORS(app.app)
        app.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(port=port)

    def export(self, path_to_export_settings: Path):
        export_settings = load_and_validate(path_to_export_settings,
                                            EXPORT_SCHEMA_PATH)
        ModelLoader(
            step_size=export_settings["stepSize"],
            offline_mode=True
        ).load_models()
        Exporter(
            root_folder=resolve_path(export_settings["target"], SCHEMAS_PATH),
            generators=[ModelLoader.get_generator(id)
                        for id in export_settings["generators"]],
            evaluators=[ModelLoader.get_evaluator(id)
                        for id in export_settings["evaluators"]]
        ).export()
