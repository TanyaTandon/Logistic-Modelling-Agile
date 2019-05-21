import yaml
import numpy as np
import pandas as pd


def ingestdata(): 
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    return(config)
    
def convert_to_data( path, file_name): 
    temp_ad = path +  "/" + file_name
    with open(temp_ad,'r') as f:
       data = [[s for s in line.split(' ') if s!=''] for line in f.readlines()]
    return( data)

def data_path():
    config = ingestdata() 
    ingest_parameters = config["load_data"]["ingest"]
    file_name = ingest_parameters["name"]
    path = ingest_parameters[ "path"]
    data = convert_to_data(path,file_name)
    return(data)
    
def generate_cloud(first_start, first_back): 
    columns = ['visible_mean', 'visible_max', 'visible_min', 
           'visible_mean_distribution', 'visible_contrast', 
           'visible_entropy', 'visible_second_angular_momentum', 
           'IR_mean', 'IR_max', 'IR_min']
    
    data = data_path()
    first_cloud = data[first_start:first_back]
    first_cloud = [[float(s.replace('/n', '')) for s in cloud]
               for cloud in first_cloud]
    first_cloud = pd.DataFrame(first_cloud, columns= columns)

    
    return(first_cloud)
    
def concat2():
    config = ingestdata() 
    ingest_parameters = config["load_data"]["clean"]
    first_start = ingest_parameters[ "first_start"]
    first_back = ingest_parameters[ "first_back"]
    first_cloud = generate_cloud(first_start, first_back)
    first_cloud['class'] = np.zeros(len(first_cloud))
    second_start = ingest_parameters[ "second_start"]
    second_back = ingest_parameters[ "second_back"]
    second_cloud = generate_cloud(second_start, second_back)
    second_cloud['class'] = np.ones(len(second_cloud))
    data = pd.concat([first_cloud, second_cloud])
    data.to_csv("./clean/cleaned_data.csv", index = False, header= True)