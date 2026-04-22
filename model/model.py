from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def get_all_situazioni(self):
        return MeteoDao.get_all_situazioni()