import logging
import os
import yaml
from pathlib import Path
from deepmerge import always_merger
import copy


logger = logging.getLogger(__name__)
CONFIG_ROOT = Path("data/config")
_DEFAUL_CONFIG_PATH = Path("module/conf/application-template.yml").resolve()
try:
    from module.__version__ import VERSION
except ImportError:
    logger.info("Can't find version info, use DEV_VERSION instead")
    VERSION = "DEV_VERSION"


CONFIG_PATH = (
    CONFIG_ROOT / "application-dev.yml"
    if VERSION == "DEV_VERSION"
    else CONFIG_ROOT / "application.yml"
).resolve()

config = {}

def _load_config():
    global config
    if CONFIG_PATH.exists():
        _load()
    else:
        _init()


def _load():
    global config
    with open(_DEFAUL_CONFIG_PATH, "r", encoding='utf-8') as file:
        _default_config = yaml.safe_load(file.read())
    with open(CONFIG_PATH, "r", encoding='utf-8') as file:
        _config = yaml.safe_load(file.read())
    # 使用实际配置的覆盖default的
    always_merger.merge(_default_config, _config)
    # 回写配置
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(_default_config, file, default_flow_style=False, sort_keys=False)
    config.update(copy.deepcopy(_default_config))

def _init():
    global config
    with open(_DEFAUL_CONFIG_PATH, "r", encoding='utf-8') as file:
        _config = yaml.safe_load(file.read())
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(_config, file, default_flow_style=False, sort_keys=False)
    config = _config

def reload():
    _load()

def save(_config):
    global config
    config.update(copy.deepcopy(_config))
    # 回写配置
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)
    logger.info("Save config and write to config file success")


if config.__len__() == 0:
    # 加载配置
    _load_config()
