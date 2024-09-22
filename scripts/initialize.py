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
from src.file_operations.file_processor import FileHandler, FileReader
from src.util_operations.validator import ValueValidator
from src.text_operations.text_converter import TextConverter
from src.text_operations.text_remover import TextRemover
from src.text_operations.text_replacer import TextReplacer
from src.web_operations.web_handler import WebScraper
from src.log_operations.log_handlers import setup_logger
from src.text_operations.text_manager import TextManager
from src.folder_operations.folder_processor import FolderRemover
from src.wp_operations.wp_manager import WordPressAPI
from src.ai_operations.bing_handler import BingHandler
from src.web_operations.web_handler import WebScraper, HTMLParser
from src.web_operations.google_search_analyzer import GoogleSearchAnalyzer
from src.format_operations.text_formatter import TextFormatter
from src.script_operations.script_executor import ScriptExecutor
from src.file_operations.file_processor import FilePathHandler

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
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
file_reader = FileReader()
web_scraper = WebScraper()
text_converter = TextConverter()
text_remover = TextRemover()
folder_remover = FolderRemover()
text_replacer = TextReplacer()
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
file_path_handler = FilePathHandler()
