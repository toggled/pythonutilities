#!/usr/bin/env python

import sys,os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from pandas.tools.plotting import parallel_coordinates
from pandas import DataFrame,read_table
from math import modf

jmetal_dir=str(os.getcwd()).split('/')
pfdir=jmetal_dir[:-1]
pfdir.append('pf')
pfdir='/'.join(pfdir)
print pfdir
dirctry=jmetal_dir[:-1]
dirctry.append('abcGenerations')
gen_dir='/'.join(dirctry)

def plot_scatter(srcfile,destdir,filename="fig.png"):
    """
    1. if srcfile is 2d , plot scatter
        otherwise parallel coordinate plot
    """
    file_name = filename
    x_values = []
    y_values = []
    with open(srcfile) as f:
        while 1:
            line = f.readline()
            if not line:
                break
            x,y = line.split()
            x_values.append(float(x))
            y_values.append(float(y))
    pylab.scatter(x_values,y_values)
    #pylab.savefig(file_name)
    pylab.show()

def get_num_obj(srcfile):
    f = open(srcfile,'r')
    x = f.readline()
    f.close()
    return len(x.split())

def get_num_solutions(srcfile):
    f = open(srcfile,'r')
    x = len(f.readlines())
    f.close()
    return x

def plot_parallel_coordinate(gen_dir,destdir,filename="fig.png"):
    from matplotlib.widgets import Slider
    file_name = filename
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.10, bottom=0.15)
    p=1
    srcfile=gen_dir+'/'+'generation'+str(p)
    df=read_table(srcfile,sep=' ',header=None)
    num_of_sol = get_num_solutions(srcfile)
    num_of_obj = get_num_obj(srcfile)
    solutions = ['solution '+str(i) for i in range(1,num_of_sol+1)]

        #plt.figure()
        #plt.legend(label=solutions,loc='best')
    df['solutions']=solutions
    parallel_coordinates(df,'solutions')    
    axamp  = plt.axes([0.10, 0.05, 0.70, 0.03])

    sfreq = Slider(axamp, 'Freq', 1, 30, valinit=1)
    def update(val):    
        dec,integ= modf(val)
        p=int(integ)
        if dec>0.9999:
            p=integ+1
        srcfile=gen_dir+'/'+'generation'+str(p)
        num_of_sol = get_num_solutions(srcfile)
        solutions = ['solution '+str(i) for i in range(1,num_of_sol+1)]
        df=read_table(srcfile,sep=' ',header=None)
        df['solutions']=solutions
        axamp  = plt.axes([0.10, 0.05, 0.70, 0.03])
        sfreq = Slider(axamp, 'Freq', 1, 30, valinit=1)
        parallel_coordinates(df,'solutions')    
        
    sfreq.on_changed(update)
    plt.show()

def main():
    if len(sys.argv)==1:
        home = os.getenv("HOME")
        source_file = home+"/NetBeansProjects/jmetal/FUN"
        dest_dir = os.getcwd()+"/figures"
    else:
        source_file = os.getcwd()+"/"+sys.argv[1]
        if len(sys.argv)==2:
            dest_dir = os.getcwd()+"/figures"
        else:
            dest_dir = os.getcwd()+"/"+sys.argv[2]
    print source_file," ",dest_dir
    #plot_scatter(source_file,dest_dir)
    plot_parallel_coordinate(gen_dir,dest_dir)

if __name__ == "__main__":
    main()
