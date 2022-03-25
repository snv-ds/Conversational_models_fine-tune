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

###  Results

For simple model without history validation perplexity was **20.2**

For model with history (saved only 2 last replicas) validation perplexity was **8.4**

For model with history and some person information validation perplexity was **6.1**


### Thoughts

As an autoregressive task it`s common to use models like GPT. After lookup at data I started to clean/preprocess data, add special tokens and integrated all data in fine tune script made by Sber.

### Further ideas to developing

- try ruT5_small from `cointegrated` (folder in transformers repo)
- add graphics of learning functions
- add evaluation scripts
- code refactoring