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
    chatgpt_handler,
    value_validator,
    web_scraper,
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

    logger.info("open browser")
    if CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_BING:
        edge_handler.open_url_in_browser(BING_URL)
        bing_handler.press_new_chat_button()
    elif CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_CHATGPT:
        edge_handler.open_url_in_browser(CHATGPT_GPTS_BROWSER_URL)

    logger.info("send direction")
    for direction in directions:
        if value_validator.is_valid(direction):
            if CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_BING:
                prompt_head = prompt_generator.replace_marker(
                    prompt=CREATE_BLOG_WP_GET_EVIDENCE_BING_PROMPT,
                    theme=theme,
                    heading="",
                )
            elif CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_CHATGPT:
                prompt_head = prompt_generator.replace_marker(
                    prompt=CREATE_BLOG_WP_GET_EVIDENCE_CHATGPT_PROMPT,
                    theme=theme,
                    heading="",
                )
            prompt = prompt_generator.replace_marker(
                prompt=direction, theme=theme, heading=""
            )
            prompt = prompt_head + prompt
            if CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_BING:
                bing_handler.send_prompt(prompt=prompt)
            elif CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_CHATGPT:
                chatgpt_handler.send_prompt_and_generate_content(
                    prompt, repeat_count=0, is_reload=True
                )

    logger.info("convert html to md")
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_HTML:
        html_file_name = CREATE_BLOG_WP_GET_EVIDENCE_FILE_NAME + EXTENSION_HTML
        edge_handler.ui_save_html(html_file_name)
        html_file_full_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(html_file_full_path):
            html_content = file_reader.read_file(html_file_full_path)
        if CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_BING:
            results = html_parser.find_elements_with_attributes(
                content=html_content,
                tag=BING_OUTPUT_TAG,
                class_name=BING_OUTPUT_CLASS_LIST,
                attributes={BING_OUTPUT_ATTRIBUTE_KEY: BING_OUTPUT_ATTRIBUTE_VALUE},
            )
        elif CREATE_BLOG_WP_GET_EVIDENCE_METHOD == AI_TOOL_CHATGPT:
            results = web_scraper.find_elements(
                html_content,
                tag_name=CHATGPT_OUTPUT_TAG,
                class_list=CHATGPT_OUTPUT_CLASS_LIST,
            )
        md_contents = []
        for i in range(len(results)):
            md_content = text_converter.convert_to_markdown(results[i])
            md_contents.append(md_content)
        file_handler.delete_file(html_file_full_path)
        folder_remover.remove_folder(
            DOWNLOAD_FOLDER_DIR_FULL_PATH
            + CREATE_BLOG_WP_GET_EVIDENCE_FILE_NAME
            + DOWNLOAD_HTML_FOLDER_SUFFIX
        )

    logger.info("close tab")
    edge_handler.close_tab()

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_HTML:
        for i, content in enumerate(md_contents):
            excel_manager.cell_handler.update_cell(
                row=start_row + i, column=columns["evidence"], value=content
            )
    excel_manager.file_handler.save()


def main():
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

    chatgpt_handler.set_info(
        wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
        wait_time_after_prompt_medium=WAIT_TIME_AFTER_PROMPT_MEDIUM,
        wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
        wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
        short_wait_time=KEYBOARD_ACTION_SHORT_DELAY,
        model_type=MODEL_TYPE_GPTS,
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
