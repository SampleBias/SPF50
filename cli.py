from fuzzer import fuzz, generate_stoplight_report, set_target_llm_config
from termcolor import colored
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    logo = """
     ███████╗██████╗ ███████╗███████╗ ██████╗ 
     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔═══██╗
     ███████╗██████╔╝█████╗  ███████╗██║   ██║
     ╚════██║██╔═══╝ ██╔══╝  ╚════██║██║   ██║
     ███████║██║     ██║     ███████║╚██████╔╝
     ╚══════╝╚═╝     ╚═╝     ╚══════╝ ╚═════╝ 
    """
    print(colored(logo, "cyan"))
    print(colored("SPF50 - LLM Security Testing Tool", "yellow"))
    print(colored("Remember to Wear Sunscreen", "yellow"))
    print()

def print_welcome_message():
    print("Welcome to the LLM Security Screening Tool")
    print("This tool helps assess the security of Large Language Models (LLMs)")
    print("by testing their responses to potentially malicious inputs.")
    print("\nPress Enter to continue...")
    input()

def main_menu():
    while True:
        clear_screen()
        print_logo()
        print("\nMain Menu:")
        print("1. Start Fuzzing")
        print("2. Configure Target LLM")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            start_fuzzing()
        elif choice == '2':
            configure_target_llm()
        elif choice == '3':
            print("Thank you for using SPF50. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)

def configure_target_llm():
    clear_screen()
    print_logo()
    print("\nConfigure Target Large Language Model (LLM)")
    llm_name = input("Enter the name of the Target LLM: ")
    api_endpoint = input("Enter the API endpoint for the Target LLM: ")
    api_key = input("Enter the API key for the Target LLM: ")
    set_target_llm_config(llm_name, api_endpoint, api_key)
    print("\nTarget LLM configuration updated.")
    input("Press Enter to continue...")

def start_fuzzing():
    clear_screen()
    print_logo()
    print("\nStarting Fuzzing Process")
    print("This process will test the security of the configured Large Language Model (LLM)")
    
    num_iterations = int(input("Enter the number of iterations: "))
    mode = input("Choose mode (1: Automated, 2: Manual): ")
    
    automated = (mode == '1')
    
    attack_results = fuzz(num_iterations, automated)
    
    print(colored("\n--- Fuzzing Summary ---", "cyan", attrs=["bold"]))
    print(f"Total iterations: {num_iterations}")
    print("\nVulnerability Assessment:")
    print(generate_stoplight_report(attack_results))
    print("\nRecommendations:")
    print("1. Address any 'Red' vulnerabilities immediately")
    print("2. Investigate and mitigate 'Yellow' vulnerabilities")
    print("3. Continue monitoring 'Green' areas for potential future vulnerabilities")
    print("4. Conduct tests for any 'White' (untested) attack types")
    
    print("\nFuzzing complete. Press Enter to return to the main menu...")
    input()

def main():
    clear_screen()
    print_logo()
    print_welcome_message()
    main_menu()

if __name__ == "__main__":
    main()
