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
    theme = excel_manager.cell_handler.get_cell_value(start_row, columns["theme"])

    related_keywords = google_search_analyzer.get_related_keyword(theme)
    related_keywords_string = google_search_analyzer.get_related_keywords_string(
        theme, related_keywords
    )
    logger.info(related_keywords_string)

    for i, related_keyword in enumerate(
        related_keywords[:CREATE_BLOG_WP_EXCEL_GROUP_SIZE], 1
    ):
        excel_manager.cell_handler.update_cell(
            row=start_row + i - 1,
            column=columns["theme_suggestions"],
            value=related_keyword,
        )
    excel_manager.cell_handler.update_cell(
        row=start_row,
        column=columns["theme"],
        value=related_keywords[0],
    )

    excel_manager.file_handler.save()


def main():
    try:
        if not excel_manager.set_info(
            CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH, CREATE_BLOG_WP_EXCEL_SHEET_NAME
        ):
            return

        columns = excel_manager.search_handler.find_and_map_column_indices(
            index=CREATE_BLOG_WP_EXCEL_INDEX_ROW,
            search_strings=CREATE_BLOG_WP_EXCEL_INDEX_STRINGS,
        )
        if value_validator.any_invalid(columns):
            return

        flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
            column=columns["flag"]
        )
        for i in range(flag_end_row):
            start_row = (
                i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
            )
            flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
            if value_validator.is_valid(flag):
                logger.prominent_log(
                    f"Google get theme, processing group starting at row {start_row}"
                )
                get_themes(start_row, columns)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
