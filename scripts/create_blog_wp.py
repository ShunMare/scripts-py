from scripts.load_env import *
from scripts.initialize import logger, script_executor, file_path_handler

def main():
    GET_EVIDENCE_NAME = "get_evidence_bing.py"
    CREATE_BLOG_NAME = "create_blog_chatgpt.py"
    POST_WP_NAME = "upload_wp_post.py"

    get_evidence_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, GET_EVIDENCE_NAME
    )
    create_blog_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, CREATE_BLOG_NAME
    )
    post_wp_full_path = file_path_handler.join_path(
        SCRIPT_CREATE_BLOG_WP_DIR, POST_WP_NAME
    )

    try:
        if EXECUTE_GET_EVIDENCE_BING:
            script_executor.run_script(get_evidence_full_path)
        if EXECUTE_CREATE_BLOG_WP_CHATGPT:
            script_executor.run_script(create_blog_full_path)
        if EXECUTE_UPLOAD_WP_POST:
            script_executor.run_script(post_wp_full_path)
    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )


if __name__ == "__main__":
    main()
