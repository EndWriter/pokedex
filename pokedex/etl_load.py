import sys
import os
# me permet d'éviter le problème dimportation des methodes de mon fichier extract and load
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

# init Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokedex.settings')
django.setup()
from db.models import FactPokemon, DimTrainer, DimType, PokemonTypes, PokemonTrainers

# Import des fonctions de transformation
from etl_transform import load_tables, clean_data, assign_types, compute_pokemon_score, compute_trainer_score

# Extract et transform
pokemon_df, trainers_df = load_tables()
print('Vérification trainerID=0:', trainers_df[trainers_df['trainerID'] == 0])
pokemon_df, trainers_df = clean_data(pokemon_df, trainers_df)
pokemon_df[['type1', 'type2']] = pokemon_df.apply(assign_types, axis=1)
pokemon_df['pokemon_score'] = pokemon_df.apply(compute_pokemon_score, axis=1)
compute_trainer_score(pokemon_df, trainers_df)

# change lees NaN par 0 
import numpy as np
numeric_cols_pokemon = ['pokelevel', 'hp', 'maxhp', 'attack', 'defense', 'spatk', 'spdef', 'speed', 'pokemon_score']
for col in numeric_cols_pokemon:
	if col in pokemon_df.columns:
		pokemon_df[col] = pokemon_df[col].replace(np.nan, 0)
if 'trainer_score' in trainers_df.columns:
	trainers_df['trainer_score'] = trainers_df['trainer_score'].replace(np.nan, 0)

# Afficher les lignes quand il manque le nom des trainers
if 'trainername' in trainers_df.columns:
	missing_names = trainers_df[trainers_df['trainername'].isnull() | (trainers_df['trainername'].astype(str).str.strip() == '')]
	if not missing_names.empty:
		print("trainers sans nom :")
		print(missing_names)

# on ne garder que les dresseurs avec un nom renseigné
trainers_df = trainers_df[trainers_df['trainername'].notnull() & (trainers_df['trainername'].astype(str).str.strip() != '')]


# chargement types
type_names = set(pokemon_df['type1'].dropna().unique()) | set(pokemon_df['type2'].dropna().unique())
for type_name in type_names:
	if type_name and not DimType.objects.filter(type_name=type_name).exists():
		DimType.objects.create(type_name=type_name)

# chargement trainers

for _, row in trainers_df.iterrows():
	# verif que les trainers ont bien un nom
	if 'trainername' not in row or str(row['trainername']).strip() == '':
		raise ValueError(f"trainername manquant pour trainerID={row['trainerID']}")
	name = str(row['trainername'])
	trainer, created = DimTrainer.objects.get_or_create(
		trainer_id=str(row['trainerID']),
		defaults={
			'trainer_name': name,
			'trainer_score': row.get('trainer_score', 0)
		}
	)
	if not created:
		trainer.trainer_name = name
		trainer.trainer_score = row.get('trainer_score', 0)
		trainer.save()

# chargement Poké
for _, row in pokemon_df.iterrows():
	poke, created = FactPokemon.objects.get_or_create(
		pokemon_name=row['pokename'],
		level=row['pokelevel'],
		hp=row['hp'],
		atk=row['attack'],
		def_stat=row['defense'],
		atk_spe=row['spatk'],
		def_spe=row['spdef'],
		spd=row['speed'],
		pokemon_score=row.get('pokemon_score', 0)
	)
	if not created:
		poke.level = row['pokelevel']
		poke.hp = row['hp']
		poke.atk = row['attack']
		poke.def_stat = row['defense']
		poke.atk_spe = row['spatk']
		poke.def_spe = row['spdef']
		poke.spd = row['speed']
		poke.pokemon_score = row.get('pokemon_score', 0)
		poke.save()

# chargement des relations PokéTYpes
for _, row in pokemon_df.iterrows():
	poke = FactPokemon.objects.filter(pokemon_name=row['pokename'], level=row['pokelevel']).first()
	for type_col in ['type1', 'type2']:
		type_name = row[type_col]
		if type_name:
			type_obj = DimType.objects.get(type_name=type_name)
			if poke:
				PokemonTypes.objects.get_or_create(pokemon=poke, type=type_obj)

# chargement des relations PokéTrainers
for _, row in pokemon_df.iterrows():
	poke = FactPokemon.objects.filter(pokemon_name=row['pokename'], level=row['pokelevel']).first()
	trainer = DimTrainer.objects.get(trainer_id=str(row['trainerID']))
	if poke:
		PokemonTrainers.objects.get_or_create(pokemon=poke, trainer=trainer)

print("chargement OK")
