from scripts.load_env import *
from scripts.initialize import logger, script_executor, file_path_handler


def main():
    # CREATE BLOG WP
    GET_THEMES_GOOGLE_NAME = "get_themes_google.py"
    GET_HEADING_GOOGLE = "get_heading_google.py"
    GET_EVIDENCE_NAME = "get_evidence_bing.py"
    CREATE_BLOG_NAME = "create_blog_wp_chatgpt.py"
    POST_WP_NAME = "upload_wp_post.py"

    # CREATE BLOG MD
    CREATE_FOLDER_AND_FILE = "create_folder_and_file.py"
    CREATE_BLOG_CHATGPT = "create_blog_md_chatgpt.py"
    GET_TITLE_IN_MD = "get_title_in_md.py"
    REPLACE_TEXT = "replace_text.py"
    CREATE_THUMBNAIL = "create_thumbnail.py"
    MOVE_TARGET_FOLDERS = "move_target_folders.py"
    DELETE_FILES_IN_FOLDERS = "delete_files_in_folder.py"

    # CREATE BLOG WP
    get_themes_google_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, GET_THEMES_GOOGLE_NAME
    )
    get_heading_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, GET_HEADING_GOOGLE
    )
    get_evidence_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, GET_EVIDENCE_NAME
    )
    create_blog_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, CREATE_BLOG_NAME
    )
    post_wp_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, POST_WP_NAME
    )

    # CREATE BLOG MD
    create_folder_and_file_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_FOLDER_AND_FILE
    )
    create_blog_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_BLOG_CHATGPT
    )
    get_title_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, GET_TITLE_IN_MD
    )
    replace_text_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, REPLACE_TEXT
    )
    create_thumbnail_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_THUMBNAIL
    )
    move_target_folders_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, MOVE_TARGET_FOLDERS
    )
    delete_files_in_folders_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, DELETE_FILES_IN_FOLDERS
    )

    try:
        if EXECUTE_CREATE_BLOG_WP:
            if EXECUTE_GET_THEMES_GOOGLE:
                script_executor.run_script(get_themes_google_full_path)
            if EXECUTE_GET_HEADING_GOOGLE:
                script_executor.run_script(get_heading_full_path)
            if EXECUTE_GET_EVIDENCE_BING:
                script_executor.run_script(get_evidence_full_path)
            if EXECUTE_CREATE_BLOG_WP_CHATGPT:
                script_executor.run_script(create_blog_full_path)
            if EXECUTE_UPLOAD_WP_POST:
                script_executor.run_script(post_wp_full_path)

        if EXECUTE_CREATE_BLOG_MD:
            if EXECUTE_CREATE_FOLDER_AND_FILE:
                script_executor.run_script(create_folder_and_file_full_path)
            if EXECUTE_CREATE_BLOG_CHATGPT:
                script_executor.run_script(create_blog_full_path)
            if EXECUTE_GET_TITLE_IN_MD:
                script_executor.run_script(get_title_full_path)
            if EXECUTE_REPLACE_TEXT:
                script_executor.run_script(replace_text_full_path)
            if EXECUTE_CREATE_THUMBNAIL:
                script_executor.run_script(create_thumbnail_full_path)
            if EXECUTE_MOVE_TARGET_FOLDERS:
                script_executor.run_script(move_target_folders_full_path)
            if EXECUTE_DELETE_FILES_IN_FOLDERS:
                script_executor.run_script(delete_files_in_folders_full_path)

    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )


if __name__ == "__main__":
    main()
