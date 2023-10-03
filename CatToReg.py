import codecs 
import re
import string
import os
import math
import csv
def main():
    data_cat = file_controller()
    #print(type(data_reg[0][0][0]))
    data_list=[]
    for i in range(len(data_cat)):
        result = cat_to_reg(data_cat[i])
        data_list.append(result)

    print(data_list)
    name_txt = ['pic23']
    #name_txt = ['pic5catText']
    for i in range(len(name_txt)):
        with open(name_txt[i]+'cat.txt', 'w') as f:
            f.writelines("""# Region file format: DS9 version 4.1
global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
fk5\n""")
            for item in data_list[i]:
                f.write("%s\n" % item)
            f.close()


        
def file_controller():
    data_cat = []
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
    return data_cat


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
        key_splited[i][0] = (float(ra[0]) + float(ra[1]) /  60 + float(ra[2])/3600)*15        # RA
        key_splited[i][1] = float(
            dec[0]) + float(dec[1])/60 + float(dec[2])/3600          # DEC
    return key_splited

def ra_convert(ra):
    h = int(ra//15)
    m = int(math.floor(((ra/15)-h)*60))
    s = ((((ra/15)-h)*60)-m)*60
    
    return str(h)+":"+str(m)+":"+'{:.4f}'.format(s)

def dec_convert(dec):
    d = int(math.floor(dec))
    arcmin = int(math.floor((dec-d)*60))
    arcsec =  (((dec-d)*60)-arcmin)*60
    return "+"+str(d)+":"+str(arcmin)+":"+'{:.3f}'.format(arcsec)

def cat_to_reg(data_cat):
    list_ra_dec = []
    for i in data_cat:
        ra = ra_convert(float(i[0]))
        dec = dec_convert(float(i[1]))
        string_to_add = "circle("+ra+","+dec+",2"+'"'+")"
        list_ra_dec.append(string_to_add)
    return list_ra_dec

def match_reg_cat(data_reg,data_cat):
    data_match_class = []
    for i in data_reg:
        list_distance = []
        for j in data_cat:
            box=[]
            D_ra=float(i[0])-float(j[0])        # find ra distance 
            D_dec=float(i[1])-float(j[1])       # find dec distance 
            result = (D_ra**2)+(D_dec**2)                           
            result = math.sqrt(result)                              # Co-ordinate Geometry to find distance between 2 point
            if result<=2:                                        #if distance < radius go 
                box.append(result)
                box.extend(j)
                box.append(i[3])                                        # class
                list_distance.append(box)
        match=sorted(list_distance,key=lambda k:k[0], reverse=False)  # sort Select max mag_aper 
        if len(match)!=0 :
            data_match_class.append(match[0])
    return data_match_class

if __name__ == "__main__":
    main()