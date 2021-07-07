import csv
from glob import glob
import sys
import fileinput
import re
import templates_detector

# Run from ~/src/neutrons/ as python planet2detector.py <name of dir with CSV files>

# Step 1: Store total counts in dictionary, e.g. {0.1: {}}
# dirs = ['CI_chondrites_0to5',
#         'CI_chondrites_5to50',
#         'CO_chondrites_0to5',
#         'CO_chondrites_5to50',
#         'CM_chondrites_0to5',
#         'CM_chondrites_5to50',
#         'Novo_Urei_0to5',
#         'Novo_Urei_5to50',
#         'Psyche_0to5',
#         'Psyche_5to50',
#         'Tagish_Lake_0to5',
#         'Tagish_Lake_5to50']

bins = ['0.00',
        '1.00E-09',
        '1.58E-09',
        '2.51E-09',
        '3.98E-09',
        '6.31E-09',
        '1.00E-08',
        '1.58E-08',
        '2.51E-08',
        '3.98E-08',
        '6.31E-08',
        '1.00E-07',
        '1.58E-07',
        '2.51E-07',
        '3.98E-07',
        '6.31E-07',
        '1.00E-06',
        '1.58E-06',
        '2.51E-06',
        '3.98E-06',
        '6.31E-06',
        '1.00E-05',
        '1.58E-05',
        '2.51E-05',
        '3.98E-05',
        '6.31E-05',
        '1.00E-04',
        '1.58E-04',
        '2.51E-04',
        '3.98E-04',
        '6.31E-04',
        '1.00E-03',
        '1.58E-03',
        '2.51E-03',
        '3.98E-03',
        '6.31E-03',
        '1.00E-02',
        '1.58E-02',
        '2.51E-02',
        '3.98E-02',
        '6.31E-02',
        '1.00E-01',
        '1.58E-01',
        '2.51E-01',
        '3.98E-01',
        '6.31E-01',
        '1.00E+00']

file_dir = sys.argv[1]

counts_by_comp = {}
counts_by_weh = {}
results_files = glob(file_dir + '/*.csv')
for f in results_files:
    with open(f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        counts_by_alt = {}
        counts_by_bin = {}
        current_alt = 0
        for row in csvreader:
            if row[0].startswith('surface'):
                if row[0][-1] == '1':
                    current_alt = 0
                else if row[0][-1] == '2':
                    current_alt = 105
                else if row[0][-1] == '3':
                    current_alt = 14
            else if row[0] in bins:
                counts_by_bin[row[0]] = row[1]
                counts_by_alt[current_alt] = counts_by_bin
        # Check if files are 0 to 5 or 5 to 50
        if f.split('_')[1].startswith('0'):
            weh = int(f[-5])*0.1 + 0.1
        else if f.split('_')[1].startswith('5'):
            weh = int(f[-5])*5 + 5
        counts_by_weh[weh] = counts_by_alt
        comp = re.split('_|/', f)[1]
        counts_by_comp[comp] = counts_by_weh
        f.close()
print counts_by_comp

# For each composition, need a file for each wt. % at each altitude
for comp in counts_by_comp:
    for weh in counts_by_weh:
        for alt in counts_by_alt:
            newfn = file_dir + '/' + comp + '_' + weh + '_' + alt + '.mx'
            f = open(newfn, 'w+')
            spectrum = []
            bins = counts_by_bin.keys()
            bins.sort()
            for b in bins:
                spectrum.append(counts_by_bin[b])
            ftext = templates_detector.file_text % tuple(spectrum)
            f.write(ftext)

