# Messaging application conversation analysis

# Overview
Modern messaging applications generate massive amounts of data through user interactions. Analyzing this data can be challenging without the right tools. This project leverages Apache tools to gather messages from a messaging application, process them, and provide a summarized overview. <br>
This project is designed to gather messages from a messaging application and summarize them using Apache tools. It aims to provide a convenient way to analyze and understand the content of the messages exchanged within the messaging application.

## How it Works
The project follows these general steps:

1. Message Gathering:
Stream local dataset to reprduce live behaviour. Stores the messages in a Kafka topic.

2. Data Processing:
Apache Spark read messages from Kafka to apply data transformations and filters to clean and organize the data.
Stores raw data in mongoDB and processed data in postgres DB for further analysis.

3. Message Summarization:
Utilizes transformer model to create summaries an classifier to assign a category to each conversation.

4. Visualization:
Apache Superset is used to generate graphical representations of the message data.

![](./assets/flowchart.drawio.svg)

# Conversation processing 📤

## Conversation summarization & classification
It uses capabilities of the SparkNLP library to provide real-time summarization and classification of user conversations.

## Dataset
In order to stream conversation to apache cluster, dataset taken from:
[Common sense dialogues](https://github.com/alexa/Commonsense-Dialogues)

# Installation

## Setup
- Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/conversation_analysis_data_stream.git
cd conversation_analysis_data_stream
```
- Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage
### Start Apache Services:
In order to launch the apache cluster, navigate to the docker folder and run the docker compose file. Ensure all the necessary Apache services like Kafka, Spark, and ZooKeeper are up and running.
```python
cd ./docker
docker-compose-up
```

### Start message streaming:
Execute the message gathering script in different prompt:
```python
cd ./src
python spark_datalake.py
```
```python
python spark_sentiment_analysis.py
```
```python
python data_source.py
```

# To be done next 🛠
Following steps are considered:
[] Monitoring & alert
[] Scaling
[] Security
[] BI
[] Rollback & backup
[] Unittest
