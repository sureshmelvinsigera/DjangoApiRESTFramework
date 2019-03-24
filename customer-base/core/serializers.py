from rest_framework import serializers
from .models import (
    Customer,
    Profession,
    DataSheet,
    Document
    )


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = (
            'id',
            'description',
            'historical_data',
            )


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = (
            'id',
            'description',
            )


# Serializers define the API representation.
class CustomerSerializer(serializers.ModelSerializer):
    number_of_professions = serializers.SerializerMethodField()
    data_sheet = DataSheetSerializer()
    professions = ProfessionSerializer(many=True)
    document_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'address',
            'professions',
            'data_sheet',
            'active',
            'status_message',
            'number_of_professions',
            'document_set',
            )

    def get_number_of_professions(self, obj):
        return obj.number_of_professions()

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'dtype',
            'doc_number',
            'customer',
            )