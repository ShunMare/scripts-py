from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    wp_manager,
)


def get_blog_slugs():
    try:
        all_slugs = []
        page = 1
        per_page = 100

        while True:
            slugs = wp_manager.get_slugs(
                post_type="posts", per_page=per_page, page=page
            )
            if not slugs:
                break
            all_slugs.extend(slugs)
            logger.debug(f"Retrieved {len(slugs)} slugs from page {page}")
            if len(slugs) < per_page:
                break
            page += 1
        logger.debug(f"Retrieved a total of {len(all_slugs)} slugs from WordPress")
        return all_slugs
    except Exception as e:
        logger.error(f"Error retrieving slugs: {str(e)}")
        return []


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

    all_slugs = get_blog_slugs()

    logger.prominent_log(f"Total slugs retrieved: {len(all_slugs)}")
    target_row = CREATE_SNS_EXCEL_START_ROW
    for slug in all_slugs:
        while not excel_manager.cell_handler.is_cell_empty_or_match(
            target_row, columns["slug"]
        ):
            target_row += 1
        if (
            excel_manager.search_handler.find_matching_index(
                index=columns["slug"],
                search_string=slug,
                is_row_flag=False,
            )
            == None
        ):
            excel_manager.cell_handler.update_cell(target_row, columns["flag"], "1")
            excel_manager.cell_handler.update_cell(target_row, columns["slug"], slug)

    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
