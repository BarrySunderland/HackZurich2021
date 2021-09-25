import pandas as pd
import json


def line_to_dict_format(row: list):
    """
    This function converts a pandas dataframe row to a dictionary
    """

    latitude = row[0]
    longtitude = row[1]
    quality2 = row[2]
    quality1 = row[3]
    a2_rssi = row[4]
    quality2_std = row[5]
    quality1_std = row[6]
    a2_rssi_std = row[7]
    past_dates = row[8]
    date = row[9]
    position_no_leap = row[10]
    disruption = row[11]

    # saves the data in the form of a dict
    json_dict = {"type": "Feature",
                 "geometry": {"type": "Point", "coordinates": [longtitude, latitude]},
                 "properties": {"quality_1": quality1,
                                "quality_2": quality2,
                                "a2_rssi": a2_rssi,
                                "quality_1_std": quality1_std,
                                "quality_2_std": quality2_std,
                                "a2_rssi_std": a2_rssi_std,
                                "past_dates": past_dates,
                                "date": date,
                                "position_no_leap": position_no_leap,
                                "disruption": disruption}}
    return json_dict


def convert_csv_to_geojson(path_to_csv_file='aneesh_data.csv'):
    """
    This function converts a csv file to a geojson format
    :param path_to_csv_file: the path to the csv provided by aneesh analysis
    """
    # reading the csv file
    aneesh_csv = pd.read_csv(path_to_csv_file, index_col=0)
    rows_list = list(aneesh_csv.values)

    # creating the features for the geojson
    list_of_dicts = []

    for row_list in rows_list:
        dict_row = line_to_dict_format(row_list)
        list_of_dicts.append(dict_row)

    # finishing touches for the geojson
    entire_json_dict = {
        "type": "FeatureCollection",
        "features": list_of_dicts
    }

    # saving it as geojson.json
    with open('horizon.geojson', 'w') as outfile:
        json.dump(entire_json_dict, outfile)
