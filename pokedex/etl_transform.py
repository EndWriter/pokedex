import sqlite3
import pandas as pd
import random

# Chemin vers sqlite
SQLITE_PATH = 'c:/Users/UIMM/Desktop/stage/Dernière dance/pokedex/database.sqlite'

# types Pokémon
TYPES = [
    "acier", "combat", "dragon", "eau", "électrik", "feu", "fée", "glace", "insecte",
    "normal", "plante", "poison", "psy", "roche", "sol", "spectre", "ténèbres", "vol"
]

def load_tables():
    # Charge les tables depuis le fichier sqlite.
    conn = sqlite3.connect(SQLITE_PATH)
    pokemon_df = pd.read_sql_query("SELECT * FROM Pokemon", conn)
    trainers_df = pd.read_sql_query("SELECT * FROM Trainers", conn)
    conn.close()
    print("Colonnes table pokemon :", list(pokemon_df.columns))
    print("Colonnes table trainers :", list(trainers_df.columns))
    return pokemon_df, trainers_df

def clean_data(pokemon_df, trainers_df):
    #Nettoie les doublons et les vides(sauf pour types et scores (à remplir))
    pokemon_df = pokemon_df.drop_duplicates()
    trainers_df = trainers_df.drop_duplicates()
    pokemon_df = pokemon_df.dropna(subset=[
        'pokename', 'pokelevel', 'hp', 'attack', 'defense', 'spatk', 'spdef', 'speed'
    ])
    trainers_df = trainers_df.dropna(subset=['trainerID'])
    return pokemon_df, trainers_df

def assign_types(row):
    # Donner un type au pokemon
    type1 = random.choice(TYPES)
    # Donner un second type au pokemon (ou vide de maniere aléatoire)
    if random.random() < 0.5:
        type2 = ""
    else:
        #le 2eme type doit etre different du premier
        type2 = random.choice([t for t in TYPES if t != type1])
    return pd.Series([type1, type2])

def compute_pokemon_score(row):
    # calcul d'une note sur 100 pour chaque Pokémon
    attack_norm = (row['attack'] / 361) * 100
    defense_norm = (row['defense'] / 501) * 100
    spatk_norm = (row['spatk'] / 349) * 100
    spdef_norm = (row['spdef'] / 501) * 100
    speed_norm = (row['speed'] / 361) * 100
    note_stats = (attack_norm + defense_norm + spatk_norm + spdef_norm + speed_norm) / 5
    note_avec_niveau = 0.7 * note_stats + 0.3 * row['pokelevel']
    n_types = 1 if pd.isna(row['type2']) or row['type2'] == '' else 2
    bonus_type = 0 if n_types == 1 else 0.08
    note_finale = note_avec_niveau * (1 + bonus_type)
    return round(note_finale, 2)

def compute_trainer_score(pokemon_df, trainers_df):
    # calcul le score du dresseur sur 100,  (bonus diversité des types)
    trainer_scores = []
    for trainer_id in trainers_df['trainerID']:
        team = pokemon_df[pokemon_df['trainerID'] == trainer_id]
        if len(team) == 0:
            score = None
        else:
            base_score = team['pokemon_score'].sum() / len(team)
            types = set(team['type1']).union(set(team['type2']) - {''})
            diversity = len(types) / 18
            score = round(base_score * (1 + diversity), 2)
        trainer_scores.append(score)
    trainers_df['trainer_score'] = trainer_scores
    print(trainers_df[['trainerID', 'trainer_score']].head())

if __name__ == '__main__':
    print("lancement ETL")
    # extraction + nettoyage
    pokemon_df, trainers_df = load_tables()
    pokemon_df, trainers_df = clean_data(pokemon_df, trainers_df)
    print(f"poké restants : {len(pokemon_df)}")
    print(f"trainers restants : {len(trainers_df)}")

    # type aléatoire
    pokemon_df[['type1', 'type2']] = pokemon_df.apply(assign_types, axis=1)
    print(pokemon_df[['pokename', 'type1', 'type2']].head())

    # score Pokémon
    pokemon_df['pokemon_score'] = pokemon_df.apply(compute_pokemon_score, axis=1)
    print(pokemon_df[['pokename', 'pokemon_score']].head())

    # score dresseur
    compute_trainer_score(pokemon_df, trainers_df)
