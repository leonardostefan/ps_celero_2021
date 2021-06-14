from django.db import models


class Athlete(models.Model):
    '''
    Definições "imutaveis" de um Atleta
    - name = Nome do atleta 
    - sex = Sexo do atleta, booleano: 0 = Feminino , 1 = Masculino
    - birth_year  = Ano de nascimento do atleta (calculado para não ter de armazenar a idade em cada evento)
    '''
    name = models.CharField(max_length=255)
    sex = models.BooleanField()  # 0 = F , 1 = M
    birth_year = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.name


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


class Event(models.Model):
    '''
    Evento esportivo:
    event - Nome/modalidade do evento
    sport - Esporte em questão
    games - Jogos olimpicos ao qual ocorreu o evento
    '''
    event = models.CharField(max_length=63)
    sport = models.CharField(max_length=63)
    game_id = models.ForeignKey(Games, to_field='games',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.event


class Noc(models.Model):
    '''
    National Olympic Committee (Comitê Olímpico Nacional )
    acronym - Acronimo/sigla do comitê 
    region - Região de referencia 
    notes - Informações extras (outras regiões pertencentes)
    '''
    acronym = models.CharField(max_length=3)
    region = models.CharField(max_length=63)
    notes = models.TextField()

    def __str__(self):
        return self.acronym


class Team (models.Model):
    '''
    Equipes existentes:
    name - nome da equipe 
    noc - Comitê Olímpico Nacional pertencente
    '''
    name = models.CharField(max_length=63)
    noc_id = models.ForeignKey(Noc, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AthleteEventStat(models.Model):
    '''
    Definições/estatisticas do Atleta no evento:
    - atlhete =  Identificação do atlheta
    - height = Altura do atleta em centimetros
    - weight  = Altura do atleta em Kg
    - event = Evento em questão
    - team  = Time pertencente
    - medal = Medalha recebida, 1 = Ouro, 2 = Prata , 3 = Bronze, 0 = Não Atribuido(N/A), 4+ = Posicionamento/rank na competição
    '''
    atlhete_id = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    medal = models.SmallIntegerField(null=True)
    # Inteiros 1 = Ouro, 2 = Prata , 3 = Bronze, 4 = N/A

    # TODO: ver uma saida melhor
    def __str__(self):
        return self.atlhete
