
import sys
from glob import glob

def buildSGE(filename):
        new_fn = filename[:-3] + '.sge'
        writ = open(new_fn, 'w+')
        jobname = new_fn.split('/')[0] + '_' + new_fn.split('/')[1][:-4]
        writ.write('#$ -N j' + jobname + '\n')
        writ.write('#$ -cwd -V\n')
        writ.write('#$ -q short*\n')
        writ.write('#$ -pe openmpi* 125-250\n')
        writ.write('\n')
        writ.write('mpirun mcnpx i='+filename.split('/')[1] +' n='+filename.split('/')[1][:-3]+'.\n')
        writ.write('\n')
        writ.write('rm core*\n')
        writ.write('rm '+filename.split('/')[1][:-3]+'.r\n')

# Collect all the input file names
file_dir = sys.argv[1]
filenames = glob(file_dir + '/*')
print filenames
for fn in filenames:
        buildSGE(fn)