# Client app of Drug and Disease Mining and Prediction (DDMP)

## About this app

This dashboard allows you to explore ...

## Requirements

* Python 3

## How to run this app

We suggest you to create a virtual environment for running this app with Python 3. Clone this repository 
and open your terminal/command prompt in the root folder.


In Unix system:
```
python3 -m venv ~/.virtualenvs/ddmp
source ~/.virtualenvs/ddmp/bin/activate

git clone https://github.com/sofi007/tigergraph_challenge/
cd tigergraph_challenge

pip3 install --upgrade pip
pip3 install -r requirements.txt

```

Install all required packages by running:
```
pip install -r Client/requirements.txt
```



Open Client/app.py and the TigerGraph creadentials:
```
conn = tg.TigerGraphConnection(host="put_your_address",
                               graphname="graph_drug_disease",
                               username="tigergraph",
                               password="tigergraph",
                               apiToken="put_your_apiToken")
```



Run this app locally with:
```
python app.py
```

## Screenshot

![screenshot](img/screencapture.png)

## Resources

* [Dash](https://dash.plot.ly/)

