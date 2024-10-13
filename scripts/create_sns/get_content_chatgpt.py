from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    value_validator,
)


def get_content(start_row, columns):
    slug = excel_manager.cell_handler.get_cell_value(start_row, columns["slug"])
    if not slug:
        logger.debug(f"Empty slug found at row {start_row}")
        return None

    url = f"{CREATE_BLOG_WP_WP_URL}/{slug}"
    prompt = CREATE_SNS_PROMPT + url
    edge_handler.open_url_in_browser(CHATGPT_GPTS_SNS_URL)
    chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=0)
    content = chatgpt_handler.get_generated_content()
    excel_manager.cell_handler.update_cell(
        row=start_row,
        column=columns["content"],
        value=content,
    )
    excel_manager.cell_handler.update_cell(
        row=start_row,
        column=columns["post_content"],
        value=content + "\n\n" + url,
    )
    excel_manager.file_handler.save()


def main():
    if not excel_manager.set_info(
        CREATE_SNS_EXCEL_FILE_FULL_PATH, CREATE_SNS_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_SNS_EXCEL_INDEX_ROW,
        search_strings=CREATE_SNS_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        column=columns["flag"]
    )
    for start_row in range(CREATE_SNS_EXCEL_START_ROW, flag_end_row + 1):
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(
                f"Google get heading, processing group starting at row {start_row}"
            )
            get_content(start_row, columns)


if __name__ == "__main__":
    main()
