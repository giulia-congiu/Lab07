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

    def handle_umidita_media(self, e):
        mese = int(self._view.dd_mese.value)
        perMese = [o for o in self._model.get_all_situazioni() if o.data.month == mese]
            #prendo le situazioni che hanno come mese quello che ho scelto

        perLocalita = defaultdict(list) #crea automaticamente una lista vuota per ogni chiave
        for s in perMese:
            perLocalita[s.localita].append(s.umidita)
            #creo un dizionario Località-[lista di umidità per quel mese]

        medie = {}
        for loc, umidita in perLocalita.items(): #ricorda che .items da chiave-valore
            medie[loc]= sum(umidita)/len(umidita)

        #oppure list comprehension
        # medie={loc: sum(umidita)/len(umidita) for loc, umidita in perLocalita.items()}

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))

        for localita, media in medie.items():
            self._view.lst_result.controls.append(ft.Text(f"{localita}: {media: .4f}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

