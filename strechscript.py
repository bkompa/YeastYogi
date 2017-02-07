import os
import fnmatch
import numpy as np

#this needs to make the array of T/F
def getColorArray(path,number):
    f = open(path,'r')
    mass_color = []
    for line in f:
        if line=='4':
            mass_color.append(True)
        if line=='0':
            mass_color.append(False)
    length = len(mass_color)
    for i in range(length,number):
        mass_color.append(False)
    assert(len(mass_color)==number)
    f.close()
    return mass_color

def processHeaderMicrons(path,out_path,length):
    mass_counter = 0
    in_time_step = False
    file_name = path.split('/')[-1].split('.')[0]
    processed_path = out_path+file_name+'.txt'
    processed_file = open(processed_path,'a')
    f = open(path,'r')
    if(length>0):
        for line in f:
            if line.startswith('Time'):
                in_time_step = True
                processed_file.write(line)
                continue
            if in_time_step:
                coordinates = line.strip().split(' ')
                processed_file.write(str(1000000.*float(coordinates[0]))+' '+str(1000000.*float(coordinates[1]))+' '+str(1000000.*float(coordinates[2]))+'\n')
                mass_counter+=1
                if(mass_counter==length):
                    #unsure if I need to write out this newline
                    processed_file.write('\n')
                    in_time_step = False
                    mass_counter = 0
    processed_file.close()
    f.close()
    return processed_path

#write out just the true elements of the array
def processFile(path,color_path,out_path):
    #Need to get the mass colors to know what masses to write out
    #The mass color array will tell us what lines from each time step to write out
    mass_color = getColorArray(path,color_path)
    #Need to only write the time steps that have the valid colors
    processed_file = open(out_path,'a')
    input_file = open(path,'r')
    for line in input_file:
        if line.startswith('Time') or len(line)<2:
            processed_file.write(line)
            for i in range(len(mass_color)):
                if(mass_color[i]):
                    processed_file.write(input_file.readline())
    processed_file.close()
    input_file.close()
    return

def convertColorFiles(file_name,out_path,number):
    for csv in os.listdir(file_name):
        if fnmatch.fnmatch(file, '*.csv'):
            with open(os.path.join([file_name,csv])) as csv_file:
                out_file = open(os.path.join([out_path,csv.replace('.csv','.txt')]),'a')
                mass_color = getColorArray(os.path.join([file_name,csv]),number)
                for mass in mass_color:
                    if mass:
                        out_file.write('4'+'\n')
                    if not mass:
                        out_file.write('0'+'\n')
                out_file.close()
    return
