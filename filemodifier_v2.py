
import fileinput
from subprocess import call
from time import ctime
import templates
from Tkinter import *
import math

class FileBuilder():

    def __init__(self):
        # Main window frame
        self.window = Tk()
        self.window.title("MCNP6/X Input File Generator")
        self.window.geometry('650x1025')

        # Name the project
        self.project_name = Entry(self.window)
        self.pn_label = Label(self.window, text="Name of project:")

        # Planetary radius
        self.radius = Entry(self.window)
        self.r_label = Label(self.window, text="Planet radius (km):")

        # Planetary density
        self.density = Entry(self.window)
        self.d_label = Label(self.window, text="Planet density (g/cc):")

        # Spacecraft altitude
        self.sc_label = Label(self.window, text="Spacecraft altitude (km):")
        self.sc_start = Entry(self.window)
        self.sc_end = Entry(self.window)
        self.sc_int = Entry(self.window)

        # Go button
        self.button = Button(self.window, text="All the input files!", command=self.make_files)

        # Arrange the layout: labels on left, text boxes on right
        Label(self.window, text="File Information").grid(row=0, sticky='w')
        self.pn_label.grid(row=2, column=0)
        self.project_name.grid(row=2, column=1)

        Label(self.window, text="Mission Parameters").grid(row=3, sticky='w')
        self.r_label.grid(row=4, column=0)
        self.radius.grid(row=4, column=1)
        self.d_label.grid(row=5, column=0)
        self.density.grid(row=5, column=1)
        self.sc_label.grid(row=6)
        Label(self.window, text='Start').grid(row=7, column=0, sticky='e')
        self.sc_start.grid(row=7, column=1)
        Label(self.window, text='End').grid(row=8, column=0, sticky='e')
        self.sc_end.grid(row=8, column=1)
        Label(self.window, text='Interval').grid(row=9, column=0, sticky='e')
        self.sc_int.grid(row=9, column=1)

        Label(self.window, text="Geochemical Information").grid(row=10, column=0, stick='w')

        Label(self.window, text="Base Geochemistry").grid(row=11, column=1)

        Label(self.window, text='C').grid(row=13, column=0, sticky='e')
        self.c = Entry(self.window)
        self.c.grid(row=13, column=1)

        Label(self.window, text='N').grid(row=14, column=0, sticky='e')
        self.n = Entry(self.window)
        self.n.grid(row=14, column=1)

        Label(self.window, text='O-16').grid(row=15, column=0, sticky='e')
        self.o16 = Entry(self.window)
        self.o16.grid(row=15, column=1)

        Label(self.window, text='O-17').grid(row=16, column=0, sticky='e')
        self.o17 = Entry(self.window)
        self.o17.grid(row=16, column=1)

        Label(self.window, text='Na').grid(row=17, column=0, sticky='e')
        self.na = Entry(self.window)
        self.na.grid(row=17, column=1)

        Label(self.window, text='Mg').grid(row=18, column=0, sticky='e')
        self.mg = Entry(self.window)
        self.mg.grid(row=18, column=1)

        Label(self.window, text='Al').grid(row=19, column=0, sticky='e')
        self.al = Entry(self.window)
        self.al.grid(row=19, column=1)

        Label(self.window, text='Si-28').grid(row=20, column=0, sticky='e')
        self.si28 = Entry(self.window)
        self.si28.grid(row=20, column=1)

        Label(self.window, text='Si-29').grid(row=21, column=0, sticky='e')
        self.si29 = Entry(self.window)
        self.si29.grid(row=21, column=1)

        Label(self.window, text='Si-30').grid(row=22, column=0, sticky='e')
        self.si30 = Entry(self.window)
        self.si30.grid(row=22, column=1)

        Label(self.window, text='P').grid(row=23, column=0, sticky='e')
        self.p = Entry(self.window)
        self.p.grid(row=23, column=1)

        Label(self.window, text='S').grid(row=24, column=0, sticky='e')
        self.s = Entry(self.window)
        self.s.grid(row=24, column=1)

        Label(self.window, text='Cl').grid(row=25, column=0, sticky='e')
        self.cl = Entry(self.window)
        self.cl.grid(row=25, column=1)

        Label(self.window, text='K').grid(row=26, column=0, sticky='e')
        self.k = Entry(self.window)
        self.k.grid(row=26, column=1)

        Label(self.window, text='Ca').grid(row=27, column=0, sticky='e')
        self.ca = Entry(self.window)
        self.ca.grid(row=27, column=1)

        Label(self.window, text='Sc').grid(row=28, column=0, sticky='e')
        self.sc = Entry(self.window)
        self.sc.grid(row=28, column=1)

        Label(self.window, text='Ti').grid(row=29, column=0, sticky='e')
        self.ti = Entry(self.window)
        self.ti.grid(row=29, column=1)

        Label(self.window, text='Cr-50').grid(row=30, column=0, sticky='e')
        self.cr50 = Entry(self.window)
        self.cr50.grid(row=30, column=1)

        Label(self.window, text='Cr-52').grid(row=31, column=0, sticky='e')
        self.cr52 = Entry(self.window)
        self.cr52.grid(row=31, column=1)

        Label(self.window, text='Cr-53').grid(row=32, column=0, sticky='e')
        self.cr53 = Entry(self.window)
        self.cr53.grid(row=32, column=1)

        Label(self.window, text='Cr-54').grid(row=33, column=0, sticky='e')
        self.cr54 = Entry(self.window)
        self.cr54.grid(row=33, column=1)

        Label(self.window, text='Mn-55').grid(row=34, column=0, sticky='e')
        self.mn55 = Entry(self.window)
        self.mn55.grid(row=34, column=1)

        Label(self.window, text='Fe-54').grid(row=35, column=0, sticky='e')
        self.fe54 = Entry(self.window)
        self.fe54.grid(row=35, column=1)

        Label(self.window, text='Fe-56').grid(row=36, column=0, sticky='e')
        self.fe56 = Entry(self.window)
        self.fe56.grid(row=36, column=1)

        Label(self.window, text='Fe-57').grid(row=37, column=0, sticky='e')
        self.fe57 = Entry(self.window)
        self.fe57.grid(row=37, column=1)

        Label(self.window, text='Fe-58').grid(row=13, column=2, sticky='e')
        self.fe58 = Entry(self.window)
        self.fe58.grid(row=13, column=3)

        Label(self.window, text='Co').grid(row=14, column=2, sticky='e')
        self.co = Entry(self.window)
        self.co.grid(row=14, column=3)

        Label(self.window, text='Ni').grid(row=15, column=2, sticky='e')
        self.ni = Entry(self.window)
        self.ni.grid(row=15, column=3)

        Label(self.window, text='Cu').grid(row=16, column=2, sticky='e')
        self.cu = Entry(self.window)
        self.cu.grid(row=16, column=3)

        Label(self.window, text='Zn').grid(row=17, column=2, sticky='e')
        self.zn = Entry(self.window)
        self.zn.grid(row=17, column=3)

        Label(self.window, text='Ga').grid(row=18, column=2, sticky='e')
        self.ga = Entry(self.window)
        self.ga.grid(row=18, column=3)

        Label(self.window, text='Ge').grid(row=19, column=2, sticky='e')
        self.ge = Entry(self.window)
        self.ge.grid(row=19, column=3)

        Label(self.window, text='As').grid(row=20, column=2, sticky='e')
        self.ars = Entry(self.window)
        self.ars.grid(row=20, column=3)

        Label(self.window, text='Se').grid(row=21, column=2, sticky='e')
        self.se = Entry(self.window)
        self.se.grid(row=21, column=3)

        Label(self.window, text='W').grid(row=22, column=2, sticky='e')
        self.w = Entry(self.window)
        self.w.grid(row=22, column=3)

        Label(self.window, text='Re').grid(row=23, column=2, sticky='e')
        self.re = Entry(self.window)
        self.re.grid(row=23, column=3)

        Label(self.window, text='Ir').grid(row=24, column=2, sticky='e')
        self.ir = Entry(self.window)
        self.ir.grid(row=24, column=3)

        Label(self.window, text='Pt').grid(row=25, column=2, sticky='e')
        self.pt = Entry(self.window)
        self.pt.grid(row=25, column=3)

        Label(self.window, text='Au').grid(row=26, column=2, sticky='e')
        self.au = Entry(self.window)
        self.au.grid(row=26, column=3)

        Label(self.window, text='Sm').grid(row=27, column=2, sticky='e')
        self.sm = Entry(self.window)
        self.sm.grid(row=27, column=3)

        Label(self.window, text='Gd').grid(row=28, column=2, sticky='e')
        self.gd = Entry(self.window)
        self.gd.grid(row=28, column=3)

        Label(self.window, text='Th-232').grid(row=29, column=2, sticky='e')
        self.th232 = Entry(self.window)
        self.th232.grid(row=29, column=3)

        Label(self.window, text='U-234').grid(row=30, column=2, sticky='e')
        self.u234 = Entry(self.window)
        self.u234.grid(row=30, column=3)

        Label(self.window, text="WEH Variation (wt. %)").grid(row=31, column=3)
        Label(self.window, text='Start').grid(row=32, column=2, sticky='e')
        self.h_start = Entry(self.window)
        self.h_start.grid(row=32, column=3)
        Label(self.window, text='End').grid(row=33, column=2, sticky='e')
        self.h_end = Entry(self.window)
        self.h_end.grid(row=33, column=3)
        Label(self.window, text='Interval').grid(row=34, column=2, sticky='e')
        self.h_int = Entry(self.window)
        self.h_int.grid(row=34, column=3)

        Label(self.window, text="# Particles in Simulation").grid(row=35, column=3)
        Label(self.window, text='NPS').grid(row=36, column=2, sticky='e')
        self.nps = Entry(self.window)
        self.nps.grid(row=36, column=3)

        self.button.grid(row=38)

        self.window.mainloop()

    def make_files(self):

        num_files = int((float(self.h_end.get()) - float(self.h_start.get())) / float(self.h_int.get()) + 1)

        fname_post = ".mx"
        dirname = ctime().replace(' ', '')
        call(["mkdir", dirname])

        for i in range(num_files):
            new_fname = dirname + '/' + self.project_name.get() + str(i) + fname_post
            weh = float(self.h_start.get()) + i*float(self.h_int.get())
            self.build_file(new_fname, weh)

        self.quit()

    def build_file(self, filename, weh):
        # Bookkeep altitude information
        num_alts = int(math.ceil((float(self.sc_end.get()) - float(self.sc_start.get())) / float(self.sc_int.get())))
        alts = [float(self.sc_start.get()) + i*float(self.sc_int.get()) for i in range(num_alts+1)]
        alts.insert(0, 0) # add 0 to beginning of list for planet surface
        num_surfaces = len(alts)

        # Calculate weight fraction H
        h = ((1.0/9.0) * weh)/100.0
        # Subtract hydrogen amount from oxygen
        o16 = float(self.o16.get()) - h
        # Open new file to write to it
        f = open(filename, 'w+')
        # file = fileinput.input(filename, inplace=True)

        f.write('c\n')
        # Add the surfaces
        surface_ids = ['1'+str(i) for i in range(1, num_surfaces+1)]
        for i, s in enumerate(surface_ids):
            if s == '11':
                line = templates.surface_cell_planet % (s, self.density.get(), s)
            else:
                line = templates.surface_cell_alt % (s, s, prev_surface, str(alts[i]) + 'km')
            prev_surface = s
            f.write(line)
        f.write(templates.surface_cell_outside % s)
        f.write('c\n\n')
        f.write('c surface cards\n')
        # Convert altitudes to cm
        alts = [a*100000 for a in alts]
        # Convert radius to cm
        r = float(self.radius.get())*100000
        for i, s in enumerate(surface_ids):
            line = templates.surface_card % (s, r + alts[i])
            f.write(line)
        f.write('\n')
        # Add the material (Only one material supported)
        f.write(templates.material_header % weh)

        f.write(templates.h % h)
        if self.c.get() != '0': f.write(templates.c % self.c.get())
        if self.n.get() != '0': f.write(templates.n % self.n.get())
        if self.o16.get() != '0': f.write(templates.o16 % o16)
        if self.o17.get() != '0': f.write(templates.o17 % self.o17.get())
        if self.na.get() != '0': f.write(templates.na % self.na.get())
        if self.mg.get() != '0': f.write(templates.mg % self.mg.get())
        if self.al.get() != '0': f.write(templates.al % self.al.get())
        if self.si28.get() != '0': f.write(templates.si28 % self.si28.get())
        if self.si29.get() != '0': f.write(templates.si29 % self.si29.get())
        if self.si30.get() != '0': f.write(templates.si30 % self.si30.get())
        if self.p.get() != '0': f.write(templates.p % self.p.get())
        if self.s.get() != '0': f.write(templates.s % self.s.get())
        if self.cl.get() != '0': f.write(templates.cl % self.cl.get())
        if self.k.get() != '0': f.write(templates.k % self.k.get())
        if self.ca.get() != '0': f.write(templates.ca % self.ca.get())
        if self.sc.get() != '0': f.write(templates.sc % self.sc.get())
        if self.ti.get() != '0': f.write(templates.ti % self.ti.get())
        if self.cr50.get() != '0': f.write(templates.cr50 % self.cr50.get())
        if self.cr52.get() != '0': f.write(templates.cr52 % self.cr52.get())
        if self.cr53.get() != '0': f.write(templates.cr53 % self.cr53.get())
        if self.cr54.get() != '0': f.write(templates.cr54 % self.cr54.get())
        if self.mn55.get() != '0': f.write(templates.mn55 % self.mn55.get())
        if self.fe54.get() != '0': f.write(templates.fe54 % self.fe54.get())
        if self.fe56.get() != '0': f.write(templates.fe56 % self.fe56.get())
        if self.fe57.get() != '0': f.write(templates.fe57 % self.fe57.get())
        if self.fe58.get() != '0': f.write(templates.fe58 % self.fe58.get())
        if self.co.get() != '0': f.write(templates.co % self.co.get())
        if self.ni.get() != '0': f.write(templates.ni % self.ni.get())
        if self.cu.get() != '0': f.write(templates.cu % self.cu.get())
        if self.zn.get() != '0': f.write(templates.zn % self.zn.get())
        if self.ga.get() != '0': f.write(templates.ga % self.ga.get())
        if self.ge.get() != '0': f.write(templates.ge % self.ge.get())
        if self.ars.get() != '0': f.write(templates.ars % self.ars.get())
        if self.se.get() != '0': f.write(templates.se % self.se.get())
        if self.w.get() != '0': f.write(templates.w % self.w.get())
        if self.re.get() != '0': f.write(templates.re % self.re.get())
        if self.ir.get() != '0': f.write(templates.ir % self.ir.get())
        if self.pt.get() != '0': f.write(templates.pt % self.pt.get())
        if self.au.get() != '0': f.write(templates.au % self.au.get())
        if self.sm.get() != '0': f.write(templates.sm % self.sm.get())
        if self.gd.get() != '0': f.write(templates.gd % self.gd.get())
        if self.th232.get() != '0': f.write(templates.th232 % self.th232.get())
        if self.u234.get() != '0': f.write(templates.u234 % self.u234.get())
        f.write('c\n')

        # Add sdef for particle source surface
        f.write(templates.sdef)
        f.write('c\n')

        # Add physics
        f.write(templates.physics)

        # Add tallies
        f.write(templates.tally_header)
        tmp_str = ' 8.617E-09'*len(surface_ids) + ' 0'
        f.write(templates.tally_tmp % tmp_str)
        for i, s in enumerate(surface_ids):
            line = templates.tally_surface % (i+1, s, i+1, i+1, i+1, i+1)
            f.write(line)
            f.write('c\n')

        # Add num particles
        f.write(templates.nps % self.nps.get())

        fileinput.close()

    def quit(self):
        self.window.destroy()

app = FileBuilder()

