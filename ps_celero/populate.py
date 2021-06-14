

from os import path

from pandas.core.base import SelectionMixin
# environ['DJANGO_SETTINGS_MODULE'] = 'ps_celero.settings'
import api.models as models
# import csv
import pandas as pd
from math import isnan
from tqdm import tqdm
# exec(open("populate.py").read())
thisDir = path.abspath('..')
tpMedal = {"Gold": 1, "Silver": 2, "Bronze": 3}

# Posição na coluna da tabela
NOC = 0
region = 1
notes = 2
# Posição na coluna da tabela
ID = 0
Name = 1
Sex = 2
Age = 3
Height = 3
Weight = 4
Team = 5
NOC = 6
Year = 7
Games = 8
Season = 9
City = 10
Sport = 11
Event = 12
Medal = 13


def main():
    print("Lendo Atletas")
    # file1= open(path.join(thisDir, 'athlete_events.csv'))
    # athletes = csv.reader(file1)
    # next(athletes,None)
    athletes = pd.read_csv(path.join(thisDir, 'athlete_events.csv'),)
    print(athletes.columns)
    print("Lendo NOCs")
    # file2 = open(path.join(thisDir, 'noc_regions.csv'))
    # noc = csv.reader(file2)
    # next(noc,None)
    noc = pd.read_csv(path.join(thisDir, 'noc_regions.csv'))
    print(noc.columns)
    print("Inserindo NOCs")
    for i, row in noc.iterrows():
        # print("CARAIO")
        # print (list(row), flush=True)

        models.Noc.objects.get_or_create(
            acronym=row["NOC"],
            region=row["region"],
            notes=row["notes"])
    print("Inserindo Atletas")
    for i, row in tqdm(athletes.iterrows()):
        try:
            sex = False if row["Sex"] == 'F' else True
            if not isnan(row["Year"])  or not isnan(row["Age"]):
                bY = -1
            else:
                bY = row["Year"] - row["Age"]

            athlete = models.Athlete.objects.get_or_create(
                name=row["Name"],
                sex=sex,
                birth_year=bY
            )
            game = models.Games.objects.get_or_create(
                games=row["Games"],
                season=row["Season"],
                year=row["Year"],
                city=row["City"]
            )
            event = models.Event.objects.get_or_create(
                event=row["Event"],
                sport=row["Sport"],
                game_id=game[0]
            )
            noc = models.Noc.objects.get_or_create(acronym=row["NOC"])
            noc = models.Noc.objects.get(acronym=row["NOC"])
            team = models.Team.objects.get_or_create(
                name=row["Name"],
                noc_id=noc
            )


            # Define medalha
            medal = tpMedal[row["Medal"]] if row["Medal"] in tpMedal else 0
            athleteEventStat = models.AthleteEventStat.objects.get_or_create(

                atlhete_id=athlete[0],
                height=row["Height"],
                weight=row["Weight"],
                event_id=event[0],
                team_id=team[0],
                medal=medal
            )   
        except Exception as e:
            print('\n\033[31mERRO:\033[39m')
            print("\tLinha:\n",row)
            print(str(e))
            # print(traceback.format_exc(), '\n')

main()
