import json
from dataclasses import dataclass, field


@dataclass
class Position:
    latitude: int
    longitude: int


@dataclass
class Pompe:
    prix: int
    nom: str


@dataclass
class Station:
    id: str
    cp: str
    departement: str
    region: str
    adresse: str
    epci_nom: str
    carburant: str
    prix: int
    geom: list
    position: Position = field(init=False)
    pompes: list = field(init=False)
    services: list
    flag_automate_24: bool

    def __post_init__(self):
        self.position = Position(self.geom[0], self.geom[1])
        self.pompes = [Pompe(self.prix, self.carburant), ]


    @classmethod
    def from_dict(cls, dict):
        services = dict.get('services_service', '').split('//')
        automate = (True if(dict['horaires_automate_24_24'] == 'Non') else False)
        station = Station(
            dict['id'],
            dict['com_arm_code'],
            dict['dep_name'],
            dict['reg_name'],
            dict['adresse'],
            dict['epci_name'],
            dict['prix_nom'],
            dict['prix_valeur'],
            dict['geom'],
            services,
            automate
        )
        return station

    @staticmethod
    def parse_from_text(data_json_url):
        stations_list = []
        data = get_data(data_json_url)

        for fields in data['records']:
            station = Station.from_dict(fields['fields'])
            stations_list.append(station)

        grouped_stations = {}

        for station in stations_list:
            if station.id not in grouped_stations:
                grouped_stations[station.id] = station
            else:
                for carburant in station.pompes:
                    if carburant.nom not in {p.nom for p in grouped_stations[station.id].pompes}:
                        grouped_stations[station.id].pompes.append(carburant)

        return grouped_stations


def get_data(url):
    with open(url, "r", encoding='utf-8') as file:
        return json.loads(file.read())


if __name__ == '__main__':
    station = Station.from_dict(get_data("./assets/station.json"))
    print(f'Station.from_dict :  {station}')

    print()

    stations = Station.parse_from_text("./assets/data.json")
    print(f'Station.parse_from_text :  {stations}')
    print(f'len(stations) = {len(stations)}')






