
import logging
import os
import requests
import yaml


logger = logging.getLogger(__name__)

def load_data_first(): 
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    # get relevant parameters from  YAML file     
    ingest_parameters = config["load_data"]["ingest"]    
    # parse out parameters    
    url = ingest_parameters["source_data_url"]
    file_name = ingest_parameters["name"]
    path = ingest_parameters[ "path"]   
    r = requests.get(url) 
    with open(os.path.join(path, file_name), 'wb') as f:
        f.write(r.content)
   

