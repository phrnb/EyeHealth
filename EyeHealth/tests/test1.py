
import unittest
from image_processor_service import ImageProcessorService

class TestImageProcessorService(unittest.TestCase):

    def setUp(self):
        self.processor = ImageProcessorService()

    def test_resize_image(self):
        result = self.processor.resize_image("sample_image", 200, 300)
        self.assertEqual(result, "Resized image to 200x300")

    def test_resize_image_no_image(self):
        with self.assertRaises(ValueError):
            self.processor.resize_image(None, 200, 300)

    def test_normalize_image(self):
        result = self.processor.normalize_image("sample_image")
        self.assertEqual(result, "Normalized image")

    def test_normalize_image_no_image(self):
        with self.assertRaises(ValueError):
            self.processor.normalize_image(None)

if __name__ == "__main__":
    unittest.main()
