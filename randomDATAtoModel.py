import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.model_selection import train_test_split
def main():
    c_class= ['star', 'gc','fo','gx_e','gx_r']
    seed_list = [17]
    name_csv = ['pic23']
    #list_head_data = ['NUMBER', 'MAG_APER', 'MAGERR_APER', 'MAG_AUTO', 'MAGERR_AUTO', 'MAG_BEST', 'MAGERR_BEST', 'KRON_RADIUS', 'BACKGROUND', 'THRESHOLD', 'ISOAREA_IMAGE', 'ISOAREAF_IMAGE', 'ALPHAPEAK_J2000',
    #         'DELTAPEAK_J2000', 'X_IMAGE', 'Y_IMAGE', 'FWHM_IMAGE', 'FWHM_WORLD', 'ELONGATION', 'ELLIPTICITY', 'CLASS_STAR', 'FLUX_RADIUS', 'FILE_NAME','CLASS_OBJECT']
    for name in name_csv:
        for c in c_class:
            name_file = name+c+'_gallary.csv'
            script_dir = os.path.dirname(name_file)
            rel_path = "region5,14,23,32\\"+name+"\\"+name_file
            abs_file_path = os.path.join(script_dir, rel_path)
            data = pd.read_csv(abs_file_path,  header=0)
            #print(data)
            for seed in seed_list:
                print(name, c, seed)
                train, test = [], []
                #print(data['NUMBER'])
                #data = data.drop(data.index[0],axis = 0)
                train, test = train_test_split(data,test_size=0.4, random_state=seed, shuffle=True)
                # train = data[mrk]
                # test = data[~mrk]
                train.to_csv("region5,14,23,32\\"+name+"\\seed"+str(seed)+"\\train\\"+c+"_train.csv",index = False)
                #print(train)
                test.to_csv("region5,14,23,32\\"+name+"\\seed"+str(seed)+"\\test\\"+c+"_test.csv",index = False)
                #print(test)

    return 0

if __name__ == "__main__":
    main()


    