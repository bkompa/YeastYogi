def getColorArray(path, valid_colors):
    f = open(path,'r')
    mass_color = []
    in_mass_color = False
    for line in f:
        if 'MassColors' in line:
            in_mass_color = True
            continue
        if in_mass_color:
            try:
                num = int(line.strip())
                if num in valid_colors:
                    mass_color.append(True)
                else:
                    mass_color.append(False)
            #if we can't parse an int, we have reached the end of masscolors
            except:
                in_mass_color = False
                break
    f.close()
    return mass_color

def writeSRC(path,mass_color):
    file_name = path.split('/')[-1].split('.out')[0]
    base_path = '/'.join(path.split('/')[0:-1])+'/'
    src_path = base_path+file_name+'_color.txt'
    some_color_file = open(src_path,'a')
    for i in range(np.count_nonzero(mass_color)):
        some_color_file.write('4\n')
    some_color_file.close()
    return src_path

def write


def processFile(path, valid_colors):

    #Need to get the mass colors to know what masses to write out
    #The mass color array will tell us what lines from each time step to write out
    mass_color = getColorArray(path,valid_colors)
    #Now that we have the masscolors, need to write the some colors text file
    src_path = writeSRC(path,mass_color)
    #Need to only write the time steps that have the valid colors
    processed_path = processHeaderMicrons(path,mass_color)
    return

def processHeaderMicrons(path,mass_color):
    mass_counter = 0
    in_time_step = False
    processed_path = base_path+file_name+'.txt'
    processed_file = open(processed_path,'a')
    if(len(mass_color)>0):
        for line in f:
            if line.startswith('Time'):
                in_time_step = True
                processed_file.write(line)
                continue
            if in_time_step:
                if mass_color[mass_counter]:
                    coordinates = line.strip().split(' ')
                    processed_file.write(str(1000000.*float(coordinates[0]))+' '+str(1000000.*float(coordinates[1]))+' '+str(1000000.*float(coordinates[2]))+'\n')
                mass_counter+=1
                if(mass_counter==len(mass_color)):
                    #unsure if I need to write out this newline
                    processed_file.write('\n')
                    in_time_step = False
                    mass_counter = 0
    processed_file.close()
    return processed_path

def convertColorFiles(file_name,number):
    for csv in os.listdir(file_name):
        with open('/'.join([file_name,csv])) as csv_file:
            out_file = open('/'.join([file_name,csv.replace('.csv','.txt')]),'a')
            line_count = 0
            for line in csv_file:
                out_file.write(line)
                line_count+=1
            while line_count<number:
                out_file.write('0\n')
                line_count+=1
            out_file.close()
    return
csv = '6p8_coh_SRC/outfile1.csv'
with open('6p8_coh_SRC/outfile1.csv') as csv_file:
    out_file = open(csv.replace('.csv','.txt'),'a')
    line_count = 0
    for line in csv_file:
        out_file.write(line)
        line_count+=1
    while line_count<12416:
        out_file.write('0\n')
        line_count+=1
    out_file.close()

path = os.getcwd()
for out_file in os.listdir('/'.join([path,'txt_files'])):
    #These have cohesin
    if out_file in ['WT.txt','no_cond.txt']:
        for color_file in os.listdir('/'.join([path,'6p8_coh_SRC'])):
            #Make our directory
            sub_dir = '/'.join([path, 'parsed_txt',out_file.replace('.txt',''),color_file.replace('.txt','')])
            try:
                os.stat(sub_dir)
            except:
                os.mkdir(sub_dir)
            print('/'.join([out_file,color_file]))
            os.system("python ParseBrownian.py -PSF GFPbigain.txt -out {} -width 75 -height 75 -every 100 {} {}".format(sub_dir,'/'.join([path,'6p8_coh_SRC',color_file]),'/'.join([path,'txt_files',out_file])))
    #These do not have cohesin
    if out_file in ['no_coh.txt', 'no_coh_no_cond.txt']:
        for color_file in os.listdir('/'.join([path,'6p8_no_coh_SRC'])):
            #Make our directory
            sub_dir = '/'.join([path, 'parsed_txt',out_file.replace('.txt',''),color_file.replace('.txt','')])
            try:
                os.stat(sub_dir)
            except:
                os.mkdir(sub_dir)
            print('/'.join([out_file,color_file]))
            os.system("python ParseBrownian.py -PSF GFPbigain.txt -out {} -width 75 -height 75 -every 100 {} {}".format(sub_dir,'/'.join([path,'6p8_coh_SRC',color_file]),'/'.join([path,'txt_files',out_file])))

