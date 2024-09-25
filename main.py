import argparse
import logging
from typing import List, Optional

from .config import AppConfig, ClientConfig, AttackConfig, setup_logging
from .fuzzer import execute_fuzzing, get_available_attacks
from .chat import interactive_chat
from .utils import summarize_system_prompts

def parse_arguments():
    parser = argparse.ArgumentParser(description="ATLAS-H Security Fuzzer")
    parser.add_argument('--debug', type=int, choices=[0, 1, 2], default=1,
                        help='Debug level: 0=WARNING, 1=INFO, 2=DEBUG')
    parser.add_argument('--interactive', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('--attack', type=str, choices=get_available_attacks(),
                        help='Specific attack to run')
    parser.add_argument('--system-prompt', type=str,
                        help='System prompt to use for testing')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.debug)
    
    # Load configurations
    app_config = AppConfig()
    client_config = ClientConfig()
    attack_config = AttackConfig()
    
    if args.interactive:
        interactive_mode(app_config, client_config, attack_config)
    else:
        batch_mode(args, app_config, client_config, attack_config)

def interactive_mode(app_config: AppConfig, client_config: ClientConfig, attack_config: AttackConfig):
    logging.info("Starting interactive mode")
    while True:
        system_prompt = input("Enter system prompt (or 'q' to quit): ")
        if system_prompt.lower() == 'q':
            break
        
        attack_type = input("Enter attack type (or press Enter for all): ")
        if not attack_type:
            attack_type = None
        
        execute_fuzzing(app_config, client_config, attack_config, system_prompt, attack_type)
        
        chat_option = input("Do you want to start an interactive chat? (y/n): ")
        if chat_option.lower() == 'y':
            interactive_chat(client_config, system_prompt)

def batch_mode(args, app_config: AppConfig, client_config: ClientConfig, attack_config: AttackConfig):
    logging.info("Starting batch mode")
    system_prompt = args.system_prompt or input("Enter system prompt: ")
    execute_fuzzing(app_config, client_config, attack_config, system_prompt, args.attack)

if __name__ == "__main__":
    main()