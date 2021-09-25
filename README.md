# HackZurich2021


# setup and configure python envrionment
## Environment variables:
```
export BASE_PATH=<path_to_repo>
export PYTHONPATH=$BASE_PATH
```

```
python3 -m venv ../seimens_env
source ../seimens_env/bin/activate
pip install -r  requirements.txt
```

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




### TO Remove
```
export BASE_PATH=/home/aneesh/Documents/HackZurich2021/team_repo/HackZurich2021
export PYTHONPATH=$BASE_PATH
export PYTHONPATH=/home/aneesh/Documents/HackZurich2021/team_repo/HackZurich2021/data-processing
```