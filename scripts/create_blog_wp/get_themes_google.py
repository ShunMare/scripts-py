import traceback
from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    google_search_analyzer,
)


def get_themes(start_row, columns):
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )

    related_keywords = google_search_analyzer.get_related_keyword(theme)
    google_search_analyzer.print_related_keywords(theme, related_keywords)

    for i, related_keyword in enumerate(
        related_keywords[:CREATE_BLOG_WP_EXCEL_GROUP_SIZE], 1
    ):
        excel_manager.update_cell(
            row=start_row + i - 1,
            column=columns["theme_suggestions"],
            value=related_keyword,
        )
    excel_manager.update_cell(
        row=start_row,
        column=columns["theme"],
        value=related_keywords[0],
    )

    excel_manager.save_workbook()


def main():
    try:
        excel_manager.set_file_path(CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH)
        if not excel_manager.load_workbook():
            return

        excel_manager.set_active_sheet(CREATE_BLOG_WP_EXCEL_SHEET_NAME)
        search_strings = ["flag", "theme_suggestions", "theme", "heading"]
        column_indices = excel_manager.search_handler.find_multiple_matching_indices(
            worksheet=excel_manager.current_sheet,
            index=CREATE_BLOG_WP_EXCEL_INDEX_ROW,
            search_strings=search_strings,
            is_row_flag=True,
        )
        columns = dict(zip(search_strings, column_indices))

        if value_validator.has_any_invalid_value_in_array(list(columns.values())):
            return

        flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
            worksheet=excel_manager.current_sheet, column=columns["flag"]
        )
        for i in range(flag_end_row):
            start_row = (
                i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
            )
            flag = excel_manager.cell_handler.get_cell_value(
                excel_manager.current_sheet, start_row, columns["flag"]
            )
            if value_validator.is_single_value_valid(flag):
                logger.prominent_log(
                    f"Google get theme, processing group starting at row {start_row}"
                )
                get_themes(start_row, columns)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
