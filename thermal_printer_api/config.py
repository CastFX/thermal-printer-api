"""Configuration management for thermal printer API."""

import json
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class PrinterConfig(BaseModel):
    """Printer configuration model."""

    type: str = "EPSON"
    interface: str = "/dev/usb/lp0"
    width: int = 60
    timeout: int = 5000
    idVendor: int = 0x0FE6
    idProduct: int = 0x811E
    in_ep: int = 0x82
    out_ep: int = 0x02


class Settings(BaseSettings):
    """Application settings."""

    port: int = 3000
    host: str = "0.0.0.0"
    log_level: str = "info"

    class Config:
        env_file = ".env"


def get_config_path() -> Path:
    """Get path to printer configuration file."""
    return Path(__file__).parent.parent / "printer-config.json"


def load_printer_config() -> PrinterConfig:
    """Load printer configuration from JSON file."""
    config_path = get_config_path()

    try:
        if config_path.exists():
            with open(config_path, "r") as f:
                config_data = json.load(f)
                config_data["idVendor"] = int(config_data["idVendor"], 16)
                config_data["idProduct"] = int(config_data["idProduct"], 16)
                config_data["in_ep"] = int(config_data["in_ep"], 16)
                config_data["out_ep"] = int(config_data["out_ep"], 16)
            return PrinterConfig(**config_data)
    except Exception as e:
        print(f"Warning: Error loading printer config, using defaults: {e}")

    return PrinterConfig()


def save_printer_config(config: PrinterConfig) -> bool:
    """Save printer configuration to JSON file."""
    config_path = get_config_path()

    try:
        with open(config_path, "w") as f:
            json.dump(config.model_dump(), f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving printer config: {e}")
        return False


settings = Settings()
