import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import math
import numpy as np
import glob
from sklearn.model_selection import train_test_split
def main():
    #list_head_data = ['NUMBER', 'MAG_APER', 'MAGERR_APER', 'MAG_AUTO', 'MAGERR_AUTO', 'MAG_BEST', 'MAGERR_BEST', 'KRON_RADIUS', 'BACKGROUND', 'THRESHOLD', 'ISOAREA_IMAGE', 'ISOAREAF_IMAGE', 'ALPHAPEAK_J2000',
    #         'DELTAPEAK_J2000', 'X_IMAGE', 'Y_IMAGE', 'FWHM_IMAGE', 'FWHM_WORLD', 'ELONGATION', 'ELLIPTICITY', 'CLASS_STAR', 'FLUX_RADIUS', 'FILE_NAME','CLASS_OBJECT']
    seed_list = [17]
    name_csv = ['pic23']
    t = 'test'    # train or test here!!!
    for name in name_csv:
        for seed in seed_list:
            path = "region5,14,23,32\\"+name+"\\seed" +str(seed)+"\\"+t+"\\"
            all_files =['gc_'+t,'star_'+t,'gx_e_'+t,'gx_r_'+t,'fo_'+t]
            print(all_files)
            li = []

            for filename in all_files:

                df = pd.read_csv(path+filename+".csv", index_col=None, header=0)
                df.drop(['NUMBER', 'X_IMAGE', 'Y_IMAGE', 'FILE_NAME'],axis='columns',inplace= True)
                li.append(df)

            frame = pd.concat(li, axis=0, ignore_index=True)
            #frame.to_csv("pic5gallary\\seed"+str(seed)+"\\train.csv",index = False)
            #print(train)
            destination = "region5,14,23,32\\"+name+"\\seed"+str(seed)+"\\data"+t+".csv"
            frame.to_csv(destination , index = False)
            #print(test)
    return 0

if __name__ == "__main__":
    main()