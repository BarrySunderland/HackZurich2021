# unzip the raw data


import os
from zipfile import ZipFile


if __name__ == "__main__":
    
    input_dir = "../data/raw" 
    output_dir = input_dir # "../data/interim"

    zipfiles = [f for f in os.listdir(input_dir) if f.endswith(".zip")]
    print(zipfiles)

    for zipfile in zipfiles:
        fpath_in = os.path.join(input_dir, zipfile)

        with ZipFile(fpath_in, 'r') as zipObj:
           # Extract all the contents of zip file
           zipObj.extractall(output_dir)
