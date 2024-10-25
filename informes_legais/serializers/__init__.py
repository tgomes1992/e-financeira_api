from rest_framework import serializers
from informes_legais.models import AplicacoesJcot


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        # Ensure start_date is before or equal to end_date
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be before or equal to end date.")
        return data



class AplicacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplicacoesJcot
        fields = '__all__'


