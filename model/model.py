from collections import defaultdict

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def get_all_situazioni(self):
        return MeteoDao.get_all_situazioni()

    def calcola_sequenza(self, mese):
        situazioni = self.get_all_situazioni()
        perMese = [s for s in situazioni if s.data.month == mese]
        perLocalita = defaultdict(list)
        for s in perMese:
            perLocalita[s.localita].append(s.umidita)

        self._soluzioni = []
        self._best = None
        self._ricorsione([], 15, perLocalita)
        return self._best  # restituisce la soluzione migliore

    def _ricorsione(self, parziale, giorniRimanenti, perLocalita):
        # qui va la logica ricorsiva
        if giorniRimanenti == 0:
            # calcola costo e salva se è il migliore
            return
        else:
            giorno_corrente = 15 - giorniRimanenti
            for citta in ["Milano", "Torino", "Genova"]:
                situazione = perLocalita[citta][giorno_corrente]

                # vincolo 1: non si può stare più di 6 giorni in una città
                if len([s for s in parziale if s.localita == citta]) >= 6:
                    #equivalente a sum(1 for s in parziale if s.località == citta) >= 6
                    continue

                # vincolo 2: il tecnico deve stare almeno 3 giorni in una città
                if len(parziale) > 0 and parziale[-1].localita != citta:
                    consecutivi = 0
                    #guarda solo la coda di parziale e conta quanti elementi consecutivi hanno la stessa città dell'ultimo.
                    for s in reversed(parziale):
                        if s.localita == parziale[-1].localita:
                            consecutivi += 1
                        else: # appena trovo una città diversa mi fermo
                            break
                    if consecutivi < 3:
                        continuew

                parziale.append(situazione)
                self._ricorsione(parziale, giorniRimanenti - 1, perLocalita)
                parziale.pop()