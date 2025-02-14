import tensorflow as tf
from tensorflow import keras
import numpy as np
import psycopg2
import json


# ================= DatabaseHandler (PostgreSQL) ==================
class DatabaseHandler:
    def __init__(self, db_name="ml_predictions", user="postgres", password="password", host="localhost", port="5432"):
        self.conn_params = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self._initialize_db()

    def _initialize_db(self):
        """Создание таблицы для хранения предсказаний в PostgreSQL"""
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Predictions (
                id SERIAL PRIMARY KEY,
                input_data JSONB,
                prediction JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save_prediction(self, input_data, prediction):
        """Сохранение предсказания в БД"""
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Predictions (input_data, prediction) VALUES (%s, %s)",
                       (json.dumps(input_data), json.dumps(prediction)))
        conn.commit()
        conn.close()

    def load_predictions(self):
        """Загрузка предсказаний из PostgreSQL"""
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Predictions")
        predictions = cursor.fetchall()
        conn.close()
        return predictions


# ================= DataLoader ==================
class DataLoader:
    def load_from_database(self, db_handler, query):
        """Загрузка данных из PostgreSQL"""
        conn = psycopg2.connect(**db_handler.conn_params)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return np.array(data)  # Преобразуем в numpy

    def load_from_file(self, file_path):
        """Загрузка данных из файла"""
        print(f"Loading data from file: {file_path}")
        return np.random.rand(100, 10)


# ================= ModelLayers ==================
class ModelLayers:
    def DenseLayer(self, units, activation='relu'):
        return keras.layers.Dense(units, activation=activation)

    def Dropout(self, rate):
        return keras.layers.Dropout(rate)


# ================= NeuralNetworkModel ==================
class NeuralNetworkModel:
    def __init__(self):
        self.model = None

    def build_model(self, input_shape):
        """Создание модели"""
        self.model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])

    def compile_model(self):
        """Компиляция модели"""
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        """Обучение модели"""
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)


# ================= ModelTrainer ==================
class ModelTrainer:
    def __init__(self, data_loader, db_handler):
        self.data_loader = data_loader
        self.db_handler = db_handler
        self.model = NeuralNetworkModel()

    def train(self):
        """Обучение модели"""
        X_train = self.data_loader.load_from_database(self.db_handler, "SELECT * FROM training_data")
        y_train = np.random.randint(0, 2, X_train.shape[0])  # Генерация случайных меток
        self.model.build_model(X_train.shape[1])
        self.model.compile_model()
        self.model.train(X_train, y_train)


# ================= ModelSaver ==================
class ModelSaver:
    def save_model(self, model, path="model.h5"):
        """Сохранение модели"""
        model.save(path)

    def load_model(self, path="model.h5"):
        """Загрузка модели"""
        return keras.models.load_model(path)


# ================= InferenceEngine ==================
class InferenceEngine:
    def __init__(self, model):
        self.model = model

    def predict(self, input_data):
        """Выполнение предсказания"""
        return self.model.predict(np.array([input_data])).tolist()


# ================= PredictionLogger ==================
class PredictionLogger:
    def __init__(self, database_handler):
        self.database_handler = database_handler

    def log_prediction(self, input_data, prediction):
        """Логирование предсказания в PostgreSQL"""
        self.database_handler.save_prediction(input_data, prediction)

    def retrieve_logs(self):
        """Получение логов предсказаний"""
        return self.database_handler.load_predictions()
        
        class ProxyNeuralNetworkModel:
    """Прокси для модели нейронной сети, который загружает и обучает модель только по необходимости."""
    
    def __init__(self, model_saver: ModelSaver):
        self.model_saver = model_saver
        self._model = None  # Модель пока не загружена

    def _load_model(self):
        """Загрузка модели, если она ещё не была загружена."""
        if self._model is None:
            print("Загружаем модель...")
            self._model = self.model_saver.load_model()  # Загружаем модель с диска
        return self._model

    def predict(self, input_data):
        """Предсказание через прокси."""
        model = self._load_model()  # Лениво загружаем модель, если это необходимо
        inference_engine = InferenceEngine(model)
        return inference_engine.predict(input_data)  # Выполняем предсказание через реальную модель
    
    def train(self, X_train, y_train, epochs=10, batch_size=32):
        """Обучение модели через прокси."""
        model = self._load_model()  # Лениво загружаем модель, если это необходимо
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)  # Обучаем модель


# ================= NeuralNetworkService (Основной сервис) ==================
class NeuralNetworkService:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.data_loader = DataLoader()
        self.trainer = ModelTrainer(self.data_loader, self.db_handler)
        self.model_saver = ModelSaver()
        self.logger = PredictionLogger(self.db_handler)
        self.model_proxy = ProxyNeuralNetworkModel(self.model_saver)  # Используем прокси

    def train_model(self):
        """Запуск процесса обучения через прокси"""
        X_train = self.data_loader.load_from_database(self.db_handler, "SELECT * FROM training_data")
        y_train = np.random.randint(0, 2, X_train.shape[0])  # Генерация случайных меток
        self.model_proxy.train(X_train, y_train)  # Обучаем модель через прокси
        self.model_saver.save_model(self.model_proxy._model)  # Сохраняем модель после обучения

    def predict(self, input_data):
        """Инференс модели через прокси"""
        prediction = self.model_proxy.predict(input_data)  # Используем прокси для предсказания
        self.logger.log_prediction(input_data, prediction)
        return prediction



# ================= Тестирование ==================
if __name__ == "__main__":
    service = NeuralNetworkService()

    # Обучение модели
    print("Training model...")
    service.train_model()

    # Тестовое предсказание
    test_input = np.random.rand(10)
    print("Making prediction...")
    prediction = service.predict(test_input)

    print(f"Prediction: {prediction}")
    @app.post("/train_model")
def train_model():
    global model
    # Генерируем случайную модель (заглушка для обучения)
    model = np.random.rand(10, 10)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return {"message": "Модель успешно обучена и сохранена."}

@app.post("/predict")
def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=400, detail="Модель не загружена. Сначала обучите или загрузите её.")
    
    input_array = np.array(input_data.input_data)
    prediction = input_array.dot(model.mean(axis=1))  # Пример вычисления
    
    return {"prediction": prediction.tolist(), "message": "Предсказание успешно выполнено."}

@app.post("/log_prediction")
def log_prediction(input_data: PredictionInput, prediction: List[float]):
    log_entry = {
        "id": len(logs) + 1,
        "input_data": input_data.input_data,
        "prediction": prediction,
        "created_at": datetime.datetime.now().isoformat()
    }
    logs.append(log_entry)
    return {"message": "Предсказание успешно залогировано в базе данных."}

@app.get("/retrieve_logs", response_model=List[PredictionLog])
def retrieve_logs():
    return logs

@app.post("/save_model")
def save_model(model_path: ModelPath):
    if model is None:
        raise HTTPException(status_code=400, detail="Нет модели для сохранения.")
    with open(model_path.path, "wb") as f:
        pickle.dump(model, f)
    return {"message": "Модель успешно сохранена."}

@app.post("/load_model")
def load_model(model_path: ModelPath):
    global model
    if not os.path.exists(model_path.path):
        raise HTTPException(status_code=404, detail="Файл модели не найден.")
    with open(model_path.path, "rb") as f:
        model = pickle.load(f)
    return {"message": "Модель успешно загружена."}

