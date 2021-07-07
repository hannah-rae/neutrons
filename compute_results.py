import sys
import csv
import re
from glob import glob

file_dir = sys.argv[1]
# Take totals out of CSV files for each composition, wt % WEH, and altitude
count_totals = []
results_files = glob(file_dir + '/*.csv')
newfn = 'end_results.csv'
resfile = open(newfn, 'w')
writer = csv.writer(resfile)
writer.writerow(['composition', 'weh', 'altitude', 'total counts', 'error'])
for f in results_files:
    with open(f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        current_alt = 0
        for row in csvreader:
            if row[0].startswith('surface'):
                if row[0][-1] == '1':
                    current_alt = 0
                elif row[0][-1] == '2':
                    current_alt = 105
                elif row[0][-1] == '3':
                    current_alt = 14
            # Sentinel value for total
            if str(row[0]) == '9999999.0':
                # attr = [dir, comp, comp2, [5to50, 0to5], num.csv]
                attr = re.split('_|/', f)
                if attr[-2] == '5to50':
                    weh = int(attr[-1][:-4]) * 5 + 5
                elif attr[-2] == '0to5':
                    weh = int(attr[-1][:-4]) * 0.1 + 0.1
                # new_tup = [comp, weh, alt, total counts, error]
                writer.writerow([attr[1], weh, current_alt, row[1], row[2]])