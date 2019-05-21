MODEL_NAME=logistic.pkl
CONFIG=config.yml
BUCKET=bin

.PHONY: load_data clean_data generate_features target_run train_model evaluate_model venv clean_dir

cloud/${BUCKET}/activate: requirements.txt
	test -d cloud ||    virtualenv cloud
	. cloud/${BUCKET}/activate; pip install -r requirements.txt
	touch cloud/${BUCKET}/activate

venv: cloud/${BUCKET}/activate

clean_dir:
	test -d data |  rm -rf data
	test -d clean | rm -rf clean
	test -d eval |  rm -rf eval
	test -d feature_gen |   rm -rf feature_gen
	test -d models |    rm -rf models
	mkdir data
	mkdir clean
	mkdir eval 
	mkdir feature_gen
	mkdir models

data/clouds.data: venv clean_dir
	. cloud/${BUCKET}/activate; python run.py ingest_data

load_data: data/clouds.data venv
	. cloud/${BUCKET}/activate

clean/cleaned_data.csv: data/clouds.data venv
	. cloud/${BUCKET}/activate; python run.py Returns_concatanted_data

clean_data: clean/cleaned_data.csv venv
	. cloud/${BUCKET}/activate

feature_gen/features.csv: clean/cleaned_data.csv venv
	. cloud/${BUCKET}/activate; python run.py generate_feature

generate_features: feature_gen/features.csv venv
	. cloud/${BUCKET}/activate

feature_gen/target.csv: clean/cleaned_data.csv venv
	. cloud/${BUCKET}/activate; python run.py target_return

target_run: feature_gen/target.csv venv
	. cloud/${BUCKET}/activate

models/${MODEL_NAME}: feature_gen/features.csv feature_gen/target.csv venv
	. cloud/${BUCKET}/activate; python run.py initial_model

train_model: models/${MODEL_NAME} venv
	. cloud/${BUCKET}/activate

eval/evaluate.txt: models/${MODEL_NAME} venv
	. cloud/${BUCKET}/activate; python run.py eval

evaluate_model: eval/evaluate.txt venv
	. cloud/${BUCKET}/activate

all: evaluate_model venv
	. cloud/${BUCKET}/activate