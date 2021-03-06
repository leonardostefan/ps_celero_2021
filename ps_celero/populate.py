# Após executar ./rebase.sh
# execute 'exec(open("populate.py").read())' dentro de um 'python manage.py shell'
from os import path
import api.models as models

import pandas as pd
import sqlalchemy

from math import isnan
from tqdm import tqdm
# exec(open("populate.py").read())
thisDir = path.abspath('.')
filesDir = path.dirname(thisDir)
dbPath = path.join(thisDir, "db.sqlite3")

eng = sqlalchemy.create_engine('sqlite:///'+dbPath, )

print("Lendo Atletas")
athletesDf = pd.read_csv(path.join(filesDir, 'athlete_events.csv'),)
print(athletesDf.columns)
print("Lendo NOCs")
noc = pd.read_csv(path.join(filesDir, 'noc_regions.csv'))
print(noc.columns)

print("\nInserindo NOCs")
noc = models.Noc.DataFrameToModel(noc)
noc.to_sql("api_noc", eng, if_exists="append", index=False, chunksize=500)

print("Inserindo games")
targCol = ["Games", "Season", "Year", "City"]
games = athletesDf[targCol].drop_duplicates(targCol)
games = games.drop_duplicates(["Games"])
games = models.Games.DataFrameToModel(games)
games.to_sql('api_games', eng, if_exists="append", index=False, chunksize=500)

print("Inserindo events")
targCol = ["Event", "Sport", "Games"]
events = athletesDf[targCol].drop_duplicates(targCol)
events = models.Event.DataFrameToModel(events)
events.to_sql('api_event', eng, if_exists="append", index=False, chunksize=500)


print("Inserindo athletes")
targCol = ["ID", "Name", "Sex", "Age", "Year"]
athletes = athletesDf[targCol].drop_duplicates(targCol)
athletes = models.Athlete.DataFrameToModel(athletes)
athletes = athletes.drop_duplicates(["id"])
athletes[['id', 'name', 'sex', 'birth_year']].to_sql(
    'api_athlete', eng, if_exists="append", index=False, chunksize=500)


print("Inserindo atlhetEvent")
targCol = ["ID", "Height", "Weight", "Event","Games", "Team", "Medal", "NOC"]
atlhetEvent = athletesDf[targCol].drop_duplicates(targCol)
atlhetEvent = models.AthleteEventStat.DataFrameToModel(atlhetEvent)
atlhetEvent.drop("Games", axis =1).to_sql('api_athleteeventstat', eng,
                   if_exists="append", index=False, chunksize=1000)
