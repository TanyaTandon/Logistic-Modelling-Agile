
import yaml
import pandas as pd
import seaborn as sns
import pandas as pd
#import feature_generate as fg
import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn import metrics
from sklearn.externals import joblib


def ingestdata(): 
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    return(config)


#def ingestdata(args): 
 #   with open(args.config, 'r') as f:
  #      config = yaml.load(f)
   # return(config)

def initial_model(): 
    config = ingestdata() 
    ingest_parameters = config["train_model"]["start"]
    seed = ingest_parameters["seed"]
    split_coeff = ingest_parameters[ "split"]
    features = pd.read_csv("./feature_gen/features.csv")
    target = pd.read_csv("./feature_gen/target.csv")
    #print(target)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        features, target, test_size=  split_coeff, random_state = seed)
    
    initial_features = ingest_parameters["features"]
    lr = linear_model.LogisticRegression()
    fittedModel = lr.fit(X_train[initial_features], y_train)
    joblib.dump(fittedModel, "models/logistic.pkl")
    X_train.to_csv("models/X_train.csv", index = False, header= True)
    X_test.to_csv("models/X_test.csv", index = False, header= True)
    y_train.to_csv("models/y_train.csv", index = False, header= True)
    y_test.to_csv("models/y_test.csv", index = False, header= True)
    ypred_proba_test =pd.DataFrame (lr.predict_proba(X_test[initial_features])[:,0]) 
    ypred_bin_test = pd.DataFrame(lr.predict(X_test[initial_features]))
    ypred_proba_test.to_csv("models/ypred_proba_test.csv", index = False,header = True)
    ypred_bin_test.to_csv("models/ypred_bin_test.csv", index = False,header = True)
    
#initial_model()