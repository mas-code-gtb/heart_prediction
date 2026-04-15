import joblib
import numpy as np
import os

class HeartDiseasePredictor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Charge le modèle ML et le scaler"""
        # Récupère le dossier racine du projet (où est manage.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_path = os.path.join(base_dir, 'heart_disease_model.pkl')
        scaler_path = os.path.join(base_dir, 'scaler.pkl')
        features_path = os.path.join(base_dir, 'feature_names.pkl')
        
        # Vérification et chargement
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modèle non trouvé: {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler non trouvé: {scaler_path}")
        if not os.path.exists(features_path):
            raise FileNotFoundError(f"Features non trouvées: {features_path}")
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.feature_names = joblib.load(features_path)
        
        print(f"✅ Modèle chargé avec succès depuis {base_dir}")
        
    def predict(self, data):
        """
        Effectue la prédiction pour un patient
        
        Args:
            data: dict contenant les caractéristiques du patient
            
        Returns:
            tuple: (prediction, probability)
        """
        # Créer le tableau des features dans le bon ordre
        features = []
        for col in self.feature_names:
            value = data.get(col, 0)
            # Gérer les valeurs None/NaN
            if value is None or (isinstance(value, float) and np.isnan(value)):
                value = 0
            features.append(float(value))
        
        # Transformer en array numpy
        features_array = np.array(features).reshape(1, -1)
        
        # Standardiser
        features_scaled = self.scaler.transform(features_array)
        
        # Prédiction
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0, 1]
        
        return int(prediction), float(probability)


# Instance globale
predictor = HeartDiseasePredictor()