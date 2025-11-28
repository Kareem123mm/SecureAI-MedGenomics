"""
AI Prediction Engine for SecureAI-MedGenomics

Unified prediction pipeline that:
1. Accepts genomic file content
2. Extracts features
3. Runs all 6 AI models
4. Ensembles results (voting/averaging)
5. Returns comprehensive analysis
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path

from .model_loader import ModelLoader
from .feature_extractor import GenomicFeatureExtractor

logger = logging.getLogger(__name__)


class PredictionEngine:
    """
    Complete AI prediction pipeline
    """
    
    def __init__(self, models_dir: Optional[Path] = None):
        """
        Initialize prediction engine
        
        Args:
            models_dir: Directory containing AI models
        """
        # Initialize components
        self.model_loader = ModelLoader(models_dir)
        self.feature_extractor = GenomicFeatureExtractor(expected_features=587)
        
        # Load all models
        self.models = self.model_loader.load_all_models()
        
        # Statistics
        self.prediction_count = 0
        
        logger.info("Prediction Engine initialized")
    
    def is_ready(self) -> bool:
        """Check if engine is ready to make predictions"""
        # At least one model must be loaded
        loaded = self.model_loader.get_loaded_models()
        return any(loaded.values())
    
    def extract_features(self, content: bytes) -> np.ndarray:
        """
        Extract features from genomic file
        
        Args:
            content: Raw file bytes (FASTA format)
        
        Returns:
            Feature vector (587 features)
        """
        features = self.feature_extractor.extract_features_from_file(content)
        
        # Validate
        if not self.feature_extractor.validate_features(features):
            logger.error("Feature validation failed")
            raise ValueError("Invalid features extracted")
        
        return features
    
    def predict_disease_risk_single(
        self,
        features: np.ndarray,
        model_type: str
    ) -> Optional[float]:
        """
        Predict disease risk using a single model
        
        Args:
            features: Feature vector
            model_type: 'nn', 'rf', or 'xgb'
        
        Returns:
            Risk probability (0-1) or None if model not available
        """
        model_name = f"disease_risk_{model_type}"
        model = self.model_loader.get_model(model_name)
        
        if model is None:
            logger.warning(f"Model not available: {model_name}")
            return None
        
        try:
            if model_type == 'nn':
                # PyTorch prediction
                with torch.no_grad():
                    features_tensor = torch.FloatTensor(features).unsqueeze(0)
                    features_tensor = features_tensor.to(self.model_loader.device)
                    prediction = model(features_tensor)
                    return float(prediction.cpu().numpy()[0][0])
            
            else:
                # sklearn/XGBoost prediction
                features_2d = features.reshape(1, -1)
                prediction = model.predict_proba(features_2d)[0][1]  # Probability of class 1
                return float(prediction)
        
        except Exception as e:
            logger.error(f"Prediction failed for {model_name}: {e}")
            return None
    
    def predict_drug_response_single(
        self,
        features: np.ndarray,
        model_type: str
    ) -> Optional[float]:
        """
        Predict drug response using a single model
        
        Args:
            features: Feature vector
            model_type: 'nn', 'rf', or 'xgb'
        
        Returns:
            Drug response value or None if model not available
        """
        model_name = f"drug_response_{model_type}"
        model = self.model_loader.get_model(model_name)
        
        if model is None:
            logger.warning(f"Model not available: {model_name}")
            return None
        
        try:
            if model_type == 'nn':
                # PyTorch prediction
                with torch.no_grad():
                    features_tensor = torch.FloatTensor(features).unsqueeze(0)
                    features_tensor = features_tensor.to(self.model_loader.device)
                    prediction = model(features_tensor)
                    return float(prediction.cpu().numpy()[0][0])
            
            else:
                # sklearn/XGBoost prediction
                features_2d = features.reshape(1, -1)
                prediction = model.predict(features_2d)[0]
                return float(prediction)
        
        except Exception as e:
            logger.error(f"Prediction failed for {model_name}: {e}")
            return None
    
    def ensemble_disease_risk(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Ensemble disease risk predictions from all available models
        
        Strategy:
        - If metadata available, use best model
        - Otherwise, average all predictions (soft voting)
        
        Args:
            features: Feature vector
        
        Returns:
            Ensemble result with confidence
        """
        predictions = {}
        
        # Get predictions from all models
        for model_type in ['nn', 'rf', 'xgb']:
            pred = self.predict_disease_risk_single(features, model_type)
            if pred is not None:
                predictions[model_type] = pred
        
        if not predictions:
            logger.error("No disease risk models available")
            return {
                "risk_probability": 0.0,
                "risk_level": "unknown",
                "confidence": 0.0,
                "models_used": [],
                "individual_predictions": {}
            }
        
        # Check if we have metadata about best model
        metadata = self.model_loader.metadata.get('disease_risk', {})
        best_model = metadata.get('best_model', '').replace('.pkl', '').replace('_disease_risk', '')
        
        if best_model in predictions:
            # Use best model prediction
            final_prediction = predictions[best_model]
            logger.info(f"Using best model ({best_model}) for disease risk: {final_prediction:.3f}")
        else:
            # Average all predictions (soft voting)
            final_prediction = np.mean(list(predictions.values()))
            logger.info(f"Averaging {len(predictions)} models for disease risk: {final_prediction:.3f}")
        
        # Calculate confidence (inverse of standard deviation)
        if len(predictions) > 1:
            std = np.std(list(predictions.values()))
            confidence = max(0.0, min(1.0, 1.0 - std))
        else:
            confidence = 0.8  # Single model confidence
        
        # Determine risk level
        if final_prediction >= 0.7:
            risk_level = "high"
        elif final_prediction >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_probability": float(final_prediction),
            "risk_level": risk_level,
            "confidence": float(confidence),
            "models_used": list(predictions.keys()),
            "individual_predictions": {k: float(v) for k, v in predictions.items()}
        }
    
    def ensemble_drug_response(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Ensemble drug response predictions from all available models
        
        Args:
            features: Feature vector
        
        Returns:
            Ensemble result with confidence
        """
        predictions = {}
        
        # Get predictions from all models
        for model_type in ['nn', 'rf', 'xgb']:
            pred = self.predict_drug_response_single(features, model_type)
            if pred is not None:
                predictions[model_type] = pred
        
        if not predictions:
            logger.error("No drug response models available")
            return {
                "response_value": 0.0,
                "response_category": "unknown",
                "confidence": 0.0,
                "models_used": [],
                "individual_predictions": {}
            }
        
        # Check if we have metadata about best model
        metadata = self.model_loader.metadata.get('drug_response', {})
        best_model = metadata.get('best_model', '').replace('.pkl', '').replace('_drug_response', '')
        
        if best_model in predictions:
            # Use best model prediction
            final_prediction = predictions[best_model]
            logger.info(f"Using best model ({best_model}) for drug response: {final_prediction:.3f}")
        else:
            # Average all predictions
            final_prediction = np.mean(list(predictions.values()))
            logger.info(f"Averaging {len(predictions)} models for drug response: {final_prediction:.3f}")
        
        # Calculate confidence
        if len(predictions) > 1:
            std = np.std(list(predictions.values()))
            # Normalize std to confidence (assuming response is 0-1 range)
            confidence = max(0.0, min(1.0, 1.0 - std))
        else:
            confidence = 0.8
        
        # Categorize response
        if final_prediction >= 0.7:
            response_category = "excellent"
        elif final_prediction >= 0.5:
            response_category = "good"
        elif final_prediction >= 0.3:
            response_category = "moderate"
        else:
            response_category = "poor"
        
        return {
            "response_value": float(final_prediction),
            "response_category": response_category,
            "confidence": float(confidence),
            "models_used": list(predictions.keys()),
            "individual_predictions": {k: float(v) for k, v in predictions.items()}
        }
    
    def predict_from_file(self, content: bytes) -> Dict[str, Any]:
        """
        Complete prediction pipeline from raw file
        
        Args:
            content: Raw genomic file bytes (FASTA format)
        
        Returns:
            Complete analysis results
        """
        try:
            # Step 1: Extract features
            logger.info("Step 1/3: Extracting features...")
            features = self.extract_features(content)
            
            # Step 2: Disease risk prediction
            logger.info("Step 2/3: Predicting disease risk...")
            disease_risk = self.ensemble_disease_risk(features)
            
            # Step 3: Drug response prediction
            logger.info("Step 3/3: Predicting drug response...")
            drug_response = self.ensemble_drug_response(features)
            
            # Update statistics
            self.prediction_count += 1
            
            # Combine results
            result = {
                "success": True,
                "feature_count": len(features),
                "disease_risk": disease_risk,
                "drug_response": drug_response,
                "metadata": {
                    "models_loaded": sum(1 for v in self.model_loader.get_loaded_models().values() if v),
                    "total_models": 6,
                    "prediction_number": self.prediction_count
                }
            }
            
            logger.info("✅ Prediction complete")
            return result
        
        except Exception as e:
            logger.error(f"Prediction pipeline failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "feature_count": 0,
                "disease_risk": None,
                "drug_response": None
            }
    
    def get_statistics(self) -> Dict:
        """Get engine statistics"""
        return {
            "prediction_count": self.prediction_count,
            "models_loaded": self.model_loader.get_loaded_models(),
            "model_info": self.model_loader.get_model_info(),
            "is_ready": self.is_ready()
        }


if __name__ == "__main__":
    # Test prediction engine
    print("🧬 Testing Prediction Engine...")
    
    engine = PredictionEngine()
    
    print(f"\nEngine ready: {engine.is_ready()}")
    print(f"\nModels loaded:")
    for name, loaded in engine.model_loader.get_loaded_models().items():
        status = "✅" if loaded else "❌"
        print(f"  {status} {name}")
    
    # Test prediction with sample data
    test_fasta = b""">test_sequence
ATCGATCGATCGATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
ATCGATCGATCGATCGATCGATCGATCGATCG
"""
    
    print("\n🔬 Running prediction...")
    result = engine.predict_from_file(test_fasta)
    
    if result['success']:
        print("\n✅ Prediction successful!")
        print(f"\nDisease Risk:")
        dr = result['disease_risk']
        print(f"  Probability: {dr['risk_probability']:.3f}")
        print(f"  Level: {dr['risk_level']}")
        print(f"  Confidence: {dr['confidence']:.3f}")
        print(f"  Models used: {dr['models_used']}")
        
        print(f"\nDrug Response:")
        drg = result['drug_response']
        print(f"  Value: {drg['response_value']:.3f}")
        print(f"  Category: {drg['response_category']}")
        print(f"  Confidence: {drg['confidence']:.3f}")
        print(f"  Models used: {drg['models_used']}")
    else:
        print(f"\n❌ Prediction failed: {result.get('error')}")
