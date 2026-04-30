import copy
from collections import defaultdict

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    #con questa funzione il controller legge il mese e quando viene cliccato il bottone
    #(e è l'evento chiamato dalla view)
    def read_mese(self, e):
        self._mese = int(e.control.value)

    def handle_umidita_media(self, e):
        if self._mese == 0:
           self._view.create_alert("Selezionare un mese")
           return
        risultato= self._model.get_umidita_media(self._mese)  #[{Località: Torino, umidità: 89}, {...}]
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
        for r in risultato:
            self._view.lst_result.controls.append(ft.Text(f"{r[0]}: {r[1]}"))
        self._view.update_page()

        '''se nel dao avessi messo dictionary=True, e AVG(s.Umidita) as umidita
        col fetchall avrei ottenuto una lista di dizionari: [{Località: Torino, umidita: 89}, {...}].
        In questo caso avrei fatto: 
         for dizionario in risultato:
            self._view.lst_result.controls.append(ft.Text(f"{dizionario["Localita"]}: {dizionario["umidita"]}"))
        self._view.update_page()
        '''

    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza, costo = self._model.get_sequenza_ottima(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for s in sequenza:
            self._view.lst_result.controls.append(ft.Text(s))
        self._view.update_page()




