from django.db import models
import pandas as pd


class Athlete(models.Model):
    '''
    Definições "imutaveis" de um Atleta
    - id =  Nº de identificação do atleta
    - name = Nome do atleta 
    - sex = Sexo do atleta, booleano: 0 = Feminino , 1 = Masculino
    - birth_year  = Ano de nascimento do atleta (calculado para não ter de armazenar a idade em cada evento)
    '''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    sex = models.BooleanField()  # 0 = F , 1 = M
    birth_year = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.name

    def originalMap():
        rn = {
            "ID": 'id',
            'Name': 'name',
            'Sex': 'sex'
        }
        return rn

    def DataFrameToModel(df: pd.DataFrame) -> pd.DataFrame:
        '''
        Metodo de conversão do modelo do CSV para a estrutura de dados definidas na API
        Entrada:
            df = Dataframe com as colunas a serem formatadas
        Saida
            Dataframe formatado. Nenhuma linha ou coluna é excluida, apenas modificado.
        '''
        df = df.rename(Athlete.originalMap(), axis=1)
        df.loc[:, 'id'] = df.loc[:, 'id'].apply(lambda x: int(x))

        if "Year" in df.columns and "Age" in df.columns:
            df["birth_year"] = (df["Year"] - df["Age"]).fillna(int(-1))
        else:
            df["birth_year"] = -1
        df["sex"] = df["sex"].apply(
            lambda x: False if (x == 'F' or x == False) else True)
        return df


class Games(models.Model):
    '''
    Jogos Olimpicos existentes:
     - games = Nome e temporada
     - season = temporada (inverdo/verão)
     - year = ano de acontecimento
     - city = cidade hospedeira
    '''
    games = models.CharField(max_length=63, primary_key=True)
    season = models.CharField(max_length=63)
    year = models.SmallIntegerField(null=True)
    city = models.CharField(max_length=63)

    def __str__(self):
        return self.games

    def originalMap():
        rn = {
            'Games': 'games',
            'Season': 'season',
            'Year': 'year',
            'City': 'city'
        }
        return rn

    def DataFrameToModel(df: pd.DataFrame) -> pd.DataFrame:
        '''
        Metodo de conversão do modelo do CSV para a estrutura de dados definidas na API
        Entrada:
            df = Dataframe com as colunas a serem formatadas
        Saida
            Dataframe formatado. Nenhuma linha ou coluna é excluida, apenas modificado.
        '''
        df = df.rename(Games.originalMap(), axis=1)
        return df


class Event(models.Model):
    '''
    Evento esportivo:
    event - Nome/modalidade do evento
    sport - Esporte em questão
    gameId - Jogos olimpicos ao qual ocorreu o evento
    '''
    id = models.CharField(max_length=127, primary_key=True)
    event = models.CharField(max_length=63)
    sport = models.CharField(max_length=63)
    gameId = models.ForeignKey(Games, to_field='games',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def originalMap():
        rn = {
            'Event': 'event',
            'Sport': 'sport',
            'Games': 'gameId_id'
        }
        return rn

    def DataFrameToModel(df: pd.DataFrame) -> pd.DataFrame:
        '''
        Metodo de conversão do modelo do CSV para a estrutura de dados definidas na API
        Entrada:
            df = Dataframe com as colunas a serem formatadas
        Saida
            Dataframe formatado. Nenhuma linha ou coluna é excluida, apenas modificado.
        '''
        df = df.rename(Event.originalMap(), axis=1)
        df['id'] = df['gameId_id']+':'+df['event']
        return df


class Noc(models.Model):
    '''
    National Olympic Committee (Comitê Olímpico Nacional )
    acronym - Acronimo/sigla do comitê 
    region - Região de referencia 
    notes - Informações extras (outras regiões pertencentes)
    '''
    acronym = models.CharField(max_length=3, primary_key=True)
    region = models.CharField(max_length=63, null=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.acronym

    def originalMap():
        rn = {
            'NOC': 'acronym',
            'region': 'region',
            'notes': 'notes'
        }
        return rn

    def DataFrameToModel(df: pd.DataFrame) -> pd.DataFrame:
        '''
        Metodo de conversão do modelo do CSV para a estrutura de dados definidas na API
        Entrada:
            df = Dataframe com as colunas a serem formatadas
        Saida
            Dataframe formatado. Nenhuma linha ou coluna é excluida, apenas modificado.
        '''
        df = df.rename(Noc.originalMap(), axis=1)
        return df


class AthleteEventStat(models.Model):
    '''
    Definições/estatisticas do Atleta no evento:
    - atlheteId =  Identificação do atlheta
    - height = Altura do atleta em centimetros
    - weight  = Altura do atleta em Kg
    - eventId = ID Evento em questão
    - team  = Time pertencente
    - medal = Medalha recebida, 1 = Ouro, 2 = Prata , 3 = Bronze, 0 = Não Atribuido(N/A), 4+ = Posicionamento/rank na competição
    - nocId = Comitê Olímpico Nacional
    '''
    atlheteId = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=63, null=True)
    medal = models.SmallIntegerField(null=True)
    nocId = models.ForeignKey(Noc, on_delete=models.CASCADE)
    # Inteiros 1 = Ouro, 2 = Prata , 3 = Bronze, 4 = N/A

    # TODO: ver uma saida melhor
    def __str__(self):
        r = str("athlete: {}; medal: {}º").format(self.atlheteId, self.medal)
        return (r)

    def originalMap():
        rn = {
            'ID': 'atlheteId_id',
            'Height': 'height',
            'Weight': 'weight',
            'Event': 'eventId_id',
            'Team': 'team',
            'Medal': 'medal',
            'NOC': 'nocId_id'
        }
        return rn

    def DataFrameToModel(df: pd.DataFrame) -> pd.DataFrame:
        '''
        Metodo de conversão do modelo do CSV para a estrutura de dados definidas na API
        Entrada:
            df = Dataframe com as colunas a serem formatadas
        Saida
            Dataframe formatado. Nenhuma linha ou coluna é excluida, apenas modificado.
        '''
        tpMedal = {"Gold": 1, "Silver": 2, "Bronze": 3}
        df.loc[:, 'ID'] = df.loc[:, 'ID'].apply(lambda x: int(x))
        df = df.rename(AthleteEventStat.originalMap(), axis=1)
        df.loc[:, 'medal'] = df.loc[:, 'medal'].apply(
            lambda x: tpMedal[x]if x in tpMedal else 0)
        df['eventId_id'] = df['Games']+':'+df['eventId_id']

        return df
