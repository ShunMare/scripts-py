from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    value_validator,
    file_writer,
    file_path_handler,
)


def generate_and_process_prompts(target_row, columns):
    prompt = excel_manager.cell_handler.get_cell_value(target_row, columns["prompt"])

    if not value_validator.is_valid(prompt):
        return

    logger.info("getting short md content")
    chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=1)
    md_content = chatgpt_handler.get_generated_content()

    logger.info("update md")
    folder_name = excel_manager.cell_handler.get_cell_value(
        target_row, columns["folder_name"]
    )
    path_elements = [
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
        folder_name,
        CREATE_BLOG_MD_TARGET_MDX_FILE_NAME,
    ]
    file_full_path = file_path_handler.join_and_normalize_path(path_elements)
    file_writer.replace_file_content(file_full_path, md_content)


def main():
    if not excel_manager.set_info(
        CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH, CREATE_BLOG_MD_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=CREATE_BLOG_MD_EXCEL_INDEX_STRINGS,
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
    count = 0
    for i in range(flag_end_row):
        target_row = i + CREATE_BLOG_MD_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(target_row, columns["flag"])
        if value_validator.is_valid(flag):
            if count % 20 == 0:
                edge_handler.open_url_in_browser(CHATGPT_GPTS_BLOG_MASTER_URL)
            count += 1
            logger.prominent_log(f"Processing group starting at row {target_row}")
            generate_and_process_prompts(target_row, columns)


if __name__ == "__main__":
    main()
