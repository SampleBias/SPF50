import sys
import os
import argparse

# Add the current directory and its parent to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from SPF50.fuzzer import Fuzzer, get_available_attacks

def main():
    parser = argparse.ArgumentParser(description='SPF50 Fuzzer')
    parser.add_argument('--target', type=str, required=True, help='Target URL to fuzz')
    parser.add_argument('--attack', type=str, choices=get_available_attacks(), help='Specific attack to run')
    parser.add_argument('--model', type=str, default='llama3.2', help='Model to use for attack generation')
    parser.add_argument('--list-attacks', action='store_true', help='List available attacks and exit')

    args = parser.parse_args()

    if args.list_attacks:
        print("Available attacks:", ", ".join(get_available_attacks()))
        return

    fuzzer = Fuzzer(model=args.model)
    
    if args.attack:
        result = fuzzer.fuzz(args.target, args.attack)
        print(f"Attack: {args.attack}")
        print(f"Target: {args.target}")
        print(f"Result: {result}")
    else:
        print(f"Running all available attacks against {args.target}")
        results = fuzzer.fuzz_all(args.target)
        for result in results:
            print(f"Attack: {result['attack_type']}")
            print(f"Result: {result}")
            print("---")

if __name__ == "__main__":
    main()
