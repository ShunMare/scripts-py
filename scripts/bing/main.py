import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)

load_dotenv(dotenv_path, override=True)
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 100))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
WAIT_TIME_AFTER_SWITCH = int(os.getenv("WAIT_TIME_AFTER_SWITCH", 3))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
BING_PATH = os.getenv("BING_PATH", "https://www.bing.com/chat?form=NTPCHB")
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH", "")
GROUP_SIZE = 10

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.ai_operations.bing_handler import BingHandler
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
bing_handler = BingHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
)
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1


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

    edge_handler.open_url_in_browser(BING_PATH)

    logger.info("sent direction")
    for direction in directions:
        if ValueValidator.is_single_value_valid(direction):
            prompt = prompt_generator.replace_marker(
                prompt=direction, theme=theme, heading=""
            )
            bing_handler.send_prompt(prompt=prompt)


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["flag", "theme", "direction"]
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
