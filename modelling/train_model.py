from data_processing.src.feature_extractor import DataGenerator
from data_processing.src.data_processor import DataProcessor
from paths import PATHS
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import os


def main():
    disruption_df = pd.read_csv(
        DataProcessor.gen_proc_file_name("disruption.csv"),
        infer_datetime_format=True,
        parse_dates=True,
    )
    # ideally this should be from a database, as loading entirety of this data is super slow.
    print("Following step takes a lot of time, around 30-35 min, go get a coffee!")
    print("14 models into the future are trained")
    print("Collecting RSSI historical Data")
    rssi_comb_df = DataProcessor.combine_events(save=False)
    print("Data collection Done!")
    train_disruptions_df, test_disruptions_df = train_test_split(
        disruption_df, test_size=0.2
    )
    features = ["A2_RSSI"]
    train_disruptions_df, test_disruptions_df = train_test_split(
        disruption_df, test_size=0.2
    )
    models = []
    scores = []
    for d in range(1, 14):
        train_data = DataGenerator(train_disruptions_df, rssi_comb_df, features)
        train_x, train_y = train_data.generate_samples(
            num_samples=300, prediction_days=d, history=20
        )
        test_data = DataGenerator(test_disruptions_df, rssi_comb_df, features)
        test_x, test_y = test_data.generate_samples(
            num_samples=50, prediction_days=d, history=20
        )
        model = lgb.LGBMClassifier()
        model.fit(X=train_x, y=train_y)
        print(
            f"Train accuracy score for {d} days into future  {model.score(train_x,train_y)}"
        )
        print(
            f"Test accuracy score for {d} days into future {model.score(test_x,test_y)}"
        )
        scores.append([model.score(test_x, test_y), model.score(train_x, train_y)])
        model.booster_.save_model(
            os.path.join(PATHS.data, "model", f"lgb_model_d{d}.txt")
        )
        models.append(model)

    print(scores)


if __name__ == "__main__":
    main()
