from flask import Flask, jsonify, request
from analyticService import AnalyticService
from apiGateway import ApiGateway
from db import Database
from imageProcessor import ImageProcessor
from monitoringService import MonitoringService
from neuralNetwork import NeuralNetwork
from security_handlers import SecurityHandlers
from userService import UserService

app = Flask(__name__)

# Инициализация сервисов
analytic_service = AnalyticService()
api_gateway = ApiGateway()
db = Database()
image_processor = ImageProcessor()
monitoring_service = MonitoringService()
neural_network = NeuralNetwork()
security_handlers = SecurityHandlers()
user_service = UserService()

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    result = analytic_service.analyze(data)
    return jsonify(result)

@app.route("/api/upload-image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    result = image_processor.process(file)
    return jsonify(result)

@app.route("/api/login", methods=["POST"])
def login():
    credentials = request.get_json()
    user = user_service.authenticate(credentials)
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/monitoring", methods=["GET"])
def get_monitoring_data():
    data = monitoring_service.get_data()
    return jsonify(data)

@app.route("/api/neural-network", methods=["POST"])
def neural_network_predict():
    data = request.get_json()
    prediction = neural_network.predict(data)
    return jsonify({"prediction": prediction})

@app.route("/api/security/check", methods=["GET"])
def check_security():
    status = security_handlers.check_security()
    return jsonify({"security_status": status})

@app.route("/api/gateway", methods=["GET"])
def api_gateway_route():
    data = api_gateway.handle_request()
    return jsonify(data)

@app.route("/api/users", methods=["GET"])
def get_users():
    users = user_service.get_users()
    return jsonify(users)

@app.route("/api/database", methods=["GET"])
def get_database_status():
    status = db.get_status()
    return jsonify({"db_status": status})

if __name__ == "__main__":
    app.run(debug=True)
