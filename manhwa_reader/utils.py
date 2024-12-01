import os
from pdf2image import convert_from_path
from django.conf import settings

def convert_pdf_to_images(pdf_path, chapter):
    print(f"Starting PDF conversion for {pdf_path}...")

    # Ensure that the images are saved in the correct location in 'media/manhwa_images/'
    output_dir = os.path.join(settings.MEDIA_ROOT, 'manhwa_images', f'chapter_{chapter.id}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Convert PDF to images
    images = convert_from_path(pdf_path)
    image_paths = []

    # Save each page as an image
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
        print(f"Saved image {image_path}")

    print(f"PDF conversion completed. Total pages: {len(image_paths)}")
    return image_paths
