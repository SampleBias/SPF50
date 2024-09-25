import logging
from logging.handlers import RotatingFileHandler
from typing import Literal, Dict, Any
from dataclasses import dataclass

# Define the log file path for the ATLAS security fuzzer
LOG_FILE_PATH = "ATLAS-security-fuzzer.log"

# Define valid debug levels
DebugLevel = Literal[0, 1, 2]

@dataclass
class AppConfig:
    """Configuration class for the ATLAS-H Security Fuzzer application."""
    num_workers: int = 4
    debug_level: DebugLevel = 1

@dataclass
class ClientConfig:
    """Configuration class for the client used in attacks."""
    api_key: str
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 150

@dataclass
class AttackConfig:
    """Configuration class for attack parameters."""
    attack_prompts_count: int = 10

    def __post_init__(self):
        if not isinstance(self.attack_prompts_count, int) or self.attack_prompts_count <= 0:
            raise ValueError("attack_prompts_count must be a positive integer")

def setup_logging(debug_level: DebugLevel) -> None:
    """
    Set up logging for the ATLAS Security Fuzzer.

    Args:
        debug_level (DebugLevel): 0 for WARNING, 1 for INFO, 2 for DEBUG
    """
    logging_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }
    logging_level = logging_levels.get(debug_level, logging.WARNING)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s')

    # File Handler
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, 
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Root Logger Configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info(f"ATLAS Security Fuzzer logging initialized at level: {logging.getLevelName(logging_level)}")

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Loaded configuration as a dictionary.
    """
    # Implement configuration loading logic here
    # This could involve reading from a JSON, YAML, or INI file
    # For now, we'll return a dummy configuration
    return {
        "app": AppConfig(),
        "client": ClientConfig(api_key="dummy_key"),
        "attack": AttackConfig()
    }