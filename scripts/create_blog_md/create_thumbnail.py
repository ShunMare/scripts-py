from typing import Any
from initialize import *
from scripts.load_env import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    file_path_handler,
    folder_path_handler,
    font_manager,
    image_manager,
    json_parser,
    text_drawer,
    text_handler,
)

font_path_elements = [
    CREATE_BLOG_MD_FOLDER_PATH,
    "statics",
    CREATE_PNG_FONTS_DIR_NAME,
    "M_PLUS_Rounded_1c",
    "MPLUSRounded1c-Bold.ttf",
]
font_full_path = file_path_handler.join_and_normalize_path(font_path_elements)

setting_path_elements = [
    CREATE_BLOG_MD_FOLDER_PATH,
    "statics",
    CREATE_PNG_SETTINGS_DIR_NAME,
    f"{CREATE_PNG_CONFIG_NAME}.json",
]
setting_full_path = file_path_handler.join_and_normalize_path(setting_path_elements)

image_path_elements = [
    CREATE_BLOG_MD_FOLDER_PATH,
    "statics",
    CREATE_PNG_IMAGES_DIR_NAME,
]
image_folder_path = folder_path_handler.join_and_normalize_path(image_path_elements)

SEPARATE_KEYWORD = "プロパティの使い方"


def read_excel_data():
    excel_manager.set_file_path(CREATE_BLOG_MD_EXCEL_FILE_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = [
        "title",
        "subtitle",
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

    title_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["title"]
    )

    data = []
    for i in range(title_end_row):
        target_row = i + CREATE_BLOG_MD_EXCEL_START_ROW
        title = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, target_row, columns["title"]
        )
        subtitle = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, target_row, columns["subtitle"]
        )
        folder_name = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, target_row, columns["folder_name"]
        )
        if (
            value_validator.is_single_value_valid(title)
            and value_validator.is_single_value_valid(subtitle)
            and value_validator.is_single_value_valid(folder_name)
        ):
            if not SEPARATE_KEYWORD == "":
                processed_title = text_handler.format_text_with_keyword_split(
                    text=title,
                    keyword=SEPARATE_KEYWORD,
                    split_char="",
                    max_line_length=25,
                    max_lines=3,
                )
            else:
                processed_title = title
            data.append(
                {
                    "title": processed_title,
                    "subtitle": subtitle,
                    "folder_name": folder_name,
                }
            )
            logger.info(f"Row {i} added to processing list")
        else:
            logger.info(f"Row {i} skipped due to missing data")
    return data


def create_image(title: str, subtitle: str, setting_path: str) -> Any:
    json_data = json_parser.load(setting_path)

    background_image = json_parser.get_value(json_data, "backgroundImage")
    settings = json_parser.get_value(json_data, "settings", default={})

    background_full_path = file_path_handler.join_path(
        image_folder_path, background_image
    )
    background = image_manager.load_image(background_full_path)
    draw = image_manager.get_draw(background)

    elements = [
        ("tag", CREATE_PNG_TAG_NAME),
        ("title", title),
        ("subtitle", subtitle),
    ]

    for element, text in elements:
        element_settings = json_parser.get_value(settings, element, default={})
        font_size = json_parser.get_value(element_settings, "size", default=0)
        font = font_manager.load_font(font_full_path, int(font_size))
        color = json_parser.get_value(element_settings, "color", default="#000000")

        horizontal_type = json_parser.get_value(
            element_settings, "horizontalType", default="absolute"
        )
        if horizontal_type == "relative":
            horizontal_align = json_parser.get_value(
                element_settings, "horizontal", default="left"
            )
            x = 0
        else:
            horizontal_align = "left"
            x = int(json_parser.get_value(element_settings, "x", default=0))

        vertical_type = json_parser.get_value(
            element_settings, "verticalType", default="absolute"
        )
        if vertical_type == "relative":
            vertical_align = json_parser.get_value(
                element_settings, "vertical", default="top"
            )
            y = 0
        else:
            vertical_align = "top"
            y = int(json_parser.get_value(element_settings, "y", default=0))

        text_drawer.draw_multiline_text(
            draw,
            text,
            font,
            color,
            x,
            y,
            background.width,
            background.height,
            horizontal_align,
            vertical_align,
        )
    return background


def main():
    excel_data_list = read_excel_data()
    for index, excel_data in enumerate(excel_data_list):
        logger.info(
            f"Processing item {index}/{len(excel_data_list)}: {excel_data['folder_name']}"
        )
        image = create_image(
            title=excel_data["title"],
            subtitle=excel_data["subtitle"],
            setting_path=setting_full_path,
        )
        output_path_elements = [
            CREATE_BLOG_MD_TARGET_FOLDER_PATH,
            excel_data["folder_name"],
            "featured.png",
        ]
        output_full_path = file_path_handler.join_and_normalize_path(
            output_path_elements
        )
        logger.info("output_full_path")
        logger.info(output_full_path)
        image.save(output_full_path)


if __name__ == "__main__":
    main()
