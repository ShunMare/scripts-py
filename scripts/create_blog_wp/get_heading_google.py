from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    file_handler,
    file_reader,
    web_scraper,
    text_converter,
    value_validator,
    google_search_analyzer,
    text_formatter,
)


def get_heading(start_row, columns):
    theme = excel_manager.cell_handler.get_cell_value(start_row, columns["theme"])

    heading_results = google_search_analyzer.extract_heading(theme)
    results_str = []
    for i, heading_result in enumerate(heading_results[:10], 1):
        result_data = {
            "url": heading_result["url"],
            "h2": heading_result["h2"],
            "h3": heading_result["h3"],
        }
        result_str = text_formatter.format_heading_result(result_data)
        excel_manager.cell_handler.update_cell(
            row=start_row + i - 1,
            column=columns["heading_suggestions"],
            value=result_str,
        )
        results_str.append(result_str)

    combined_results = "\n".join(results_str)
    combined_results = CREATE_BLOG_WP_HEADING_PROMPT + "\n" + combined_results
    edge_handler.open_url_in_browser(CHATGPT_DEFAULT_URL)
    prompt = combined_results
    chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=0)

    heading_content = ""
    if GET_CONTENT_METHOD == "clipboard":
        heading_content = chatgpt_handler.get_generated_content()
    else:
        html_file_name = CREATE_BLOG_WP_GET_HEADING_GOOGLE_FILE_NAME + ".html"
        edge_handler.ui_save_html(html_file_name)
        chatgpt_html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
        if file_handler.exists(chatgpt_html_path):
            chatgpt_html = file_reader.read_file(chatgpt_html_path)
        results = web_scraper.find_elements(
            chatgpt_html,
            tag_name=CHATGPT_OUTPUT_ELEMENT,
            class_list=CHATGPT_OUTPUT_CLASS_LIST,
        )
        if len(results) == 1:
            heading_content = text_converter.convert_to_markdown(results[0])
        file_handler.delete_file(chatgpt_html_path)

    excel_manager.cell_handler.update_cell(
        row=start_row,
        column=columns["heading"],
        value=heading_content,
    )
    excel_manager.file_handler.save()


SEARCH_STRINGS = ["flag", "theme", "heading_suggestions", "heading"]


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
            logger.prominent_log(
                f"Google get heading, processing group starting at row {start_row}"
            )
            get_heading(start_row, columns)


if __name__ == "__main__":
    main()
