from os.path import isabs
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent.resolve()

MODELS_PATH = ROOT_PATH / "models.json"

CACHE_PATH = ROOT_PATH / "resources" / ".cache"
CACHE_PATH.mkdir(parents=True, exist_ok=True)

SCHEMAS_PATH = ROOT_PATH / "schemas"
EXPORT_SCHEMA_PATH = SCHEMAS_PATH / "export_schema.json"
GENERATOR_SETTINGS_SCHEMA_PATH = SCHEMAS_PATH / "generator_settings_schema.json"
MODELS_SCHEMA_PATH = SCHEMAS_PATH / "models_schema.json"

API_DIRECTORY_PATH = str(
    ROOT_PATH / "stylegan2_hypotheses_explorer" / "swagger")


def resolve_path(relative_or_absolute_path: str, working_directory: Path) -> Path:
    if isabs(relative_or_absolute_path):
        return Path(relative_or_absolute_path).resolve()
    else:
        return (working_directory / Path(relative_or_absolute_path)).resolve()
