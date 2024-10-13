import logging
import colorama
import os
from typing import List, Dict, Union

colorama.init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Colored formatter class for adding colors to log levels."""

    COLORS = {
        "DEBUG": colorama.Fore.BLUE,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.RED + colorama.Back.WHITE,
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{colorama.Style.RESET_ALL}"


class CustomLogger(logging.Logger):
    """
    CustomLogger class sets up a logger with colored console output and file output.
    """

    def __init__(self, name: str, level=logging.INFO, log_folder="logs"):
        """
        Initializes the logger with a name, log level, and log folder for file output.

        :param name: Name of the logger
        :param level: Logging level (default is INFO)
        :param log_folder: Folder to save log files (default is 'logs')
        """
        super().__init__(name, level)

        # Avoid adding multiple handlers to the logger if they already exist
        if not self.hasHandlers():
            self._initialize_logger(level, log_folder)

    def _initialize_logger(self, level, log_folder):
        """
        Initializes the logger with both console and file handlers.
        """
        self.setLevel(level)
        self.propagate = False

        # Setup console handler with colored output
        self._add_console_handler(level)

        # Setup file handler
        self._add_file_handler(level, log_folder)

    def _add_console_handler(self, level):
        """
        Adds a console handler with colored formatting to the logger.

        :param level: Logging level for the console output
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(
            ColoredFormatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.addHandler(console_handler)

    def _add_file_handler(self, level, log_folder):
        """
        Adds a file handler for saving log messages to a file.

        :param level: Logging level for the file output
        :param log_folder: Folder to save log files
        """
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file_path = os.path.join(log_folder, f"{self.name}.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.addHandler(file_handler)

    def prominent_log(self, message: str, level=logging.INFO, box_width=60):
        """
        Logs a prominent message inside a box for better visibility, with box characters
        depending on the logging level.

        :param message: The message to log prominently.
        :param level: The logging level for this message (default is INFO).
        :param box_width: The width of the box (default is 60 characters).
        """

        if level == logging.DEBUG:
            border_char = "#"
        elif level == logging.INFO:
            border_char = "-"
        elif level == logging.WARNING:
            border_char = "!"
        elif level == logging.ERROR:
            border_char = "*"
        elif level == logging.CRITICAL:
            border_char = "="
        else:
            border_char = "#"

        border = border_char * box_width
        padded_message = (
            f"{border_char*2} {message.center(box_width - 6)} {border_char*2}"
        )

        self.log(level, border)
        self.log(level, padded_message)
        self.log(level, border)

    def highlighted_log(self, message: str, level=logging.INFO, box_width=60):
        """
        Logs a highly visible message with multiple box borders for emphasis.

        :param message: The message to log prominently.
        :param level: The logging level for this message (default is INFO).
        :param box_width: The width of the box (default is 60 characters).
        """
        border_char = "#"
        double_border = border_char * box_width
        single_border = "=" * box_width
        padded_message = (
            f"{border_char*2} {message.center(box_width - 6)} {border_char*2}"
        )

        self.log(level, double_border)
        self.log(level, single_border)
        self.log(level, padded_message)
        self.log(level, single_border)
        self.log(level, double_border)

    def subtle_log(self, message: str, level=logging.INFO, box_width=60):
        """
        Logs a subtle message with minimal formatting.

        :param message: The message to log subtly.
        :param level: The logging level for this message (default is INFO).
        :param box_width: The width of the box (default is 60 characters).
        """
        border_char = "."
        border = border_char * box_width
        padded_message = f"{message.center(box_width)}"

        self.log(level, border)
        self.log(level, padded_message)
        self.log(level, border)

    def log_related_keywords(self, keyword: str, related_keywords: List[str]):
        """
        Logs related keywords line by line using info level.

        :param keyword: The original keyword
        :param related_keywords: List of related keywords
        """
        self.info(f"Related search keywords for '{keyword}':")

        if related_keywords:
            for i, related_keyword in enumerate(related_keywords, 1):
                self.info(f"{i}. {related_keyword}")
        else:
            self.info("No related keywords found.")

    def log_heading_results(self, results: List[Dict[str, Union[str, List[str]]]]):
        """
        Logs the heading extraction results in a formatted manner.

        :param results: List of dictionaries containing URL, h2, and h3 headings
        """
        for i, result in enumerate(results, 1):
            self.info(f"\nArticle {i}:")
            self.info(f"URL: {result['url']}")
            self.info("h2 Headings:")
            for h2 in result["h2"]:
                self.info(f"  - {h2}")
            self.info("h3 Headings:")
            for h3 in result["h3"]:
                self.info(f"  - {h3}")

    def log_keywords_results(
        self,
        results: Dict[str, List[str]],
        result_type: str = "Related Search Keywords",
    ):
        """
        Logs the results in a formatted manner.

        :param results: A mapping of keywords to results
        :param result_type: Type of result (e.g., "Related Search Keywords" or "Headings")
        """
        self.info(f"\nResults for {result_type}:")
        for keyword, items in results.items():
            self.info(f"Results for keyword '{keyword}' ({result_type}):")
            if items:
                for i, item in enumerate(items, 1):
                    self.info(f"{i}. {item}")
            else:
                self.info(f"No {result_type} found.")
