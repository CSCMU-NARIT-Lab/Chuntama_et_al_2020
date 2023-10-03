import pandas as pd
import os
import csv
def main():
    #type_gallary = ['gx','gc','sf','star']
    type_gallary = ['gx_e','gx_r','gc','fo','star','None']
    name_csv = ['pic23']
    #list_head_data = ['NUMBER', 'MAG_APER', 'MAGERR_APER', 'MAG_AUTO', 'MAGERR_AUTO', 'MAG_BEST', 'MAGERR_BEST', 'KRON_RADIUS', 'BACKGROUND', 'THRESHOLD', 'ISOAREA_IMAGE', 'ISOAREAF_IMAGE', 'ALPHAPEAK_J2000',
    #         'DELTAPEAK_J2000', 'X_IMAGE', 'Y_IMAGE', 'FWHM_IMAGE', 'FWHM_WORLD', 'ELONGATION', 'ELLIPTICITY', 'CLASS_STAR', 'FLUX_RADIUS', 'FILE_NAME','CLASS_OBJECT']
    for g in type_gallary:
        for i in name_csv:
            gallary = []
            script_dir = os.path.dirname(i)
            rel_path = "region5,14,23,32\\"+i+'_newMatchClass.csv'
            abs_file_path = os.path.join(script_dir, rel_path)
            data = pd.read_csv(abs_file_path,header=0,comment='#')
            data.drop(0, axis=0)
            print(data)
            temp_df = data.loc[data['CLASS_OBJECT'] == g]
            gallary.append(temp_df)
            frame = pd.concat(gallary, axis = 0 ,ignore_index = True)
            print(len(gallary[0]))
            frame.to_csv("region5,14,23,32\\"+i+"\\"+i+g+"_gallary.csv",index = False)
            #frame.to_csv("r2gallaryDATA\\"+i+"\\"+i+g+"_gallary.csv",index = False)
    return 0

if __name__ == "__main__":
    main()