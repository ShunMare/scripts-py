from functools import partial
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
    text_replacer,
    file_path_handler,
    file_processor,
    file_reader,
)


def main():
    folder_prefix = ""

    target_text = CREATE_BLOG_MD_PNG_TAG_NAME
    replacement_text = "`" + CREATE_BLOG_MD_PNG_TAG_NAME + "`"
    exclude_pattern = "`" + CREATE_BLOG_MD_PNG_TAG_NAME + "`"

    process_function = partial(
        text_replacer.replace_with_exclusion,
        target_text=target_text,
        replacement_text=replacement_text,
        exclusion_pattern=exclude_pattern,
    )

    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
        folder_prefix,
        process_function,
        [],
    )

    # target_text = "【"
    # replacement_text = ""
    # exclude_pattern = "【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】"

    # process_function = partial(
    #     text_replacer.replace_with_exclusion,
    #     target_text=target_text,
    #     replacement_text=replacement_text,
    #     exclusion_pattern=exclude_pattern,
    # )

    # target_text = "】"
    # replacement_text = ""
    # exclude_pattern = "【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】"

    # process_function = partial(
    #     text_replacer.replace_with_exclusion,
    #     target_text=target_text,
    #     replacement_text=replacement_text,
    #     exclusion_pattern=exclude_pattern,
    # )

    # file_processor.process_all_matching_files(
    #     CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
    #     folder_prefix,
    #     process_function,
    #     [],
    # )

    target_text = "`"
    replacement_text = ""
    start_marker = "---"
    end_marker = "---"
    use_markers = True

    process_function = partial(
        text_replacer.replace_between,
        target_text=target_text,
        replacement_text=replacement_text,
        start_marker=start_marker,
        end_marker=end_marker,
        use_markers=use_markers,
    )

    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
        folder_prefix,
        process_function,
        [],
    )

    target_text = "`: "
    replacement_text = "`  \n  "
    marker = "---"

    process_function = partial(
        text_replacer.replace_from_marker,
        target_text=target_text,
        replacement_text=replacement_text,
        marker=marker,
    )

    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
        folder_prefix,
        process_function,
        [],
    )

    replacements = [
        ("**", ""),
        ("# 1. ", "# "),
        ("# 2. ", "# "),
        ("# 3. ", "# "),
        ("# 4. ", "# "),
        ("# 5. ", "# "),
        ("# 6. ", "# "),
        ("# 7. ", "# "),
        ("# 8. ", "# "),
        ("# 9. ", "# "),
        ("# 10. ", "# "),
        ("【", "`"),
        ("】", "`"),
        (
            "# `" + CREATE_BLOG_MD_PNG_TAG_NAME + "`",
            "# " + CREATE_BLOG_MD_PNG_TAG_NAME,
        ),
        (
            "title: `" + CREATE_BLOG_MD_PNG_TAG_NAME + "`",
            "title: 【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】",
        ),
        (
            "title: `" + CREATE_BLOG_MD_PNG_TAG_NAME,
            "title: 【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】",
        ),
    ]

    for target_text, replacement_text in replacements:
        process_function = partial(
            text_replacer.replace_content,
            target_text=target_text,
            replacement_text=replacement_text,
        )
        file_processor.process_all_matching_files(
            CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_prefix, process_function, []
        )

    target_text = "**"
    replacement_text = ""
    process_function = partial(
        text_replacer.replace_content,
        target_text=target_text,
        replacement_text=replacement_text,
    )
    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_prefix, process_function, []
    )

    target_text = r"categories: \[.*?\]"
    replacement_text = "categories: [Coding]"
    process_function = partial(
        text_replacer.replace_content_regex,
        pattern=target_text,
        replacement=replacement_text,
    )
    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_prefix, process_function, []
    )

    target_text = r"tags: \[.*?\]"
    replacement_text = "tags: [" + CREATE_BLOG_MD_PNG_TAG_NAME + "]"
    process_function = partial(
        text_replacer.replace_content_regex,
        pattern=target_text,
        replacement=replacement_text,
    )
    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_prefix, process_function, []
    )

    target_text = r"\n{2,}"
    replacement_text = "\n"
    process_function = partial(
        text_replacer.replace_content_regex,
        pattern=target_text,
        replacement=replacement_text,
    )
    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_prefix, process_function, []
    )


if __name__ == "__main__":
    main()
