from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    prompt_generator,
    file_handler,
    file_reader,
    web_scraper,
    text_converter,
    folder_remover,
    text_replacer,
    value_validator,
    folder_creator,
)


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(start_row, columns["theme"])
    heading = excel_manager.cell_handler.get_cell_value(start_row, columns["heading"])
    md_array = excel_manager.cell_handler.get_range_values(
        start_row,
        columns["md"],
        CREATE_BLOG_WP_EXCEL_GROUP_SIZE,
    )
    if not value_validator.any_invalid(md_array):
        return

    logger.info("open browser")
    edge_handler.open_url_in_browser(CHATGPT_4O_WITH_CANVAS_URL)

    for i, md in enumerate(md_array):
        logger.info(f"getting md and html content : {i+1}/{len(md_array)}")
        if md is not None:
            if i == 0:
                prompt = prompt_generator.create_initial_prompt(
                    theme, heading, md, CREATE_BLOG_WP_ADJUSTED_HTML_INIT_PROMPT
                )
            else:
                prompt = CREATE_BLOG_WP_ADJUSTED_HTML_PROMPT + md
            chatgpt_handler.send_prompt_and_generate_content(
                prompt, repeat_count=0, is_reload=True
            )
    if i in range(2):
        chatgpt_handler.send_prompt_and_generate_content(
            CREATE_BLOG_WP_ADJUSTED_HTML_COMPLETE_TRUNCATED_PROMPT,
            repeat_count=0,
            is_reload=True,
        )
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_ADJUSTED_HTML_FINAL_PROMPT, repeat_count=0, is_reload=True
    )
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        md_content = chatgpt_handler.get_generated_content()

    logger.info("convert html to md")
    if GET_CONTENT_METHOD != GET_CONTENT_METHOD_CLIPBOARD:
        html_file_name = CREATE_BLOG_WP_GET_ADJUSTED_HTML_FILE_NAME + EXTENSION_HTML
        edge_handler.ui_save_html(html_file_name)
        html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(html_path):
            html_content = file_reader.read_file(html_path)
        results = web_scraper.find_elements(
            content=html_content,
            tag_name=CHATGPT_OUTPUT_TAG,
            class_list=CHATGPT_CANVAS_OUTPUT_CLASS_LIST,
        )
        html_content = results[0]
        html_content_converted = text_replacer.replace_from_end(
            html_content,
            '<div class="_main_gvo0h_1 z-10 markdown prose dark:prose-invert focus:outline-none bg-transparent ProseMirror" style="width: 580px;" contenteditable="true" translate="no">',
            "",
        )
        html_content_converted = text_replacer.replace_from_end(
            html_content,
            '<div class="_main_gvo0h_1 z-10 markdown prose dark:prose-invert focus:outline-none bg-transparent ProseMirror" contenteditable="true" style="width: 580px;" translate="no">',
            "",
        )
        html_content_converted = text_replacer.replace_from_end(
            html_content_converted, "</div>", ""
        )
        html_content_converted = text_converter.convert_html_to_string_array(
            html_content_converted
        )
        md_content = text_converter.convert_to_markdown(html_content)

        logger.info("close tab")
        edge_handler.close_tab()

        logger.info("delete unnecessary file and directory")
        file_handler.delete_file(html_path)
        source_folder_full_path = folder_path_handler.join_and_normalize_path(
            [
                DOWNLOAD_FOLDER_DIR_FULL_PATH,
                CREATE_BLOG_WP_GET_ADJUSTED_HTML_FILE_NAME,
                + DOWNLOAD_HTML_FOLDER_SUFFIX,
            ]
        )
        destination_folder_full_path = folder_path_handler.join_and_normalize_path(
            [DOWNLOAD_FOLDER_DIR_FULL_PATH, theme]
        )
        folder_creator.create_folder(destination_folder_full_path)
        file_handler.move_files_with_name(
            source_folder_full_path, destination_folder_full_path, EXTENSION_WEBP
        )
        logger.info(source_folder_full_path)
        folder_remover.remove_folder(source_folder_full_path)

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD != GET_CONTENT_METHOD_CLIPBOARD:
        excel_manager.cell_handler.update_cell(
            start_row,
            columns["adjusted_html"],
            html_content_converted,
        )
        excel_manager.cell_handler.update_cell(
            start_row,
            columns["adjusted_md"],
            md_content,
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
        model_type=MODEL_TYPE_4O,
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
