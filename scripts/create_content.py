from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    script_executor,
)


def main():
    try:
        if EXECUTE_CREATE_BLOG_WP:
            if EXECUTE_CREATE_BLOG_WP_GET_THEMES_GOOGLE:
                script_executor.run_script(
                    CREATE_BLOG_WP_GET_THEMES_GOOGLE_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_WP_GET_HEADING_GOOGLE:
                script_executor.run_script(CREATE_BLOG_WP_GET_HEADING_FILE_FULL_PATH)
            if EXECUTE_CREATE_BLOG_WP_GET_DIRECTION:
                script_executor.run_script(CREATE_BLOG_WP_GET_DIRECTION_FILE_FULL_PATH)
            if EXECUTE_CREATE_BLOG_WP_GET_EVIDENCE:
                script_executor.run_script(CREATE_BLOG_WP_GET_EVIDENCE_FILE_FULL_PATH)
            if EXECUTE_CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT:
                script_executor.run_script(CREATE_BLOG_WP_CREATE_BLOG_WP_FILE_FULL_PATH)
            if EXECUTE_CREATE_BLOG_WP_UPLOAD_WP_POST:
                script_executor.run_script(CREATE_BLOG_WP_POST_WP_FILE_FULL_PATH)

        if EXECUTE_CREATE_BLOG_MD:
            if EXECUTE_CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE:
                script_executor.run_script(
                    CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT:
                script_executor.run_script(
                    CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_MD_REPLACE_TEXT:
                script_executor.run_script(CREATE_BLOG_MD_REPLACE_TEXT_FILE_FULL_PATH)
            if EXECUTE_CREATE_BLOG_MD_GET_TITLE_IN_MD:
                script_executor.run_script(
                    CREATE_BLOG_MD_GET_TITLE_IN_MD_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_MD_CREATE_THUMBNAIL:
                script_executor.run_script(
                    CREATE_BLOG_MD_CREATE_THUMBNAIL_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_MD_MOVE_TARGET_FOLDERS:
                script_executor.run_script(
                    CREATE_BLOG_MD_MOVE_TARGET_FOLDERS_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_BLOG_MD_DELETE_FILES_IN_FOLDERS:
                script_executor.run_script(
                    CREATE_BLOG_MD_DELETE_FILES_IN_FOLDERS_FILE_FULL_PATH
                )

        if EXECUTE_CREATE_SNS:
            if EXECUTE_CREATE_SNS_GET_BLOG_SLUG:
                script_executor.run_script(CREATE_SNS_GET_BLOG_SLUG_FILE_FULL_PATH)
            if EXECUTE_CREATE_SNS_GET_BLOG_TITLE:
                script_executor.run_script(CREATE_SNS_GET_BLOG_TITLE_FILE_FULL_PATH)
            if EXECUTE_CREATE_SNS_GET_CONTENT_CHATGPT:
                script_executor.run_script(
                    CREATE_SNS_GET_CONTENT_CHATGPT_FILE_FULL_PATH
                )
            if EXECUTE_CREATE_SNS_UPDATE_POST_CONTENT_GAS:
                script_executor.run_script(
                    CREATE_SNS_UPDATE_POST_CONTENT_GAS_FILE_FULL_PATH
                )

        if EXECUTE_STANDALONE:
            if EXECUTE_STANDALONE_GET_TITLE_IN_MD:
                script_executor.run_script(STANDALONE_GET_TITLE_IN_MD_FILE_FULL_PATH)
            if EXECUTE_STANDALONE_GET_TITLE_IN_HTML:
                script_executor.run_script(STANDALONE_GET_TITLE_IN_HTML_FILE_FULL_PATH)
            if EXECUTE_STANDALONE_REPLACE_FOLDER_NAME:
                script_executor.run_script(
                    STANDALONE_REPLACE_FOLDER_NAME_FILE_FULL_PATH
                )

        if EXECUTE_STACKOVERFLOW:
            if EXECUTE_STACKOVERFLOW_GET_SLUG:
                script_executor.run_script(STACKOVERFLOW_GET_SLUG_FILE_FULL_PATH)

    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )


if __name__ == "__main__":
    main()
