from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    web_scraper,
)

def get_blog_title(start_row, columns):
    try:
        slug = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["slug"]
        )
        if not slug:
            logger.warning(f"Empty slug found at row {start_row}")
            return None

        url = f"{CREATE_BLOG_WP_WP_URL}/{slug}"
        tags_to_extract = ["title"]
        results = web_scraper.scrape(url, tags_to_extract)
        if results and results["title"]:
            return results["title"]
        else:
            logger.warning(f"No title found for URL: {url}")
            return None
    except Exception as e:
        logger.error(f"Error in get_blog_title for row {start_row}: {str(e)}")
        return None


def main():
    excel_manager.set_file_path(CREATE_SNS_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(CREATE_SNS_EXCEL_SHEET_NAME)
    search_strings = ["slug", "title"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=1,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        logger.error("Invalid column indices found")
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["slug"]
    )

    for start_row in range(2, flag_end_row + 1):
        if not excel_manager.cell_handler.is_cell_empty(
            excel_manager.current_sheet, start_row, columns["slug"]
        ):
            title = get_blog_title(start_row, columns)
            if title:
                excel_manager.cell_handler.update_cell(
                    excel_manager.current_sheet, start_row, columns["title"], title
                )
            else:
                logger.warning(f"Skipping update for row {start_row} due to missing title")

    excel_manager.save_workbook()
    logger.info("Workbook saved successfully")


if __name__ == "__main__":
    main()
