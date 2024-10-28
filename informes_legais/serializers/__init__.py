from rest_framework import serializers
from informes_legais.models import AplicacoesJcot ,  ResgatesJcot


class DateRangeSerializer(serializers.Serializer):
    data_inicio = serializers.DateField()
    data_fim = serializers.DateField()
    def validate(self, data):
        # Ensure start_date is before or equal to end_date
        if data['data_inicio'] > data['data_inicio']:
            raise serializers.ValidationError("Start date must be before or equal to end date.")
        return data



class AplicacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplicacoesJcot
        fields = '__all__'


class ResgatesJcotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResgatesJcot
        fields = '__all__'
