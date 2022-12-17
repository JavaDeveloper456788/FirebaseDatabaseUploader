import csv
from caching import Caching
from const import USAGE_LIMIT
from utils import log, getInt, printProgressBar
import time
from compare import Compare
from limit_handler import LimitHandler
from firebase_admin import firestore

def getFormatted(data: str):
    if data.isdecimal():
        return int(data)
    elif data == '':
        return None
    else:
        return str(data)

def genData(headers: list, row: list):
        data = {}
        for header in headers:
            try:
                data[str(header)] = getFormatted(row[headers.index(header)])
            except:
                data[str(header)] = None
        return data

class Parser:
    def openCSV(path):
        log("Parser - openCSV Called")
        file = open(path, encoding="utf8")
        log(type(file))
        return csv.reader(file)

    def parse(path, entry_name):
        log("Parser -  parse called")

        db = firestore.client()

        usage = LimitHandler.getCurrentUsage()
        print("Current usage: {}".format(usage))
        print("Daily writes left: {}".format(USAGE_LIMIT - usage))

        file = open(path, encoding="utf8")
        csvreader = csv.reader(file)

        header = next(csvreader)
        rows = []
        for row in csvreader:
            # log("Prasing row {}".format(row[0]))
            rows.append(row)

        log("Starting import to Firestore job...")
        time.sleep(2)

        l = len(rows)
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        doc_ref = db.collection(entry_name)

        i = 0
        for row in rows:
            usage += 1
            if(usage > USAGE_LIMIT):
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle.")
                Caching.saveCachingIndex(path, i)
                exit()
            try:
                data = genData(header, row)
                doc_ref.document(str(row[0])).set(data)
            except:
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle. (Server)")
                Caching.saveCachingIndex(i)
                exit()
            i += 1
            LimitHandler.incrementUsage()
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete ({}/{})'.format(i,l), length = 50)
        Caching.saveCachingIndex(path, -1)

    def parseUpdated(path, old, entry_name):
        log("Parser -  parse updated called")

        db = firestore.client()

        usage = LimitHandler.getCurrentUsage()
        print("Current usage: {}".format(usage))
        print("Daily writes left: {}".format(USAGE_LIMIT - usage))

        file = open(path, encoding="utf8")
        csvreader = csv.reader(file)

        header = next(csvreader)

        file.close()

        updated_rows = Compare.compare(path, old)
        deletedFields = Compare.getDeletedFields(path, old)

        print("Delete: ")
        print(deletedFields)

        log("Starting import to Firestore job...")
        time.sleep(2)

        l = len(updated_rows)

        if(l == 0):
            print("No Updated Field found.")
        

        doc_ref = db.collection(entry_name)

        i = 0
        for row in updated_rows:
            usage += 1
            if(usage > USAGE_LIMIT):
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle.")
                Caching.saveCachingIndex(path, i)
                exit()
            try:
                data = genData(header, row)
                doc_ref.document(str(row[0])).set(data)
            except:
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle. (Server)")
                Caching.saveCachingIndex(i)
                exit()
            i += 1
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete ({}/{})'.format(i,l), length = 50)

        print("Deleting unused fields")

        for id in deletedFields:
            log("deleting {} {}".format(entry_name, id))
            doc_ref.document(id).delete()
    

    
    def parseCached(path, count):
        log("Parser -  parse updated called")

        db = firestore.client()

        usage = LimitHandler.getCurrentUsage()
        print("Current usage: {}".format(usage))
        print("Daily writes left: {}".format(USAGE_LIMIT - usage))
        
        file = open(path, encoding="utf8")
        csvreader = csv.reader(file)

        header = next(csvreader)

        rows = []

        c = 0
        for row in csvreader:
            rows.append(row)

        log("Starting import to Firestore job...")
        time.sleep(2)

        l = len(rows)

        doc_ref = db.collection("entries")

        i = 0
        for row in rows:
            if i > count - 1:
                usage += 1
                if(usage > USAGE_LIMIT):
                    print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle.")
                    Caching.saveCachingIndex(path, i)
                    exit()
                try:
                    data = genData(header, row)
                    doc_ref.document(str(row[0])).set(data)
                except:
                    print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle. (Server)")
                    Caching.saveCachingIndex(path, i)
                    exit()
                LimitHandler.incrementUsage()
                printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete ({}/{})'.format(i,l), length = 50)
            i += 1
        Caching.saveCachingIndex(path, -1)
    
    