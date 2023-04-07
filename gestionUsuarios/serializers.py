from rest_framework import serializers
from gestionUsuarios.models import colaborador


class imageuploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = colaborador
        fields = (
            'user',
            'picture'
        )
