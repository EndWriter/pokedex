from rest_framework import serializers
from .models import DimType, FactPokemon, PokemonTypes, DimTrainer, PokemonTrainers

class DimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimType
        fields = '__all__'

class FactPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactPokemon
        fields = '__all__'

class PokemonTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonTypes
        fields = '__all__'

class DimTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimTrainer
        fields = '__all__'

class PokemonTrainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonTrainers
        fields = '__all__'
