# Server app of Drug and Disease Mining and Prediction (DDMP)

## About this app

This app is composed of a set of modules:
* Data processing module used for processing and cleaning the input data: codes/processing_precsciptor_drug.ipynb
* Graph database module used for creating the graph database using pyTigerGraph, a Python package for connecting to TigerGraph databases (https://github.com/pyTigerGraph/pyTigerGraph): codes/Tg_graph_database_creation.ipynb
* Graph queries module used for installing a set of GSQL queries including: simple queries for searching patterns: codes/install_search_patterns.ipynb
  * Install a set of GSQL queries from codes/queries folder: containing 30 queries.
* Graph Data science module for 
  * finding clusters of prescribers, drugs, diseases, and gene. The clustering algorithms uses random walks,  node2vec, KNN algorithms: codes/clustering.ipynb
  * Predicting drugs for a specific disease or diseases for a specific drug using the common neighbors algorithm: Predictions.ipynb.

## Requirements

* Python 3
* pyTigerGraph

## How to run this app

Install the classic Jupyter Notebook with:

```
pip install notebook
```
Just run 'jupyter notebook' command in the command prompt or Powershell and the jupyter environment will open up. Click on the kernel and click change kernel you will be able to see the kernel you just created.

In Graph database and Graph queries modules
you have to use your credentials for instantiate a connection to the graph database:
```
import pyTigerGraph as tg

conn = tg.TigerGraphConnection(host="http://127.0.0.1",graphname="graph_drug_disease", username="tigergraph", password="tigergraph",  apiToken="<PUT_YOUR_TOKEN_PROVIDED_BY_Tigergraph>")

```
