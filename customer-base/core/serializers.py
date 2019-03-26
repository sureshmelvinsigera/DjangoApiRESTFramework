from rest_framework import serializers
from .models import (
    Customer,
    Profession,
    DataSheet,
    Document
    )

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'dtype',
            'doc_number',
            'customer'
            )

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'dtype',
            'doc_number',
            'customer'
            )

        read_only_fields = ['customer']


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = (
            'id',
            'description',
            'historical_data'
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
    document_set = DocumentSerializer(many=True)

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
            'document_set'
            )

    def create(self, validated_data):
        professions = validated_data['professions']
        del validated_data['professions']

        document_set = validated_data['document_set']
        del validated_data['document_set']

        data_sheet = validated_data['data_sheet']
        del validated_data['data_sheet']

        d_sheet = DataSheet.objects.create(**data_sheet)
        customer = Customer.objects.create(**validated_data)
        customer.data_sheet = d_sheet

        for doc in document_set:
            Document.objects.create(
                dtype=doc['dtype'],
                doc_number=doc['doc_number'],
                customer_id=customer.id
            )

        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.professions.add(prof)

        customer.save()
        return customer

    def get_number_of_professions(self, obj):
        return obj.number_of_professions()