'''
This program is the main function, which calls the components, and displays them in the html format
'''
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import datetime
# Components created
from modules.server import server
from modules.LumedReader import apiReader
from modules.LumedBlocks import BuilderDash, stetic
from modules.functions import *
from modules.configurations import configurationsTabs


components = configurationsTabs().components
menus=['Tweets','Palabras']
myReader = apiReader()
myDrawer = stetic()
myBuilder = BuilderDash()

buttons = []
for i,lista in enumerate(menus): 
    buttons.append(
        myBuilder.make_btn(title_k=lista,class_k=f'myBtn{i+1} mt-3',id_k=f'MyBtn{i+1}')
    )

app = dash.Dash(name='app_admi', server=server, url_base_pathname='/',external_stylesheets=[myDrawer.themes],assets_url_path = '..\assets')

app.layout= html.Div([

        # Component to detect the url
        dcc.Location(id='url', refresh=False),
        
        # Dashboard body
        dbc.Row([

            dbc.Col([# The elements of the card are placed that filters the content
                dbc.Card(
                    children=[
                            html.P('Filtrar', style=myDrawer.TitleTextCardFilterDate, className='mytitle texto'),
                            html.P('Fecha', style=myDrawer.TitleTextCardFilterDate, className='texto'),
                            myBuilder.makeDatePiker(id_k='my-date-picker-range',text='Fecha'),
                            dbc.Input(id="input-text", placeholder="Busca tu preferencia", type="text"),
                            myBuilder.make_btn(title_k='Buscar',class_k=f'myBtnBuscar mt-3',id_k=f'MyBtnBuscar'),
                            html.Div(
                                id='menusFilter', 
                                className='MenusFilter',
                                style = myDrawer.CardMenuFilter,
                                )
                    ],
                    style= myDrawer.CardMenuFilter,
                    color = myBuilder.getColor('light-blue'),
                    id = 'cardfilter',
                    className= 'CardFilter mb-2',),
                
                dbc.Card(
                    children=[
                            html.P('Exportar', style=myDrawer.TitleTextCardButtons, className='mytitle texto'),
                            html.Div(
                                id='downloadFiles', 
                                className='DownloadFiles',
                                style = myDrawer.CardMenuFilter,
                                children=buttons
                                )
                    ],
                    style= myDrawer.CardMenuFilter,
                    color = myBuilder.getColor('buttonCard'),
                    id = 'cardDfiles',
                    className= 'CardDFiles',),
                    ]),

            # Contains the tabs to select
            html.Div([
                dcc.Tabs(
                    id="tabs-styled-with-inline", 
                    value='tab-1', 
                    children=myDrawer.chooseTab(components=components),# contruye las pestañas con las opciones activas
                        ),

                ],
                # End of the tab to choose
                style=myDrawer.styleMainTab,
                id= 'tabstopics',
                className = "TabsTopics"),

            ],
            # End of Dashboard body
            id = 'body',
            className= 'Body',),

    ],
    # End of Dashboard
    id = 'mainContainer',
    className= 'MainContainer',
    style=myDrawer.mainContainer
    )


#daterange piker
@app.callback(
    myDrawer.chooseOutputs(components=components), # componente que despliega los datos
    [Input('my-date-picker-range', 'start_date'), # variables de entrada
     Input('my-date-picker-range', 'end_date'),
     Input("input-text","value"),
     Input('MyBtnBuscar',"n_clicks"),
     Input('url', 'pathname')],
     prevent_initial_call=True,)
def update_piker(start_date, end_date,value,n_clicks, pathname):
    '''
    This is the first input function, it is responsible for generating the information and consulting the data to be used in the rest of the program, 
    from two acquired dates, it generates a series of menus with the data extracted from the APIs, they are called in the function getData() linea 117
    '''
    try:
        mytabs=[]
        global df # contiene tanto los datos unicos por paciente como la tabla
        if value == None or n_clicks != 1: #posteriomente lo validamos
            n_clicks=None
            return tuple([[html.P(),dbc.Alert("No hay información por mostrar, completa el menú de filtros", color="primary")]])
        else:
            n_clicks=None
            # obtenemos las coordenadas dando pais
            #loc= myReader.getCoordinates(country=country)
            loc = '19.2538495, -99.6452721, 700km'
            df= myReader.getData(loc=loc, keyword=value, start=start_date, end=end_date)
            #salary,description= myReader.getApi(keyword=keyword,country=country)
            #data=[df,salary,keyword,description]
            
            
        
        ids=[v[1][1] for v in components.values()]
        for i in myDrawer.chooseOutputs(components=components):
            if i.component_id == ids[0]:
                mytabs.append(
                    getCard(
                        df=df
                        )
                )
            else:
                mytabs.append([html.P(),dbc.Alert("No hay información por mostrar, completa el menú de filtros", color="primary")])
        return tuple(mytabs)
    
    except Exception as ex:
        print(ex)
        return tuple([[html.P(),dbc.Alert("No hay información por mostrar, completa el menú de filtros", color="primary")]])


# Requests
@app.callback(
    Output("download"+'MyBtn1', "data"),
    dash.dependencies.Input("MyBtn1", "n_clicks"),
    prevent_initial_call=True,)
def funcRegistro(n_clicks):
    ''' This function detects when clicking, to activate the csv file download item '''
    file = dcc.send_data_frame(df[0][['content','sentimiento','seguridad']].to_excel, "tweets.csv")
    return file

# Requests
@app.callback(
    Output("download"+'MyBtn2', "data"),
    dash.dependencies.Input("MyBtn2", "n_clicks"),
    prevent_initial_call=True,)
def funcRegistro2(n_clicks):
    ''' This function detects when clicking, to activate the csv file download item '''
    file = dcc.send_data_frame(df[1].to_excel, "words.csv")
    return file