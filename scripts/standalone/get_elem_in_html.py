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
    web_scraper,
    value_validator,
    web_fetcher,
    array_keeper,
)


def get_links(url):
    edge_handler.open_url_in_browser(url)
    html_file_name = STANDALONE_GET_ELEM_IN_HTML_FILE_NAME + ".html"
    edge_handler.ui_save_html(html_file_name)
    html_path = DOWNLOAD_FOLDER_DIR_FULL_PATH + html_file_name
    if file_handler.exists(html_path):
        html_content = file_reader.read_file(html_path)
    html_parser.set_html_content(html_content)
    href_links = web_scraper.find_elements_with_attributes(
        html_content=html_content, tag="a", classes=["s-link"], attribute="href"
    )
    file_handler.delete_file(html_path)
    folder_remover.remove_folder(
        DOWNLOAD_FOLDER_DIR_FULL_PATH + STANDALONE_GET_ELEM_IN_HTML_FILE_NAME + "_files"
    )
    return href_links


def main():
    EXCEL_FILE_PATH = "C:/Users/okubo/OneDrive/ドキュメント/004_blogs/succulent/data/nexunity_stackoverflow.xlsx"
    excel_manager.set_file_path(EXCEL_FILE_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["link"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=1,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    BASE_URL = "https://stackoverflow.com/search?"
    start_page = 1
    end_page = 5
    urls = [
        f"{BASE_URL}page={page}&tab=Relevance&pagesize=50&q=hasaccepted%3ayes%20{CREATE_BLOG_MD_TARGET_TAG_NAME}&searchOn=3"
        for page in range(start_page, end_page + 1)
    ]

    target_row = 2
    for url in urls:
        href_links = get_links(url)
        elements_to_keep = ["https://stackoverflow.com/questions/"]
        href_links = array_keeper.keep_elements(href_links, elements_to_keep)

        for href_link in href_links:
            while not excel_manager.cell_handler.is_cell_empty(
                excel_manager.current_sheet, target_row, columns["link"]
            ):
                target_row += 1

            if (
                excel_manager.search_handler.find_matching_index(
                    worksheet=excel_manager.current_sheet,
                    index=columns["link"],
                    search_string=href_link,
                    is_row_flag=False,
                )
                == None
            ):
                excel_manager.update_cell(target_row, columns["link"], href_link)

    excel_manager.save_workbook()


if __name__ == "__main__":
    main()
