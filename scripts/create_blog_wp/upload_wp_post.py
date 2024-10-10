from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    wp_manager,
    value_validator,
    array_combiner,
    text_finder,
    text_replacer,
)


def upload_wp_post(start_row, columns):
    title = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["title"]
    )
    html_array = excel_manager.cell_handler.get_range_values(
        excel_manager.current_sheet,
        start_row,
        columns["html"],
        CREATE_BLOG_WP_EXCEL_GROUP_SIZE,
    )
    html_array = array_combiner.merge_elements(
        html_array, CREATE_BLOG_WP_EXCEL_GROUP_SIZE, ""
    )
    html = html_array[0]
    h2_count = text_finder.count_occurrences(html, "<h2>")
    html = text_replacer.replace(html, "<b>", "")
    html = text_replacer.replace(html, "</b>", "")
    html = text_replacer.replace(html, "<strong>", "")
    html = text_replacer.replace(html, "</strong>", "")
    if h2_count < 3:
        html = text_replacer.replace(html, "<h3>", "<h2>")
        html = text_replacer.replace(html, "</h3>", "</h2>")
        html = text_replacer.replace(html, "<h4>", "<h4>")
        html = text_replacer.replace(html, "</h4>", "</h3>")
        html = text_replacer.replace(html, "<h5>", "<h4>")
        html = text_replacer.replace(html, "</h5>", "</h4>")
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
    excel_manager.set_file_path(CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(CREATE_BLOG_WP_EXCEL_SHEET_NAME)
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
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if value_validator.is_single_value_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            upload_wp_post(start_row, columns)


if __name__ == "__main__":
    main()
