import pandas as pd
from flask import Flask
from paths import PATHS
from flask_restful import Resource, Api, reqparse
from data_processing.src.data_processor import DataProcessor
import datetime
import requests
import numpy as np
import lightgbm as lgb
import os

app = Flask(__name__)
api = Api(app)

BASE_URL = "http://127.0.0.1:5000/"


def get_location(position):
    global location_df
    data = location_df.loc[int(position)]
    return {
        "Lattitude": data.Latitude,
        "Longitude": data.Longitude,
        "position": int(position),
    }

class Coordinates(Resource):
    def get(self):
        global location_df
        parser = reqparse.RequestParser()
        # in 100 meters int. varies from 97 to 428
        parser = parser.add_argument("position", required=True)
        args = parser.parse_args()
        try:
            data = location_df.loc[int(args.position)]
        except Exception as e:

            data = location_df.loc[120]
            return {} , 400
        return {
            "Lattitude": data.Latitude,
            "Longitude": data.Longitude,
            "position": int(args.position),
        }, 200

class Prediction(Resource):
    def __init__(self):
        # TODO; Load models.
        models = []
        for d in range(1, 14):
            model_path = os.path.join(PATHS.model, f"lgb_model_d{d}.txt")
            models.append(lgb.Booster(model_file=model_path))
        self.models = models

    def _extract_features(self, position, history):
        rssi = np.array(
            [history[step]["A2_RSSI"] for step in sorted(list(history.keys()))]
        )
        print(position)
        return [np.mean(rssi), np.std(rssi), int(position) * 1000.0]

    def get(self):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("date", required=True)
        parser.add_argument("position", required=True)
        args = parser.parse_args()
        params = {"position": args.position, "date": args.date}
        print("Making historical data request")
        history = requests.get(url=BASE_URL + "/api/historical", params=params).json()
        features = self._extract_features(args.position, history)
        scores = []
        for model in self.models:
            scores.append(model.predict(np.array(features).reshape(1, -1))[0])
        scores = np.array(scores)
        confidence = np.abs(scores - 0.5) / 0.5 * 100
        coords = get_location(args.position)
        return {
            **{
                "position":args.position,
                "date":args.date,
                "predictions": ((scores > 0.5) * 1).tolist(),
                "confidence": confidence.tolist(),
                "description": {1: "disruption", 2: "no-disruption"},
            },
            **coords,
        }


api.add_resource(Prediction, "/api/predict")
api.add_resource(Coordinates, "/api/coordinates")

if __name__ == "__main__":
    global location_df
    location_path = DataProcessor.gen_proc_file_name("location.csv")
    location_df = pd.read_csv(location_path, index_col="Position_m")
    app.run(port=5789)
