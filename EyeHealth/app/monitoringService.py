from fastapi import FastAPI, HTTPException
import psutil
import redis
import smtplib
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import datetime

# ========== Конфигурация ==========
DATABASE_URL = "postgresql://postgres:password@localhost/monitoringdb"
REDIS_URL = "redis://localhost:6379/0"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
ADMIN_EMAIL = "admin@example.com"
ALERT_THRESHOLD_CPU = 80
ALERT_THRESHOLD_MEM = 80

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI()

# ========== Логирование ==========
logging.basicConfig(filename="monitoring.log", level=logging.INFO, format="%(asctime)s - %(message)s")


class LoggingService:
    @staticmethod
    def log_event(event: str):
        logging.info(event)


# ========== Сбор метрик ==========
class MetricsCollector:
    @staticmethod
    def collect():
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "requests_count": redis_client.get("requests") or 0
        }


# ========== Обнаружение аномалий ==========
class AnomalyDetector:
    @staticmethod
    def check_anomalies(metrics):
        alerts = []
        if metrics["cpu_usage"] > ALERT_THRESHOLD_CPU:
            alerts.append(f"Высокая нагрузка на CPU: {metrics['cpu_usage']}%")
        if metrics["memory_usage"] > ALERT_THRESHOLD_MEM:
            alerts.append(f"Высокое использование памяти: {metrics['memory_usage']}%")
        return alerts


# ========== Отправка уведомлений ==========
class AlertService:
    @staticmethod
    def send_alert(message):
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail("monitoring@example.com", ADMIN_EMAIL, f"Subject: ALERT!\n\n{message}")


# ========== База данных ==========
class MonitoringLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=func.now())
    message = Column(String)


Base.metadata.create_all(bind=engine)


class ReportGenerator:
    @staticmethod
    def generate_report():
        session = SessionLocal()
        logs = session.query(MonitoringLog).all()
        session.close()
        return [f"{log.timestamp}: {log.message}" for log in logs]


# ========== API ==========
@app.get("/metrics")
def get_metrics():
    metrics = MetricsCollector.collect()
    LoggingService.log_event(f"Собраны метрики: {metrics}")

    alerts = AnomalyDetector.check_anomalies(metrics)
    if alerts:
        for alert in alerts:
            AlertService.send_alert(alert)
            LoggingService.log_event(alert)

    return metrics


@app.get("/report")
def get_report():
    return {"report": ReportGenerator.generate_report()}
