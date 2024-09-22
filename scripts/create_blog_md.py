from scripts.load_env import *
from scripts.initialize import logger, script_executor, file_path_handler

def main():
    CREATE_BLOG_NAME = "create_blog_chatgpt.py"
    GET_TITLE_IN_MD = "get_title_in_md.py"
    CREATE_PNG = "create_png.py"

    create_blog_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_BLOG_NAME
    )
    get_title_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, GET_TITLE_IN_MD
    )
    create_png_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_MD_DIR, CREATE_PNG
    )

    try:
        if EXECUTE_CREATE_BLOG_MD_CHATGPT:
            # script_executor.run_script(create_blog_full_path)
            # script_executor.run_script(get_title_full_path)
            script_executor.run_script(create_png_full_path)
    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )


if __name__ == "__main__":
    main()
