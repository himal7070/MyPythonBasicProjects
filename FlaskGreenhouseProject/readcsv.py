
import csv


# with open ('csvfile.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')

#     for row in reader:
#         print(row)
   

from csv import reader
# open file in read mode
with open('csvfile.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        print(row)
