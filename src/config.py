from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib  # type: ignore
# 配置文件路径
cfg =  Path("config/settings.toml")

with cfg.open("rb") as f:
    data = tomllib.load(f)

def get_options(section):
    """
    读取配置属性
    :param section: 配置节名
    """
    return data.get(section)
