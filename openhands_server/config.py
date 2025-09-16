
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Dict


# Environment variable name for config file path
CONFIG_FILE_ENV_VAR = "OPENHANDS_SERVER_CONFIG_FILE"

# Default config file location
DEFAULT_CONFIG_FILE = "workspace/openhands_server_sdk_config.json"


@dataclass
class Config:
    session_api_key: str | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary."""
        return cls(
            session_api_key=data.get('session_api_key')
        )


def get_default_config() -> Config:
    """
    Get default configuration by reading from JSON file and applying environment variable overrides.
    
    The config file path is determined by:
    1. Environment variable OPENHANDS_SERVER_CONFIG_FILE
    2. Default location: workspace/openhands_server_sdk_config.json
    
    Environment variable overrides for legacy compatibility:
    - SESSION_API_KEY: overrides session_api_key from config file
    """
    # Determine config file path
    config_file_path = os.getenv(CONFIG_FILE_ENV_VAR, DEFAULT_CONFIG_FILE)
    
    # Initialize with empty config
    config_data: Dict[str, Any] = {}
    
    # Try to read JSON config file
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f) or {}
        except (json.JSONDecodeError, IOError) as e:
            # If config file exists but can't be read, log warning but continue
            print(f"Warning: Could not read config file {config_file_path}: {e}")
    
    # Create config from file data
    config = Config.from_dict(config_data)
    
    # Apply environment variable overrides for legacy compatibility
    if os.getenv('SESSION_API_KEY'):
        config.session_api_key = os.getenv('SESSION_API_KEY')
    
    return config