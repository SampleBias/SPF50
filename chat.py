import logging
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

import colorama
from prompt_toolkit import prompt as prompt_toolkit_prompt, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from config import ClientConfig
from some_module import InteractiveChat  # Add this import statement

# Initialize colorama for cross-platform colored output
colorama.init()

# Color constants
RESET = colorama.Style.RESET_ALL
BRIGHT = colorama.Style.BRIGHT
BRIGHT_BLUE = colorama.Fore.BLUE + BRIGHT
BRIGHT_RED = colorama.Fore.RED + BRIGHT
BRIGHT_ORANGE = colorama.Fore.LIGHTYELLOW_EX + BRIGHT

# Set up logging
logger = logging.getLogger(__name__)

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

MessageList = List[Message]

class ChatClient(ABC):
    """Abstract base class for chat clients."""

    def __init__(self, config: ClientConfig):
        self.config = config

    @abstractmethod
    def interact(self, messages: List[Dict[str, Any]], new_message: Dict[str, Any]) -> str:
        """Interact with the chat client."""
        pass

class FakeChatClient(ChatClient):
    def interact(self, messages: List[Dict[str, Any]], new_message: Dict[str, Any]) -> str:
        return "FakeChat response"

class ClientLangChain(ChatClient):
    def __init__(self, config: ClientConfig):
        self.config = config
        # Initialize LangChain client here

    def interact(self, messages: List[Dict[str, Any]], new_message: Dict[str, Any]) -> str:
        messages.append(new_message)
        try:
            # Implement LangChain interaction here
            response = "LangChain response"  # Placeholder
            messages.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logger.warning(f"Chat inference failed with error: {e}")
            raise

class LangChainClient(ChatClient):
    """LangChain chat client implementation."""

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        # Initialize LangChain client here

    def interact(self, messages: List[Dict[str, Any]], new_message: Dict[str, Any]) -> str:
        messages.append(new_message)
        try:
            # Implement LangChain interaction here
            response = "LangChain response"  # Placeholder
            messages.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logger.warning(f"LangChain interaction failed with error: {e}")
            raise

class ChatSession:
    def __init__(self, client: ChatClient, system_prompts: Optional[List[str]] = None):
        self.client = client
        self.history: MessageList = []
        self.system_prompts: Optional[List[Message]] = None
        if system_prompts:
            self.system_prompts = [Message("system", prompt) for prompt in system_prompts]

    def say(self, user_prompt: str) -> str:
        logger.debug(f"say: system_prompt={self.system_prompts}")
        logger.debug(f"say: prompt={user_prompt}")

        input_messages: MessageList = []
        if not self.history and self.system_prompts:
            input_messages.extend(self.system_prompts)
        input_messages.append(Message("user", user_prompt))

        result = self.client.interact([msg.__dict__ for msg in self.history], input_messages[-1].__dict__)
        logger.debug(f"say: result={result}")
        return result

def text_input(prompt_text: str, initial_text: str = "") -> str:
    bindings = KeyBindings()
    
    @bindings.add('c-m')  # Enter key
    def _(event):
        event.app.exit(result=event.app.current_buffer.text)

    try:
        return prompt_toolkit_prompt(
            HTML(f"<prompt>{prompt_text}</prompt>"),
            default=initial_text,
            multiline=False,
            key_bindings=bindings,
            style=Style.from_dict({
                'prompt': 'fg:orange',
            }),
        )
    except KeyboardInterrupt:
        logger.info("Edit cancelled by user.")
        print(f"{BRIGHT_RED}Edit cancelled by user.{RESET}")
        return initial_text

def interactive_chat(client_config: ClientConfig, system_prompt: str):
    chat_client = LangChainClient(client_config)
    chat_interface = InteractiveChat(chat_client, system_prompt)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        messages = [{"role": "user", "content": user_input}]
        response = chat_interface.interact(chat_interface.history, messages)
        print(f"Assistant: {response}")

def main():
    # Your main program logic here
    pass

if __name__ == "__main__":
    try:
        main()
        print("Program executed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")