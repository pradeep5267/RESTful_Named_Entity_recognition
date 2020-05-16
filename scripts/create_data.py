#%%
import pandas as pd
import numpy as np 
import spacy
import os
import re
import json
# %%
# os.getcwd()
# os.chdir('/home/pradeep/Desktop/ambrapali_electrotech')
#%%
def read_csv_from_path(filepath, nrows=5000):
    df = pd.read_csv(filepath, nrows=nrows)
    df.head()
    return df
#%%
def remove_column(df, target_col):
    target_col = str(target_col)
    try:
        df.drop(columns=[target_col],inplace = True)
    except:
        print('column not present, no changes made')
    return df 
# %%
def clean_text(df, target_col):
    regex_patterns = {r'<[^>]*>':' ',  # remove html tags
                      r"[^a-zA-Z#]":' ' # remove spl chars and number
                 }
    df_clean_series = df[target_col].replace(to_replace=regex_patterns, regex=True) 
    return df_clean_series
#%%
def write_file(file_name, df_series):
    fname = file_name + '.txt'
    with open(fname,'a+') as fhandle: 
        for index, row in enumerate(df_series):
            fhandle.write(row)
            fhandle.write('\n')

def read_file(file_name):
    with open(file_name,'r') as fhandle:
        for idx,line in enumerate(fhandle):
            if idx >= 1:
                break
            else:
                print(line)

def read_file_list(file_name):
    l = []
    with open(file_name,'r') as fhandle:
        for idx,line in enumerate(fhandle):
            l.append(line)
    return l
#%%
def create_text_list(df_series):
    text_list = []
    for index, row in enumerate(df_series):
        text_list.append(row)
    return text_list
#%%
def create_data_dict(text_list, spacy_model_name):
    nlp = spacy.load(spacy_model_name)
    data_dict = {}
    for i in range(len(text_list) - 1):
        doc = nlp(text_list[i])
        if (i % 10 == 0):
            print(f'done with {i} sentences')

        for ent in doc.ents:
            if (ent.label_ == 'GPE' or ent.label_ == 'PERSON'):
                ent_string = str(ent)
                ent_string.strip()
                data_dict[ent_string] = ent.label_
    return data_dict
#%%
def create_dataframe_from_dict(data_dict):
    df_processed = pd.DataFrame(list(data_dict.items()), columns=['data','entity'])
    df_processed['data'] = df_processed.data
    return df_processed
#%%
def create_json_from_dataframe(df):
    dd_json = {}
    dd_json = df_processed.to_json(orient='records', lines=False)
    return dd_json
#%%
def write_json_file(file_name, json_data):
    with open(file_name, "w") as outfile: 
        outfile.write(dd_json) 
#%%
json_file_path = "./flask_app/data_entity_list_full.json"
dataset_path = './dataset/imdb-dataset-of-50k-movie-reviews(1)/IMDB Dataset.csv'
#%%
df = read_csv_from_path(dataset_path, nrows=5000)
df = remove_column(df, 'sentiment')
df_clean_series = clean_text(df, 'review')
#%%
text_list = []
text_list = create_text_list(df_clean_series)
#%%
data_dict = {}
spacy_model_name = 'en_core_web_sm' # used small Spacy model, accuracy can be improved if bigger model is used but i didnt have enough compute power to do so
data_dict = create_data_dict(text_list,spacy_model_name)
#%%
df_processed = create_dataframe_from_dict(data_dict)
df_processed.head()
dd_json = create_json_from_dataframe(df_processed)
#%%
write_json_file(json_file_path, dd_json)
#%%
########### Sanity check #############
data = 'imperi'
with open(file_name,'r') as json_file:
    json_data = json.load(json_file)
    for i in range(len(json_data)):
        if (str(data).lower() in json_data[i]['data'].lower()):
            print(json_data[i]['data']) 
            print('True')
        else:
            print('false')

#%%
############## Flask ###################

