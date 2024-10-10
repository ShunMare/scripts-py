from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    prompt_generator,
    file_handler,
    file_reader,
    folder_remover,
    html_parser,
    bing_handler,
    value_validator,
)


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )
    directions = excel_manager.cell_handler.get_range_values(
        worksheet=excel_manager.current_sheet,
        start_row=start_row,
        column=columns["direction"],
        num_rows=CREATE_BLOG_WP_EXCEL_GROUP_SIZE,
    )
    if not value_validator.has_any_valid_value_in_array(directions):
        return

    edge_handler.open_url_in_browser(BING_URL)

    logger.info("sent direction")
    for direction in directions:
        if value_validator.is_single_value_valid(direction):
            prompt = prompt_generator.replace_marker(
                prompt=direction, theme=theme, heading=""
            )
            bing_handler.send_prompt(prompt=prompt)

    logger.info("convert html to md")
    if GET_CONTENT_METHOD == "html":
        html_file_name = CREATE_BLOG_WP_GET_EVIDENCE_BING_FILE_NAME + ".html"
        edge_handler.ui_save_html(html_file_name)
        bing_html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(bing_html_path):
            bing_html = file_reader.read_file(bing_html_path)
        results = html_parser.find_aria_labels(
            content=bing_html,
            tag=BING_OUTPUT_ELEMENT,
            class_list=BING_OUTPUT_CLASS_LIST,
        )
        direction_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
            excel_manager.current_sheet,
            column=columns["direction"],
            start_row=start_row,
            end_row=start_row + CREATE_BLOG_WP_EXCEL_GROUP_SIZE - 1,
        )
        if len(results) == direction_count:
            md_contents = []
            for i in range(direction_count):
                md_contents.append(results[i])
        file_handler.delete_file(bing_html_path)
        folder_remover.remove_folder(
            DOWNLOAD_FOLDER_DIR_FULL_PATH
            + CREATE_BLOG_WP_GET_EVIDENCE_BING_FILE_NAME
            + "_files"
        )

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD == "html":
        for i, content in enumerate(md_contents):
            excel_manager.cell_handler.update_cell(
                excel_manager.current_sheet,
                start_row + i,
                columns["evidence"],
                content,
            )
    excel_manager.save_workbook()


def main():
    excel_manager.set_file_path(CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(CREATE_BLOG_WP_EXCEL_SHEET_NAME)
    search_strings = ["flag", "theme", "direction", "evidence"]
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
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
