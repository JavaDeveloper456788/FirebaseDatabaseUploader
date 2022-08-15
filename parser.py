import csv
import imp
from caching import Caching
from const import USAGE_LIMIT
from utils import log, getInt, printProgressBar
import time
from compare import Compare
from limit_handler import LimitHandler
from firebase_admin import firestore

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
                Caching.saveCachingIndex(i)
                exit()
            doc_ref.document(row[0]).set({
                "id": int(row[0]),
                header[1]: row[1],
                header[2]: row[2],
                header[3]: row[3],
                header[4]: getInt(row[4]),
                header[5]: row[5],
                header[6]: row[6],
                header[7]: row[7],
                header[8]: row[8],
            })
            i += 1
            LimitHandler.incrementUsage()
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete ({}/{})'.format(i,l), length = 50)

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
        else:
            printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

        doc_ref = db.collection(entry_name)

        i = 0
        for row in updated_rows:
            usage += 1
            if(usage > USAGE_LIMIT):
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle.")
                Caching.saveCachingIndex(i)
                exit()
            doc_ref.document(row[0]).set({
                "id": int(row[0]),
                header[1]: row[1],
                header[2]: row[2],
                header[3]: row[3],
                header[4]: getInt(row[4]),
                header[5]: row[5],
                header[6]: row[6],
                header[7]: row[7],
                header[8]: row[8],
            })
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
            if(c < count - 1):
                log("ignoring {}".format(c))
                c += 1
                continue
            rows.append(row)

        log("Starting import to Firestore job...")
        time.sleep(2)

        l = len(rows)
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

        doc_ref = db.collection("entries")

        i = 0
        for row in rows:
            usage += 1
            if(usage > USAGE_LIMIT):
                print("Daily usage limit exceeded, rest of the data is cached and will be uploaded in the next cycle.")
                exit()
            doc_ref.document(row[0]).set({
                "id": int(row[0]),
                header[1]: row[1],
                header[2]: row[2],
                header[3]: row[3],
                header[4]: getInt(row[4]),
                header[5]: row[5],
                header[6]: row[6],
                header[7]: row[7],
                header[8]: row[8],
            })
            i += 1
            LimitHandler.incrementUsage()
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete ({}/{})'.format(i,l), length = 50)
        Caching.saveCachingIndex(0)
    
    