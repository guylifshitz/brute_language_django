from rest_framework import serializers
from .models import Article, Pos, Definition


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('__all__')


class PosSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(many=True)

    class Meta:
        model = Pos
        fields = ('__all__')


class WordDetailsSerializer(serializers.ModelSerializer):
    poses = PosSerializer(many=True)

    class Meta:
        model = Article
        fields = ('__all__')
