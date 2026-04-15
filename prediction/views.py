from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionSerializer, PredictionResponseSerializer
from .ml_model import predictor
import numpy as np

class PredictAPIView(APIView):
    """
    API endpoint pour la prédiction du risque de maladie coronarienne
    POST /predict/
    """
    
    def post(self, request):
        # Valider les données d'entrée
        serializer = PredictionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Données invalides',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les données validées
        data = serializer.validated_data
        
        # Définir les valeurs par défaut pour les champs optionnels
        default_values = {
            'education': 2.0,
            'cigsPerDay': 0.0,
            'BPMeds': 0,
            'totChol': 200.0,
            'BMI': 25.0,
            'heartRate': 75.0,
            'glucose': 80.0
        }
        
        for key, default in default_values.items():
            if key not in data or data[key] is None:
                data[key] = default
        
        # Liste complète des features
        feature_order = [
            'male', 'age', 'education', 'currentSmoker', 'cigsPerDay',
            'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes',
            'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'
        ]
        
        # Construire le vecteur de features
        features = []
        for col in feature_order:
            val = data.get(col, 0)
            if val is None or (isinstance(val, float) and np.isnan(val)):
                val = 0
            features.append(float(val))
        
        # Faire la prédiction
        prediction, probability = predictor.predict(dict(zip(feature_order, features)))
        
        # Déterminer le niveau de risque
        if probability >= 0.7:
            risk_level = "Élevé"
            message = "⚠️ Risque ÉLEVÉ de maladie coronarienne"
        elif probability >= 0.3:
            risk_level = "Modéré"
            message = "⚠️ Risque MODÉRÉ de maladie coronarienne"
        else:
            risk_level = "Faible"
            message = "✅ Risque FAIBLE de maladie coronarienne"
        
        # Préparer la réponse
        response_data = {
            'prediction': message,
            'probability': round(probability * 100, 2),
            'risk_level': risk_level,
            'prediction_code': prediction
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


def home_view(request):
    """Vue pour l'interface web"""
    return render(request, 'prediction/index.html')