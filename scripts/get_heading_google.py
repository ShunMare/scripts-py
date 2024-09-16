import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)
load_dotenv(dotenv_path, override=True)

# common
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_MEDIUM = int(os.getenv("WAIT_TIME_AFTER_PROMPT_MEDIUM", 100))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 5))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
WAIT_TIME_AFTER_SWITCH = int(os.getenv("WAIT_TIME_AFTER_SWITCH", 3))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
GET_CONTENT_METHOD = os.getenv("GET_CONTENT_METHOD", "clipboard")
# chatgpt
CHATGPT_PATH = os.getenv("CHATGPT_PATH", "https://chatgpt.com/")
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
CHATGPT_OUTPUT_ELEMENT = os.getenv("CHATGPT_OUTPUT_ELEMENT", "div")
CHATGPT_OUTPUT_CLASS_LIST = os.environ.get(
    "CHATGPT_OUTPUT_CLASS_LIST", "markdown,prose"
).split(",")
# google
HEADING_PROMPT = os.getenv("HEADING_PROMPT", "")
# define
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1
DOWNLOAD_FOLDER_PATH = "C:/Users/okubo/Downloads/"
CHATGPT_HTML_FILE_NAME = "chatgpt_get_heading.html"

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.web_operations.google_search_analyzer import GoogleSearchAnalyzer
from src.format_operations.text_formatter import TextFormatter
from src.json_operations.json_processor import JSONProcessor
from src.ai_operations.chatgpt_handler import ChatGPTHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.util_operations.validator import ValueValidator
from src.file_operations.file_processor import FileHandler, FileReader
from src.text_operations.text_converter import TextConverter
from src.web_operations.web_handler import WebScraper
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_MEDIUM,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
chatgpt_handler = ChatGPTHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_medium=WAIT_TIME_AFTER_PROMPT_MEDIUM,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
google_search_analyzer = GoogleSearchAnalyzer()
json_processor = JSONProcessor()
text_formatter = TextFormatter()
file_handler = FileHandler()
file_reader = FileReader()
web_scraper = WebScraper()
text_converter = TextConverter()


def get_heading(start_row, columns):
    """"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )

    heading_results = google_search_analyzer.extract_heading(theme)
    results_str = []
    for i, heading_result in enumerate(heading_results[:10], 1):
        result_data = {
            "url": heading_result["url"],
            "h2": heading_result["h2"],
            "h3": heading_result["h3"],
        }
        result_str = text_formatter.format_heading_result(result_data)
        excel_manager.update_cell(
            row=start_row + i - 1,
            column=columns["heading_suggestions"],
            value=result_str,
        )
        results_str.append(result_str)

    combined_results = "\n".join(results_str)
    combined_results = HEADING_PROMPT + "\n" + combined_results
    edge_handler.open_url_in_browser(CHATGPT_PATH)
    prompt = HEADING_PROMPT + "\n" + combined_results
    chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=0)

    heading_content = ""
    if GET_CONTENT_METHOD == "clipboard":
        heading_content = chatgpt_handler.get_generated_content()
    else:
        chatgpt_handler.save_html(CHATGPT_HTML_FILE_NAME)
        chatgpt_html_path = DOWNLOAD_FOLDER_PATH + CHATGPT_HTML_FILE_NAME
        if file_handler.exists(chatgpt_html_path):
            chatgpt_html = file_reader.read_file(chatgpt_html_path)
        results = web_scraper.find_elements(
            chatgpt_html,
            tag_name=CHATGPT_OUTPUT_ELEMENT,
            class_list=CHATGPT_OUTPUT_CLASS_LIST,
        )
        if len(results) == 1:
            heading_content = text_converter.convert_to_markdown(results[0])
        print("heading_content", heading_content)
        file_handler.delete_file(chatgpt_html_path)

    excel_manager.update_cell(
        row=start_row,
        column=columns["heading"],
        value=heading_content,
    )
    excel_manager.save_workbook()


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["flag", "theme", "heading_suggestions", "heading"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if ValueValidator.has_any_invalid_value_in_array(list(columns.values())):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * GROUP_SIZE + EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if ValueValidator.is_single_value_valid(flag):
            logger.prominent_log(
                f"Google get heading, processing group starting at row {start_row}"
            )
            get_heading(start_row, columns)


if __name__ == "__main__":
    main()
