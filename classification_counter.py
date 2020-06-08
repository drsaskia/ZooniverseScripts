#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np 
import pandas as pd
#import seaborn as sns

def getClassCounts(infile):
    """reads zooniverse .csv and extracts subject id list by pond ID"""
    vh = pd.read_csv(infile, error_bad_lines=False)
    # to make new column from old column, string by delimiter then transfer only the nth field of the list
    #vh['filename'] = vh['metadata'].str.split('\"').str[3]
    #vh['iscat'] = vh['filename'].str.split(':').str[0]
    
    colNames = vh.columns.values.tolist()
    #print colNames
    
    ## remove (replace by nothing) all double quotes from string to make human-readable and remove need for escapes
    vh['annotations_r'] = vh['annotations'].str.replace('\"', "")
    vh['annotations_r'] = vh['annotations_r'].str.replace('\[', "") 
    vh['subject_data_r'] = vh['subject_data'].str.replace('\"', "")
    
    ## copy last field of string split by : which happens to be filename
    vh['filename'] = vh['subject_data_r'].str.split(':').str[-1]
    vh['comment'] = vh['annotations_r'].str.split(',').str[-2]
    #print vh['comment'].head(10)
    
    ## count occurrences of value:n, which is classifications (class count 6 is control)
    vh['class_count0'] = vh['annotations_r'].str.count('value:0')
    vh['class_count1'] = vh['annotations_r'].str.count('value:1')
    vh['class_count2'] = vh['annotations_r'].str.count('value:2')
    vh['class_count3'] = vh['annotations_r'].str.count('value:3')
    vh['class_count4'] = vh['annotations_r'].str.count('value:4')
    vh['class_count5'] = vh['annotations_r'].str.count('value:5')
    vh['class_control1'] = vh['annotations_r'].str.count('value:')
    col_list = ['class_count0', 'class_count1', 'class_count2', 'class_count3', 'class_count4', 'class_count5']
    vh['class_control2'] = vh[col_list].sum(axis=1)
    vh['class_control3'] = vh['class_control1'] - vh['class_control2']
    # select filenames where difference between class count and total occurrence of 'value:' is > 2
    flag_list = vh['filename'].where(vh['class_control3'] > 2).tolist()
    new_flag_list = []
    for item in flag_list:
        try:
            float(item)
        except:
            new_flag_list.append(str(item))
    #print new_flag_list
    ## print first ten lines for fields with counts & filename
    #print vh[['filename', 'comment', 'class_count0', 'class_count1', 'class_count2', 'class_count3', 'class_count4', 'class_count5', 'class_count6']].head(10)
    
    ## make new dataframe with subset of old dataframe based on contents of field 'pondID'
    # newdf = vh[vh['pondID'].isin(['VH-HCF', 'BTR-', 'VH1009', 'VH1009x10', 'vh1006-'])]
    ## print stats for number of files per value of 'pondID'
    #print vh.groupby('class_control1')['subject_ids'].nunique()
    print vh.groupby('class_control3')['subject_ids'].nunique()
    #vh[['class_count0', 'class_count1', 'class_count2', 'class_count3', 'class_count4', 'class_count5', 'class_control1', 'class_control2']].hist()
    vh[['class_control1', 'class_control3']].hist()
    ## drop columns from dataframe by column name
    out_data = vh[['filename', 'comment', 'class_count0', 'class_count1', 'class_count2', 'class_count3', 'class_count4', 'class_count5', 'class_control1', 'class_control2', 'class_control3']]
    #print out_data.describe()
    ## save to csv
    out_data.to_csv("tamara-readable-data.csv", index=False)
    return colNames

infile = "Downloads/tamara-classifications(1).csv"
subjectids = getClassCounts(infile)


# In[ ]:




