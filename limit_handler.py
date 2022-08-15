from datetime import datetime
import os.path

class LimitHandler:
    def getCurrentUsage():
        currentDate = datetime.today().strftime('%Y-%m-%d')

        if not os.path.exists("data/{}.data".format(currentDate)):
            file = open("data/{}.data".format(currentDate), mode = "w+")
            file.write("0")
            file.close()
        
        file = open("data/{}.data".format(currentDate), mode = "r+")
        return int(file.read())
    
    def incrementUsage():
        currentDate = datetime.today().strftime('%Y-%m-%d')

        if not os.path.exists("data/{}.data".format(currentDate)):
            file = open("data/{}.data".format(currentDate), mode = "w+")
            file.write("0")
            file.close()
        
        file = open("data/{}.data".format(currentDate), mode = "r+")
        data = int(file.read())
        data += 1
        file.close()
        file = open("data/{}.data".format(currentDate), mode = "w")
        file.write(str(data))
        file.close()