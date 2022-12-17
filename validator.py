from utils import log
import csv

class Validator:
    def isCorrupted(path):
        log("Validating {}".format(path))
        file = open(path, encoding="utf8")
        csv_reader = csv.reader(file) 

        header_len = len(next(csv_reader))

        count = 0
        try:
            for row in csv_reader:
                if not len(row) == header_len:
                    print("Invalid csv file: Number of column is not constant. Skipping...")
                    return True
                count += 1
                # print("{} {} {} {} {} {} {} {}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        except Exception as e:
            return True
        
        print("Total row found: {}".format(count))
        return False
    
    def checkDuplicateEntry(path: str):
        log("Checking for duplicate entry{}".format(path))
        file = open(path, encoding="utf8")
        log(type(file))
        
        csv_reader = csv.reader(file)

        next(csv_reader)

        list_keys = []
        for row in csv_reader:
            if row[0] in list_keys:
                print("Duplicate entry found. Entry name: {}, skipping this file.".format(row[0]))
                return True
            else:
                list_keys.append(row[0])
        return False