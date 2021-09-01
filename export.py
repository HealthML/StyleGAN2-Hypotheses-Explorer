import json
import sys
from os import listdir
from pathlib import Path
from shutil import move
from subprocess import run

from server.stylegan2_hypotheses_explorer.logic.paths import resolve_path


def get_export_directory(export_settings_path: str) -> Path:
    with open(export_settings_path, "r") as file:
        export_settings = json.load(file)
    return resolve_path(export_settings["target"], Path(export_settings_path))


def export_models(export_settings_path: str):
    server_dir = (Path(__file__).parent / "server").resolve()
    export_settings_path = str(Path(export_settings_path).absolute())
    run(["python",
         "-m",
         "stylegan2_hypotheses_explorer",
         "--export",
         export_settings_path],
        cwd=str(server_dir),
        shell=True).check_returncode()
    pass


def export_sapper(export_directory: Path):
    client_dir = (Path(__file__).parent / "client").resolve()
    sapper_dir = client_dir / "__sapper__" / "export"
    run(["npm", "run", "export"],
        cwd=str(client_dir), shell=True).check_returncode()
    for file in listdir(str(sapper_dir)):
        move(str(sapper_dir / file), str(export_directory / file))


def export(export_settings_path: str):
    print("#### EXPORTING MODELS... ####")
    export_models(export_settings_path)
    print("#### EXPORTING CLIENT... ####")
    export_sapper(get_export_directory(export_settings_path))
    print("#### DONE ####")


if __name__ == "__main__":
    assert len(sys.argv) == 2
    export_settings_path = sys.argv[1]
    export(export_settings_path)
