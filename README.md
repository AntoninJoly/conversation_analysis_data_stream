# Converstation analysis using Apache tools

Flowchart
![](./assets/flowchart.drawio.svg)

# Dataset 
In order to stream conversation to apache cluster, dataset taken from:
[Common sense dialogues](https://github.com/alexa/Commonsense-Dialogues)

# Conversation summarization 📤
In order to summarize conversation, an abstractive summarization method is considered since extractive summarization method might not be as accurate. 
In order to natively run this model on an Apache cluster, various steps need to be adressed.
1. Selection of model from HuggingFace.
-> Transformers from philschmid/bart-large-cnn-samsum transformer is considered.
- Issue: There is no TF implementation.
-> Need to fine-tune original model from facebook/bart-large-cnn on philschmid implementation dataset ([SAMsum](https://huggingface.co/datasets/samsum)).

# Summary classification 📰
TBD

# Apache cluster 📦
In order to launch the apache cluster, navigate to the docker folder and run the docker compose file.
```python
cd ./docker
docker-compose-up
```

# 

# Overview & example 📈


# To be done next 🛠
Following steps are considered:
[ ] Mobile app implementation
[ ] Model quantization
