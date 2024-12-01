from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Chapter, Manhwa, Image
from .utils import convert_pdf_to_images

class PDFConversionTest(TestCase):
    def setUp(self):
        # Create a dummy Manhwa and Chapter
        self.manhwa = Manhwa.objects.create(title="Test Manhwa")
        self.chapter = Chapter.objects.create(title="Test Chapter", manhwa=self.manhwa)

        # Create a dummy PDF file
        self.pdf_file = SimpleUploadedFile("test.pdf", b"dummy content", content_type="application/pdf")

    def test_convert_pdf_to_images(self):
        # Test the conversion function
        pdf_path = self.pdf_file.name  # Use a dummy path or mock an actual PDF
        image_paths = convert_pdf_to_images(pdf_path, self.chapter)

        # Assert images were created and associated with the chapter
        self.assertTrue(len(image_paths) > 0)
        self.assertEqual(Image.objects.filter(chapter=self.chapter).count(), len(image_paths))
