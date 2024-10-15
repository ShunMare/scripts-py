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
    folder_remover,
    text_replacer,
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
    if not value_validator.any_invalid(evidences):
        return

    edge_handler.open_url_in_browser(CHATGPT_DEFAULT_URL)

    initial_prompt = file_reader.read_file(CREATE_BLOG_WP_PROMPT_TEMPLATE_FULL_PATH)
    for i, evidence in enumerate(evidences):
        logger.info(f"getting md and html content : {i}/{len(evidences)}")
        if evidence is not None:
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
            chatgpt_handler.send_prompt_and_generate_content(
                prompt, repeat_count=0, is_reload=True
            )
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        md_content = chatgpt_handler.get_generated_content()

    logger.info("getting title content")
    title_prompt = prompt_generator.replace_marker(
        prompt=CREATE_BLOG_WP_TITLE_PROMPT, theme=theme, heading=""
    )
    chatgpt_handler.send_prompt_and_generate_content(title_prompt, repeat_count=0)
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        title_content = chatgpt_handler.get_generated_content()

    logger.info("sent long description content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_LONG_DESCRIPTION_PROMPT, repeat_count=0
    )

    logger.info("getting short description content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_SHORT_DESCRIPTION_PROMPT, repeat_count=0
    )
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        description_content = chatgpt_handler.get_generated_content()

    logger.info("getting keywords content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_KEYWORDS_PROMPT, repeat_count=0
    )
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        keywords_content = chatgpt_handler.get_generated_content()

    logger.info("getting permalink content")
    chatgpt_handler.send_prompt_and_generate_content(
        CREATE_BLOG_WP_PERMALINK_PROMPT, repeat_count=0
    )
    if GET_CONTENT_METHOD == GET_CONTENT_METHOD_CLIPBOARD:
        link_content = chatgpt_handler.get_generated_content()

    logger.info("getting image content")
    if CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED:
        chatgpt_handler.send_prompt_and_generate_content(
            CREATE_BLOG_WP_IMAGE_PROMPT, repeat_count=0
        )
        chatgpt_handler.send_prompt_and_generate_content(
            CREATE_BLOG_WP_THUMBNAIL_IMAGE_PROMPT, repeat_count=0
        )

    logger.info("convert html to md")
    if GET_CONTENT_METHOD != GET_CONTENT_METHOD_CLIPBOARD:
        html_file_name = (
            CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME + EXTENSION_HTML
        )
        edge_handler.ui_save_html(html_file_name)
        chatgpt_html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(chatgpt_html_path):
            chatgpt_html = file_reader.read_file(chatgpt_html_path)
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
            html_contents = []
            md_contents = []
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
                html_content_converted = text_converter.convert_html_to_string_array(
                    html_content_converted
                )
                html_contents.append(html_content_converted)
                md_content = text_converter.convert_to_markdown(html_content)
                md_contents.append(md_content)
            title_content = text_converter.convert_to_markdown(results[evidence_count])
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
        file_handler.delete_file(chatgpt_html_path)
        source_folder_full_path = folder_path_handler.join_path(
            [
                DOWNLOAD_FOLDER_DIR_FULL_PATH,
                CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME,
                DOWNLOAD_HTML_FOLDER_SUFFIX,
            ]
        )
        destination_folder_full_path = folder_path_handler.join_path(
            [source_folder_full_path, theme]
        )
        folder_creator.create_folder(destination_folder_full_path)
        file_handler.move_files_with_name(
            source_folder_full_path, destination_folder_full_path, EXTENSION_WEBP
        )
        folder_remover.remove_folder(source_folder_full_path)

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD != GET_CONTENT_METHOD_CLIPBOARD:
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
    else:
        excel_manager.cell_handler.update_cell(
            start_row,
            columns["md"],
            md_content,
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
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
