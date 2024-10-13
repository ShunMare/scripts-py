from PIL import ImageFont
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class FontManager:
    _fonts = {}

    @staticmethod
    def load_font(font_path, size):
        """
        Load a font with the specified path and size.
        If the font is already loaded, return the cached version.

        :param font_path: Path to the font file
        :param size: Font size
        :return: Loaded font object
        """
        font_key = (font_path, size)
        if font_key not in FontManager._fonts:
            try:
                font = ImageFont.truetype(font_path, size)
                logger.debug(
                    f"Successfully loaded custom font (size {size}) from {font_path}"
                )
            except IOError:
                logger.debug(
                    f"Failed to load custom font (size {size}) from {font_path}. Using default system font."
                )
                font = ImageFont.load_default()
            FontManager._fonts[font_key] = font
        return FontManager._fonts[font_key]

    @staticmethod
    def get_font(font_path, size):
        """
        Get a font with the specified path and size.
        This method is a convenient wrapper around load_font.

        :param font_path: Path to the font file
        :param size: Font size
        :return: Font object
        """
        return FontManager.load_font(font_path, size)

    @staticmethod
    def clear_font_cache():
        """
        Clear the font cache to free up memory.
        """
        FontManager._fonts.clear()
        logger.debug("Font cache has been cleared")
