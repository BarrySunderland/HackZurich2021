import pandas as pd
import tqdm
from paths import PATHS
import os


class DataProcessor:
    @staticmethod
    def gen_proc_file_name(file_name):
        return os.path.join(PATHS.data, "processed", file_name)

    @staticmethod
    def add_rssi_fields_to_disruptions(save: bool = True):
        """This methods perform inner join on disruptions with the rssi values.
        This results in obtaining values in rssi table for events of interest.

        Returns:
            [type]: [description]
        """
        # RSSI data is too big to load onn cpu at a time.
        rssi_df_s = pd.read_csv(
            PATHS.rssi,
            chunksize=10000,
            iterator=True,
            infer_datetime_format=True,
            parse_dates=True,
        )
        disruption_df = pd.read_csv(
            PATHS.disruption, infer_datetime_format=True, parse_dates=True
        )
        merged_dfs = []
        with tqdm.tqdm(total=3098) as pbar:
            for rssi_df in rssi_df_s:
                merged_dfs.append(pd.merge(rssi_df, disruption_df, on="DateTime"))
                pbar.update(1)
        result_df = pd.concat(merged_dfs)
        if save:
            result_df.to_csv(DataProcessor.gen_proc_file_name("disruption.csv"))
        return result_df

    @staticmethod
    def add_rssi_fields_to_events(save: bool = True):
        """This methods perform inner join on disruptions with the rssi values.
        This results in obtaining values in rssi table for events of interest.

        Returns:
            [type]: [description]
        """
        # RSSI data is too big to load onn cpu at a time.
        rssi_df_s = pd.read_csv(
            PATHS.rssi,
            chunksize=10000,
            iterator=True,
            infer_datetime_format=True,
            parse_dates=True,
        )
        events_df = pd.read_csv(
            PATHS.events, infer_datetime_format=True, parse_dates=True
        )
        merged_dfs = []
        with tqdm.tqdm(total=3098) as pbar:
            for rssi_df in rssi_df_s:
                merged_dfs.append(pd.merge(rssi_df, events_df, on="DateTime"))
                pbar.update(1)
            result_df = pd.concat(merged_dfs)

        if save:
            result_df.to_csv(DataProcessor.gen_proc_file_name("events.csv"))
        return pd.concat(merged_dfs)

    @staticmethod
    def combine_events(save: bool = False):
        """This methods combines "A1_TotalTel","A1_ValidTel","A2_RSSI","A2_TotalTel","A2_ValidTel"
        for a day and location based on day and distance.
        """
        # RSSI data is too big to load onn cpu at a time.
        column_of_interest = [
            "PositionNoLeap",
            "Date",
            "Latitude",
            "Longitude",
            "A1_TotalTel",
            "A1_ValidTel",
            "A2_RSSI",
            "A2_TotalTel",
            "A2_ValidTel",
        ]
        rssi_df_s = pd.read_csv(
            PATHS.rssi,
            chunksize=10000,
            iterator=True,
            infer_datetime_format=True,
            parse_dates=True,
        )
        merged_dfs = []
        with tqdm.tqdm(total=3098) as pbar:
            for rssi_df in rssi_df_s:
                rssi_df["Date"] = pd.to_datetime(rssi_df["DateTime"]).dt.date
                merged_dfs.append(
                    rssi_df[column_of_interest]
                    .groupby(by=["Date", "PositionNoLeap"])
                    .mean()
                )
                pbar.update(1)
        result_df = pd.concat(merged_dfs)
        if save:
            result_df.to_csv(DataProcessor.gen_proc_file_name("rssi_mean.csv"))
        return result_df

    @staticmethod
    def make_positional_mapping(save=True):
        column_of_interest = ["PositionNoLeap", "Latitude", "Longitude"]
        rssi_df_s = pd.read_csv(
            PATHS.rssi,
            chunksize=10000,
            iterator=True,
            infer_datetime_format=True,
            parse_dates=True,
        )
        merged_dfs = []
        with tqdm.tqdm(total=3098) as pbar:
            for rssi_df in rssi_df_s:
                temp = (
                    rssi_df[column_of_interest]
                    .groupby(by=["PositionNoLeap"])
                    .mean()
                    .reset_index()
                )
                temp["Position_m"] = temp["PositionNoLeap"] // 1000
                temp = temp.groupby(by=["Position_m"]).mean()
                merged_dfs.append(temp)
                pbar.update(1)
        #             break
        result_df = pd.concat(merged_dfs)
        result_df = (
            result_df.reset_index()
            .drop_duplicates("Position_m")
            .set_index("Position_m")
        )
        if save:
            result_df.to_csv(DataProcessor.gen_proc_file_name("location.csv"))
        return result_df


def main():
    print("1. Adding RSSI values to disruption")
    disruption_path = DataProcessor.gen_proc_file_name("disruption.csv")
    location_path = DataProcessor.gen_proc_file_name("location.csv")
    rssi_mean_path = DataProcessor.gen_proc_file_name("rssi_mean.csv")
    if not os.path.exists(disruption_path):
        DataProcessor.add_rssi_fields_to_disruptions()
    else:
        print("skipping disruption processing, file already exists!")

    print("2. Mapping locations to coordinates")
    if not os.path.exists(location_path):
        DataProcessor.make_positional_mapping()
    else:
        print("skipping location processing, file already exists!")
    print("3. Processing mean_rssi values")
    if not os.path.exists(rssi_mean_path):
        DataProcessor.combine_events(save= True)
    else:
        print("skipping mean_rssi processing, file already exists!")


if __name__ == "__main__":
    main()
