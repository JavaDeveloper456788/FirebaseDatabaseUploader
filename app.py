from utils import log
from parser_1 import Parser
from validator import Validator
from compare import Compare
import shutil
from os import listdir
import os.path
import firebase_admin
from firebase_admin import credentials

def main():
    try:
        cred = credentials.Certificate("config/firebase.json")
        firebase_admin.initialize_app(cred)
    except:
        print('Please put the creds in the config folder and rename it to "firebas.json"')
    files = [f for f in listdir("csv/") if os.path.isfile(os.path.join("csv/", f))]

    csv_files = []

    for f in files:
        if f.endswith("csv"):
            csv_files.append(f)

    if(len(csv_files) == 0):
        print("No CSV Files found. Please put the CSV Files in the csv folder")

    for file in csv_files:
        if not Validator.validate("csv/{}".format(file)):
            print("{} is corrupted, exiting...".format(file))
            exit()
    
    for file in csv_files:
        path = "csv/{}".format(file)
        old_path = "local/" + file.replace(".csv", ".old")
        entry_name = file.split('.')[0].replace(' ', '')

        print(entry_name)

        if os.path.exists(old_path):
            log("parseUpdated")
            Parser.parseUpdated(path, old_path, entry_name)
        else:
            log("parse")
            Parser.parse(path, entry_name)
        
        shutil.copyfile(path, old_path)
    
if __name__ == "__main__":
    main()