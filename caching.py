import os.path
import time

class Caching:
    def checkIfCachingExist(filePath):
        if not os.path.exists("data/{}.data".format(filePath)):
            file = open("data/{}.data".format(filePath), mode = "w+")
            file.write("0")
            file.close()
            return 0
        
        file = open("data/{}.data".format(filePath), mode = "r+")
        return int(file.read())
    
    def saveCachingIndex(file : str, count):
        file = file.split("/")[-1]
        file = open("data/{}.data".format(file), mode = "w+")
        file.write(str(count))
        file.close()
        return