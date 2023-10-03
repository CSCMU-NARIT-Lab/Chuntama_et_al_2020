import codecs 
import re
import string
import os
import math
import csv
def main():
    data_reg, data_cat = file_controller()
    #print(type(data_reg[0][0][0]))
    match_list=[]
    for i in range(len(data_cat)):
        print(len(data_reg[i]))
        result = match_reg_cat(data_reg[i], data_cat[i])
        match_list.append(result)
    # name_csv = ['pic1', 'pic2', 'pic3', 'pic4', 'pic5', 'pic6', 
    #         'pic7', 'pic8', 'pic9', 'pic10', 'pic11', 'pic12', 
    #         'pic13', 'pic14', 'pic15', 'pic16', 'pic17', 'pic18', 
    #         'pic19', 'pic20', 'pic21', 'pic22', 'pic23', 'pic24', 
    #         'pic25', 'pic26', 'pic27', 'pic28', 'pic29', 'pic30', 
    #         'pic31', 'pic32', 'pic33', 'pic34', 'pic35', 'pic36']
    name_csv = ['pic23_new']
    for i in range(len(name_csv)):
        csv_export(match_list[i],name_csv[i])

        
def file_controller():
    data_reg, data_cat = [], []
    file_reg = ['i23_classified_sep25.reg']
    # file_reg = ['pic1.reg', 'pic2.reg', 'pic3.reg', 'pic4.reg', 'pic5.reg', 'pic6.reg', 
    #         'pic7.reg', 'pic8.reg', 'pic9.reg', 'pic10.reg', 'pic11.reg', 'pic12.reg', 
    #         'pic13.reg', 'pic14.reg', 'pic15.reg', 'pic16.reg', 'pic17.reg', 'pic18.reg', 
    #         'pic19.reg', 'pic20.reg', 'pic21.reg', 'pic22.reg', 'pic23.reg', 'pic24.reg', 
    #         'pic25.reg', 'pic26.reg', 'pic27.reg', 'pic28.reg', 'pic29.reg', 'pic30.reg', 
    #         'pic31.reg', 'pic32.reg', 'pic33.reg', 'pic34.reg', 'pic35.reg', 'pic36.reg']
    for i in file_reg: 
        script_dir = os.path.dirname(i)
        print(script_dir)
        rel_path = 'regfile\\'+i
        abs_file_path = os.path.join(script_dir, rel_path)
        temp_box = read_reg_file(abs_file_path)
        data_reg.append(convert_to_degree(temp_box))
    file_cat=['i23.cat']
    # file_cat=['i1.cat', 'i2.cat', 'i3.cat', 'i4.cat', 'i5.cat', 'i6.cat',
    #         'i7.cat', 'i8.cat', 'i9.cat', 'i10.cat', 'i11.cat', 'i12.cat', 
    #         'i13.cat', 'i14.cat', 'i15.cat', 'i16.cat', 'i17.cat', 'i18.cat', 
    #         'i19.cat', 'i20.cat', 'i21.cat', 'i22.cat', 'i23.cat', 'i24.cat', 
    #         'i25.cat', 'i26.cat', 'i27.cat', 'i28.cat', 'i29.cat', 'i30.cat', 
    #         'i31.cat', 'i32.cat', 'i33.cat', 'i34.cat', 'i35.cat', 'i36.cat']
    for i in file_cat:
        script_dir = os.path.dirname(i)
        rel_path = "dataset\\"+i
        abs_file_path = os.path.join(script_dir, rel_path)
        temp_box=read_file(abs_file_path)
        data_cat.append(filter_magnitude(temp_box))
    return data_reg, data_cat


def filter_magnitude(data):

    sort_list = sorted(data, key=lambda l: l[2], reverse=False)
    # select top 30 row that are sorted
    result = sort_list[0:600]
    return result

