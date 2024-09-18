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
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 100))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
WAIT_TIME_AFTER_SWITCH = int(os.getenv("WAIT_TIME_AFTER_SWITCH", 3))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
GET_CONTENT_METHOD = os.getenv("GET_CONTENT_METHOD", "clipboard")
# bing
BING_URL = os.getenv("BING_URL", "https://www.bing.com/chat?form=NTPCHB")
BING_OUTPUT_ELEMENT = os.getenv("BING_OUTPUT_ELEMENT", "div")
BING_OUTPUT_CLASS_LIST = os.environ.get(
    "BING_OUTPUT_CLASS_LIST", "content,user-select-text"
).split(",")
# define
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1
DOWNLOAD_FOLDER_PATH = "C:/Users/okubo/Downloads/"
TMP_NAME = "get_evidence_bing"

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.ai_operations.bing_handler import BingHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.util_operations.validator import ValueValidator
from src.log_operations.log_handlers import setup_logger
from src.file_operations.file_processor import FileHandler, FileReader
from src.web_operations.web_handler import WebScraper, HTMLParser
from src.text_operations.text_converter import TextConverter
from src.folder_operations.folder_processor import FolderRemover

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
bing_handler = BingHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
)
file_handler = FileHandler()
file_reader = FileReader()
web_scraper = WebScraper()
text_converter = TextConverter()
folder_remover = FolderRemover()


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )
    directions = excel_manager.cell_handler.get_range_values(
        worksheet=excel_manager.current_sheet,
        start_row=start_row,
        column=columns["direction"],
        num_rows=GROUP_SIZE,
    )
    if not ValueValidator.has_any_valid_value_in_array(directions):
        return

    edge_handler.open_url_in_browser(BING_URL)

    logger.info("sent direction")
    for direction in directions:
        if ValueValidator.is_single_value_valid(direction):
            prompt = prompt_generator.replace_marker(
                prompt=direction, theme=theme, heading=""
            )
            bing_handler.send_prompt(prompt=prompt)

    logger.info("convert html to md")
    if GET_CONTENT_METHOD == "html":
        bing_html_file_name = TMP_NAME + ".html"
        bing_handler.save_html(bing_html_file_name)
        bing_html_path = DOWNLOAD_FOLDER_PATH + bing_html_file_name
        if file_handler.exists(bing_html_path):
            bing_html = file_reader.read_file(bing_html_path)
        html_parser = HTMLParser(bing_html)
        results = html_parser.find_aria_labels(
            tag=BING_OUTPUT_ELEMENT,
            class_list=BING_OUTPUT_CLASS_LIST,
        )
        direction_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
            excel_manager.current_sheet,
            column=columns["direction"],
            start_row=start_row,
            end_row=start_row + GROUP_SIZE - 1,
        )
        if len(results) == direction_count:
            md_contents = []
            for i in range(direction_count):
                md_contents.append(results[i])
        file_handler.delete_file(bing_html_path)
        folder_remover.remove_folder(DOWNLOAD_FOLDER_PATH + TMP_NAME + "_files")

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD == "html":
        for i, content in enumerate(md_contents):
            excel_manager.cell_handler.update_cell(
                excel_manager.current_sheet,
                start_row + i,
                columns["evidence"],
                content,
            )
    excel_manager.save_workbook()


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["flag", "theme", "direction", "evidence"]
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
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
