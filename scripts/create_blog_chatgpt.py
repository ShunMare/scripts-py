import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)

load_dotenv(dotenv_path, override=True)
# common
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_MEDIUM = int(os.getenv("WAIT_TIME_AFTER_PROMPT_MEDIUM", 100))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 5))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
GET_CONTENT_METHOD = os.getenv("GET_CONTENT_METHOD", "clipboard")
# chatgpt
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
IS_IMAGE_GENERATION_ENABLED = (
    os.getenv("IS_IMAGE_GENERATION_ENABLED", "false").lower() == "true"
)
CHATGPT_URL = os.getenv("CHATGPT_URL", "https://chatgpt.com/")
PROMPT_TEMPLATE_PATH = os.getenv("PROMPT_TEMPLATE_PATH", "")
TITLE_PROMPT = os.getenv("TITLE_PROMPT")
LONG_DESCRIPTION_PROMPT = os.getenv("LONG_DESCRIPTION_PROMPT", "")
SHORT_DESCRIPTION_PROMPT = os.getenv("SHORT_DESCRIPTION_PROMPT")
KEYWORDS_PROMPT = os.getenv("KEYWORDS_PROMPT")
PERMALINK_PROMPT = os.getenv("PERMALINK_PROMPT")
IMAGE_PROMPT = os.getenv("IMAGE_PROMPT")
CHATGPT_OUTPUT_ELEMENT = os.getenv("CHATGPT_OUTPUT_ELEMENT", "div")
CHATGPT_OUTPUT_CLASS_LIST = os.environ.get(
    "CHATGPT_OUTPUT_CLASS_LIST", "markdown,prose"
).split(",")
# define
SOURCE_COPILOT_CONVERSATION = "ソース: Copilot との会話"
SUPERSCRIPT_CITATION_PATTERN = r"\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+:\s*\[[^\]]+\]\([^\)]+\)"
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1
DOWNLOAD_FOLDER_PATH = "C:/Users/okubo/Downloads/"
TMP_NAME = "create_blog_chatgpt"

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.input_operations.keyboard_handler import KeyboardHandler
from src.ai_operations.chatgpt_handler import ChatGPTHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.file_operations.file_processor import FileHandler, FileReader
from src.util_operations.validator import ValueValidator
from src.text_operations.text_converter import TextConverter
from src.text_operations.text_remover import TextRemover
from src.text_operations.text_replacer import TextReplacer
from src.web_operations.web_handler import WebScraper
from src.log_operations.log_handlers import setup_logger
from src.text_operations.text_manager import TextManager
from src.folder_operations.folder_processor import FolderRemover

