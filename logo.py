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

logo = """
   _____ _____  ______   ______ _                ____  
  / ____|  __ \|  ____| |  ____(_)              / __ \ 
 | (___ | |__) | |__    | |__   ___   _____    | |  | |
  \___ \|  ___/|  __|   |  __| | \ \ / / _ \   | |  | |
  ____) | |    | |      | |    | |\ V /  __/   | |__| |
 |_____/|_|    |_|      |_|    |_| \_/ \___|    \____/ 
                                                       
           LLM Vulnerability Fuzzer
"""

def print_logo():
    print(logo)

# Usage example
if __name__ == "__main__":
    print_logo()