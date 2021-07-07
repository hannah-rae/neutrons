import fileinput
import sys
import subprocess
from glob import glob
from time import sleep

input_dir = sys.argv[1]
output_pfx = 'outputs/'
output_dir = input_dir + output_pfx

subprocess.call(["mkdir", output_dir])

infiles = glob(input_dir + '*')
print infiles

for file in infiles:
    inp = 'i=' + file
    nfile = file.split('.')[-2]
    nfile = nfile.split('/')[-1]
    n = 'n=' + nfile + '.'
    print n

    subprocess.check_call(["mcnp6", inp, n])

subprocess.call(["mv", '*.o', output_dir])