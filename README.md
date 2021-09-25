# HackZurich2021


# setup and configure python envrionment

# Data download
Download and unzip the data in ``/data/raw/`` directory.
# Data preperation

```
python data_processing/src/data_processor.py
```

# Model training and evaluation

```
python modelling/train_model.py
```
Adjust paths for data_procssing and model training.


export BASE_PATH=/home/aneesh/Documents/HackZurich2021/team_repo/HackZurich2021/data
export PYTHONPATH=/home/aneesh/Documents/HackZurich2021/team_repo/HackZurich2021/data-processing