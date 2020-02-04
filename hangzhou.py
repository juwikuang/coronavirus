# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 23:02:41 2020

@author: eric
"""

import re
import pandas as pd

class Patient():
    name='unknown'
    sex='unknown'
    age=-1
    district='unknown'
    infection_type='unknown'
    body_temperature=None
    symptom_date=None
    info=''
    
def extract_date(s):
    result=re.match('(\d+)月(\d+)日', s)
    if not result:
        return None
    month, day = result.groups()
    month = int(month)
    day = int(day)
    return f'2019-{month}-{day}'
    
def get_body_temperature(s):
    result=re.search('体温(.+)℃', s)
    if not result:
        return None
    temperature  =  result.groups()[0]
    temperature = float(temperature)
    return temperature

def get_symptom_date(s):
    result=re.search('(\d+)月(\d+)日出现不适', s)
    if not result:
        return None
    month, day = result.groups()
    month = int(month)
    day = int(day)
    return f'2019-{month}-{day}'

def get_infection_type(s):
    dict_key_infection_type={}
    dict_key_infection_type['隔离中的病例密切接触者']='病例的密切接触者'
    dict_key_infection_type['感染来源调查中']='调查中'
    
    dict_key_infection_type['为1月24日乘TR188航班自新加坡到达萧山机场湖北旅客']='入境排查'

    dict_key_infection_type['为1月25日乘TR188次航班自新加坡到达萧山机场武汉乘客']='入境排查'
    dict_key_infection_type['1月24日TR188航班到达萧山机场']='入境排查'
    dict_key_infection_type['目前尚未找到明确的感染来源']='调查中'
    
    dict_key_infection_type['有武汉发热病例接触史']='接触湖北人员'
    dict_key_infection_type['有湖北来杭人员接触史']='接触湖北人员'
    dict_key_infection_type['有武汉人员接触史']='接触湖北人员'
    dict_key_infection_type['武汉人员有接触史']='接触湖北人员'
    dict_key_infection_type['为武汉来杭患者的密切接触者']='密切接触湖北人员'
    dict_key_infection_type['为武汉来杭发热疑似病例密切接触者']='密切接触湖北人员'
    

    dict_key_infection_type['确诊病例的密切接触者']='病例的密切接触者'
    dict_key_infection_type['有病例接触史']='病例的接触者'
    
    
    dict_key_infection_type['有武汉旅居史']='湖北来杭'
    dict_key_infection_type['有湖北旅行史']='湖北来杭'
    dict_key_infection_type['湖北旅居史']='湖北来杭'
    dict_key_infection_type['有湖北省旅居史']='湖北来杭'
    dict_key_infection_type['湖北来杭']='湖北来杭'
    
    dict_key_infection_type['武汉旅居史']='湖北来杭'
    dict_key_infection_type['武汉旅行史']='湖北来杭'
    dict_key_infection_type['武汉来杭']='湖北来杭'
    dict_key_infection_type['武汉回杭']='湖北来杭'
    
    for key, value in dict_key_infection_type.items():
        if s.find(key)>0:
            return value
        
    return None


def parse_file(txt_path):

    sentences=[]

    
    with open(txt_path) as f:
        sentences=f.readlines()
        f.flush()
        f.close()
    
    
    sentences=[s.strip() for s in sentences if s.strip()!='']
    
    if len(sentences)==0:
        return
    
    data=pd.DataFrame()
    
    for sentence in sentences:
    
        labels=sentence.split('，')
        
        p=Patient()
        
        p.name=labels[0]
        p.sex=labels[1]
        p.age=labels[2].replace('岁','')
        p.district=labels[3].replace('现住','').replace('1月24日TR188航班到达萧山机场','萧山机场') \
        .replace('为1月24日乘TR188航班自新加坡到达萧山机场湖北旅客','萧山机场') \
        .replace('为1月25日乘TR188次航班自新加坡到达萧山机场武汉乘客','萧山机场')
        p.infection_type=get_infection_type(sentence)
        
        p.symptom_date=get_symptom_date(sentence)
        if not p.symptom_date:
            p.symptom_date=extract_date(labels[5])
            
        p.body_temperature=get_body_temperature(sentence)
        p.info=sentence
        
        data=data.append({'name':p.name,'sex':p.sex, 'age':p.age, 'district':p.district,
                          'infection_type':p.infection_type,
                          'body_temperature':p.body_temperature,
                          'symptom_date':p.symptom_date,
                          'info':p.info
                          },ignore_index=True)
        
    data=data[['name','sex','age','district','infection_type','body_temperature','symptom_date','info']]
        
    data.to_csv(txt_path.replace('.txt','.csv'), encoding='utf-8-sig', index=False)
    



import os
for file in os.listdir("data/"):
    if file.endswith(".txt"):
        parse_file("data/"+file)

    
    
    
    


