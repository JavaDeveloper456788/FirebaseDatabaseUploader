from bdb import effective
from sre_parse import GLOBAL_FLAGS
from this import d
import time
import weakref
from caching import Caching
from parser import Parser

def main():
    count = Caching.checkIfCachingExist()
    if count > 0:
        print("Cached data found, upload process of cached data will start in 10 sec")
        time.sleep(10)
        Parser.parseCached("data.csv", count)
        exit()

if __name__=="__main__":
    main()