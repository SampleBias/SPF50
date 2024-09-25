import logging
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

import colorama
from prompt_toolkit import prompt as prompt_toolkit_prompt, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from .config import ClientConfig

# Initialize colorama for cross-platform colored output
colorama.init()

# Color constants
RESET = colorama.Style.RESET_ALL
BRIGHT = colorama.Style.BRIGHT
BRIGHT_BLUE = colorama.Fore.BLUE + BRIGHT
BRIGHT_RED = colorama.Fore.RED + BRIGHT
BRIGHT_ORANGE = colorama.Fore.YELLOW + BRIGHT

# Set up logging
logger = logging.getLogger(__name__)

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

MessageList = List[Message]

class ClientBase(ABC):
    @abstractmethod
    def interact(self, history: MessageList, messages: MessageList) -> str:
        pass

class FakeChatClient(ClientBase):
    def interact(self, history: MessageList, messages: MessageList) -> str:
        return "FakeChat response"

class ClientLangChain(ClientBase):
    def __init__(self, config: ClientConfig):
        self.config = config
        # Initialize LangChain client here

    def interact(self, history: MessageList, messages: MessageList) -> str:
        history.extend(messages)
        try:
            # Implement LangChain interaction here
            response = "LangChain response"  # Placeholder
            history.append(Message("assistant", response))
            return response
        except Exception as e:
            logger.warning(f"Chat inference failed with error: {e}")
            raise

class ChatSession:
    def __init__(self, client: ClientBase, system_prompts: Optional[List[str]] = None):
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

        result = self.client.interact(self.history, input_messages)
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
    client = ClientLangChain(client_config)
    chat_session = ChatSession(client, [system_prompt])

    print(f"{BRIGHT_BLUE}Starting interactive chat. Type 'exit' to end the session.{RESET}")
    while True:
        user_input = text_input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = chat_session.say(user_input)
        print(f"{BRIGHT_ORANGE}Assistant: {response}{RESET}")

    print(f"{BRIGHT_BLUE}Chat session ended.{RESET}")