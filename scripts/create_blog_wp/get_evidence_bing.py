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
    text_converter,
    bing_handler,
    value_validator,
)


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(start_row, columns["theme"])
    directions = excel_manager.cell_handler.get_range_values(
        start_row=start_row,
        column=columns["direction"],
        num_rows=CREATE_BLOG_WP_EXCEL_GROUP_SIZE,
    )
    if not value_validator.any_valid(directions):
        return

    edge_handler.open_url_in_browser(BING_URL)
    bing_handler.press_new_chat_button()

    logger.info("sent direction")
    for direction in directions:
        if value_validator.is_valid(direction):
            prompt = prompt_generator.replace_marker(
                prompt=direction, theme=theme, heading=""
            )
            prompt = (
                "下記の内容についてできるだけ詳しく教えてほしい、Bing AIでエビデンスを用いて答えて\n必ず参考文献を引用して\n\n"
                + prompt
            )
            bing_handler.send_prompt(prompt=prompt)

    logger.info("convert html to md")
    if GET_CONTENT_METHOD == "html":
        html_file_name = CREATE_BLOG_WP_GET_EVIDENCE_BING_FILE_NAME + ".html"
        edge_handler.ui_save_html(html_file_name)
        bing_html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(bing_html_path):
            bing_html = file_reader.read_file(bing_html_path)
        results = html_parser.find_elements_with_attributes(
            content=bing_html,
            tag="div",
            class_name="space-y-3",
            attributes={"data-content": "ai-message"},
        )
        direction_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
            column=columns["direction"],
            start_row=start_row,
            end_row=start_row + CREATE_BLOG_WP_EXCEL_GROUP_SIZE - 1,
        )
        if len(results) == direction_count:
            md_contents = []
            for i in range(direction_count):
                md_content = text_converter.convert_to_markdown(results[i])
                md_contents.append(md_content)
        file_handler.delete_file(bing_html_path)
        folder_remover.remove_folder(
            DOWNLOAD_FOLDER_DIR_FULL_PATH
            + CREATE_BLOG_WP_GET_EVIDENCE_BING_FILE_NAME
            + "_files"
        )

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD == "html":
        print(columns["evidence"])
        for i, content in enumerate(md_contents):
            excel_manager.cell_handler.update_cell(
                row=start_row + i, column=columns["evidence"], value=content
            )
    excel_manager.file_handler.save()


SEARCH_STRINGS = ["flag", "theme", "direction", "evidence"]


def main():
    if not excel_manager.set_info(
        CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH, CREATE_BLOG_WP_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_BLOG_WP_EXCEL_INDEX_ROW,
        search_strings=SEARCH_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
