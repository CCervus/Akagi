import json
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path


ROOT = Path(".")

CONFIG_PATH = ROOT / "configs" / "akagi.json"


@dataclass
class Config:
    @dataclass
    class XMLRPCClient:
        max_ping_count: int = 10
        refresh_interval: float = 0.05

    xmlrpc_client: XMLRPCClient = field(default_factory=lambda: Config.XMLRPCClient())

    @classmethod
    def fromdict(cls, data: dict):
        try:
            for field in fields(cls):
                if is_dataclass(field.type) and field.name in data:
                    data[field.name] = field.type(**data[field.name])
            return cls(**data)
        except (TypeError, KeyError):
            print("Configuration file is outdated, please delete it manually")
            raise


if CONFIG_PATH.exists():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = Config.fromdict(json.load(f))
else:
    config = Config()
with CONFIG_PATH.open("w", encoding="utf-8") as f:
    json.dump(asdict(config), f, indent=2, ensure_ascii=False)