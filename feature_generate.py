
import yaml 
#from clean_data import concat2 
import pandas as pd
import numpy as np
import seaborn as sns


def generate_feature(): 
    data = pd.read_csv("./clean/cleaned_data.csv")
    columns = ['visible_mean', 'visible_max', 'visible_min', 
           'visible_mean_distribution', 'visible_contrast', 
           'visible_entropy', 'visible_second_angular_momentum', 
           'IR_mean', 'IR_max', 'IR_min']
    features = data[columns]
    features['visible_range'] = (features.visible_max - features.visible_min)
    features['visible_norm_range'] = (
    features.visible_max - features.visible_min).divide(features.visible_mean)
    features['log_entropy'] = features.visible_entropy.apply(np.log)
    features['entropy_x_contrast'] = features.visible_contrast.multiply(
    features.visible_entropy)
    features['IR_range']  = features.IR_max - features.IR_min
    features['IR_norm_range'] = (features.IR_max - features.IR_min).divide(
    features.IR_mean)
    features.to_csv("./feature_gen/features.csv", header = True, index = False)
   
    
def target_return():
    data = pd.read_csv("./clean/cleaned_data.csv")
    columns = ['visible_mean', 'visible_max', 'visible_min', 
           'visible_mean_distribution', 'visible_contrast', 
           'visible_entropy', 'visible_second_angular_momentum', 
           'IR_mean', 'IR_max', 'IR_min']
    target = data["class"]
    target.to_csv("./feature_gen/target.csv", header = True, index = False)
    



   



