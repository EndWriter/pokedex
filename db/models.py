from django.db import models

class DimType(models.Model):
	type_id = models.AutoField(primary_key=True)
	type_name = models.CharField(max_length=255, null=True, blank=True)

class FactPokemon(models.Model):
	pokemon_id = models.AutoField(primary_key=True)
	pokemon_name = models.CharField(max_length=255)
	level = models.IntegerField()
	hp = models.IntegerField()
	atk = models.IntegerField()
	def_stat = models.IntegerField()
	atk_spe = models.IntegerField()
	def_spe = models.IntegerField()
	spd = models.IntegerField()
	pokemon_score = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

class PokemonTypes(models.Model):
	pokemon = models.ForeignKey(FactPokemon, on_delete=models.CASCADE, null=True)
	type = models.ForeignKey(DimType, on_delete=models.CASCADE, null=True)

class DimTrainer(models.Model):
	trainer_id = models.CharField(max_length=50, primary_key=True)
	trainer_name = models.CharField(max_length=255)
	trainer_score = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

class PokemonTrainers(models.Model):
	pokemon = models.ForeignKey(FactPokemon, on_delete=models.CASCADE, null=True)
	trainer = models.ForeignKey(DimTrainer, on_delete=models.CASCADE, null=True)
