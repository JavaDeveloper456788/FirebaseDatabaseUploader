import os
import time
from caching import Caching
from parser_1 import Parser
import firebase_admin
from firebase_admin import credentials

def main():
    try:
        cred = credentials.Certificate("config/firebase.json")
        firebase_admin.initialize_app(cred)
    except:
        print('Please put the creds in the config folder and rename it to "firebas.json"')

    files = [f for f in os.listdir("csv/") if os.path.isfile(os.path.join("csv/", f))]

    csv_files = []

    for f in files:
        if f.endswith("csv"):
            csv_files.append(f)
    
    for f in csv_files:
        count = Caching.checkIfCachingExist(f)    
        if count != -1:
            print("Cached data found in {}, upload process of cached data will start in 10 sec".format(f))
            time.sleep(10)
            Parser.parseCached("csv/"+f, count)

if __name__=="__main__":
    main()