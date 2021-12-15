

from modules.LumedReader import apiReader
from modules.LumedBlocks import BuilderDash, stetic
myReader = apiReader()
myDrawer = stetic()
myBuilder = BuilderDash()
'''
importante usar la posicion para las condiciones

'''


def getCard(**kwargs):

    df=kwargs['data'][0]
    salary=kwargs['data'][1]
    keyword=kwargs['data'][2]
    description=kwargs['data'][3]

    cards = myBuilder.GphCards(
                    pos11=myBuilder.makeTopCard(
                        text_k='Salario en:',
                        value_k=keyword.replace('+',' '),
                        ),
                    pos12=myBuilder.makeTopCard(
                        text_k='Salario mínimo',
                        value_k=int(salary['minimo']),
                        ),
                    pos13=myBuilder.makeTopCard(
                        text_k='Salario máximo',
                        value_k=int(salary['maximo']),
                        ),
                    pos21=myBuilder.makeGraph(
                        df=df,
                        x='palabra',
                        y='frecuencia',
                        id_k='pieGph03',
                        id_K='PieGph03',
                        type='treemap',
                    ),
                    pos31=myBuilder.makeGraph(
                        df=description.iloc[:30],
                        x='palabra',
                        y='frecuencia',
                        id_k='pieGph04',
                        id_K='PieGph04',
                        type='cloudword',
                    ),
                    id_k='mycardIntClinic',
                    id_K='MyCardOutClinic',
                    class_k='MyCardClinic',
                )
    return cards
