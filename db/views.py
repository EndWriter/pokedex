from rest_framework import viewsets
from .models import DimType, FactPokemon, PokemonTypes, DimTrainer, PokemonTrainers
from .serializers import (
	DimTypeSerializer,
	FactPokemonSerializer,
	PokemonTypesSerializer,
	DimTrainerSerializer,
	PokemonTrainersSerializer,
)

class DimTypeViewSet(viewsets.ModelViewSet):
	queryset = DimType.objects.all()
	serializer_class = DimTypeSerializer

class FactPokemonViewSet(viewsets.ModelViewSet):
	queryset = FactPokemon.objects.all()
	serializer_class = FactPokemonSerializer

class PokemonTypesViewSet(viewsets.ModelViewSet):
	queryset = PokemonTypes.objects.all()
	serializer_class = PokemonTypesSerializer

class DimTrainerViewSet(viewsets.ModelViewSet):
	queryset = DimTrainer.objects.all()
	serializer_class = DimTrainerSerializer

class PokemonTrainersViewSet(viewsets.ModelViewSet):
	queryset = PokemonTrainers.objects.all()
	serializer_class = PokemonTrainersSerializer
