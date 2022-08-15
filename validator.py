from utils import log
import csv

class Validator:
    def validate(path):
        log("Validating {}".format(path))
        file = open(path, encoding="utf8")
        log(type(file))
        csv_reader = csv.reader(file) 

        count = -1
        try:
            for row in csv_reader:
                count += 1
                # print("{} {} {} {} {} {} {} {}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        except Exception as e:
            print("CSV File corruption detected, please recheck everything and try again.")
            print(e)
            return False
        
        print("Total row found: {}".format(count))
        return True