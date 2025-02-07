from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ================= Инициализация =================
DATABASE_URL = "postgresql://postgres:password@localhost/analyticsdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# ================= Модель данных =================
class DataPoint(Base):
    __tablename__ = "data_points"
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ================= DataCollector =================
class DataCollector:
    def __init__(self, db: Session):
        self.db = db

    def collect_data(self, metric_name: str, value: float):
        new_data = DataPoint(metric_name=metric_name, value=value)
        self.db.add(new_data)
        self.db.commit()
        return new_data

# ================= DataProcessor =================
class DataProcessor:
    def clean_data(self, data: pd.DataFrame):
        data = data.dropna()
        data = data[data["value"] > 0]
        return data

    def aggregate_metrics(self, data: pd.DataFrame):
        return data.groupby("metric_name").agg({"value": ["mean", "max", "min"]})

# ================= AnomalyDetector =================
class AnomalyDetector:
    def detect_anomalies(self, data: pd.DataFrame):
        model = IsolationForest(contamination=0.05)
        data["anomaly"] = model.fit_predict(data[["value"]])
        return data[data["anomaly"] == -1]

# ================= TrendAnalyzer =================
class TrendAnalyzer:
    def analyze_trends(self, data: pd.DataFrame):
        trends = data.groupby("metric_name").resample("D", on="timestamp").mean()
        return trends

# ================= PredictionModel =================
class PredictionModel:
    def predict_trend(self, data: pd.DataFrame):
        trend = np.polyfit(data.index.astype(int), data["value"], 1)
        return trend

# ================= ReportGenerator =================
class ReportGenerator:
    def generate_report(self, data: pd.DataFrame):
        plt.figure(figsize=(10, 5))
        for metric in data["metric_name"].unique():
            subset = data[data["metric_name"] == metric]
            plt.plot(subset["timestamp"], subset["value"], label=metric)
        plt.legend()
        plt.savefig("report.png")

# ================= AnalyticService =================
class AnalyticService:
    def __init__(self, db: Session):
        self.data_collector = DataCollector(db)
        self.data_processor = DataProcessor()
        self.anomaly_detector = AnomalyDetector()
        self.trend_analyzer = TrendAnalyzer()
        self.prediction_model = PredictionModel()
        self.report_generator = ReportGenerator()

    def analyze_data(self):
        query = f"SELECT * FROM data_points"
        data = pd.read_sql(query, engine)

        clean_data = self.data_processor.clean_data(data)
        anomalies = self.anomaly_detector.detect_anomalies(clean_data)
        trends = self.trend_analyzer.analyze_trends(clean_data)
        predictions = self.prediction_model.predict_trend(trends)
        self.report_generator.generate_report(clean_data)

        return {"anomalies": anomalies.to_dict(), "predictions": predictions.tolist()}

# ================= API =================
@app.post("/collect")
def collect_data(metric_name: str, value: float, db: Session = Depends(SessionLocal)):
    service = DataCollector(db)
    return service.collect_data(metric_name, value)

@app.get("/analyze")
def analyze_data(db: Session = Depends(SessionLocal)):
    service = AnalyticService(db)
    return service.analyze_data()