def read_file(filename):
    data = []
    myfile = open(filename)
    info = myfile.readlines()
    for i in range(len(info)):
        info[i].rstrip('\n')
        a = re.findall(r"\S+", info[i])
        if(a[0] != '#'):
            temp = []
            temp.append(float(a[12]))   # 0: RA
            temp.append(float(a[13]))   # 1: DEC
            temp.append(float(a[1]))           # 2: MAG_APER
            temp.append(filename)       # 3: file name
            temp.append(a[0])           # 4: Object number
            temp.append(float(a[14]))   # 5: X
            temp.append(float(a[15]))   # 6: Y
            data.append(temp)
        myfile.close()
    return data

def read_reg_file(filename):
    print(filename)
    regFile = codecs.open (filename)
    reg = regFile.read()
    regFile.close()
    x=reg.splitlines()
    data_reg=[]
    for i in x:
        temp=re.split("[" + "#(),+" +'" '+"]+", i)
        if temp[0]=="circle":
            if temp[-1]=='':
                temp[-1]='green'
            else:
                color=temp[-1]
                temp.pop(-1)
                c=color.split("=")
                temp.append(c[1])
            data_reg.append(temp[1:])
    #print(data_reg)
    # 0: RA
    # 1: DEC
    # 2: radius
    # 3: class
    return(data_reg)

def convert_to_degree(key_splited):
    for i in range(len(key_splited)):
        # use for file 'aj341087t2_ascii.txt' that RA and Dec have ':' between number
        ra = key_splited[i][0].split(':')
        dec = key_splited[i][1].split(':')
        # calculate HH:MM:SS to degree RA
        key_splited[i][0] = (float(ra[0]) + float(ra[1]) /
                             60 + float(ra[2])/3600)*15        # RA
        key_splited[i][1] = float(
            dec[0]) + float(dec[1])/60 + float(dec[2])/3600          # DEC
    return key_splited

def match_reg_cat(data_reg,data_cat):
    radius = 0.1
    data_match_class = []
    for i in data_reg:
        list_distance = []
        for j in data_cat:
            box=[]
            D_ra=float(i[0])-float(j[0])        # find ra distance 
            D_dec=float(i[1])-float(j[1])       # find dec distance 
            result = (D_ra**2)+(D_dec**2)                           
            result = math.sqrt(result)                              # Co-ordinate Geometry to find distance between 2 point
            if result<=radius:                                        #if distance < radius go 
                box.append(result)
                box.extend(j)
                box.append(i[3])                                        # class
                list_distance.append(box)
        match=sorted(list_distance,key=lambda k:k[0], reverse=False)  # sort Select minimum distance
        #print(match)
        if len(match)!=0 :
            data_match_class.append(match[0])
    return data_match_class

def splitter(g_file):
    splited = []
    myfile = open(g_file)
    info = myfile.readlines()
    for text in info:
        if(text[0] != '#'):
            text = text.rstrip('\n')
            text = re.findall(r'\S+', text)
            text.append(g_file)
            splited.append(text)
            myfile.close()
    return splited

