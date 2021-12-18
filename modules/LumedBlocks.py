import datetime
#from modules.components import makeMenus
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from numpy import character, show_config
import plotly.express as px
import pandas as pd
# components maked
#from modules.dataframes import info_df
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from plotly.offline import plot
import random
import plotly
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class BuilderDash():
    def __init__(self):
        self.start=datetime.date.today()-datetime.timedelta(days=700)
        self.end=datetime.date.today()
        self.id_medico='3648bf49-a2a4-43ff-acbb-95c8ea878479'
        self.searchType=2
        self.myDrawer=stetic()
        

    def getColor(self,color):
        '''
        This function receives a string color and returns the #hex setting of the color
        Input:
            color: is the written color
        Output: 
            colors [f '{color}'] is the dictionary response

        '''
        colors = {'white': '#FFFFFF', 'sky-blue': '#00b3dc', 'green': '#82c341','strong-blue': '#003963', 'black': '#000000', 'dark-blue':'#00111e',
                'turquoise': '#4c7492', 'king-blue': '#002845','gray':'#ccd8e0','light-blue':'#e5f8fc','bright-blue':'#4cf8fc','gray-blue':'#6688a2',
                'bg':'#e5ebf0','buttonCard':'#f3f9ec'}
        return colors[f'{color}']
    

    def make_btn(self,**kwargs):
        '''
        This function creates the button component, with its document download function
        Input:
            title_k: The title for the button
            class_k: The name of the class
            id_k: the identifier of the button
            Note: The unloading component is not modularized
        Output:
            button
            download function
        '''
        # element that displays the download button  it's callback
        btn_csv = html.Div(
                            [
                                dbc.Button(kwargs['title_k'], outline=True, color="success", className=kwargs['class_k'],id=kwargs['id_k'],
                                        style=self.myDrawer.stylebutton),
                                dcc.Download(id="download"+kwargs['id_k'])
                            ]
        )
        return btn_csv

    def make_nav(self,**kwargs):
        '''
        This function creates the graying of the dashboard
        Input:
            title_k: dashboard title
            class_k: class name
        '''
        myNav = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src='', height="30px")),
                                dbc.Col(dbc.NavbarBrand(kwargs['title_k'], 
                                className=kwargs['class_k'], 
                                style=self.myDrawer.stylenav)),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href=kwargs['link_k'],
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2"),
                ]
            ),
            self.getColor('sky-blue'),
            dark=True,
            className=kwargs['title_K'],)
        return myNav

    def makeDatePiker(self,**kwargs):
        '''
        This function creates the datepiker
        Input:
            id_k: Identifier for the element
        '''
        filterDate=html.Div([
                dcc.DatePickerRange(
                    id=kwargs['id_k'],
                    start_date=self.start,
                    end_date=self.end,
                    style= {'padding': '10px','text-align': 'center'},
                ),
            ])
        return filterDate
    
    def makeTable(self,**kwargs):
        '''
        This function creates the table with the content of the dataframe, it is invoked by the main program for the table tab
        Input:
            df: Filtered Dataframe
            class_k: Name of the inner class
            class_K: Name of the outer class
            id_K: identificador d ela table
        Output:
            TableToday: Table with content
        '''
        try:
            kwargs['df']=kwargs['df'].replace({'Videoconferencia':'Video','Exploración a distancia':'Exploración','Consulta Presencial':'Presencial'})
        except Exception as e:
            print(e)

        king=self.getColor('king-blue')
        gray=self.getColor('gray')
        tableToday = html.Div([
        dbc.Row([
                dbc.Col(dbc.Card([
                dash_table.DataTable(
                    id=kwargs['id_k'],
                    columns=[
                        {'name': i, 'id': i, 'deletable': False} for i in kwargs['df'].columns
                        # omit the id column
                        if i != 'id'
                    ],
                    style_as_list_view=False,
                    style_cell={'padding': '5px'},
                    style_header={
                        'backgroundColor': king,
                        'fontWeight': 'bold',
                        'text-align': 'center',
                    },
                    style_data_conditional=[
                            {
                                'backgroundColor': gray,
                                'color': king,
                                'fontWeight': 'bold',
                                'text-align': 'center',
                            }
                        ],
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode='multi',
                    #row_selectable='multi',
                    #row_deletable=True,
                    selected_rows=[],
                    page_action='native',
                    page_current=0,
                    page_size=20,
                    data=kwargs['df'].to_dict('records'),),
                    ], 
                inverse=True),),
            ],className=kwargs['class_k'],),
        ], className=kwargs['class_K'])
        return tableToday

    def makeMenu(self,**kwargs):
        '''
        This function creates the menus, with which the filter selection is made
        Input:
            df: Dataframe with the information between two dates
            column_k = column with the characteristic to select the filter
        Output:
            dropDown: Menu
        '''
        data=kwargs['df']
        characteristic= kwargs['column_k']
        dropDown = dcc.Dropdown(
            options=[
                {'label': i, 'value': i} for i in set(data[f'{characteristic}'])
            ],
            #value=list(set(data[f'{characteristic}'])),
            value=[],
            multi=True,
            placeholder=f"Elige una {characteristic}",
            id=f"id_dd{characteristic}",
            style=self.myDrawer.styleMenu,
        )
        return dropDown


    def makeGraph(self, **kwargs):
        '''
        This function allows you to plot the data
        Input:
            df a dataframe that already contains the sum of the characteristics
            x: column x study characteristic
            y: column and value of the sum of queries
            id_k: internal identifier name
            id_K: external identifier name
            type: type of chart
        Output:
            myGraph: It is the cited graph with the entries
        '''
         
        try:
            if kwargs['type'] == 'pie':
                dataTable=kwargs['df'].groupby([kwargs['x']]).size().reset_index(name=kwargs['y'])
                fig=px.pie(dataTable,values=kwargs['y'], names=kwargs['x'], title='Analisis de comentarios')
                fig.update_traces(textposition='inside', textfont_size=14)
            elif kwargs['type'] == 'treemap': # This function is not universal
                fig = px.treemap(kwargs['df'], path=[kwargs['x']], values=kwargs['y'])
                fig.update_traces(textinfo = 'label + value'),
            elif kwargs['type'] == 'line':
                df_line=self.addTimeSeries(df=kwargs['df'])
                # desplegar las fechas seleccionadas
                fig = px.line(df_line, x=kwargs['x'], y=kwargs['y'])
            elif kwargs['type'] == 'cloudword':
                texto=''
                #for tabla in kwargs['dataTable']['sugerencia']:
                #    texto=texto+tabla
                # create a mask based on the image we wish to include
                #my_mask = np.array(Image.open('https://media-public.canva.com/GTvSs/MAEICXGTvSs/1/s.png'))
                # create a wordcloud 
                words =  kwargs['df']['palabra'].tolist()
                frequency = kwargs['df']['frecuencia'].tolist()
                lower, upper = 15, 45
                try:
                    frequency = [((x - min(frequency)) / (max(frequency) - min(frequency))) * (upper - lower) + lower for x in frequency]
                except:
                    frequency=0


                #percent = [0.362086258776329, 0.13139418254764293, 0.11802072885322636, 0.055834169174189235, 0.041123370110330994, 0.03978602474088933, 0.02774991641591441, 0.02139752591106653, 0.01905717151454363, 0.015379471748579069, 0.01471079906385824, 0.013373453694416584, 0.012370444667335341, 0.010364426613172852, 0.009695753928452023, 0.009695753928452023, 0.009361417586091608, 0.008692744901370779, 0.008358408559010365, 0.0076897358742895345, 0.0076897358742895345, 0.00735539953192912, 0.007021063189568706, 0.006352390504847877, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.0056837178201270475, 0.005015045135406218, 0.005015045135406218, 0.005015045135406218, 0.005015045135406218, 0.004680708793045804, 0.004680708793045804, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.004012036108324975, 0.004012036108324975, 0.00367769976596456, 0.00367769976596456, 0.00367769976596456, 0.00367769976596456, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146]

                lenth = len(words)
                colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]

                data = go.Scatter(
                x=list(range(lenth)),
                y=random.choices(range(lenth), k=lenth),
                mode='text',
                text=words,
                hovertext=['{0}{1}'.format(w, f) for w, f in zip(words, frequency)],
                hoverinfo='text',
                textfont={'size': frequency, 'color': colors})
                layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})

                fig = go.Figure(data=[data], layout=layout)
                
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            myGraph=dcc.Graph(
                id=f"{kwargs['id_k']}",
                figure= fig.update_layout(
                            title = f"{kwargs['x']}" ,
                            plot_bgcolor = self.getColor('white'),
                            paper_bgcolor = self.getColor('white'),
                            font_color = self.getColor('strong-blue'),

                            title_font_color = self.getColor('strong-blue'),
                            title_font_family = "Old Standard TT",
                            xaxis={'title':f"{kwargs['x']}"},
                            yaxis={'title':'Registros'},
                ),
                style = self.myDrawer.styleGraphData
            )
        except Exception as ex:
            myGraph=dcc.Graph()
        return myGraph

    def makeTopCard(self,**kwargs):
        '''
        This function is the creator of the header of the cards
        Input:
            text_k: text to display
            value_k: variable to display
        Output:
            card_content: It is the card at the top of the dashboard
        '''
        card_content = [
            dbc.CardHeader(
            [html.H4(f"{kwargs['text_k']}"),
            html.P(f"{kwargs['value_k']}")],
            style={'boxShadow': '0 0 14px 0 rgba(0, 0, 0, 0.2)','text-align': 'center'},
            className="card-text"),
        ]
        return card_content

    def GphCards(self,**kwargs):
        '''
        This function allows you to create graphs on cards that show the interaction with the filters, to work it requires
        call the graphing functions at each position
        Input: 
            pos11: makeTopCard Medico más activo
            pos12: makeTopCard Tipo de cita más solicitada
            pos13: makeTopCard Numero total de citas
        Output:
            cards
        '''
        cards = html.Div(
            [
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(kwargs['pos11'], color=self.getColor('dark-blue'), inverse=True)),
                        dbc.Col(dbc.Card(kwargs['pos12'], color=self.getColor('dark-blue'), inverse=True)),
                        dbc.Col(dbc.Card(kwargs['pos13'], color=self.getColor('dark-blue'), inverse=True)),
                    ],
                    className=f"{kwargs['id_k']}",
                ),
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(kwargs['pos21'], inverse=True)),

                    ],className=f"{kwargs['id_k']}",),
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(kwargs['pos31']),
                    ],className=f"{kwargs['id_k']}",),
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(kwargs['pos41']),
                    ],className=f"{kwargs['id_k']}",),
            ], className=f"{kwargs['class_k']}", id=f"{kwargs['id_K']}"
        )
        return cards
    
    def addTimeSeries(self,**kwargs):
        '''
        start_date
        end_date
        df
        '''
        # generar un vector de fechas vacio
        df_line=pd.DataFrame([i.date() for i in pd.date_range(start=kwargs['df']['Citas por Fecha'].min(),end=kwargs['df']['Citas por Fecha'].max())],columns=['Citas por Fecha'])
        # En el vector df line se llenará con 0 cuando no se encunetra la fecha, si no se pasa el valor
        num=[]
        i=0
        for date in df_line['Citas por Fecha']:
            if date.strftime('%Y-%m-%d') in kwargs['df']['Citas por Fecha'].tolist():
                num.append(kwargs['df'].num.iloc[i])
                i=i+1
            else:
                num.append(0)
        df_line['num']=num
        return df_line
    


