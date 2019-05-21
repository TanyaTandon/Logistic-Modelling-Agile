import pandas as pd
# For modeling
import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn import metrics
from cycler import cycler
import logging
# Update matplotlib defaults to something nicer

# for appending dates to filenames
import datetime
import pickle
import yaml
import os
import joblib
import numpy as np

def eval():
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    
    ypred_proba_test = pd.read_csv("./models/ypred_proba_test.csv")
    ypred_bin_test = pd.read_csv("./models/ypred_bin_test.csv")
    y_test = pd.read_csv("./models/y_test.csv")
    auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
    confusion = sklearn.metrics.confusion_matrix(y_test, ypred_bin_test)
    accuracy = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)
    classification_report = sklearn.metrics.classification_report(y_test, ypred_bin_test)

  
    path = config[ "train_model"]["path"]
    file_name= "evaluate.txt"
        #logger.debug('Checking if the dir exists and if not, making the dir')
        #if os.path.exists(path) == False:
         #   os.makedirs(path)
          #  logger.debug('Directory created')
        
    f = open(os.path.join(path,file_name),"w+")
     
    f.write('Performance measures for model: {}\n'.format(config["train_model"]["file_name"]))

    f.write('AUC on test: %0.3f\n' % auc)
    f.write('Accuracy on test: %0.3f\n' % accuracy)
    f.write('\n------------------------------------------------------------\n')
    f.write('Confusion Matrix:\n\n')
    temp_df = pd.DataFrame(confusion,index=['Actual negative','Actual positive'],\
    columns=['Predicted negative', 'Predicted positive'])
    temp_df.to_string(f)
    f.write('\n------------------------------------------------------------\n')
    f.write('feature importances/ odd ratios:\n\n')
    fitted = pd.DataFrame(index=config["train_model"]["start"]["features"])
    lr = joblib.load(open(os.path.join(config["train_model"]["save_location"],config["train_model"]["f_name"]), 'rb'))
    fitted['coefs'] = lr.coef_[0]
    fitted['odds_ratio'] = fitted.coefs.apply(np.exp)
    fitted = fitted.sort_values(by='odds_ratio', ascending=False)
    fitted.to_string(f)
    f.write('\n------------------------------------------------------------\n')
    f.close()
        
        
   

#print('AUC on test: %0.3f' % auc)
#print('Accuracy on test: %0.3f' % accuracy)
#print()
#print(pd.DataFrame(confusion,
 #                 index=['Actual negative','Actual positive'],
  #                columns=['Predicted negative', 'Predicted positive']))
  
  
#eval()