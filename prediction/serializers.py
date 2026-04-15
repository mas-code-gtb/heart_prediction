from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    # Caractéristiques du patient
    male = serializers.IntegerField(min_value=0, max_value=1)
    age = serializers.FloatField(min_value=0, max_value=120)
    education = serializers.FloatField(required=False, allow_null=True)
    currentSmoker = serializers.IntegerField(min_value=0, max_value=1)
    cigsPerDay = serializers.FloatField(required=False, allow_null=True)
    BPMeds = serializers.IntegerField(min_value=0, max_value=1, required=False, allow_null=True)
    prevalentStroke = serializers.IntegerField(min_value=0, max_value=1)
    prevalentHyp = serializers.IntegerField(min_value=0, max_value=1)
    diabetes = serializers.IntegerField(min_value=0, max_value=1)
    totChol = serializers.FloatField(required=False, allow_null=True)
    sysBP = serializers.FloatField(min_value=0)
    diaBP = serializers.FloatField(min_value=0)
    BMI = serializers.FloatField(required=False, allow_null=True)
    heartRate = serializers.FloatField(required=False, allow_null=True)
    glucose = serializers.FloatField(required=False, allow_null=True)


class PredictionResponseSerializer(serializers.Serializer):
    prediction = serializers.CharField()
    probability = serializers.FloatField()
    risk_level = serializers.CharField()