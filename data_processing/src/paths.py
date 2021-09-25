import os


class PATHS:
    base_path = os.environ['BASE_PATH']
    rssi = os.path.join(base_path, "data","raw","rssi.csv")
    events = os.path.join(base_path, "data","raw","events.csv")
    disruption =  os.path.join(base_path, "data","raw","disruptions.csv")
    data = os.path.join(base_path, "data")