def csv_export(matched_list,name):
    c_class= {'star': 0, 'gx_e': 0 ,'gx_r': 0 ,'gc': 0, 'fo': 0 , 'None' : 0}
    file_name = name+'MatchClass.csv'
    with open('region5,14,23,32\\'+file_name, 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        description=[
        ["#   1 NUMBER                 Running object number                                     "],
        ["#   2 MAG_APER               Fixed aperture magnitude vector                            [mag]"],
        ["#   3 MAGERR_APER            RMS error vector for fixed aperture mag.                   [mag]"],
        ["#   4 MAG_AUTO               Kron-like elliptical aperture magnitude                    [mag]"],
        ["#   5 MAGERR_AUTO            RMS error for AUTO magnitude                               [mag]"],
        ["#   6 MAG_BEST               Best of MAG_AUTO and MAG_ISOCOR                            [mag]"],
        ["#   7 MAGERR_BEST            RMS error for MAG_BEST                                     [mag]"],
        ["#   8 KRON_RADIUS            Kron apertures in units of A or B                         "],
        ["#   9 BACKGROUND             Background at centroid position                            [count]"],
        ["#  10 THRESHOLD              Detection threshold above background                       [count]"],
        ["#  11 ISOAREA_IMAGE          Isophotal area above Analysis threshold                    [pixel**2]"],
        ["#  12 ISOAREAF_IMAGE         Isophotal area (filtered) above Detection threshold        [pixel**2]"],
        ["#  13 ALPHAPEAK_J2000        Right ascension of brightest pix (J2000)                   [deg]"],
        ["#  14 DELTAPEAK_J2000        Declination of brightest pix (J2000)                       [deg]"],
        ["#  15 X_IMAGE                Object position along x                                    [pixel]"],
        ["#  16 Y_IMAGE                Object position along y                                    [pixel]"],
        ["#  17 FWHM_IMAGE             FWHM assuming a gaussian core                              [pixel]"],
        ["#  18 FWHM_WORLD             FWHM assuming a gaussian core                              [deg]"],
        ["#  19 ELONGATION             A_IMAGE/B_IMAGE                                           "],
        ["#  20 ELLIPTICITY            1 - B_IMAGE/A_IMAGE                                       "],
        ["#  21 CLASS_STAR             S/G classifier output                                     "],
        ["#  22 FLUX_RADIUS            Fraction-of-light radii                                    [pixel]"],
        ["#  23 FILE_NAME              File location"],
        ["#  24 CLASS_OBJECT           1 = GC 2 = SF 3 = STAR 4 = GALAXY"],
        ]
        #a.writerows(description)
        #print((description[0]),(description[23]))
        data = [['NUMBER', 'MAG_APER', 'MAGERR_APER', 'MAG_AUTO', 'MAGERR_AUTO', 'MAG_BEST', 'MAGERR_BEST', 'KRON_RADIUS', 'BACKGROUND', 'THRESHOLD', 'ISOAREA_IMAGE', 'ISOAREAF_IMAGE', 'ALPHAPEAK_J2000',
                 'DELTAPEAK_J2000', 'X_IMAGE', 'Y_IMAGE', 'FWHM_IMAGE', 'FWHM_WORLD', 'ELONGATION', 'ELLIPTICITY', 'CLASS_STAR', 'FLUX_RADIUS', 'FILE_NAME','CLASS_OBJECT']]
        a.writerows(data)
        #print("ml = ",matched_list)
        for i in range(len(matched_list)):
            m = matched_list[i]
            #print("m = " ,m)
            # use splitter function to split data in file name
            temp = splitter(m[4])
            tag = int(m[5])-1 # select obj num but use in order list -1 to data 
            #print("temp = ",temp)
            #print(tag)
            class_object=class_def(m[-1])
            c_class[class_object]+=1
            data = [[temp[int(tag)][0], temp[int(tag)][1], temp[int(tag)][2], temp[int(tag)][3], temp[int(tag)][4], temp[int(tag)][5], temp[int(tag)][6], temp[int(tag)][7], temp[int(tag)][8], 
                temp[int(tag)][9], temp[int(tag)][10], temp[int(tag)][11], temp[int(tag)][12], temp[int(tag)][13], temp[int(tag)][14], temp[int(tag)][15], temp[int(tag)][16], temp[int(tag)][17], temp[int(tag)][18],
                temp[int(tag)][19], temp[int(tag)][20], temp[int(tag)][21], m[4], class_object]]
            a.writerows(data)
    print(c_class)

#CLASS 1 = Globalar Cluster, 2 = Star forming region, 3 = Star, 4 = Galaxy
def class_def(color):
    switcher = {
        'red' : 'gc',
        'magenta' : 'fo',
        'black' : 'star',
        'cyan' : 'gx_r',
        'blue' : 'gx_e',
        'green' : 'None'
    }
    return switcher.get(color,'None')

if __name__ == "__main__":
    main()