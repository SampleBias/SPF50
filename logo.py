"""
SPF50 Logo Module for Healthcare LLM Security Fuzzer

This module provides a function to print a colorful ASCII art logo
for the SPF50 Security Fuzzer project, focused on Healthcare LLMs.
"""

import colorama

# Initialize colorama for cross-platform colored output
colorama.init()

# Color constants
RESET = colorama.Style.RESET_ALL
WHITE = colorama.Fore.WHITE
CYAN = colorama.Fore.CYAN

def print_logo():
    """Print the SPF50 Security Fuzzer logo."""
    logo = r"""
    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║   ███████╗██████╗ ███████╗███████╗ ██████╗         ║
    ║   ██╔════╝██╔══██╗██╔════╝██╔════╝██╔═████╗        ║
    ║   ███████╗██████╔╝█████╗  ███████╗██║██╔██║        ║
    ║   ╚════██║██╔═══╝ ██╔══╝  ╚════██║████╔╝██║        ║
    ║   ███████║██║     ██║     ███████║╚██████╔╝        ║
    ║   ╚══════╝╚═╝     ╚═╝     ╚══════╝ ╚═════╝         ║
    ║                                                    ║
    ║             Bow Down to the Fuzz                   ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
    """

    # Color mapping for easy modification
    color_map = {
        '█': WHITE,
        '─': CYAN,
        '│': CYAN,
        '╔': CYAN,
        '╗': CYAN,
        '╚': CYAN,
        '╝': CYAN,
    }

    # Apply colors to the logo
    colored_logo = ''.join(color_map.get(char, '') + char + RESET for char in logo)
    
    print(colored_logo)

# Usage example
if __name__ == "__main__":
    print_logo()