class stetic():
    def __init__(self):
        #myBuilder=BuilderDash()
        sky=self.getColor('sky-blue')
        gray=self.getColor('gray-blue')
        green=self.getColor('green')
        self.themes=dbc.themes.MINTY
        self.tabs_styles = {
            'height': '44px',
            #'width': '1000px',
        }
        self.tab_selected_style = {
            'borderTop': f"1px solid {sky}",
            'borderBottom': f"1px solid {sky}",
            'backgroundColor': f"{sky}",
            'color': 'white',
            'padding': '6px',
        }
        self.tab_style = {
            'borderTop': f"1px solid {gray}",
            'borderBottom': f"1px solid {gray}",
            'backgroundColor': f"{gray}",
            'color': 'white',
            'padding': '6px',
        }
        self.mainContainer = { 'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            }
        self.CardMenuFilter = {
                'width':'250px', #length of filter card
                'padding':'5px',
                'align-items': 'center',
                'text-align': 'center',
                }
        self.TitleTextCardFilter = {
            'color': sky, 
            'fontWeight': 'bold',
            }
        self.TitleTextCardFilterDate = {
            'width':'150px',
            'padding':'20px',
            'color': sky, 
            'fontWeight': 'bold',
            }
        self.TitleTextCardButtons = {
            'width':'150px',
            'padding':'20px',
            'color': "#82c341", 
            'fontWeight': 'bold',
            }
        self.styleGraphData={
            'border': '0px solid red',
            'boxShadow': '0 0 14px 0 rgba(0, 0, 0, 0.2)',
            'borderRadius': '15px',
            'overflow': 'hidden'
            }
        self.stylebutton= {
            'borderTop': '1px solid '+ green,
            'borderBottom': '1px solid'+ green,
            'backgroundColor': green,
            'color': 'white',
            'padding': '6px',
            'width': '220px',
            }
        self.styleMainTab = {
            "width": "850px",
            'padding':'10px'}
        self.styleMenu ={'width':'240px'}
        self.stylenav = {
            'color':self.getColor('strong-blue'),
            'fontWeight': 'bold',
            'fontSize': 28,                
                        }

    def chooseTab(self,**kwargs):
        '''
        This function builds the tabs, uses the options activated as positive to decide what position to put
        '''
        components=kwargs['components']
        activated = [v[1] for v in components.values() if v[0]]
        divComponentList=[]
        for i,items in enumerate(activated):
            divComponentList.append(
                dcc.Tab(
                    label=items[0], 
                    value=f'tab-{i+1}', 
                    style=self.tab_style, 
                    selected_style=self.tab_selected_style,
                    children=[
                        dbc.Row([   # contains the sections of tab 1
                            dbc.Col(children=[html.P(''), dbc.Spinner(id=items[1],color="#00b3dc", size='lg')]),
                            ],
                        style= self.tabs_styles)
                        ],
                    className=items[2]),
            )
        return divComponentList
    
    def chooseOutputs(self,**kwargs):
        '''
        This function builds the id Outputs, uses the options activated as positive to decide what position to put
        '''
        outputList=[]
        components=kwargs['components']
        activated = [v[1] for v in components.values() if v[0]]
        for items in activated:
            outputList.append(
                Output(f'{items[1]}', 'children')
            )
        return outputList
    
    def chooseInputs(self,**kwargs):
        '''
        This function builds the id Outputs, uses the options activated as positive to decide what position to put
        '''
        inputList=[]
        menus=kwargs['menus']
        
        for menu in menus:
            inputList.append(Input('id_dd'+menu, 'value'))
        inputList.append(Input('url', 'pathname'))

        return inputList


    def getColor(self,color):
        colors = {'white': '#FFFFFF', 'sky-blue': '#00b3dc', 'green': '#82c341','strong-blue': '#003963', 'black': '#000000', 'dark-blue':'#00111e',
                'turquoise': '#4c7492', 'king-blue': '#002845','gray':'#ccd8e0','light-blue':'#e5f8fc','bright-blue':'#4cf8fc','gray-blue':'#6688a2'}
        return colors[f'{color}']


    
