# Messaging Application converstation analysis

## Overview
Modern messaging applications generate massive amounts of data through user interactions. Analyzing this data can be challenging without the right tools. This project leverages Apache tools to gather messages from a messaging application, process them, and provide a summarized overview.
This project is designed to gather messages from a messaging application and summarize them using Apache tools. It aims to provide a convenient way to analyze and understand the content of the messages exchanged within the messaging application.

## How it Works
The project follows these general steps:

1. Message Gathering:
Connects to the messaging application using its API (if required).
Fetches the messages in the desired format.
Stores the messages in a Kafka topic.

2. Data Processing:
Apache Spark and Flink read messages from Kafka.
Applies data transformations and filters to clean and organize the data.
Stores processed data in Hadoop Distributed File System (HDFS) for further analysis.

3. Message Summarization:
Utilizes Apache HBase for storing aggregated data and summaries.
Performs word frequency analysis, sentiment analysis, and user-specific statistics.
Creates summarization reports.

4. Visualization:
Apache visualization tools (e.g., Apache Zeppelin) are used to generate graphical representations of the message data.

Flowchart
![](./assets/flowchart.drawio.svg)

## Dataset
In order to stream conversation to apache cluster, dataset taken from:
[Common sense dialogues](https://github.com/alexa/Commonsense-Dialogues)

# Conversation summarization 📤
In order to summarize conversation, an abstractive summarization method is considered since extractive summarization method might not be as accurate. 
In order to natively run this model on an Apache cluster, various steps need to be adressed.
1. Selection of model from HuggingFace.
-> Transformers from philschmid/bart-large-cnn-samsum transformer is considered.
- Issue: There is no TF implementation.
-> Need to fine-tune original model from facebook/bart-large-cnn on philschmid implementation dataset ([SAMsum](https://huggingface.co/datasets/samsum)).

## Summary classification 📰
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





Table of Contents
Introduction
Features
Requirements
Installation
Usage
How it Works
Contributing
License
Introduction


Features
Message Gathering: The project includes a script to gather messages from the messaging application, supporting popular messaging platforms.
Apache Tools Integration: It utilizes various Apache tools for data processing, analysis, and summarization.
Message Summarization: The messages are summarized based on various parameters like word frequency, sentiment analysis, or user-specific statistics.
Configurable: The project offers configurations for customization according to different messaging application formats.
Visualizations: It provides graphical representations of the message data using Apache visualization tools.

Requirements
Python 3.x
Apache Kafka
Apache Spark
Apache Hadoop
Apache Flink
Apache HBase
Apache ZooKeeper
Messaging Application API Credentials (if required by the messaging app)


## Installation
- Clone the repository to your local machine:

"""
bash
Copy code
git clone https://github.com/your-username/messaging-app-summarizer.git
cd messaging-app-summarizer
"""

- Install the required Python packages:
"""
Copy code
pip install -r requirements.txt
"""

- Install and configure Apache tools as per your operating system:

Apache Kafka Installation
Apache Spark Installation
Apache Hadoop Installation
Apache Flink Installation
Apache HBase Installation
Apache ZooKeeper Installation


## Usage
Configure Messaging Application API Credentials:
If your messaging application requires API credentials for accessing messages, make sure to provide them in the configuration file (e.g., config.yaml).

Start Apache Services:
Ensure all the necessary Apache services like Kafka, Spark, Hadoop, Flink, HBase, and ZooKeeper are up and running.

Gather Messages:
Execute the message gathering script:
"""
Copy code
python gather_messages.py
"""

Data Processing and Summarization:
Use Apache Spark and Flink for processing the gathered messages and creating summaries.

Visualization:
Utilize Apache visualization tools to generate graphs and charts for better insights.
