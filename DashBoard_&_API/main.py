from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import shap
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import base64
import joblib
import xgboost
import pandas as pd
from dash.dependencies import Input, Output, State
import numpy as np
from flask import Flask

mTest_model = joblib.load('data/mTest_model.pkl')
mTest_df = pd.read_csv('data/mTest_df.csv')
mTest_ID = pd.read_csv('data/mTest_ID.csv')
mTest_Info = pd.read_csv('data/mTest_info.csv')
mTest_Score = pd.read_csv('data/mTest_score.csv')

print(xgboost.__version__)
print("dash   ", dash.__version__)
print('html    ', html.__version__)
print('daq    ', daq.__version__)
print('dcc    ', dcc.__version__)
mTest_df_sample = mTest_df.head(50)
mTest_ID_sample = mTest_ID.head(50)
list_id = mTest_ID_sample['_ID_'].to_list()


def _finder_(value, str_col):
    _id_ = int(value)
    _row_data_ = mTest_Info.loc[mTest_Info['_ID_'] == _id_]
    _tst_1 = _row_data_[str_col]
    _tst_1 = _tst_1.to_list()
    _tst_1 = _tst_1[0]
    return _tst_1


def _finder_sc(value):
    _id_ = int(value)
    _row_data_ = mTest_Score.loc[mTest_Score['_ID_'] == _id_]
    _tst_1 = _row_data_["_pred_"]
    _tst_1 = _tst_1.to_list()
    _tst_1 = _tst_1[0]
    print('============')
    print(_tst_1)
    print('============')
    return _tst_1


