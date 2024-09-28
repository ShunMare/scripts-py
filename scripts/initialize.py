import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.load_env import *
from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.input_operations.keyboard_handler import KeyboardHandler
from src.ai_operations.chatgpt_handler import ChatGPTHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.file_operations.file_processor import (
    FileHandler,
    FileReader,
    FileWriter,
    FilePathHandler,
    FileProcessor,
    FileValidator,
)
from src.util_operations.validator import ValueValidator
from src.text_operations.text_handler import TextHandler
from src.text_operations.text_converter import TextConverter
from src.text_operations.text_remover import TextRemover
from src.text_operations.text_replacer import TextReplacer
from src.text_operations.text_finder import TextFinder
from src.text_operations.text_manager import TextManager
from src.web_operations.web_handler import WebScraper
from src.log_operations.log_handlers import setup_logger
from src.folder_operations.folder_processor import (
    FolderRemover,
    FolderPathHandler,
    FolderProcessor,
    FolderCreator,
    FolderChecker,
    FolderMover,
)
from src.wp_operations.wp_manager import WordPressAPI
from src.ai_operations.bing_handler import BingHandler
from src.web_operations.web_handler import WebScraper, HTMLParser
from src.web_operations.google_search_analyzer import GoogleSearchAnalyzer
from src.format_operations.text_formatter import TextFormatter
from src.script_operations.script_executor import ScriptExecutor
from src.font_operations.font_manager import FontManager
from src.image_operations.image_manager import ImageManager
from src.json_operations.json_processor import JSONParser
from src.text_operations.text_drawer import TextDrawer

logger = setup_logger(__name__)
excel_manager = ExcelManager()
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
chatgpt_handler = ChatGPTHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_medium=WAIT_TIME_AFTER_PROMPT_MEDIUM,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
text_manager = TextManager()
file_handler = FileHandler()
file_writer = FileWriter()
file_reader = FileReader()
file_validator = FileValidator()
file_path_handler = FilePathHandler()
file_processor = FileProcessor(file_handler, file_validator)
web_scraper = WebScraper()
text_converter = TextConverter()
text_remover = TextRemover()
text_replacer = TextReplacer()
text_finder = TextFinder()
text_handler = TextHandler()
folder_remover = FolderRemover()
folder_creator = FolderCreator()
folder_path_handler = FolderPathHandler()
folder_processor = FolderProcessor("", "")
folder_checker = FolderChecker()
folder_mover = FolderMover()
wp_manager = WordPressAPI(WP_URL, WP_USERNAME, WP_APP_PASSWORD)
value_validator = ValueValidator()
bing_handler = BingHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
)
web_scraper = WebScraper()
html_parser = HTMLParser("")
google_search_analyzer = GoogleSearchAnalyzer()
text_formatter = TextFormatter()
script_executor = ScriptExecutor()
font_manager = FontManager()
image_manager = ImageManager()
json_parser = JSONParser()
text_drawer = TextDrawer()
