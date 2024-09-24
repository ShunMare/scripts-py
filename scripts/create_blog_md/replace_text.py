from functools import partial
from initialize import *
from scripts.load_env import *
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
    folder_prefix = "vba-"

    target_text = "Excel VBA"
    replacement_text = "`Excel VBA`"
    exclude_pattern = "`Excel VBA`"

    process_function = partial(
        text_replacer.replace_with_exclusion,
        target_text=target_text,
        replacement_text=replacement_text,
        exclusion_pattern=exclude_pattern,
    )

    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_PATH,
        folder_prefix,
        process_function,
        [],
    )

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
        CREATE_BLOG_MD_TARGET_FOLDER_PATH,
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
        CREATE_BLOG_MD_TARGET_FOLDER_PATH,
        folder_prefix,
        process_function,
        [],
    )

    target_text = "**"
    replacement_text = ""
    process_function = partial(
        text_replacer.replace_content,
        target_text=target_text,
        replacement_text=replacement_text,
    )
    file_processor.process_all_matching_files(
        CREATE_BLOG_MD_TARGET_FOLDER_PATH, folder_prefix, process_function, []
    )


if __name__ == "__main__":
    main()
