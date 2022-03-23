# Data Extraction -- Youtube Music
### Author: Jayden Lee


This repository utilizes `ytmusic` [open-source library](https://ytmusicapi.readthedocs.io/en/latest/index.html) that facilitates accessibility into Youtube Music API using user credentials. With extracted data, the codebase starts [Postgres docker container](https://hub.docker.com/_/postgres), loads and stores them in structured, or relational, format.

This repository also utilizes DAG scheduler available from Apache `airflow` [open-source project](https://airflow.apache.org/) to run above tasks in scheduled manner. 

#### Caveat -- Several configurations in the scripts are either left empty, or set to values for the author's personal usage. Be sure to adjust those configurations based on your purpose