logger = setup_logger(__name__)
excel_manager = ExcelManager(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
chatgpt_handler = ChatGPTHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_medium=WAIT_TIME_AFTER_PROMPT_MEDIUM,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
text_manager = TextManager()
file_handler = FileHandler()
file_reader = FileReader()
web_scraper = WebScraper()
text_converter = TextConverter()
text_remover = TextRemover()
folder_remover = FolderRemover()
text_replacer = TextReplacer()


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )
    heading = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["heading"]
    )
    evidences = excel_manager.cell_handler.get_range_values(
        excel_manager.current_sheet, start_row, columns["evidence"], GROUP_SIZE
    )
    if not ValueValidator.has_any_valid_value_in_array(evidences):
        return

    edge_handler.open_url_in_browser(CHATGPT_URL)

    logger.info("getting md content")
    initial_prompt = file_reader.read_file(PROMPT_TEMPLATE_PATH)
    for i, evidence in enumerate(evidences):
        if evidence is not None:
            evidence = text_manager.text_remover.remove_content_after(
                evidence, SOURCE_COPILOT_CONVERSATION
            )
            evidence = text_manager.text_remover.remove_pattern(
                evidence, SUPERSCRIPT_CITATION_PATTERN
            )
            if i == 0:
                prompt = prompt_generator.create_initial_prompt(
                    theme, heading, evidence, initial_prompt
                )
            else:
                prompt = prompt_generator.create_additional_prompt(evidence)
            chatgpt_handler.send_prompt_and_generate_content(
                prompt, repeat_count=0, is_reload=True
            )
    if GET_CONTENT_METHOD == "clipboard":
        md_content = chatgpt_handler.get_generated_content()

    logger.info("getting title content")
    title_prompt = prompt_generator.replace_marker(
        prompt=TITLE_PROMPT, theme=theme, heading=""
    )
    chatgpt_handler.send_prompt_and_generate_content(title_prompt, repeat_count=0)
    if GET_CONTENT_METHOD == "clipboard":
        title_content = chatgpt_handler.get_generated_content()

    logger.info("sent long description content")
    chatgpt_handler.send_prompt_and_generate_content(
        LONG_DESCRIPTION_PROMPT, repeat_count=0
    )

    logger.info("getting short description content")
    chatgpt_handler.send_prompt_and_generate_content(
        SHORT_DESCRIPTION_PROMPT, repeat_count=0
    )
    if GET_CONTENT_METHOD == "clipboard":
        description_content = chatgpt_handler.get_generated_content()

    logger.info("getting keywords content")
    chatgpt_handler.send_prompt_and_generate_content(KEYWORDS_PROMPT, repeat_count=0)
    if GET_CONTENT_METHOD == "clipboard":
        keywords_content = chatgpt_handler.get_generated_content()

    logger.info("getting permalink content")
    chatgpt_handler.send_prompt_and_generate_content(PERMALINK_PROMPT, repeat_count=0)
    if GET_CONTENT_METHOD == "clipboard":
        link_content = chatgpt_handler.get_generated_content()

    logger.info("getting image content")
    if IS_IMAGE_GENERATION_ENABLED:
        chatgpt_handler.send_prompt_and_generate_content(IMAGE_PROMPT, repeat_count=0)

    logger.info("convert html to md")
    if GET_CONTENT_METHOD != "clipboard":
        chatgpt_html_file_name = TMP_NAME + ".html"
        chatgpt_handler.save_html(chatgpt_html_file_name)
        chatgpt_html_path = DOWNLOAD_FOLDER_PATH + chatgpt_html_file_name
        if file_handler.exists(chatgpt_html_path):
            chatgpt_html = file_reader.read_file(chatgpt_html_path)
        results = web_scraper.find_elements(
            chatgpt_html,
            tag_name=CHATGPT_OUTPUT_ELEMENT,
            class_list=CHATGPT_OUTPUT_CLASS_LIST,
        )
        evidence_count = excel_manager.cell_handler.count_nonempty_cells_in_range(
            excel_manager.current_sheet,
            column=columns["evidence"],
            start_row=start_row,
            end_row=start_row + GROUP_SIZE - 1,
        )
        if len(results) >= evidence_count + 5:
            html_contents = []
            md_contents = []
            for i in range(evidence_count):
                html_content = results[i]
                html_content_converted = text_replacer.replace_from_end(
                    html_content,
                    '<div class="markdown prose w-full break-words dark:prose-invert dark">',
                    "",
                )
                html_content_converted = text_replacer.replace_from_end(
                    html_content_converted, "</div>", ""
                )
                html_content_converted = text_converter.convert_html_to_string_array(
                    html_content_converted
                )
                html_contents.append(html_content_converted)
                md_content = text_converter.convert_to_markdown(html_content)
                md_contents.append(md_content)
            title_content = text_converter.convert_to_markdown(results[evidence_count])
            description_content = text_converter.convert_to_markdown(
                results[evidence_count + 2]
            )
            keywords_content = text_converter.convert_to_markdown(
                results[evidence_count + 3]
            )
            link_content = text_converter.convert_to_markdown(
                results[evidence_count + 4]
            )
        file_handler.delete_file(chatgpt_html_path)
        folder_remover.remove_folder(DOWNLOAD_FOLDER_PATH + TMP_NAME + "_files")

    logger.info("update cells in excel")
    if GET_CONTENT_METHOD != "clipboard":
        for i, content in enumerate(html_contents):
            excel_manager.cell_handler.update_cell(
                excel_manager.current_sheet,
                start_row + i,
                columns["html"],
                content,
            )
        for i, content in enumerate(md_contents):
            excel_manager.cell_handler.update_cell(
                excel_manager.current_sheet,
                start_row + i,
                columns["md"],
                content,
            )
    else:
        excel_manager.cell_handler.update_cell(
            excel_manager.current_sheet,
            start_row,
            columns["md"],
            md_content,
        )
    excel_manager.cell_handler.update_cell(
        excel_manager.current_sheet,
        start_row,
        columns["title"],
        title_content,
    )
    excel_manager.cell_handler.update_cell(
        excel_manager.current_sheet,
        start_row,
        columns["description"],
        description_content,
    )
    excel_manager.cell_handler.update_cell(
        excel_manager.current_sheet,
        start_row,
        columns["keywords"],
        keywords_content,
    )
    excel_manager.cell_handler.update_cell(
        excel_manager.current_sheet,
        start_row,
        columns["link"],
        link_content,
    )

    excel_manager.save_workbook()


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = [
        "flag",
        "md",
        "html",
        "theme",
        "heading",
        "title",
        "description",
        "keywords",
        "evidence",
        "link",
    ]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if ValueValidator.has_any_invalid_value_in_array(list(columns.values())):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * GROUP_SIZE + EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if ValueValidator.is_single_value_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
