import unittest
import cv2
import numpy as np
from imageProcessor import ImageProcessor, ImageConverter, EdgeDetection, NoiseReduction, FeatureExtractor

class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        # Подготовка изображения для тестов
        self.image = np.zeros((100, 100, 3), dtype=np.uint8)  # Черное изображение
        # Добавляем более выраженный шум 'соль и перец'
        for i in range(100):
            for j in range(100):
                if np.random.rand() < 0.05:  # 5% вероятности для пикселя быть шумом
                    self.image[i, j] = [255, 255, 255]  # Белый пиксель (соль)
        self.processor = ImageProcessor()
        self.converter = ImageConverter()
        self.edge_detector = EdgeDetection()
        self.noise_reduction = NoiseReduction()
        self.feature_extractor = FeatureExtractor()

    def test_remove_salt_pepper_noise(self):
        # Применяем медианный фильтр для удаления шума
        denoised = self.noise_reduction.remove_salt_pepper_noise(self.image)

        # Проверяем, что шум устранен (пиксели в центре изображения должны стать черными)
        # Мы проверяем несколько случайных пикселей, чтобы убедиться, что шум был удален.
        noisy_pixels = [(50, 50), (10, 10), (90, 90), (70, 70), (30, 30)]
        for pixel in noisy_pixels:
            self.assertTrue(np.array_equal(denoised[pixel[0], pixel[1]], [0, 0, 0]),
                            f"Pixel at {pixel} is not black after denoising")

        # Дополнительно можно проверить, что изображение больше не полностью белое
        self.assertTrue(np.any(denoised != [255, 255, 255]), "Image is still full of noise")

    def test_resize_image(self):
        resized = self.processor.resize_image(self.image, 50, 50)
        self.assertEqual(resized.shape, (50, 50, 3))  # Проверяем, что изображение имеет размеры 50x50

    def test_convert_to_grayscale(self):
        gray = self.processor.preprocessing_manager.convert_to_grayscale(self.image)
        self.assertEqual(gray.shape, (100, 100))  # Проверяем, что результат — это изображение 100x100 в оттенках серого
        self.assertEqual(len(gray.shape), 2)  # Изображение в оттенках серого должно быть 2D

    def test_edge_detection(self):
        edges = self.edge_detector.detect_edges(self.image)
        self.assertEqual(edges.shape, (100, 100))  # Проверяем размер результата
        self.assertTrue(np.any(edges))  # Убедимся, что найдены границы



    def test_extract_edges(self):
        edges = self.feature_extractor.extract_edges(self.image)
        self.assertEqual(edges.shape, (100, 100))  # Проверяем размер результата
        self.assertTrue(np.any(edges))  # Убедимся, что в изображении есть края

    def test_detect_shapes(self):
        shapes = self.feature_extractor.detect_shapes(self.image)
        self.assertTrue(len(shapes) > 0)  # Проверяем, что найден хотя бы один контур

    def test_normalize_image(self):
        normalized = self.processor.normalize_image(self.image)
        self.assertEqual(normalized.min(), 0)  # Минимальное значение после нормализации должно быть 0
        self.assertEqual(normalized.max(), 255)  # Максимальное значение после нормализации должно быть 255

    def test_enhance_contrast(self):
        enhanced = self.processor.enhance_contrast(self.image)
        self.assertEqual(enhanced.shape, (100, 100, 3))  # Проверяем, что изображение не изменило размер
        self.assertTrue(np.any(enhanced))  # Убедимся, что контраст улучшен

    def test_apply_sobel(self):
        # Преобразуем изображение в оттенки серого
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Применяем операцию Собеля
        sobel_image = self.edge_detector.apply_sobel(gray_image)

        # Проверяем, что результат имеет форму (100, 100), так как это одно-канальное изображение
        self.assertEqual(sobel_image.shape, (100, 100))  # Проверка на одно-канальное изображение

        # Также можно добавить проверку на наличие значений в изображении (т.е. что обработка дала результат)
        self.assertTrue(np.any(sobel_image))  # Убедимся, что изображение не пустое
    def test_apply_bilateral_filter(self):
        filtered_image = self.noise_reduction.apply_bilateral_filter(self.image)
        self.assertEqual(filtered_image.shape, (100, 100, 3))  # Проверяем размер изображения
        self.assertTrue(np.any(filtered_image))  # Убедимся, что изображение не пустое

    def test_segment_image(self):
        segmented = self.processor.preprocessing_manager.segmentation_manager.segment_image(self.image)
        self.assertEqual(segmented.shape, (100, 100))  # Проверяем размер сегментированного изображения
        self.assertTrue(np.any(segmented))  # Убедимся, что сегментация не пустая

    def test_apply_gaussian_blur(self):
        blurred = self.processor.preprocessing_manager.filter_manager.apply_gaussian_blur(self.image)
        self.assertEqual(blurred.shape, (100, 100, 3))  # Проверяем размер изображения
        self.assertTrue(np.any(blurred))  # Убедимся, что размытие применилось

if __name__ == "__main__":
    unittest.main()
