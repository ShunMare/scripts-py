from initialize import *
from scripts.load_env import *
from scripts.initialize import (
    logger,
    excel_manager,
    wp_manager,
    value_validator,
)


def upload_wp_post(start_row, columns):
    title = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["title"]
    )
    html = excel_manager.cell_handler.get_last_non_empty_value_in_range(
        excel_manager.current_sheet, start_row, columns["html"], EXCEL_GROUP_SIZE
    )
    description = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["description"]
    )
    keywords = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["keywords"]
    )
    link = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["link"]
    )

    post_id = wp_manager.create_post(
        title=title,
        content=html,
        status="draft",
        categories=[],
        tags=[],
        meta_description=description,
        meta_keywords=keywords,
        seo_title=title,
        permalink=link,
    )

    if post_id:
        created_post = wp_manager.get_post(post_id)
        if created_post:
            wp_manager.print_post_details(created_post)


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = [
        "flag",
        "title",
        "html",
        "description",
        "keywords",
        "link",
    ]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=EXCEL_INDEX_ROW,
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
        start_row = i * EXCEL_GROUP_SIZE + EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if value_validator.is_single_value_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            upload_wp_post(start_row, columns)


if __name__ == "__main__":
    main()
