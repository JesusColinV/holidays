'''
This is the configuration file, in which you can activate or deactivate tabs, menus or replace names

other customizations are described in line 143 of functions for more details go to the README.md file
'''

        
class configurationsTabs:
    def __init__(self) :
        self.buttons = ['Registro']
        self.components = {
            0:
                [
                    True,
                    ['Buscador','tabBuscador','TabBuscador']
                ],
            1:
                [
                    False,
                    ['Productividad','tabProductivity','TabProductivity']
                ],
            2:
                [
                    False,
                    ['Citas Programadas','tabTable','TabTable']
                ],
            3:
                [
                    False,
                    ['Planificación Familiar','tabClinic','TabClinic']
                ],
        }

        

