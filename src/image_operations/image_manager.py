from PIL import Image, ImageDraw, ImageFont
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ImageManager:
    @staticmethod
    def load_image(image_path):
        """
        Load an image from the specified path.
        """
        try:
            image = Image.open(image_path)
            logger.debug(f"Image loaded successfully: {image_path}")
            return image
        except IOError:
            logger.error(f"Failed to load image: {image_path}")
            raise

    @staticmethod
    def get_draw(image):
        """
        Return a draw object for the given image.
        """
        return ImageDraw.Draw(image)

    @staticmethod
    def draw_text(image, position, text, font, fill):
        """
        Draw text on the image.
        """
        draw = ImageManager.get_draw(image)
        draw.text(position, text, font=font, fill=fill)
        logger.debug(f"Text drawn at position {position}")
        return image

    @staticmethod
    def save_image(image, save_path):
        """
        Save the image to the specified path.
        """
        try:
            image.save(save_path)
            logger.debug(f"Image saved successfully: {save_path}")
        except IOError:
            logger.error(f"Failed to save image: {save_path}")
            raise

    @staticmethod
    def create_blank_image(size, color):
        """
        Create a new blank image with the specified size and background color.
        """
        image = Image.new("RGB", size, color)
        logger.debug(f"Created new blank image with size {size}")
        return image
