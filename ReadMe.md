# Conversational_models_fine-tune

## Description
This repo is my attempts for finetuning chating data to make conversational model based on ruGPT3_small from Sber. 
I took data from `https://toloka.ai/ru/datasets`.

## Repo review

### Structure
    TlkPersonaChatRus
    notebooks
    images
    preprocessing.py
    requirements.txt

- In TlkPersonaChatRus folder there is changed file for basic training script
- In notebooks folder there are file for EDA, data look up, and for different attempts of finetuning base model(ruGPT3_small)
- In images folder there are graphics of changes train loss and lr diring finetune
- In preprocessing.py there are class for data preparation
- requirements.txt have all libraries, that were used in projects

### Thoughts

As an autoregressive task it`s common to use models like GPT. After lookup at data I started to clean/preprocess data, add special tokens and integrated all data in fine tune script made by Sber.

### Futher ideas to developing

- try ruT5_small from `cointegrated` (folder in transformers repo)
- add graphics of learning functions
- add evaluation scripts
- code refactoring