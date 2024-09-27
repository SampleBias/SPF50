import sys
import json
from attacks import generate_attack_payload, analyze_response_with_ollama
from logo import print_logo

def get_available_attacks():
    return [
        'prompt_injection',
        'data_extraction',
        'model_behavior_manipulation',
        'output_manipulation',
        'denial_of_service'
    ]

def print_menu(options):
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

def get_user_choice(prompt, options):
    while True:
        print_menu(options)
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print_logo()  # This line ensures the logo is printed at the start
    print("Welcome to the LLM Vulnerability Fuzzer CLI")

    # Attack selection
    attacks = get_available_attacks()
    selected_attack = get_user_choice("Select an attack type: ", attacks)
    print(f"Selected attack: {selected_attack}")

    # Generate Payload
    print("\nGenerating payload...")
    payload = generate_attack_payload(selected_attack)
    print("\nGenerated Payload:")
    print(payload)

    # Get LLM Response
    print("\nUse the above payload with your target LLM.")
    llm_response = input("Paste the target LLM's response here: ")

    # Analyze Response
    print("\nAnalyzing response...")
    analysis_result = analyze_response_with_ollama(selected_attack, llm_response)

    # Display Results
    print("\nAnalysis Result:")
    print(json.dumps(analysis_result, indent=2))

    print(f"\nVulnerability Score: {analysis_result.get('vulnerability_score', 'N/A')}")

    if analysis_result.get('vulnerability_detected', False):
        print("\nWARNING: Potential vulnerability detected!")
    else:
        print("\nNo obvious vulnerabilities detected.")

    print("\nExploit Suggestions:")
    for suggestion in analysis_result.get('exploit_suggestions', []):
        print(f"- {suggestion}")

    print("\nDefense Analysis:")
    print(analysis_result.get('defense_analysis', 'No defense analysis available'))

    print("\nRecommended Next Steps:")
    for step in analysis_result.get('next_steps', []):
        print(f"- {step}")

if __name__ == "__main__":
    main()