path = '/cygdrive/c/Users/kompa/Desktop/Brownian_to_fluorosim/BottleBrushOutput/'
for folder in ['Density','BrushLength']:
	for seed in os.listdir(path+folder):
		for file in os.listdir(path+folder+'/'+seed):
			print(file)
			processFile(path+folder+'/'+seed+'/'+file,[1])

for folder in ['Density','BrushLength']:
	for seed in os.listdir(path+folder):
		for file in os.listdir(path+folder+'/'+seed):
			if(file.endswith("color.txt")):
				name = file.split('_color.txt')[0]
				print(name)
				os.system("python ParseBrownian.py -PSF GFPbigain.txt -out {} -width 75 -height 75 -every 25 {} {}".format(path+folder+'/'+seed+'/'+"output_"+name,path+folder+'/'+seed+'/'+file,path+folder+'/'+seed+'/'+name+".txt"))

for folder in ['Density','BrushLength']:
    for seed in os.listdir(path+folder):
        for file in os.listdir(path+folder+'/'+seed):
            if(file.endswith("color.txt")):
                name = file.split('_color.txt')[0]
                print(name)
                os.system("python BrownianXMLtoTIFF.py -green -out {} {}".format(path+folder+'/'+seed+'/'+"output_tiff_"+name,path+folder+'/'+seed+'/'+"output_"+name))

#DOS version for XML to TIFF
path = '/Users/kompa/Desktop/Brownian_to_fluorosim/BottleBrushOutput/'

for folder in ['Density','BrushLength']:
    for seed in os.listdir(path+folder):
        for file in os.listdir(path+folder+'/'+seed):
            if(file.endswith("color.txt")):
                name = file.split('_color.txt')[0]
                print(name)
                os.system("python ParseBrownian.py -PSF GFPbigain.txt -out {} -width 75 -height 75 -every 25 {} {}".format(path+folder+'/'+seed+'/'+"output_"+name,path+folder+'/'+seed+'/'+file,path+folder+'/'+seed+'/'+name+".txt"))

for folder in ['Density','BrushLength']:
    for seed in os.listdir(path+folder):
        for file in os.listdir(path+folder+'/'+seed):
            if(file.endswith("color.txt")):
                name = file.split('_color.txt')[0]
                print(name)
                os.system("python BrownianXMLtoTIFF.py -green -out {} {}".format(path+folder+'/'+seed+'/'+"output_tiff_"+name,path+folder+'/'+seed+'/'+"output_"+name))

f = open(path+'\s1pt431be10.out')
labeled = open(path+'\s1pt431be10_labeled.out','a')
colors = []
for line in f:
    new_line = line
    clean_line = line.strip()
    if(clean_line.startswith('mass ')):
        bead_num = int(clean_line.split('mass ')[1].split('\t')[0])
        if(bead_num>=34 and bead_num <=225):
            new_line = new_line[:-2]+'4\n'
            colors.append('4')
        elif(bead_num==0 or bead_num==248):
            new_line = new_line[:-2]+'3\n'
            colors.append('3')
        else:
            colors.append('1')
    if(clean_line.startswith('MassColors')):
        labeled.write(new_line)
        for color in reversed(colors):
            labeled.write(color+'\n')
            f.readline()
        continue
    labeled.write(new_line)