# image_filename = '/Users/soso/Desktop/projet_7_dash/data/my_graph/Graph_100002.png'
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())
# _img_ = 'data:image/png;base64,{}'.format(encoded_image.decode())


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/",
        external_stylesheets=[dbc.themes.SLATE])


    dash_app.layout = html.Div([

        html.Div(html.H1('Home Credit DashBoard'),
                 style={'text-align': 'center',
                        'margin-right': '5vw',
                        'margin-bottom': '5vw',
                        'margin-top': '3vw',
                        'margin-left': '5vw'}),

        html.Div(html.H2("Selection de l'identifiant client : "),
                 style={'text-align': 'center'}),

        html.Div([
            dcc.Dropdown(

                id='list_id',
                options=[{'label': id_, 'value': id_} for id_ in list_id],
                style={'text-align': 'center', 'width': '50%', 'margin-right': '5vw', 'margin-left': '19vw',
                       'margin-bottom': '2vw','color': 'black'},
            ),

            daq.LEDDisplay(
                id='id_led',
                value=100001,
                color="#FFFFFF",
                backgroundColor="#373e45",
                size=30,
                style={'text-align': 'center'}
            ),
        ]),

        html.Div(children=[
            html.Div(children=[html.H2(' Sexe : ', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_sexe', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block', 'border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),

            html.Div(children=[html.H2('Statut professionnel : ', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_pro', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block','border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),

            html.Div(children=[html.H2('Niveau de diplome :', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_diplome', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block','border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),
        ],
            style={'text-align': 'center', 'margin-top': '3vw', 'margin-bottom': '2vw'}),

        html.Div(children=[
            html.Div(children=[html.H2('Statut matrimonial :', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_marie', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block','border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),

            html.Div(children=[html.H2('Type de credit :', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_ty_credit', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block','border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),

            html.Div(children=[html.H2('Secteur professionnel : ', style={'fontSize': 20,'marginTop': 20,'marginBottom': 20}),
                               html.H2(id='id_sec_pro', style={'fontSize': 30,'marginBottom': 20})],

                     style={'width': '20%', 'display': 'inline-block','border': '1px solid white',
                            'text-align': 'center', 'margin-left': '1vw','backgroundColor':'#373e45'}),
        ],
            style={'text-align': 'center', 'margin-top': '3vw', 'margin-bottom': '2vw'}),

        html.Div(children=[
            daq.LEDDisplay(id='led_age',
                           label= 'Age : ',
                           value=0,
                           backgroundColor="#373e45",
                           color="#FFFFFF",
                           size=50,
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
            daq.LEDDisplay(id='led_revenu',
                           label='Montant des revenus : ',
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
            daq.LEDDisplay(id='led_anc',
                           label= 'Ancienneté : ',
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),

            daq.LEDDisplay(id='led_enfant',
                           label="Nombre d'enfant :",
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
        ],
            style={'text-align': 'center', 'margin-top': '3vw', 'fontSize': 20}),
        html.Div(children=[
            daq.LEDDisplay(id='led_end',
                           label=" Endettement : ",
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
            daq.LEDDisplay(id='led_duree',
                           label="Durée du Credit : ",
                           value=0,
                           size=50,
                           color="#FFFFFF",
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
            daq.LEDDisplay(id='led_interet',
                           label="Interet annuel : ",
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),

            daq.LEDDisplay(id='led_mnt_credit',
                           label=" Montant du credit : ",
                           value=0,
                           color="#FFFFFF",
                           size=50,
                           backgroundColor="#373e45",
                           style={'display': 'inline-block', 'margin-left': '2vw', 'margin-right': '1vw'}),
        ],
            style={'text-align': 'center', 'margin-top': '3vw', 'fontSize': 20}),

        html.Div(
            children=html.Img(id="image",
                              src=0,
                              width=900,
                              height=600),
            style={
                'width': 905,
                'height': 605,
                'border': 'thin grey solid',
                'text-align': 'center',
                'margin-left': '27vw',
                'margin-right': '1vw',
                'margin-top': '2vw',
                'margin-bottom': '2vw'

            }
        ),

        html.Div(html.H2('Demande de credit : '),
                 style={'text-align': 'center', 'margin-top': '2vw'}),

        daq.Gauge(id='my-Gauge',
                  color={"gradient": True, "ranges": {"green": [0, 33], "yellow": [33, 66], "red": [66, 100]}},
                  value=50, label='', max=100, min=0,
                  scale={'start': 0, 'interval': 100, 'labelInterval': 100},
                  #theme=DarkThemeProvider,
                  style={'text-align': 'center',
                         'margin-top': '1vw',
                         'margin-left': '35vw',
                         'border': '5px solid white',
                         'backgroundColor':'#262b2f',
                         'width': '30%',}),

        html.Div(children=[html.H2('Status : ', style={'fontSize': 20, 'marginTop': 20, 'marginBottom': 20}),
                           html.H2(id='status', style={'fontSize': 30, 'marginBottom': 20, "color":'white'})],
                 style={'width': '30%',
                        'display': 'inline-block',
                        'border': '5px solid white',
                        'text-align': 'center',
                        'margin-left': '35vw',
                        'margin-bottom': '10vw'}),

    ])

    @dash_app.callback(Output('id_led', 'value'), [Input('list_id', 'value')])
    def update_output(value):
        if value is None:
            value = str(100002)
        else:
            value = str(value)
        return value

    def _callBack_string_(__id__, __col__, __val__):
        @dash_app.callback(Output(__id__, __val__), [Input('list_id', 'value')])
        def update_output(value):
            if value is None:
                value = str(100002)
            else:
                value = int(value)
            value_display = _finder_(value, __col__)
            return str(value_display)

    _callBack_string_('id_pro', "NAME_INCOME_TYPE", "children")
    _callBack_string_('id_sexe', "CODE_GENDER", "children")
    _callBack_string_('id_marie', "NAME_FAMILY_STATUS", "children")
    _callBack_string_('id_diplome', "NAME_EDUCATION_TYPE", "children")
    _callBack_string_('id_ty_credit', "NAME_CONTRACT_TYPE", "children")
    _callBack_string_('id_sec_pro', "ORGANIZATION_TYPE", "children")

    _callBack_string_('led_age', "DAYS_BIRTH", "value")
    _callBack_string_('led_revenu', "AMT_INCOME_TOTAL", "value")
    _callBack_string_('led_anc', "DAYS_EMPLOYED", "value")
    _callBack_string_('led_enfant', "CNT_CHILDREN", "value")

    _callBack_string_('led_end', "endettement", "value")
    _callBack_string_('led_duree', "_duree_credit_", "value")
    _callBack_string_('led_interet', "_%_interet", "value")
    _callBack_string_('led_mnt_credit', "AMT_CREDIT", "value")

    def _callBack_score_(__id__, __val__, state):
        @dash_app.callback(Output(__id__, __val__), [Input('list_id', 'value')])
        def update_output(value):
            if value is None:
                value = str(100002)
            else:
                value = int(value)
            value_display = _finder_sc(value)
            if state == 'score':
                value_display = value_display * 100
            else:
                if value_display > 0.5:
                    value_display = "Refus"
                else:
                    value_display = "Accord"

            return value_display

    _callBack_score_('my-Gauge', "value", "score")
    _callBack_score_('status', "children", "reponse")

    # Image________________

    @dash_app.callback(Output('image', "src"), [Input('list_id', 'value')])
    def update_output(value):
        if value is None:
            value = str(100002)
        else:
            value = str(value)
        image_filename = '/Users/soso/Desktop/projet_7_dash/data/my_graph/Graph_' + value + ".png"
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        _img_ = 'data:image/png;base64,{}'.format(encoded_image.decode())
        return _img_

    return dash_app.server


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    with app.app_context():
        app = init_dashboard(app)

        return app


app = init_app()
if __name__ == "__main__":
    app.run(host="127.0.0.1")
