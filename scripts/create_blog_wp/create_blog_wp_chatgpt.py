from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    prompt_generator,
    text_manager,
    file_handler,
    file_reader,
    web_scraper,
    text_converter,
    text_replacer,
    folder_remover,
    value_validator,
    folder_creator,
)


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(start_row, columns["theme"])
    heading = excel_manager.cell_handler.get_cell_value(start_row, columns["heading"])
    evidences = excel_manager.cell_handler.get_range_values(
        start_row,
        columns["evidence"],
        CREATE_BLOG_WP_EXCEL_GROUP_SIZE,
    )
    if not value_validator.any_valid(evidences):
        logger.warning("evidence don't have any values")
        return

    edge_handler.open_url_in_browser(CHATGPT_DEFAULT_URL)

    initial_prompt = file_reader.read_file(CREATE_BLOG_WP_PROMPT_TEMPLATE_FULL_PATH)
    evidence_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
        column=columns["evidence"],
        start_row=start_row,
        end_row=start_row + CREATE_BLOG_WP_EXCEL_GROUP_SIZE - 1,
    )

    html_contents = []
    md_contents = []
    for i, evidence in enumerate(evidences):
        if value_validator.is_valid(evidence):
            logger.info(f"getting md and html content : {i+1}/{evidence_count}")
            evidence = text_manager.text_remover.remove_content_after(
                evidence, BING_SOURCE_COPILOT_CONVERSATION
            )
            evidence = text_manager.text_remover.remove_pattern(
                evidence, BING_SUPERSCRIPT_CITATION_PATTERN
            )
            if i == 0:
                prompt = prompt_generator.create_initial_prompt(
                    theme, heading, evidence, initial_prompt
                )
            else:
                prompt = prompt_generator.create_additional_prompt(evidence)

            chatgpt_handler.send_prompt_and_generate_content(prompt)
            match GET_CONTENT_METHOD:
                case GetContentMethod.CLIPBOARD:
                    md_content = chatgpt_handler.get_generated_content_copy_button()
                    md_contents.append(md_content)
                case GetContentMethod.SHORTCUT:
                    md_content = chatgpt_handler.get_generated_content()
                    md_contents.append(md_content)

    logger.info("getting title content")
    title_prompt = prompt_generator.replace_marker(
        prompt=CREATE_BLOG_WP_TITLE_PROMPT, theme=theme
    )
    chatgpt_handler.send_prompt_and_generate_content(title_prompt)
    match GET_CONTENT_METHOD:
        case GetContentMethod.CLIPBOARD:
            title_content = chatgpt_handler.get_generated_content_copy_button()
        case GetContentMethod.SHORTCUT:
            title_content = chatgpt_handler.get_generated_content()

    logger.info("sent long description content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_LONG_DESCRIPTION_PROMPT
    )

    logger.info("getting short description content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_SHORT_DESCRIPTION_PROMPT
    )
    match GET_CONTENT_METHOD:
        case GetContentMethod.CLIPBOARD:
            description_content = chatgpt_handler.get_generated_content_copy_button()
        case GetContentMethod.SHORTCUT:
            description_content = chatgpt_handler.get_generated_content()

    logger.info("getting keywords content")
    chatgpt_handler.send_prompt_and_generate_content(CREATE_BLOG_WP_KEYWORDS_PROMPT)
    match GET_CONTENT_METHOD:
        case GetContentMethod.CLIPBOARD:
            keywords_content = chatgpt_handler.get_generated_content_copy_button()
        case GetContentMethod.SHORTCUT:
            keywords_content = chatgpt_handler.get_generated_content()

    logger.info("getting permalink content")
    chatgpt_handler.send_prompt_and_generate_content(CREATE_BLOG_WP_PERMALINK_PROMPT)
    match GET_CONTENT_METHOD:
        case GetContentMethod.CLIPBOARD:
            link_content = chatgpt_handler.get_generated_content_copy_button()
        case GetContentMethod.SHORTCUT:
            link_content = chatgpt_handler.get_generated_content()

    logger.info("getting image content")
    if CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED:
        chatgpt_handler.send_prompt_and_generate_content(CREATE_BLOG_WP_IMAGE_PROMPT)
        chatgpt_handler.send_prompt_and_generate_content(
            CREATE_BLOG_WP_THUMBNAIL_IMAGE_PROMPT
        )

    match GET_CONTENT_METHOD:
        case GetContentMethod.HTML:
            logger.info("convert html to md")
            html_file_name = (
                CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME + EXTENSION_HTML
            )
            edge_handler.ui_save_html(html_file_name)
            html_file_full_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
            if file_handler.exists(html_file_full_path):
                chatgpt_html = file_reader.read_file(html_file_full_path)
            results = web_scraper.find_elements(
                chatgpt_html,
                tag_name=CHATGPT_OUTPUT_TAG,
                class_list=CHATGPT_OUTPUT_CLASS_LIST,
            )
            evidence_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
                column=columns["evidence"],
                start_row=start_row,
                end_row=start_row + CREATE_BLOG_WP_EXCEL_GROUP_SIZE - 1,
            )
            if len(results) >= evidence_count + 5:
                for i in range(evidence_count):
                    html_content = results[i]
                    html_content_converted = text_replacer.replace_from_end(
                        html_content,
                        '<div class="markdown prose w-full break-words dark:prose-invert dark">',
                        "",
                    )
                    html_content_converted = text_replacer.replace_from_end(
                        html_content_converted, "</div>", ""
                    )
                    html_content_converted = (
                        text_converter.convert_html_to_string_array(
                            html_content_converted
                        )
                    )
                    html_contents.append(html_content_converted)
                    md_content = text_converter.convert_to_markdown(html_content)
                    md_contents.append(text_converter.convert_to_markdown(md_content))
                title_content = text_converter.convert_to_markdown(
                    results[evidence_count]
                )
                description_content = text_converter.convert_to_markdown(
                    results[evidence_count + 2]
                )
                keywords_content = text_converter.convert_to_markdown(
                    results[evidence_count + 3]
                )
                link_content = text_converter.convert_to_markdown(
                    results[evidence_count + 4]
                )

                logger.info("delete unnecessary file and directory")
                file_handler.delete_file(html_file_full_path)
                source_folder_full_path = folder_path_handler.join_and_normalize_path(
                    [
                        DOWNLOAD_FOLDER_DIR_FULL_PATH,
                        CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME
                        + DOWNLOAD_HTML_FOLDER_SUFFIX,
                    ]
                )
                destination_folder_full_path = (
                    folder_path_handler.join_and_normalize_path(
                        [DOWNLOAD_FOLDER_DIR_FULL_PATH, theme]
                    )
                )
                folder_creator.create_folder(destination_folder_full_path)
                file_handler.move_files_with_name(
                    source_folder_full_path,
                    destination_folder_full_path,
                    EXTENSION_WEBP,
                )
                folder_remover.remove_folder(source_folder_full_path)
        case GetContentMethod.SHORTCUT:
            for md_content in md_contents:
                html_contents.append(text_converter.convert_to_html(md_content))

    logger.info("close tab")
    if CHATGPT_IS_DELETE_CHAT:
        chatgpt_handler.delete_chat()
    edge_handler.close_tab()

    logger.info("update cells in excel")
    for i, content in enumerate(html_contents):
        excel_manager.cell_handler.update_cell(
            start_row + i,
            columns["html"],
            content,
        )
    for i, content in enumerate(md_contents):
        excel_manager.cell_handler.update_cell(
            start_row + i,
            columns["md"],
            content,
        )
    excel_manager.cell_handler.update_cell(
        start_row,
        columns["title"],
        title_content,
    )
    excel_manager.cell_handler.update_cell(
        start_row,
        columns["description"],
        description_content,
    )
    excel_manager.cell_handler.update_cell(
        start_row,
        columns["keywords"],
        keywords_content,
    )
    excel_manager.cell_handler.update_cell(
        start_row,
        columns["link"],
        link_content,
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
        tab_count_4o=TAB_COUNT_4O,
        tab_count_4omini=TAB_COUNT_4OMINI,
        tab_count_gpts=TAB_COUNT_GPTS,
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
