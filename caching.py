import os.path
import time

class Caching:
    def checkIfCachingExist():
        if not os.path.exists("data/caching.data"):
            file = open("data/caching.data", mode = "w+")
            file.write("0")
            file.close()
        
        file = open("data/caching.data", mode = "r+")
        return int(file.read())
    
    def saveCachingIndex(count):
        file = open("data/caching.data", mode = "w")
        file.write(str(count))
        file.close()
        return