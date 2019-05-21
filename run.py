
import argparse
import logging.config


# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
#logger = logging.getLogger("run-penny-lane")
#logger.debug('Test log')

from load import load_data_first
from clean_data import concat2
from feature_generate import generate_feature, target_return
from model import initial_model
from evaluation import eval 


#def run_app(args):
#    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('ingest_data') 
    sub_process.set_defaults(func=load_data_first)

    sub_process = subparsers.add_parser('Returns_concatanted_data')
    sub_process.set_defaults(func=concat2)

    sub_process = subparsers.add_parser('generate_feature')
    sub_process.set_defaults(func=generate_feature)
                             
    sub_process = subparsers.add_parser('target_return')
    sub_process.set_defaults(func=target_return)
    
    sub_process = subparsers.add_parser('initial_model') 
    sub_process.set_defaults(func= initial_model)

    sub_process = subparsers.add_parser('eval')
    sub_process.set_defaults(func=eval)
    
    args = parser.parse_args()
    args.func()