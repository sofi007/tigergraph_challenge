import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction, State
from dash import dash_table
import pyTigerGraph as tg
import requests
import json
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = 'Drug & Disease Mining & Prediction'

server = app.server
app.config.suppress_callback_exceptions = True
# Please change the following parameters according to your creadentials.
conn = tg.TigerGraphConnection(host="http://127.0.0.1",
                               graphname="graph_drug_disease",
                               username="tigergraph",
                               password="tigergraph",
                               apiToken="2aa016d747ede9gg6da3drslm98srfoj")



# Path
#BASE_PATH = pathlib.Path(__file__).parent.resolve()
#DATA_PATH = BASE_PATH.joinpath("data").resolve()

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),'favicon.ico')


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("logo.png"),  style={'height':'100%'})],
        ),
        # top raw
        html.H4(className='search section', children='Search section'),
        html.Div(
            id='vp-control-tabs',
            #className="four columns",
            children=[
            dcc.Tabs(id='vp-tabs', value='what-is', children=[
                dcc.Tab(
                    label='Prescriber',
                    #value='what-is',
                    children=html.Div(className='control-tab-pres', children=[
                        # html.H4(className='prescriber', children='prescriber'),
                        html.Div(id='output-container-button-prescriber',
                                 children='Enter a prescriber and press submit'),
                        html.Div(dcc.Input(id='input-box-prescriber', type='text')),
                        html.Button('Submit', id='button-prescriber'),
                        html.Div(
                            id="right-column_prescriber",
                            #className="eight columns",
                            children=[
                                html.Div([
                                    html.Div([
                                        html.H3(children='Number of drugs'),
                                        html.Div(html.H3(id="nb_drugs_for_a_prescriber")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='five columns'),


                                ],
                                    className='row'),
                                ###########
                                html.Div([
                                    html.Div([
                                        html.B("Drugs"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_drugs_for_prescriber",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='five columns'),

                                ],
                                    className='row'),

                            ],
                        ),


                    ])
                ),
                dcc.Tab(
                    label='Drug',
                    #value='what-is',

                    children=html.Div(className='control-tab-drug', children=[
                        html.Div(id='output-container-button-drug',
                        children='Enter a drug and press submit'),
                        html.Div(dcc.Input(id='input-box-drug', type='text')),
                        html.Button('Submit', id='button-drug'),


                        #html.H4(className='drug', children='drug'),





                        html.Div(
                            id="right-column",
                            #className="eight columns",
                            children=[
                                html.Div([
                                    html.Div([
                                        html.H3(children='Number of prescribers'),
                                        html.Div(html.H3(id="nb_prescribers_for_a_drug")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.H3(children='Number of associated genes'),
                                        html.Div(html.H3(id="nb_genes_for_a_drug")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.H3(children='Number of tested diseases'),
                                        html.Div(html.H3(id="nb_tested_diseases_for_a_drug")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.H3(children='Number of used diseases'),
                                        html.Div(html.H3(id="nb_used_diseases_for_a_drug")),
                                    ], className='three columns'),
                                ],
                                    className='row'),
                                ###########
                                html.Div([
                                    html.Div([
                                        html.B("Prescriber"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat1",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.B("Gene"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat2",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.B("Disease in clinical trials"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat3",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.B("Disease"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat4",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                ],
                                    className='row'),

                                # Recommendation for diseases
                                html.Div(
                                    id="recommendation_for_diseases",
                                    children=[
                                        #html.B("Recommendation for diseases"),
                                        html.H3('Recommendation of diseases for the drug'),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat-rec-disease_for_drug",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             # filter_action='custom',
                                                             # filter_query=''
                                                             ),
                                        # dcc.Graph(id="patient_volume_hm"),
                                    ],
                                ),
                                # Recommendation for diseases based on genes

                            ],
                        ),

                    ]
                            ),

                    ),
                dcc.Tab(
                    label='Disease',
                    #value='what-is',
                    children=html.Div(className='control-tab-pres', children=[
                        # html.H4(className='disease', children='disease'),
                        html.Div(id='output-container-button-disease',
                                 children='Enter a disease and press submit'),
                        html.Div(dcc.Input(id='input-box-disease', type='text')),
                        html.Button('Submit', id='button-disease'),
                        html.Div(
                            id="right-column_disease",
                            #className="eight columns",
                            children=[
                                html.Div([
                                    html.Div([
                                        html.H3(children='Number of used drugs'),
                                        html.Div(html.H3(id="nb_drugs_for_a_disease")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.H3(children='Number of associated genes'),
                                        html.Div(html.H3(id="nb_genes_for_a_disease")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.H3(children='Number of tested drugs'),
                                        html.Div(html.H3(id="nb_tested_drugs_for_a_disease")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='three columns'),

                                ],
                                    className='row'),
                                ###########
                                html.Div([
                                    html.Div([
                                        html.B("Drugs"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_drugs_for_disease",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.B("Gene"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_gene_for_disease",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),
                                    html.Div([
                                        html.B("Tested drugs for disease"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_tested_drugs_for_disease",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='three columns'),

                                ],
                                    className='row'),

                                # Recommendation for diseases
                                html.Div(
                                    id="recommendation_for_drugs",
                                    children=[
                                        #html.B("Recommendation for diseases"),
                                        html.H3('Recommendation of drugs for the disease'),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat-rec-drug_for_disease",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             # filter_action='custom',
                                                             # filter_query=''
                                                             ),
                                        # dcc.Graph(id="patient_volume_hm"),
                                    ],
                                ),
                                # Recommendation for diseases based on genes

                            ],
                        ),



                    ]),
                ),
                dcc.Tab(
                    label='Gene',
                    #value='what-is',
                    children=html.Div(className='control-tab-pres', children=[
                        # html.H4(className='gene', children='gene'),
                        html.Div(id='output-container-button-gene',
                                 children='Enter a gene and press submit'),
                        html.Div(dcc.Input(id='input-box-gene', type='text')),
                        html.Button('Submit', id='button-gene'),
                        html.Div(
                            id="right-column_gene",
                            #className="eight columns",
                            children=[
                                html.Div([
                                    html.Div([
                                        html.H3(children='Number of drugs'),
                                        html.Div(html.H3(id="nb_drugs_for_a_gene")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='five columns'),
                                    html.Div([
                                        html.H3(children='Number of diseases'),
                                        html.Div(html.H3(id="nb_disease_for_a_gene")),
                                        # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                    ], className='five columns'),


                                ],
                                    className='row'),
                                ###########
                                html.Div([
                                    html.Div([
                                        html.B("Drugs"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_drugs_for_gene",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='five columns'),
                                    html.Div([
                                        html.B("Gene"),
                                        html.Hr(),
                                        dash_table.DataTable(id="tableStat_disease_for_gene",
                                                             page_current=0,
                                                             page_size=10,
                                                             style_cell={'textAlign': 'left'},
                                                             export_columns='visible',
                                                             export_format='csv',
                                                             filter_action='native'
                                                             #page_action='custom',
                                                             #sort_action='custom',
                                                             #sort_mode='multi',
                                                             #sort_by=[],
                                                             ),
                                    ], className='five columns'),


                                ],
                                    className='row'),

                            ],
                        ),


                    ])
                ),

                ]),
            ],
        ),

        html.H4(className='analytic section', children='Analytic section'),

        # bottom raw
        # Left column
        html.Div(
            id='vp-control-tabs2',
            # className="four columns",
            children=[
                dcc.Tabs(id='vp-tabs2', value='what-is', children=[
                    dcc.Tab(
                        label='Prescriber',
                        children=html.Div(className='control-tab-pres2', children=[
                            html.H4(className='prescribers', children='Statistics'),
                            html.Div(
                                id="stat-column_prescribers",
                                # className="eight columns",
                                children=[
                                    html.Div([
                                        html.Div([
                                            html.H3(children='Number of prescribers'),
                                            html.Div(html.H3(id="total_nb_prescribers")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        ], className='three columns'),

                                    ],
                                        className='row'),
                                    ###########

                                ],
                            ),


                            html.Button('Find clusters', id='button-prescriber2'),
                            html.Hr(),
                            dash_table.DataTable(id="table_cluster_prescriber",
                                                 page_current=0,
                                                 page_size=10,
                                                 # page_action='custom',
                                                 # sort_action='custom',
                                                 # sort_mode='multi',
                                                 # sort_by=[],
                                                 filter_action='native',
                                                 style_cell={'textAlign': 'left'},
                                                 export_columns='visible',
                                                 export_format='csv'
                                                 ),

                            # column: class id, instance count, grouped drugs, checked button (gene or gene and disease)

                            # recommend drug_x -> gene_a et disease_a

                        ])
                    ),

                    dcc.Tab(
                        label='Drug',
                        children=html.Div(className='control-tab-pres2', children=[
                            html.H4(className='drug', children='Statistics'),
                            html.Div(
                                id="stat-column",
                                # className="eight columns",
                                children=[
                                    html.Div([
                                        html.Div([
                                            html.H3(children='Number of drugs'),
                                            html.Div(html.H3(id="total_nb_drugs")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        ], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of used drugs by prescribers' ),
                                        #    html.Div(html.H3(id="total_nb_drugs_used_prescribers")),
                                        #], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of used drugs for diseases'),
                                        #    html.Div(html.H3(id="total_nb_drugs_used_diseases")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        #], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of associations drugs-genes'),
                                        #    html.Div(html.H3(id="total_nb_drugs_genes")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        #], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of used drugs for clinical trials'),
                                        #    html.Div(html.H3(id="total_nb_drugs_used_clinical_trials")),
                                        #], className='three columns'),
                                    ],
                                        className='row'),
                                    ###########


                                ],
                            ),

                            html.H4(className='drug', children='Clustering'),
                            dcc.RadioItems(
                               options=[
                                   {'label': 'Prescriber', 'value': 'prescriber'},
                                   {'label': 'Gene', 'value': 'gene'},
                                   {'label': 'Disease', 'value': 'disease'},
                                   {'label': 'Disease in clinical trials', 'value': 'disease_in_clinical_trial'},
                               ],
                                inline=True,
                                id='RadioItems_drug_section'
                            ),
                            html.Button('Find clusters', id='button-drug2'),
                            html.Hr(),
                            dash_table.DataTable(id="table_cluster_drugs",
                                                 page_current=0,
                                                 page_size=10,
                                                 #page_action='custom',
                                                 #sort_action='custom',
                                                 #sort_mode='multi',
                                                 #sort_by=[],
                                                 filter_action='native',
                                                 style_cell={'textAlign': 'left'},
                                                 export_columns='visible',
                                                 export_format='csv'
                                                 ),

                            # column: class id, instance count, grouped drugs, checked button (gene or gene and disease)

                            # recommend drug_x -> gene_a et disease_a




                        ])
                    ),

                    dcc.Tab(
                        label='Disease',
                        children=html.Div(className='control-tab-pres2', children=[
                            html.H4(className='disease', children='Statistics'),
                            html.Div(
                                id="stat-column-diseases",
                                # className="eight columns",
                                children=[
                                    html.Div([
                                        html.Div([
                                            html.H3(children='Number of diseases'),
                                            html.Div(html.H3(id="total_nb_diseases")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        ], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of diseases used by drugs'),
                                        #    html.Div(html.H3(id="total_nb_diseases_related_to_drugs")),
                                        #], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of diseases with genes'),
                                        #    html.Div(html.H3(id="total_nb_diseases_related_to_genes")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        #], className='three columns'),
                                    ],
                                        className='row'),
                                    ###########

                                ],
                            ),

                            html.H4(className='diseases', children='Clustering'),
                            dcc.RadioItems(
                                options=[
                                    {'label': 'Drugs', 'value': 'drug'},
                                    {'label': 'Genes', 'value': 'gene'},
                                ],
                                inline=True,
                                id="RadioItems_disease_section"
                            ),
                            html.Button('Find clusters', id='button-disease2'),
                            html.Hr(),
                            dash_table.DataTable(id="table_cluster_diseases",
                                                 page_current=0,
                                                 page_size=10,
                                                 # page_action='custom',
                                                 # sort_action='custom',
                                                 # sort_mode='multi',
                                                 # sort_by=[],
                                                 filter_action='native',
                                                 style_cell={'textAlign': 'left'},
                                                 export_columns='visible',
                                                 export_format='csv'
                                                 ),


                        ])

                    ),
                    dcc.Tab(
                        label='Gene',
                        # value='what-is',
                        children=html.Div(className='control-tab-pres2', children=[
                            html.H4(className='gene', children='Statistics'),
                            html.Div(
                                id="stat-column-genes",
                                # className="eight columns",
                                children=[
                                    html.Div([
                                        html.Div([
                                            html.H3(children='Number of genes'),
                                            html.Div(html.H3(id="total_nb_genes")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        ], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of genes related to drugs'),
                                        #    html.Div(html.H3(id="total_nb_genes_related_to_drugs")),
                                        #], className='three columns'),
                                        #html.Div([
                                        #    html.H3(children='Number of genes related to diseases'),
                                        #    html.Div(html.H3(id="total_nb_genes_related_to_diseases")),
                                            # dcc.Graph(                        id='graph1',                        figure=fig                    ),
                                        #], className='three columns'),
                                    ],
                                        className='row'),
                                    ###########


                                ],
                            ),

                            html.H4(className='genes', children='Clustering'),
                            dcc.RadioItems(
                               options=[
                                   {'label': 'Drugs', 'value': 'drug'},
                                   {'label': 'Diseases', 'value': 'disease'},
                               ],
                                inline=True,
                                id="RadioItems_gene_section"
                            ),
                            html.Button('Find clusters', id='button-gene2'),
                            html.Hr(),
                            dash_table.DataTable(id="table_cluster_genes",
                                                 page_current=0,
                                                 page_size=10,
                                                 # page_action='custom',
                                                 # sort_action='custom',
                                                 # sort_mode='multi',
                                                 # sort_by=[],
                                                 filter_action='native',
                                                 style_cell={'textAlign': 'left'},
                                                 export_columns='visible',
                                                 export_format='csv'
                                                 ),

                            # column: class id, instance count, grouped drugs, checked button (gene or gene and disease)

                            # recommend drug_x -> gene_a et disease_a




                        ])
                    ),

                ]),
            ],
        ),


    ],

)



def getClustering_results(node, type_node, relation_node):

    df = pd.read_csv("server/results/knn_results/knn_"+node+"_related_to_"+relation_node+".csv", names=[type_node, "Similar "+type_node], sep=" ", header=None)
    #print(len(df))
    columns = [{"name": i, "id": i} for i in df.columns]
    if(node == "prescriber"):
        data = df[:500].to_dict('records')
    else:
        data = df.to_dict('records')
    return columns, data



#def getResults(mylist, colname):
def getResults(filename, colname):
    mylist = []
    with open(filename) as f:
        mylist = f.readlines()
    for elem in mylist:
        if ("\n" == elem):
            mylist.remove("\n")



    data = pd.DataFrame(mylist, columns=[colname])
    columns = [{"name": i, "id": i} for i in data.columns]
    size = len(data)
    if(len(data) > 1000):
        data = data[:1000].to_dict('records')
    else:
        data = data.to_dict('records')

    return columns, data, size

def getResultsFromDF(filename, type_node):
    df = pd.read_csv(filename, names=[type_node, "Score (Common genes)"], header=None)
    columns = [{"name": i, "id": i} for i in df[[type_node, "Score (Common genes)"]].columns]

    data = df.to_dict('records')
    return columns, data

def init_columns_data():
    data = pd.DataFrame()
    columns = [{"name": i, "id": i} for i in data.columns]
    data = data.to_dict('records')
    nb = ""
    return columns, data, nb

@app.callback(
    [

        Output("tableStat1", "columns"),
        Output("tableStat1", "data"),
        Output("nb_prescribers_for_a_drug", "children"),

        Output("tableStat2", "columns"),
        Output("tableStat2", "data"),
        Output("nb_genes_for_a_drug", "children"),

        Output("tableStat3", "columns"),
        Output("tableStat3", "data"),
        Output("nb_tested_diseases_for_a_drug", "children"),

        Output("tableStat4", "columns"),
        Output("tableStat4", "data"),
        Output("nb_used_diseases_for_a_drug", "children"),
        Output("tableStat-rec-disease_for_drug", "columns"),
        Output("tableStat-rec-disease_for_drug", "data"),



    ],
    [
        Input('button-drug', 'n_clicks')
    ],
    [
        State('input-box-drug', 'value')

    ])
def query_stat_table_drugs(n_clicks_drug, value_drug):
    columns_prescribers, data_prescribers, nb_prescribers_for_drug = init_columns_data()
    columns_genes, data_genes, nb_genes_for_a_drug = init_columns_data()
    columns_tested_disease, data_tested_disease, nb_tested_diseases_for_a_drug = init_columns_data()
    columns_used_diseases, data_used_diseases, nb_used_diseases_for_a_drug = init_columns_data()
    column_recom_disease_for_drug, data_recom_disease_for_drug, nb= init_columns_data()
    # search
    if (n_clicks_drug != None and value_drug != ''):

         columns_prescribers, data_prescribers, nb_prescribers_for_drug = getResults("server/results/search_results/drugs/"+value_drug+"/getPRESCRIBER_for_drug.txt", "Prescribers")

         columns_genes, data_genes, nb_genes_for_a_drug = getResults("server/results/search_results/drugs/"+value_drug+"/getGENES_for_drug.txt","GENES")

         columns_tested_disease, data_tested_disease, nb_tested_diseases_for_a_drug = getResults("server/results/search_results/drugs/"+value_drug+"/get_tested_DISEASES_for_drug.txt","Tested Diseases")

         columns_used_diseases, data_used_diseases, nb_used_diseases_for_a_drug = getResults("server/results/search_results/drugs/"+value_drug+"/getDISEASES_of_drug.txt","Used Diseases")

         file = "server/results/predictions/drugs/"+value_drug+"/predictions.txt"
         #df = pd.read_csv(file, header=None)
         #print(df[[1,2]])
         column_recom_disease_for_drug, data_recom_disease_for_drug = getResultsFromDF(file, "Disease")




    return columns_prescribers, data_prescribers, nb_prescribers_for_drug,\
           columns_genes, data_genes, nb_genes_for_a_drug,\
           columns_tested_disease, data_tested_disease, nb_tested_diseases_for_a_drug,\
           columns_used_diseases, data_used_diseases, nb_used_diseases_for_a_drug,\
           column_recom_disease_for_drug, data_recom_disease_for_drug


@app.callback(
    [

        Output("tableStat_drugs_for_disease", "columns"),
        Output("tableStat_drugs_for_disease", "data"),
        Output("nb_drugs_for_a_disease", "children"),

        Output("tableStat_gene_for_disease", "columns"),
        Output("tableStat_gene_for_disease", "data"),
        Output("nb_genes_for_a_disease", "children"),

        Output("tableStat_tested_drugs_for_disease", "columns"),
        Output("tableStat_tested_drugs_for_disease", "data"),
        Output("nb_tested_drugs_for_a_disease", "children"),

        Output("tableStat-rec-drug_for_disease", "columns"),
        Output("tableStat-rec-drug_for_disease", "data"),

    ],
    [
        Input('button-disease', 'n_clicks')
    ],
    [
        State('input-box-disease', 'value')

    ])
def query_stat_table_disease(n_clicks_disease, value_disease):

    columns_genes, data_genes, nb_genes_for_a_disease = init_columns_data()
    columns_tested_drugs, data_tested_drugs, nb_tested_drugs_for_a_disease = init_columns_data()
    columns_used_drugs, data_used_drugs, nb_used_drugs_for_a_disease = init_columns_data()
    column_recom_drug_for_disease, data_recom_drug_for_disease, nb_recom_drug_for_disease = init_columns_data()

    # search
    if (n_clicks_disease != None and value_disease != ''):

         columns_genes, data_genes, nb_genes_for_a_disease  = getResults("server/results/search_results/diseases/"+value_disease+"/get_GENES_for_disease.txt","GENES")

         columns_tested_drugs, data_tested_drugs, nb_tested_drugs_for_a_disease = getResults("server/results/search_results/diseases/"+value_disease+"/get_tested_DRUGS_for_disease.txt","Tested Drugs")

         columns_used_drugs, data_used_drugs, nb_used_drugs_for_a_disease = getResults("server/results/search_results/diseases/"+value_disease+"/getDRUGS_for_disease.txt","Used Drugs")

         file = "server/results/predictions/diseases/"+value_disease+"/predictions.txt"
         column_recom_drug_for_disease, data_recom_drug_for_disease = getResultsFromDF(file, "Drug")




    return columns_used_drugs, data_used_drugs, nb_used_drugs_for_a_disease,\
           columns_genes, data_genes, nb_genes_for_a_disease,\
           columns_tested_drugs, data_tested_drugs, nb_tested_drugs_for_a_disease,\
           column_recom_drug_for_disease, data_recom_drug_for_disease


@app.callback(
    [

        Output("tableStat_drugs_for_gene", "columns"),
        Output("tableStat_drugs_for_gene", "data"),
        Output("nb_drugs_for_a_gene", "children"),

        Output("tableStat_disease_for_gene", "columns"),
        Output("tableStat_disease_for_gene", "data"),
        Output("nb_disease_for_a_gene", "children"),


    ],
    [
        Input('button-gene', 'n_clicks')
    ],
    [
        State('input-box-gene', 'value')

    ])
def query_stat_table_gene(n_clicks_gene, value_gene):


    columns_drugs, data_drugs, nb_drugs_for_a_gene = init_columns_data()
    columns_diseases, data_diseases, nb_diseases_for_a_gene = init_columns_data()

    # search
    if (n_clicks_gene != None and value_gene != ''):

         columns_drugs, data_drugs, nb_drugs_for_a_gene  = getResults("server/results/search_results/genes/"+value_gene+"/get_DRUGS_for_GENE.txt","Drugs")

         columns_diseases, data_diseases, nb_diseases_for_a_gene = getResults("server/results/search_results/genes/"+value_gene+"/get_DISEASES_for_GENE.txt","Diseases")






    return columns_drugs, data_drugs, nb_drugs_for_a_gene,\
           columns_diseases, data_diseases, nb_diseases_for_a_gene


@app.callback(
    [

        Output("tableStat_drugs_for_prescriber", "columns"),
        Output("tableStat_drugs_for_prescriber", "data"),
        Output("nb_drugs_for_a_prescriber", "children"),



    ],
    [
        Input('button-prescriber', 'n_clicks')
    ],
    [
        State('input-box-prescriber', 'value')

    ])
def query_stat_table_gene(n_clicks_prescriber, value_prescriber):


    columns_drugs, data_drugs, nb_drugs_for_a_prescriber = init_columns_data()


    # search
    if (n_clicks_prescriber != None and value_prescriber != ''):

         columns_drugs, data_drugs, nb_drugs_for_a_prescriber  = getResults("server/results/search_results/prescribers/getDRUGS_for_PRESCRIBER.txt","Drugs")




    return columns_drugs, data_drugs, nb_drugs_for_a_prescriber






##################################### Analytics section ####################







@app.callback(
    [
        Output("total_nb_drugs", "children"),
        #Output("total_nb_drugs_used_prescribers", "children"),
        #Output("total_nb_drugs_used_diseases", "children"),
        #Output("total_nb_drugs_genes", "children"),
        #Output("total_nb_drugs_used_clinical_trials", "children"),

        Output("table_cluster_drugs", "columns"),
        Output("table_cluster_drugs", "data"),



    ],
    [
        Input('button-drug2', 'n_clicks')

    ],
    [
        State('RadioItems_drug_section', 'value')
    ])
def analytic_section(n_clicks_drug, value_RadioItems_drug_section):
    #columns_clustering_drugs = {}
    data_clustering_drugs = pd.DataFrame()
    columns_clustering_drugs = [{"name": i, "id": i} for i in data_clustering_drugs.columns]
    data_clustering_drugs = data_clustering_drugs.to_dict('records')


    if (n_clicks_drug != None and value_RadioItems_drug_section != ''):
        if(value_RadioItems_drug_section == "disease_in_clinical_trial"):
            columns_clustering_drugs, data_clustering_drugs = getClustering_results("drug","Drug", "clinical_trials")

        if (value_RadioItems_drug_section == "disease"):
            columns_clustering_drugs, data_clustering_drugs = getClustering_results("drug","Drug", "disease")

        if (value_RadioItems_drug_section == "gene"):
            columns_clustering_drugs, data_clustering_drugs = getClustering_results("drug","Drug", "drug_gene")

        if (value_RadioItems_drug_section == "prescriber"):
            columns_clustering_drugs, data_clustering_drugs = getClustering_results("drug","Drug", "prescriber")

    dict_metrics = read_computed_metrics("server/results/metrics.txt")
    return dict_metrics['getDRUGS_size'], \
           columns_clustering_drugs, \
           data_clustering_drugs

'''
    return dict_metrics['getDRUGS_size'],\
           dict_metrics['getDRUGS_PESCRIBERS_size'],\
           dict_metrics['getDRUGS_DISEASES_size'],\
           dict_metrics['getDRUGS_GENES_size'],\
           dict_metrics['getDRUGS_TestedDISEASES_size'],\
           columns_clustering_drugs,\
           data_clustering_drugs
'''


@app.callback(
    [
        Output("total_nb_prescribers", "children"),
        Output("table_cluster_prescriber", "columns"),
        Output("table_cluster_prescriber", "data"),
    ],
    [
        Input('button-prescriber2', 'n_clicks')

    ])
def analytic_section_prescriber(n_clicks_prescriber):
    data_clustering_prescriber = pd.DataFrame()
    columns_clustering_prescriber = [{"name": i, "id": i} for i in data_clustering_prescriber.columns]
    data_clustering_prescriber = data_clustering_prescriber.to_dict('records')
    if (n_clicks_prescriber != None):
        columns_clustering_prescriber, data_clustering_prescriber = getClustering_results("prescriber", "Prescriber", "drug")

    dict_metrics = read_computed_metrics("server/results/metrics.txt")

    return dict_metrics['getPRESCRIBER_size'], columns_clustering_prescriber, data_clustering_prescriber


@app.callback(
    [
        Output("total_nb_genes", "children"),
        #Output("total_nb_genes_related_to_drugs", "children"),
        #Output("total_nb_genes_related_to_diseases", "children"),
        Output("table_cluster_genes", "columns"),
        Output("table_cluster_genes", "data"),
    ],
    [
        Input('button-gene2', 'n_clicks')

    ],
    [
        State('RadioItems_gene_section', 'value')
    ])
def analytic_section_gene(n_clicks_gene, value_RadioItems_gene_section):
    data_clustering_gene = pd.DataFrame()
    columns_clustering_gene = [{"name": i, "id": i} for i in data_clustering_gene.columns]
    data_clustering_gene = data_clustering_gene.to_dict('records')

    if (n_clicks_gene != None and value_RadioItems_gene_section != ''):
        if (value_RadioItems_gene_section == "drug"):
            columns_clustering_gene, data_clustering_gene = getClustering_results("gene", "Gene", "drug")
        if (value_RadioItems_gene_section == "disease"):
            columns_clustering_gene, data_clustering_gene = getClustering_results("gene", "Gene", "disease")

    dict_metrics = read_computed_metrics("server/results/metrics.txt")

    return dict_metrics['getGENES_size'],\
           columns_clustering_gene,\
           data_clustering_gene




@app.callback(
    [
        Output("total_nb_diseases", "children"),
        #Output("total_nb_diseases_related_to_drugs", "children"),
        #Output("total_nb_diseases_related_to_genes", "children"),
        Output("table_cluster_diseases", "columns"),
        Output("table_cluster_diseases", "data"),
    ],
    [
        Input('button-disease2', 'n_clicks')

    ],
    [
        State('RadioItems_disease_section', 'value')
    ])
def analytic_section_disease(n_clicks_disease, value_RadioItems_disease_section):
    data_clustering_disease = pd.DataFrame()
    columns_clustering_disease = [{"name": i, "id": i} for i in data_clustering_disease.columns]
    data_clustering_disease = data_clustering_disease.to_dict('records')

    if (n_clicks_disease != None and value_RadioItems_disease_section != ''):
        if (value_RadioItems_disease_section == "drug"):
            columns_clustering_disease, data_clustering_disease = getClustering_results("disease", "Disease", "drug")
        if (value_RadioItems_disease_section == "gene"):
            columns_clustering_disease, data_clustering_disease = getClustering_results("disease", "Disease", "gene")

    dict_metrics = read_computed_metrics("server/results/metrics.txt")

    return dict_metrics['getDISEASES_size'],\
           columns_clustering_disease,\
           data_clustering_disease



# TODO: graph cytoscape + table contenant les infortmations sur les voisiss: pour un gene:#nb diseases, drugs,
# Drug: graph cytoscape + table cotentnat les info voisiss stat + recommendations avec les clinaical trials.
    # dans le meme tab: ajouter un button liste des recommendations avec les essais cliniques
    # stat: pour un drug: afficher # prescpotr (and %), # gene (%), # disease (%), and # tested in clinical trial, and # of disease(clincal trail)
        # tableau lister: prescpotr, gene, disaese, disease(clinal)
    # cluster of drugs sharing the same disease, (+ clinical), same gene,
    # clusters of drugs sharing the gene and diseases
    # clusters of drugs from exsting diseases compared with clinical trials (two lables).
    # node2vec: dru, disease, clincal trial: label: drug(used in disease, used in clincal trial, used both)
        # ou extraire les stats suivantes: drugs: utilisés dans le traitement des maladies,
            # drugs utilise dans clinical trials
            # drugs utilisé dans les deux.
            # pattern: drug->gene->disease: recommendation de noueavu lien
# Prescpotr: cluster of preptors (same drugs), suggestions of drugs (presptor-drugs), suggestions of drugs based on clinical trials.
# clusters table: class_name, instance_count, diseases| drugs|Gene un autre table: disease & gene



def read_computed_metrics(filename):
    dict_metrics = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            metric = line.split(" ")
            dict_metrics[metric[0]] = metric[1]

    return dict_metrics


def results_from_json2(json_results):
    list_of_nodes = []
    size_object = json.loads(json_results)
    results = size_object['results'][0]
    for v in results['VertexSet_2']:
        list_of_nodes.append(v['v_id'])
    return list_of_nodes

# Run the server
if __name__ == "__main__":
    #read_computed_metrics("../server/results/metrics.txt")
    #read_computed_metrics("server/results/metrics.txt")





    app.run_server(debug=False)
