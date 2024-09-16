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
# chatgpt
CHATGPT_PATH = os.getenv("CHATGPT_PATH", "https://chatgpt.com/")
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
# google
HEADING_PROMPT = os.getenv("HEADING_PROMPT", "")
# define
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.web_operations.google_search_analyzer import GoogleSearchAnalyzer
from src.format_operations.text_formatter import TextFormatter
from src.json_operations.json_processor import JSONProcessor
from src.ai_operations.chatgpt_handler import ChatGPTHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.util_operations.validator import ValueValidator
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
chatgpt_handler = ChatGPTHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
google_search_analyzer = GoogleSearchAnalyzer()
json_processor = JSONProcessor()
text_formatter = TextFormatter()


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
    heading_content = chatgpt_handler.get_generated_content()
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
            logger.prominent_log(f"Google get heading, processing group starting at row {start_row}")
            get_heading(start_row, columns)


if __name__ == "__main__":
    main()
