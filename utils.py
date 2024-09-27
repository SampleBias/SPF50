import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Iterable
import threading
from tqdm import tqdm
import colorama

# Initialize colorama for cross-platform colored output
colorama.init()

# Color constants
RESET = colorama.Style.RESET_ALL
LIGHTBLUE = colorama.Fore.LIGHTBLUE_EX
RED = colorama.Fore.RED

logger = logging.getLogger(__name__)

@dataclass
class TestLogEntry:
    """A single test step log entry."""
    prompt: str
    response: Optional[str]
    success: bool
    additional_info: str

    def __str__(self) -> str:
        return (f"TestLog(prompt={self.prompt}, response={self.response}, "
                f"success={self.success}, additional_info='{self.additional_info}')")

@dataclass
class TestStatus:
    """Represents the current status of a test."""
    test_name: str
    status: str
    details: str = ""

@dataclass
class StatusUpdate:
    """Represents an update in the test status."""
    test_name: str
    action: str
    progress_position: int
    progress_total: int

class TestBase(ABC):
    """Base class for all test implementations."""

    def __init__(self, client_config, attack_config):
        self.client_config = client_config
        self.attack_config = attack_config
        self.test_name = self.__class__.__name__
        self.log: List[TestLogEntry] = []

    @abstractmethod
    def run(self) -> Iterable[StatusUpdate]:
        """Run the test and yield status updates."""
        pass

class ProgressWorker:
    """Manages progress for a single worker."""

    def __init__(self, worker_id: int, progress_bar: bool = False):
        self.worker_id = worker_id
        self.progress_bar = tqdm(disable=not progress_bar)

    def update(self, task_name: str, progress: int, total: int, colour: str = "white"):
        self.progress_bar.set_description(f"{task_name}")
        self.progress_bar.total = total
        self.progress_bar.n = progress
        self.progress_bar.colour = colour
        self.progress_bar.refresh()

class WorkProgressPool:
    # Your WorkProgressPool implementation here
    pass

def summarize_system_prompts(client, system_prompts: List[str]) -> str:
    """
    Summarize a list of system prompts using the provided client.

    Args:
        client: The chat client to use for summarization.
        system_prompts (List[str]): List of system prompts to summarize.

    Returns:
        str: A short (up to 5 words) representation of the idea behind the system prompts.
    """
    separator = "----------------------------------"
    user_message = f"""
    Analyze the following system prompts for an LLM system and provide a concise summary.
    Format your response as a single sentence using "verb + noun" structure, with a maximum of 5 words.

    System prompts:
    {separator}
    {separator.join(system_prompts)}
    {separator}
    """
    return client.interact([], [{"role": "user", "content": user_message}])

"""
Results Table Module for SPF50 Security Fuzzer

This module provides functionality to create and print formatted tables
for displaying test results. It uses colorama for colored output and
PrettyTable for table formatting.
"""

from typing import List, Optional, Any
import colorama
from prettytable import PrettyTable, SINGLE_BORDER

# Initialize colorama for cross-platform colored output
colorama.init()

# Color constants
RESET = colorama.Style.RESET_ALL
BRIGHT = colorama.Style.BRIGHT
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
BRIGHT_YELLOW = colorama.Fore.LIGHTYELLOW_EX + BRIGHT

def print_table(title: str, headers: List[str], data: List[List[Any]], footer_row: Optional[List[Any]] = None) -> None:
    """
    Print a formatted table with the given title, headers, data, and optional footer.

    Args:
        title (str): The title of the table.
        headers (List[str]): List of column headers.
        data (List[List[Any]]): 2D list containing the table data.
        footer_row (Optional[List[Any]]): Optional list for the footer row.
    """
    print(f"{BRIGHT}{title}{RESET} ...")
    
    table = PrettyTable(
        field_names=[f"{BRIGHT}{h}{RESET}" for h in headers],
        align="l"
    )
    table.set_style(SINGLE_BORDER)

    for row in data:
        table.add_row([str(item) for item in row])

    if footer_row:
        table.add_row(footer_row)

    # Simulate a footer line separated from the header and body
    table_lines = table.get_string().split("\n")
    if footer_row:
        # Insert the header-body separator line above the last (footer) row
        separator_line = table_lines[2]
        table_lines = table_lines[:-2] + [separator_line] + table_lines[-2:]

    for line in table_lines:
        print(line)

# Test function to demonstrate usage
def run_test():
    """Run a test to demonstrate the usage of the print_table function."""
    PASSED = f"{GREEN}✔{RESET}"
    FAILED = f"{RED}✘{RESET}"
    ERROR = f"{BRIGHT_YELLOW}⚠{RESET}"

    # Test case 1: Table without footer
    print_table(
        title="Test results simulated",
        headers=["", "Test", "Successful", "Unsuccessful", "Score (1-10)"],
        data=[
            [PASSED, "Test 1 (good)", 1, 0, 10],
            [FAILED, "Test 2 (bad)", 0, 1, 0],
            [ERROR, "Test 3 (with errors)", 5, 0, 5],
        ]
    )

    print("\n")  # Add some spacing between tables

    # Test case 2: Table with footer
    print_table(
        title="Test results simulated with footer",
        headers=["", "Test", "Successful", "Unsuccessful", "Score (1-10)"],
        data=[
            [PASSED, "Test 1 (good)", 1, 0, 10],
            [FAILED, "Test 2 (bad)", 0, 1, 0],
            [ERROR, "Test 3 (with errors)", 5, 0, 5],
        ],
        footer_row=[FAILED, "Total", 6, 1, 5.5]
    )

if __name__ == "__main__":
    run_test()