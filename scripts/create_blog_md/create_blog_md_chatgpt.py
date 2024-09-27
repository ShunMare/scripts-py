from initialize import *
from scripts.load_env import *
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
    prompt = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, target_row, columns["prompt"]
    )

    if not value_validator.is_single_value_valid(prompt):
        return

    logger.info("getting short md content")
    chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=1)
    md_content = chatgpt_handler.get_generated_content()

    logger.info("update md")
    folder_name = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, target_row, columns["folder_name"]
    )
    path_elements = [
        CREATE_BLOG_MD_TARGET_FOLDER_PATH,
        folder_name,
        CREATE_BLOG_MD_TARGET_MDX_FILE_NAME,
    ]
    file_full_path = file_path_handler.join_and_normalize_path(path_elements)
    file_writer.replace_file_content(file_full_path, md_content)


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = [
        "flag",
        "prompt",
        "folder_name",
    ]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["flag"]
    )
    count = 0
    for i in range(flag_end_row):
        target_row = i + CREATE_BLOG_MD_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, target_row, columns["flag"]
        )
        if value_validator.is_single_value_valid(flag):
            if count % 20 == 0:
                edge_handler.open_url_in_browser(CHATGPT_URL)
            count += 1
            logger.prominent_log(f"Processing group starting at row {target_row}")
            generate_and_process_prompts(target_row, columns)


if __name__ == "__main__":
    main()
