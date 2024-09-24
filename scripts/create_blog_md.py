from scripts.load_env import *
from scripts.initialize import logger, script_executor, file_path_handler


def main():
    CREATE_FOLDER_AND_FILE = "create_folder_and_file.py"
    CREATE_BLOG_CHATGPT = "create_blog_chatgpt.py"
    GET_TITLE_IN_MD = "get_title_in_md.py"
    CREATE_THUMBNAIL = "create_thumbnail.py"
    REPLACE_TEXT = "replace_text.py"

    create_folder_and_file_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_FOLDER_AND_FILE
    )
    create_blog_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_BLOG_CHATGPT
    )
    get_title_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, GET_TITLE_IN_MD
    )
    create_thumbnail_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_THUMBNAIL
    )
    replace_text_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, REPLACE_TEXT
    )

    try:
        if EXECUTE_CREATE_FOLDER_AND_FILE:
            script_executor.run_script(create_folder_and_file_full_path)

        if EXECUTE_CREATE_BLOG_CHATGPT:
            script_executor.run_script(create_blog_full_path)

        if EXECUTE_GET_TITLE_IN_MD:
            script_executor.run_script(get_title_full_path)

        if EXECUTE_CREATE_THUMBNAIL:
            script_executor.run_script(create_thumbnail_full_path)

        if EXECUTE_REPLACE_TEXT:
            script_executor.run_script(replace_text_full_path)
    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )


if __name__ == "__main__":
    main()
