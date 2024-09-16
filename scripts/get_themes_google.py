import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)
load_dotenv(dotenv_path, override=True)

# common
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
# define
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.google_search_analyzer import GoogleSearchAnalyzer
from src.format_operations.text_formatter import TextFormatter
from src.json_operations.json_processor import JSONProcessor
from src.util_operations.validator import ValueValidator
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
google_search_analyzer = GoogleSearchAnalyzer()
json_processor = JSONProcessor()
text_formatter = TextFormatter()


def get_themes(start_row, columns):
    """"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )

    related_keywords = google_search_analyzer.get_related_keyword(theme)
    google_search_analyzer.print_related_keywords(theme, related_keywords)

    for i, related_keyword in enumerate(related_keywords[:10], 1):
        excel_manager.update_cell(
            row=start_row + i - 1,
            column=columns["theme_suggestions"],
            value=related_keyword,
        )

    excel_manager.save_workbook()


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["flag", "theme_suggestions", "theme", "heading"]
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
                f"Google get theme, processing group starting at row {start_row}"
            )
            get_themes(start_row, columns)


if __name__ == "__main__":
    main()
