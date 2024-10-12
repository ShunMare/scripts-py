from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    file_handler,
    file_reader,
    folder_remover,
    html_parser,
    web_scraper,
    value_validator,
    array_keeper,
)


def get_links(url):
    edge_handler.open_url_in_browser(url)
    html_file_name = STANDALONE_GET_ELEM_IN_HTML_FILE_NAME + EXTENSION_HTML
    edge_handler.ui_save_html(html_file_name)

    html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
    if file_handler.exists(html_path):
        html_content = file_reader.read_file(html_path)
    html_parser.set_html_content(html_content)
    href_links = web_scraper.find_elements_with_attributes(
        html_content=html_content,
        tag=STANDALONE_GET_ELEM_IN_HTML_TAG,
        classes=STANDALONE_GET_ELEM_IN_HTML_CLASSES,
        attribute=STANDALONE_GET_ELEM_IN_HTML_ATTRIBUTE,
    )

    file_handler.delete_file(html_path)
    folder_remover.remove_folder(
        DOWNLOAD_FOLDER_DIR_FULL_PATH
        + STANDALONE_GET_ELEM_IN_HTML_FILE_NAME
        + DOWNLOAD_HTML_FOLDER_SUFFIX
    )
    return href_links


def main():
    if not excel_manager.set_info(
        STANDALONE_GET_ELEM_IN_HTML_EXCEL_FILE_NAME,
        STANDALONE_GET_ELEM_IN_HTML_EXCEL_SHEET_NAME,
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_ROW,
        search_strings=STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    urls = [
        f"{STANDALONE_GET_ELEM_IN_HTML_BASE_URL}page={page}&tab=Relevance&pagesize=50&q=hasaccepted%3ayes%20{CREATE_BLOG_MD_TARGET_TAG_NAME}&searchOn=3"
        for page in range(
            STANDALONE_GET_ELEM_IN_HTML_START_PAGE,
            STANDALONE_GET_ELEM_IN_HTML_END_PAGE + 1,
        )
    ]

    target_row = STANDALONE_GET_ELEM_IN_HTML_EXCEL_START_ROW
    for url in urls:
        href_links = get_links(url)
        href_links = array_keeper.keep_elements(
            href_links, STANDALONE_GET_ELEM_IN_HTML_ELEMENT_TO_KEEP
        )

        for href_link in href_links:
            while not excel_manager.cell_handler.is_cell_empty_or_match(
                target_row, columns["link"]
            ):
                target_row += 1

            if (
                excel_manager.search_handler.find_matching_index(
                    index=columns["link"],
                    search_string=href_link,
                    is_row_flag=False,
                )
                == None
            ):
                excel_manager.cell_handler.update_cell(
                    target_row, columns["link"], href_link
                )

    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
