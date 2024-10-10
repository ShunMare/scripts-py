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
            logger.info(f"Retrieved {len(slugs)} slugs from page {page}")
            if len(slugs) < per_page:
                break
            page += 1
        logger.info(f"Retrieved a total of {len(all_slugs)} slugs from WordPress")
        return all_slugs
    except Exception as e:
        logger.error(f"Error retrieving slugs: {str(e)}")
        return []


def main():
    excel_manager.set_file_path(CREATE_SNS_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(CREATE_SNS_EXCEL_SHEET_NAME)
    search_strings = ["flag", "slug"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=1,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    all_slugs = get_blog_slugs()

    logger.prominent_log(f"Total slugs retrieved: {len(all_slugs)}")
    target_row = 2
    for slug in all_slugs:
        while not excel_manager.cell_handler.is_cell_empty(
            excel_manager.current_sheet, target_row, columns["slug"]
        ):
            target_row += 1
        if (
            excel_manager.search_handler.find_matching_index(
                worksheet=excel_manager.current_sheet,
                index=columns["slug"],
                search_string=slug,
                is_row_flag=False,
            )
            == None
        ):
            excel_manager.update_cell(target_row, columns["flag"], "1")
            excel_manager.update_cell(target_row, columns["slug"], slug)

    excel_manager.save_workbook()


if __name__ == "__main__":
    main()
