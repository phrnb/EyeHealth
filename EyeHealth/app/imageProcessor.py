import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Query

app = FastAPI(
    title="Image Processing API",
    description="API для обработки изображений с использованием различных техник",
    version="1.0.0",
)

# ================= ImageConverter ==================
class ImageConverter:
    def convert_format(self, image, format_type):
        """Конвертировать изображение в нужный формат"""
        print(f"Converting image to {format_type}")
        return image

    def resize_image(self, image, width, height):
        """Изменить размер изображения"""
        return cv2.resize(image, (width, height))

    def change_color_space(self, image, conversion_code):
        """Изменить цветовое пространство"""
        return cv2.cvtColor(image, conversion_code)

# ================= EdgeDetection ==================
class EdgeDetection:
    def __init__(self):
        self.image_converter = ImageConverter()

    def detect_edges(self, image):
        """Обнаружить границы с помощью Canny"""
        return cv2.Canny(image, 100, 200)

    def apply_sobel(self, image):
        """Применить оператор Собеля"""
        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        return cv2.magnitude(grad_x, grad_y)

    def apply_canny(self, image):
        """Применить Canny"""
        return cv2.Canny(image, 50, 150)

# ================= NoiseReduction ==================
class NoiseReduction:
    def __init__(self):
        self.edge_detection = EdgeDetection()

    def remove_salt_pepper_noise(self, image):
        """Удалить шум типа 'соль и перец'"""
        return cv2.medianBlur(image, 5)

    def apply_bilateral_filter(self, image):
        """Применить билинейный фильтр"""
        return cv2.bilateralFilter(image, 9, 75, 75)

    def smooth_edges(self, image):
        """Сгладить края"""
        return cv2.GaussianBlur(image, (5, 5), 0)

# ================= FeatureExtractor ==================
class FeatureExtractor:
    def __init__(self):
        self.noise_reduction = NoiseReduction()

    def extract_edges(self, image):
        """Извлечь края"""
        return self.noise_reduction.edge_detection.detect_edges(image)

    def detect_shapes(self, image):
        """Обнаружение фигур"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def calculate_histogram(self, image):
        """Рассчитать гистограмму изображения"""
        return cv2.calcHist([image], [0], None, [256], [0, 256])

# ================= SegmentationManager ==================
class SegmentationManager:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.edge_detection = EdgeDetection()

    def segment_image(self, image):
        """Сегментация изображения (например, пороговая бинаризация)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, segmented = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        return segmented

    def detect_regions(self, image):
        """Нахождение областей в изображении"""
        return self.feature_extractor.detect_shapes(image)

    def remove_background(self, image):
        """Удаление фона"""
        mask = self.segment_image(image)
        return cv2.bitwise_and(image, image, mask=mask)

# ================= FilterManager ==================
class FilterManager:
    def apply_gaussian_blur(self, image):
        """Применить размытие Гаусса"""
        return cv2.GaussianBlur(image, (5, 5), 0)

    def apply_median_filter(self, image):
        """Применить медианный фильтр"""
        return cv2.medianBlur(image, 5)

    def apply_sharpening(self, image):
        """Применить резкость"""
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

# ================= PreprocessingManager ==================
class PreprocessingManager:
    def __init__(self):
        self.segmentation_manager = SegmentationManager()
        self.filter_manager = FilterManager()

    def convert_to_grayscale(self, image):
        """Преобразование в градации серого"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def adjust_brightness(self, image, alpha, beta):
        """Настроить яркость изображения"""
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    def crop_image(self, image, x, y, w, h):
        """Обрезка изображения"""
        return image[y:y+h, x:x+w]

# ================= ImageProcessor (Главный класс) ==================
class ImageProcessor:
    def __init__(self):
        self.preprocessing_manager = PreprocessingManager()

    def process_image(self, image):
        """Полная обработка изображения"""
        gray = self.preprocessing_manager.convert_to_grayscale(image)
        filtered = self.preprocessing_manager.filter_manager.apply_gaussian_blur(gray)
        edges = self.preprocessing_manager.segmentation_manager.edge_detection.detect_edges(filtered)
        return edges

    def resize_image(self, image, width, height):
        """Изменить размер"""
        return cv2.resize(image, (width, height))

    def normalize_image(self, image):
        """Нормализация изображения"""
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

    def enhance_contrast(self, image):
        """Повышение контраста"""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        return cv2.merge((l, a, b))

# ================= Тестирование ==================
if __name__ == "__main__":
    img = cv2.imread("sample.jpg")  # Подставьте путь к своему изображению
    processor = ImageProcessor()

    processed = processor.process_image(img)
    cv2.imshow("Processed Image", processed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # ================= Endpoints ==================
@app.post("/convert_format")
def convert_format(image: UploadFile = File(...), format_type: str = Query(...)):
    img = read_image(image)
    print(f"Converting image to {format_type}")
    return convert_image_to_response(img)

@app.post("/resize_image")
def resize_image(image: UploadFile = File(...), width: int = Query(...), height: int = Query(...)):
    img = read_image(image)
    resized = cv2.resize(img, (width, height))
    return convert_image_to_response(resized)

@app.post("/apply_sobel")
def apply_sobel(image: UploadFile = File(...)):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(grad_x, grad_y)
    return convert_image_to_response(sobel)

@app.post("/remove_noise")
def remove_noise(image: UploadFile = File(...)):
    img = read_image(image)
    denoised = cv2.medianBlur(img, 5)
    return convert_image_to_response(denoised)

@app.post("/extract_edges")
def extract_edges(image: UploadFile = File(...)):
    img = read_image(image)
    edges = cv2.Canny(img, 100, 200)
    return convert_image_to_response(edges)

@app.post("/segment_image")
def segment_image(image: UploadFile = File(...)):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, segmented = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return convert_image_to_response(segmented)

@app.post("/normalize_image")
def normalize_image(image: UploadFile = File(...)):
    img = read_image(image)
    normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return convert_image_to_response(normalized)

@app.post("/enhance_contrast")
def enhance_contrast(image: UploadFile = File(...)):
    img = read_image(image)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced = cv2.merge((l, a, b))
    return convert_image_to_response(cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR))
