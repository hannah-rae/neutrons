
import fileinput
import sys
from subprocess import call
from time import ctime
from Tkinter import *

class FileBuilder():

    def __init__(self):
        # Main window frame
        self.window = Tk()
        self.window.title("MCNP6/X Input File Generator")
        self.window.geometry('650x750')

        # Base input file
        self.base_input_file = Entry(self.window)
        self.bif_label = Label(self.window, text="Base input file:")

        # Name the project
        self.project_name = Entry(self.window)
        self.pn_label = Label(self.window, text="Name of project:")

        # Planetary radius
        self.radius = Entry(self.window)
        self.r_label = Label(self.window, text="Planet radius (km):")

        # Spacecraft altitude
        self.sc_alt = Entry(self.window)
        self.sca_label = Label(self.window, text="Spacecraft altitude (km):")

        # Go button
        self.button = Button(self.window, text="Make it so!", command=self.make_files)

        # Arrange the layout: labels on left, text boxes on right
        Label(self.window, text="File Information").grid(row=0, sticky='w')
        self.bif_label.grid(row=1, column=0)
        self.base_input_file.grid(row=1, column=1)
        self.pn_label.grid(row=2, column=0)
        self.project_name.grid(row=2, column=1)

        Label(self.window, text="Mission Parameters").grid(row=3, sticky='w')
        self.r_label.grid(row=4, column=0)
        self.radius.grid(row=4, column=1)
        self.sca_label.grid(row=5, column=0)
        self.sc_alt.grid(row=5, column=1)

        Label(self.window, text=" ").grid(row=6) # Empty row
        Label(self.window, text="Geochemical Information").grid(row=7, column=0, stick='w')

        Label(self.window, text="Base Geochemistry").grid(row=8, column=1)
        Label(self.window, text='H').grid(row=9, column=0, sticky='e')
        self.h = Entry(self.window)
        self.h.grid(row=9, column=1)
        Label(self.window, text='O').grid(row=10, column=0, sticky='e')
        self.o = Entry(self.window)
        self.o.grid(row=10, column=1)
        Label(self.window, text='Na').grid(row=11, column=0, sticky='e')
        self.na = Entry(self.window)
        self.na.grid(row=11, column=1)
        Label(self.window, text='Mg').grid(row=12, column=0, sticky='e')
        self.mg = Entry(self.window)
        self.mg.grid(row=12, column=1)
        Label(self.window, text='Al').grid(row=13, column=0, sticky='e')
        self.al = Entry(self.window)
        self.al.grid(row=13, column=1)
        Label(self.window, text='Si').grid(row=14, column=0, sticky='e')
        self.si = Entry(self.window)
        self.si.grid(row=14, column=1)
        Label(self.window, text='P').grid(row=15, column=0, sticky='e')
        self.p = Entry(self.window)
        self.p.grid(row=15, column=1)
        Label(self.window, text='S').grid(row=16, column=0, sticky='e')
        self.s = Entry(self.window)
        self.s.grid(row=16, column=1)
        Label(self.window, text='K').grid(row=17, column=0, sticky='e')
        self.k = Entry(self.window)
        self.k.grid(row=17, column=1)
        Label(self.window, text='Ca').grid(row=18, column=0, sticky='e')
        self.ca = Entry(self.window)
        self.ca.grid(row=18, column=1)
        # Label(self.window, text='Ti').grid(row=19, column=0, sticky='e')
        # self.ti = Entry(self.window)
        # self.ti.grid(row=19, column=1)
        # Label(self.window, text='Cr').grid(row=20, column=0, sticky='e')
        # self.cr = Entry(self.window)
        # self.cr.grid(row=20, column=1)
        # Label(self.window, text='Mn').grid(row=21, column=0, sticky='e')
        # self.mn = Entry(self.window)
        # self.mn.grid(row=21, column=1)
        Label(self.window, text='Fe').grid(row=22, column=0, sticky='e')
        self.fe = Entry(self.window)
        self.fe.grid(row=22, column=1)
        Label(self.window, text='Ni').grid(row=23, column=0, sticky='e')
        self.ni = Entry(self.window)
        self.ni.grid(row=23, column=1)
        Label(self.window, text='Zn').grid(row=24, column=0, sticky='e')
        self.zn = Entry(self.window)
        self.zn.grid(row=24, column=1)
        # Label(self.window, text='Br').grid(row=25, column=0, sticky='e')
        # self.br = Entry(self.window)
        # self.br.grid(row=25, column=1)
        # Label(self.window, text='Cl').grid(row=26, column=0, sticky='e')
        # self.cl = Entry(self.window)
        # self.cl.grid(row=26, column=1)

        Label(self.window, text="Hydrogen Variation (ppm)").grid(row=8, column=3)
        Label(self.window, text='Start').grid(row=9, column=2, sticky='e')
        self.h_start = Entry(self.window)
        self.h_start.grid(row=9, column=3)
        Label(self.window, text='End').grid(row=10, column=2, sticky='e')
        self.h_end = Entry(self.window)
        self.h_end.grid(row=10, column=3)
        Label(self.window, text='Interval').grid(row=11, column=2, sticky='e')
        self.h_int = Entry(self.window)
        self.h_int.grid(row=11, column=3)

        self.button.grid(row=27)

        self.window.mainloop()

    def make_files(self):

        num_files = (int(self.h_end.get()) - int(self.h_start.get())) / int(self.h_int.get()) + 1

        fname_post = ".mx"
        dirname = ctime().replace(' ', '')
        call(["mkdir", dirname])

        for i in range(num_files):
            new_fname = dirname + '/' + self.project_name.get() + str(i) + fname_post
            ppm = int(self.h_start.get()) + i*int(self.h_int.get())
            call(["cp", self.base_input_file.get(), new_fname])
            self.modify_file(new_fname, ppm)

        self.quit()

    def modify_file(self, filename, weh):

        h = ((1.0/9.0) * weh)/100000.0
        h_val = -h
        o_val = -float(self.o.get()) + h

        # To be filled in as they are found in the file
        so_11 = float(self.radius.get())
        so_12 = so_11 + float(self.sc_alt.get())

        file = fileinput.input(filename, inplace=True)

        for line in file:
            if "so" in line:
                sline = line.split("so  ")
                if sline[0].startswith("11"):
                    modline = sline[0] + "so  " + str(so_11*100000) + '\n'
                elif sline[0].startswith("12"):
                    modline = sline[0] + "so  " + str(so_12*100000) + '\n'
                sys.stdout.write(modline)
            elif line.startswith("m2"):
                sline = line.split(' ')
                modline = sline[0] + ' ' + sline[1] + ' ' + sline[2] + ' ' + sline[3] + ' ' + sline[4] + ' ' +  str(weh) + ' ' + sline[6]
                sys.stdout.write(modline)
            elif line.strip().startswith("1001"):
                sline = line.split('1001')
                modline = sline[0] + '1001  ' + '{0:.8f}'.format(h_val) + '  $ H' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("8016"):
                sline = line.split('8016')
                modline = sline[0] + '8016  ' + '{0:.8f}'.format(o_val) + '  $ O' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("11023"):
                sline = line.split('11023')
                modline = sline[0] + '11023  ' + '{0:.8f}'.format(-float(self.na.get())) + '  $ Na' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("12000"):
                sline = line.split('12000')
                modline = sline[0] + '12000  ' + '{0:.8f}'.format(-float(self.mg.get())) + '  $ Mg' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("13027"):
                sline = line.split('13027')
                modline = sline[0] + '13027  ' + '{0:.8f}'.format(-float(self.al.get())) + '  $ Al' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("14028"):
                sline = line.split('14028')
                modline = sline[0] + '14028  ' + '{0:.8f}'.format(-float(self.si.get())) + '  $ Si' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("20000"):
                sline = line.split('20000')
                modline = sline[0] + '20000  ' + '{0:.8f}'.format(-float(self.ca.get())) + '  $ Ca' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("26054"):
                sline = line.split('26054')
                modline = sline[0] + '26054  ' + '{0:.8f}'.format(-float(self.fe.get())) + '  $ Fe' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("19000"):
                sline = line.split('19000')
                modline = sline[0] + '19000  ' + '{0:.8f}'.format(-float(self.k.get())) + '  $ K' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("15000"):
                sline = line.split('15000')
                modline = sline[0] + '15000  ' + '{0:.8f}'.format(-float(self.p.get())) + '  $ P' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("16000"):
                sline = line.split('16000')
                modline = sline[0] + '16000  ' + '{0:.8f}'.format(-float(self.s.get())) + '  $ S' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("28000"):
                sline = line.split('28000')
                modline = sline[0] + '28000  ' + '{0:.8f}'.format(-float(self.ni.get())) + '  $ Ni' + '\n'
                sys.stdout.write(modline)
            elif line.strip().startswith("30000"):
                sline = line.split('30000')
                modline = sline[0] + '30000  ' + '{0:.8f}'.format(-float(self.zn.get())) + '  $ Zn' + '\n'
                sys.stdout.write(modline)
            else:
                sys.stdout.write(line)

        fileinput.close()

    def quit(self):
        self.window.destroy()

app = FileBuilder()

