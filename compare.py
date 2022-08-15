import csv

class Compare:
    def compare(csv1, csv2):
        file1 = open(csv1, encoding="utf8")
        file2 = open(csv2, encoding="utf8")

        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        rows1 = []
        rows2 = []

        updated_rows = []

        for row in reader1:
            rows1.append(row)
        
        for row in reader2:
            rows2.append(row)
        
        del rows1[0]
        del rows2[0]

        i = 0
        for row in rows1:
            try:
                if row != rows2[i]:
                    updated_rows.append(row)
            except:
                updated_rows.append(row)
            i+=1
        
        print("Updated row found: {}".format(len(updated_rows)))

        return updated_rows
    
    def getDeletedFields(csv1, csv2):
        file1 = open(csv1, encoding="utf8")
        file2 = open(csv2, encoding="utf8")

        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        ids1 = []
        ids2 = []
        deletedFields = []

        for row in reader1:
            ids1.append(row[0])
        
        for row in reader2:
            ids2.append(row[0])
        
        for id in ids2:
            if id not in ids1:
                deletedFields.append(id)
        
        return deletedFields