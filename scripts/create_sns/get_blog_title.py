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
        slug = excel_manager.cell_handler.get_cell_value(start_row, columns["slug"])
        if not slug:
            logger.info(f"Empty slug found at row {start_row}")
            return None

        url = f"{CREATE_BLOG_WP_WP_URL}/{slug}"
        tags_to_extract = ["title"]
        results = web_scraper.scrape(url, tags_to_extract)
        if results and results["title"]:
            return results["title"]
        else:
            logger.info(f"No title found for URL: {url}")
            return None
    except Exception as e:
        logger.error(f"Error in get_blog_title for row {start_row}: {str(e)}")
        return None


def main():
    if not excel_manager.set_info(
        CREATE_SNS_EXCEL_FILE_FULL_PATH, CREATE_SNS_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_SNS_EXCEL_INDEX_ROW,
        search_strings=CREATE_SNS_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        column=columns["slug"]
    )

    for start_row in range(2, flag_end_row + 1):
        if not excel_manager.cell_handler.is_cell_empty_or_match(
            start_row, columns["slug"]
        ):
            title = get_blog_title(start_row, columns)
            if title:
                excel_manager.cell_handler.update_cell(
                    start_row, columns["title"], title
                )
            else:
                logger.info(
                    f"Skipping update for row {start_row} due to missing title"
                )

    excel_manager.file_handler.save()
    logger.info("Workbook saved successfully")


if __name__ == "__main__":
    main()
