# Author: Hannah Kerner 2017
# This script takes an MCNPX output file and writes a new file with the part you care about
# To use: 'python grab_results.py your_output_file_directory/'

import sys
import fileinput
import csv
from glob import glob

dirname = sys.argv[1]
filenames = glob(dirname+'*.o')
for fn in filenames:
    outfile = open(fn)
    newfn = fn.split('.')[0] + '.csv'
    resfile = open(newfn, 'w')
    writer = csv.writer(resfile)
    results = {}

    record = False
    for line in outfile:
        if line.startswith('1tally') and len(line.split()) == 5 and line.split()[2] == 'nps':
            record = True
        if record and line.startswith(' surface'):
            surface_num = line.split()[1]
            results[surface_num] = {}
        if record and len(line.split()) == 3 and line.split()[0] != '+':
            nrg, count, err = line.split()
            if nrg == 'total':
                nrg = 9999999
            nrg = float(nrg)
            results[surface_num][nrg] = [count, err]
        if line.startswith('      total') and record:
            record = False

    keys = results.keys()
    keys.sort()
    for surf_num in keys:
        writer.writerow(['surface ' + surf_num])
        writer.writerow(['energy', 'flux', 'error'])
        energies = results[surf_num].keys()
        energies.sort()
        for nrg_bin in energies:
            row = [nrg_bin]
            row.extend(results[surf_num][nrg_bin])
            writer.writerow(row)

