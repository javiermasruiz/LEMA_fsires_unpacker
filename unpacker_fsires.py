import os
import re
import numpy as np 
import shlex
import pandas as pd

data_folder =  '20240816'
dirname = os.getcwd()
full_path = dirname+'/'+data_folder
files_list = [files for files in os.listdir(full_path) if files.endswith('.fsires')]
ordered_files_list = sorted(files_list, key=lambda x: int(x.split('.')[0]))

# READ FSIRES INFO
def read_data(file_name):
    info = dict()
    raw_data = dict()

    with open(full_path+"/"+file_name,'r') as f:
        lines = f.readlines()
        content=[x.replace('\\r\\n','') for x in lines]

    ## READING INFO DATA
    for c in content:
        try:
            dp_i=c.index(':')
            Label=''.join(c[:dp_i])
            Label=Label.strip()
            Value=''.join(c[dp_i+1:])
            Value=Value.strip()
            info[Label]=Value
        except:
            pass
    
    # READING BLOCK DATA
    for i in range(len(content)):
        a=content[i]
        if (a.__contains__('[BLOCK DATA]')): bd_i=i
    Labels=shlex.split(content[bd_i+1])
    Values=list()
    for c in content[bd_i+2:]:
        Values.append(shlex.split(c))
    Values=np.array(Values)
    for l in range(len(Labels)):
        raw_data[Labels[l]]=list(Values.transpose()[l])
    for l in raw_data.keys():
        raw_data[l]=[np.float32(x) for x in raw_data[l]]
    
    return info, raw_data


def merge_dataframe_from_dict(dict1,dict2):
    df1 = pd.DataFrame([dict1])
    df2 = pd.DataFrame(dict2)
    # Agrega la información de dict1 como columnas en cada fila de dict2
    combined_df = pd.concat([df1] * len(df2), ignore_index=True).join(df2)
    #combined_df.to_csv("combined_data.csv", index=False)
    return combined_df



if __name__ == '__main__':
    combined_dataf = pd.concat([merge_dataframe_from_dict(*read_data(i)) for i in ordered_files_list], ignore_index=True)
    print(combined_dataf.shape)
    #combined_dataf.to_csv("combined_data_carbon.csv", index=False)