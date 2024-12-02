import os
from pdf2image import convert_from_path
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def convert_pdf_to_images(pdf_path, chapter):
    logger.info(f"Starting PDF conversion for {pdf_path}...")

    # Ensure the output directory exists
    output_dir = os.path.join(settings.MEDIA_ROOT, 'manhwa_images', f'chapter_{chapter.id}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created directory: {output_dir}")

    # Convert PDF to images
    try:
        images = convert_from_path(pdf_path, dpi=150)  # Adjust DPI as needed
    except Exception as e:
        logger.error(f"Error during PDF conversion: {e}")
        return []

    image_paths = []

    # Save each page as an image
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i}.png')
        try:
            image.save(image_path, 'PNG')
            image_paths.append(os.path.relpath(image_path, settings.MEDIA_ROOT))
            logger.info(f"Saved image {image_path}")
        except Exception as e:
            logger.error(f"Error saving image {image_path}: {e}")

    logger.info(f"PDF conversion completed. Total pages: {len(image_paths)}")
    return image_paths
