

from modules.LumedReader import apiReader
from modules.LumedBlocks import BuilderDash, stetic
myReader = apiReader()
myDrawer = stetic()
myBuilder = BuilderDash()
'''
importante usar la posicion para las condiciones

'''


def getCard(**kwargs):

    df=kwargs['df'][0]
    tocken=kwargs['df'][1]

    cards = myBuilder.GphCards(
                    pos11=myBuilder.makeTopCard(
                        text_k='costo de hotel en:',
                        value_k='pendiente'
                        ),
                    pos12=myBuilder.makeTopCard(
                        text_k='mínimo',
                        value_k='pendiente'
                        ),
                    pos13=myBuilder.makeTopCard(
                        text_k='máximo',
                        value_k='pendiente'
                        ),
                    pos21=myBuilder.makeGraph(
                        df=tocken,
                        x='palabra',
                        y='frecuencia',
                        id_k='pieGph03',
                        id_K='PieGph03',
                        type='treemap',
                    ),
                    pos31=myBuilder.makeGraph(
                        df=tocken,
                        x='palabra',
                        y='frecuencia',
                        id_k='pieGph04',
                        id_K='PieGph04',
                        type='cloudword',
                    ),
                    pos41=myBuilder.makeGraph(
                        df=df,
                        x='sentimiento',
                        y='num',
                        id_k='pieGph05',
                        id_K='PieGph05',
                        type='pie',
                    ),
                    id_k='mycardIntClinic',
                    id_K='MyCardOutClinic',
                    class_k='MyCardClinic',
                )
    return cards
