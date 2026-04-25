import copy
from collections import defaultdict

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def get_all_situazioni(self):
        return MeteoDao.get_all_situazioni()

    def calcola_sequenza(self, mese):
        #preparo i dati
        situazioni = self.get_all_situazioni()
        perMese = [s for s in situazioni if s.data.month == mese]
        perLocalita = defaultdict(list)
        for s in perMese:
            perLocalita[s.localita].append(s)
            ''' perLocalita è un dizionario dove ogni chiave è una città e il valore è una LISTA di situazioni ordinate per data
            perLocalita = {
                "Genova": [Situazione(Genova, 2013-02-01, 81),   # indice 0 → giorno 1
                           Situazione(Genova, 2013-02-02, 63),   # indice 1 → giorno 2
                           Situazione(Genova, 2013-02-03, 20),   # indice 2 → giorno 3
                           ...],
                "Milano": [Situazione(Milano, 2013-02-01, 53),   # indice 0 → giorno 1
                           Situazione(Milano, 2013-02-02, 75),   # indice 1 → giorno 2
                           ...],
                "Torino": [...]
            }'''

        #inizializzo il best
        self._best = None
        self._best_costo = None
        for citta in perLocalita:
            perLocalita[citta].sort(key=lambda s: s.data)
        # avvio la ricorsione
        self._ricorsione([], 15, perLocalita)
        return self._best, self._best_costo  # restituisce la soluzione migliore

    def _ricorsione(self, parziale, giorniRimanenti, perLocalita):
        # qui va la logica ricorsiva
        # parziale è la lista delle città scelte finora, giorno per giorno:
        # parziale = [Genova, Genova, Genova, Milano, Milano, Milano, Torino]
        # CASO TERMINALE - ho riempito tutti i 15 giorni
        if giorniRimanenti == 0:
            # calcola costo
            costo = 0
            for i in range(len(parziale)):
                costo += parziale[i].umidita  # umidità sempre
                if i > 0 and parziale[i].localita != parziale[i - 1].localita:
                    #se la località prima è diversa da quella che sto guardando vuol dire che ho cambiato città e aggiungo 100
                    costo += 100  # cambio città → aggiungo 100

            # è meglio di quello che ho già?
            if self._best is None or costo < self._best_costo:
                self._best = copy.deepcopy(parziale)
                self._best_costo = costo
            return

        # CASO RICORSIVO - scelgo la città per il giorno corrente
        else:
            giorno_corrente = 15 - giorniRimanenti
            for citta in ["Milano", "Torino", "Genova"]:
                situazione = perLocalita[citta][giorno_corrente] #IL GIORNO rappresenta l'indice della lista di situa

                # vincolo 1: non si può stare più di 6 giorni in una città
                giorni_totali = len([s for s in parziale if s.localita == citta])
                '''giorni totali è una lista con dentro la località tante volte che è nel parziale. 
                Se milano è tre volte nel parziale, giorni_totali = [milano, milano, milano]
                prendo la len di questa lista per sapere appunto quante volte c'è e impongo che non può essere >6'''
                if giorni_totali >= 6:
                    continue

                # VINCOLO 2 - almeno 3 giorni consecutivi prima di spostarsi
                '''Guardo dalla fine quanti giorni consecutivi ho fatto nell'ultima città (Milano):
                [Genova, Genova, Milano]: solo 1 giorno a Milano consecutivo →  non posso spostarmi!
                Se invece fosse: [Genova, Genova, Genova, Milano, Milano, Milano]: 3 giorni consecutivi a Milano → posso spostarmi!'''
                if len(parziale) > 0 and parziale[-1].localita != citta:
                    consecutivi = 0
                    for s in reversed(parziale):
                        if s.localita == parziale[-1].localita:
                            consecutivi += 1
                        else:
                            break
                    if consecutivi < 3:
                        continue

                # aggiungo la situazione al parziale
                parziale.append(situazione)
                # vado avanti
                self._ricorsione(parziale, giorniRimanenti - 1, perLocalita)
                # backtracking - tolgo e provo la prossima città
                parziale.pop()