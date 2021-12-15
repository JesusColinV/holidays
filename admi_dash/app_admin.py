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
menus=['Registro']
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
     Input('url', 'pathname')])
def update_piker(start_date, end_date, pathname):
    '''
    This is the first input function, it is responsible for generating the information and consulting the data to be used in the rest of the program, 
    from two acquired dates, it generates a series of menus with the data extracted from the APIs, they are called in the function getData() linea 117
    '''
    try:
        global data # contiene tanto los datos unicos por paciente como la tabla
        if pathname != '/': #posteriomente lo validamos
            country=pathname.split('/')[-2]
            keyword=pathname.split('/')[-1]
            # obtenemos las coordenadas dando pais
            loc= myReader.getCoordinates(country=country)
            df= myReader.getData(loc=loc, keyword=keyword, start=start_date, end=end_date)
            salary,description= myReader.getApi(keyword=keyword,country=country)
            data=[df,salary,keyword,description]
        else:
            data=[[],[],[],[]]
            
        mytabs=[]
        ids=[v[1][1] for v in components.values()]
        for i in myDrawer.chooseOutputs(components=components):
            if i.component_id == ids[0]:
                mytabs.append(
                    getCard(
                        data=data
                        )
                )
            else:
                mytabs.append([html.P(),dbc.Alert("No hay información por mostrar, completa el menú de filtros", color="primary")])
        return tuple(mytabs)
    
    except Exception as ex:
        print(ex)


# Requests
@app.callback(
    Output("download"+'MyBtn1', "data"),
    dash.dependencies.Input("MyBtn1", "n_clicks"),
    prevent_initial_call=True,)
def funcPatient(n_clicks):
    ''' This function detects when clicking, to activate the csv file download item '''
    file = dcc.send_data_frame(data[1].to_excel, "Datoss.csv")
    return file
