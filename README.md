# Flask REST API with PII Masking & LLM Integration

Small POC to mask PII data sent to LLM.
Detecting PII is not an easy task, so this solution is quite naive and will not work in practice.
I'm using some regex for email and phone number searching in the input data and for people or organization names I used [spacy](https://github.com/explosion/spaCy) library with NLP en_core_web_sm model

LLM API used is Hugging Face [Inference API](https://huggingface.co/inference-api/serverless). It's free to use and open source.

The code is divided into 3 module - api and mask where

 - api - contains core logic
 - test - contains UT for application

## Setting up env variables
There are 2 environmental variables, in order to set them you need to edit `docker-compose.yml` file.

`TOKEN` - huggingface token in order to use any LLM model provided by the inference api. Can be generated on huggingface.com in account settings.

`MODEL` - LLM model used. By default, it is `Llama-3.2-11B-Vision-Instruct`, which is relatively big and slow. You can experiment with different models. List of supported models - https://huggingface.co/models

## Running locally
To run this locally you need to have docker engine installed with docker compose.

command:
`docker compose up`

## Unit tests
Code is covered by unit tests.

command:
`docker compose run web python -m pytest`

