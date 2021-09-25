import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tqdm
import datetime
import numpy as np

class DataGenerator:
    
    def __init__(self,disruptions_df, rssi_comp_df, features):
        self.disruptions_df = disruptions_df
        self.features = features
        self.disruptions_df["Date"] = pd.to_datetime(disruptions_df["DateTime"]).dt.date
        self.rssi_comp_df = rssi_comp_df
        
    def get_past_features(self, features:list, distance:int, query_date:datetime.date, history:int, dt:int =200):
        # dt, position tolerance in deci meters
        features_matrix = np.zeros((history,len(features)))
        for h in range(history):
            d = query_date-datetime.timedelta(days=h)
            try:
                temp = self.rssi_comp_df.loc[(d)]
                temp = temp[temp.index.isin(range(distance-dt,distance+dt))]
                temp["quality2"] = temp["A2_ValidTel"]/temp["A2_TotalTel"]
                temp["quality1"] = temp["A1_ValidTel"]/temp["A1_TotalTel"]
                features_mean = temp[features].mean().values
            except Exception as e:
                # Fills missing  values with NAN, which are later replaced with window average. 
                features_mean=np.array([np.nan]*len(features)) 
            features_matrix[h][:] = features_mean
        
        # replacing NANs because of the missing data(weekend) with average of the entire window.
        features_matrix = np.where(np.isnan(features_matrix), np.ma.array(features_matrix, mask=np.isnan(features_matrix)).mean(axis=0), features_matrix)
        return features_matrix 

    
    def generate_samples(self,num_samples:int, prediction_days:int, history:int):
        """
        Generates 50% samples for events and 50% samples for no event.
        class 1: disruption
        class 0: No disruption
        """
        x = []
        y = []
        disruptions = self.disruptions_df.sample(n=num_samples//2,replace=True)
        for i in tqdm.tqdm(range(len(disruptions))):
            sample =disruptions[["Date","PositionNoLeap"]].iloc[i]
            query_date = sample.Date - datetime.timedelta(days=prediction_days)
            features = self.get_past_features(self.features, distance =sample.PositionNoLeap,query_date =query_date, history=history)
            features = np.array([np.mean(features), np.std(features)])
            f = features.reshape((1,-1))
            if np.sum(f)>1e-5:
                f = np.append(f,[sample.PositionNoLeap])
                x.append(f.reshape((1,-1)))
                y.append(1)

        
        # reason for not weeding out disruptions from this dataset is because the chances of sampling an event are incredibly low.
        no_disrutpions = self.rssi_comp_df.sample(n=num_samples//2,replace=True).reset_index()
        for i in tqdm.tqdm(range(len(no_disrutpions))):
            sample =no_disrutpions[["Date","PositionNoLeap"]].iloc[i]

            query_date = sample.Date - datetime.timedelta(days=prediction_days)
            features = self.get_past_features(self.features, distance =sample.PositionNoLeap,query_date =query_date,history= history)
            features = np.array([np.mean(features), np.std(features)])
            f = features.reshape((1,-1))
            if np.sum(f)>1e-5:
                f = np.append(f,[sample.PositionNoLeap])
                x.append(f.reshape((1,-1)))
                y.append(0)
        
        return np.array(x).squeeze(), np.array(y)


