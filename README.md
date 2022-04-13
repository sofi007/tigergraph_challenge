# Drug and Disease Mining and Prediction (DDMP)

## Contributers and Contact Information: [Sofiane Lagraa, sofianelagraa87[at]gmail.com]

## Problem Statement addressed:

## Description:
Explain what your project is trying to accomplish 

### How is the graph technology utilized to achieve those goals?

Describe how your submission is relevant to the problem statement

### Why is it impactful to the world?

### Demo link: https://ddmp-tigergraph.herokuapp.com

### Video demo link: https://youtu.be/lLi82otLFlM

### How the entry was the most
#### Impactful in solving a real world problem


#### Innovative use case of graph


#### Ambitious and complex graph


#### Applicable graph solution

## Data : Give context for the dataset used and give full access to judges if publicly available or metadata otherwise.
## Technology Stack: Describe technologies and programming languages used.
## Visuals: Feel free to include other images or videos to better demonstrate your work.


# Dependencies

State any dependencies and their versions needed to be installed to test this project. This may include programming languages, frameworks, libraries, and etc.

# Installation

Please give detailed instructions on installing, configuring, and running the project so judges can fully replicate and assess it.

This can include:

    Clone repository
    Install dependencies
    Access data
    Steps to build/run project

# Known Issues and Future Improvements

Explain known liminations within the project and potential next steps.

# Reflections

Review the steps you took to create this project and the resources you were provided. Feel free to indiciate room for improvement and general reflections.

# References

Please give credit to other projects, videos, talks, people, and other sources that have inspired and influenced your project.

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

