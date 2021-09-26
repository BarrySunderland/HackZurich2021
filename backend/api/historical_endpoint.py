from flask import Flask
from paths import PATHS
from flask_restful import Resource, Api, reqparse
from data_processing.src.data_processor import DataProcessor
import datetime
import numpy as np
# from src.data.data_setup import data_setup
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Historical(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("date", required=True)
        parser.add_argument("position", required=True)
        args = parser.parse_args()
        query_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        try:
            return self._get_history(
                ["A2_RSSI"],
                int(args.position),
                query_date,
                20,
                200
            ) , 200
        except Exception as e:
            print(e)
            return {}, 400

    def _get_history(
        self,
        features: list,
        position: int,
        query_date: datetime.date,
        history: int,
        dt: int = 200,
    ):
        # dt, position tolerance in deci meters
        global rssi_comb_df
        f = []
        data = {}
        for h in range(history):
            d = query_date - datetime.timedelta(days=h)
            try:
                distance = position * 1000  # converting it into deci meter
                temp = rssi_comb_df.loc[(d)]
                temp = temp[temp.index.isin(range(distance - dt, distance + dt))]
                temp["quality2"] = temp["A2_ValidTel"] / temp["A2_TotalTel"]
                temp["quality1"] = temp["A1_ValidTel"] / temp["A1_TotalTel"]
                features_mean = temp[features].mean()
                f.append(features_mean)
                data[str(d)] = {f: v for f, v in zip(features, features_mean)}
            except Exception as e:
                print(e)
                data[str(d)] = {
                    f: v for f, v in zip(features, [np.nan] * len(features))
                }
        history = (
            pd.DataFrame(data)
            .apply(lambda row: row.fillna(row.mean()), axis=1)
            .to_dict()
        )
        return history

api.add_resource(Historical, '/api/historical')

if __name__ == "__main__":
    print("Loading the database in memory")
    global rssi_comb_df 
    print("Setting and collecting up the Historical database!")
    rssi_comb_df = DataProcessor.combine_events(save=False)
    app.run(port=5000)  