"""
Unified Model Loader for SecureAI-MedGenomics

Supports:
- PyTorch neural networks (.pth)
- scikit-learn models (.pkl)
- XGBoost models (.pkl)

Handles all 6 AI models:
- Disease Risk: nn, rf, xgb
- Drug Response: nn, rf, xgb
"""

import torch
import torch.nn as nn
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple
import logging
import json

logger = logging.getLogger(__name__)


class DiseaseRiskNN(nn.Module):
    """
    PyTorch Neural Network for Disease Risk Prediction
    Architecture: 587 -> 256 -> 128 -> 64 -> 1 (binary classification)
    """
    def __init__(self, input_size: int = 587):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.network(x)


class DrugResponseNN(nn.Module):
    """
    PyTorch Neural Network for Drug Response Prediction
    Architecture: 587 -> 256 -> 128 -> 64 -> 1 (regression)
    """
    def __init__(self, input_size: int = 587):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.network(x)


class ModelLoader:
    """
    Unified loader for all AI models in the system
    """
    
    def __init__(self, models_dir: Union[str, Path] = None):
        """
        Initialize model loader
        
        Args:
            models_dir: Path to directory containing models
        """
        if models_dir is None:
            # Default to models_export directory
            self.models_dir = Path(__file__).parent.parent.parent / "models_export"
        else:
            self.models_dir = Path(models_dir)
        
        if not self.models_dir.exists():
            logger.warning(f"Models directory not found: {self.models_dir}")
        
        # Storage for loaded models
        self.models = {}
        self.metadata = {}
        self.feature_info = {}
        
        # Device for PyTorch models
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"ModelLoader initialized with device: {self.device}")
        logger.info(f"Models directory: {self.models_dir}")
    
    def load_metadata(self) -> Dict:
        """Load model metadata from JSON file"""
        metadata_path = self.models_dir / "model_metadata.json"
        
        if not metadata_path.exists():
            logger.warning("model_metadata.json not found")
            return {}
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.metadata = metadata
            logger.info("Loaded model metadata successfully")
            return metadata
        
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            return {}
    
    def load_feature_info(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load feature names and selected genes
        
        Returns:
            (feature_names, selected_genes)
        """
        try:
            # Load feature names
            feature_names_path = self.models_dir / "feature_names_genomic.npy"
            if feature_names_path.exists():
                feature_names = np.load(feature_names_path, allow_pickle=True)
                self.feature_info['names'] = feature_names
                logger.info(f"Loaded {len(feature_names)} feature names")
            else:
                feature_names = None
                logger.warning("feature_names_genomic.npy not found")
            
            # Load selected genes
            selected_genes_path = self.models_dir / "selected_genes.npy"
            if selected_genes_path.exists():
                selected_genes = np.load(selected_genes_path, allow_pickle=True)
                self.feature_info['selected_genes'] = selected_genes
                logger.info(f"Loaded {len(selected_genes)} selected genes")
            else:
                selected_genes = None
                logger.warning("selected_genes.npy not found")
            
            return feature_names, selected_genes
        
        except Exception as e:
            logger.error(f"Failed to load feature info: {e}")
            return None, None
    
    def load_pytorch_model(
        self,
        model_name: str,
        model_class: nn.Module,
        input_size: int = 587
    ) -> Optional[nn.Module]:
        """
        Load PyTorch model
        
        Args:
            model_name: Name of model file (e.g., 'nn_disease_risk.pth')
            model_class: PyTorch model class
            input_size: Number of input features
        
        Returns:
            Loaded PyTorch model or None
        """
        model_path = self.models_dir / model_name
        
        if not model_path.exists():
            logger.error(f"PyTorch model not found: {model_path}")
            return None
        
        try:
            # Initialize model
            model = model_class(input_size=input_size)
            
            # Load state dict
            state_dict = torch.load(model_path, map_location=self.device)
            
            # Handle different save formats
            if isinstance(state_dict, dict) and 'model_state_dict' in state_dict:
                state_dict = state_dict['model_state_dict']
            
            # Try strict loading first, fall back to non-strict if architecture mismatch
            try:
                model.load_state_dict(state_dict, strict=True)
                logger.info(f"✅ Loaded PyTorch model: {model_name} (exact match)")
            except RuntimeError as e:
                if "size mismatch" in str(e) or "Missing key" in str(e):
                    logger.warning(f"Architecture mismatch for {model_name}, skipping (model needs retraining)")
                    return None
                else:
                    raise
            
            # Set to evaluation mode
            model.eval()
            model.to(self.device)
            
            return model
        
        except Exception as e:
            logger.error(f"Failed to load PyTorch model {model_name}: {e}")
            return None
    
    def load_sklearn_model(self, model_name: str) -> Optional[Any]:
        """
        Load scikit-learn or XGBoost model
        
        Args:
            model_name: Name of model file (e.g., 'rf_disease_risk.pkl')
        
        Returns:
            Loaded model or None
        """
        model_path = self.models_dir / model_name
        
        if not model_path.exists():
            logger.error(f"sklearn/XGBoost model not found: {model_path}")
            return None
        
        try:
            import warnings
            # Suppress sklearn version warnings during model loading
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=UserWarning)
                warnings.filterwarnings('ignore', message='.*InconsistentVersionWarning.*')
                
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            
            logger.info(f"✅ Loaded sklearn/XGBoost model: {model_name}")
            return model
        
        except Exception as e:
            # Check if it's a corrupt file issue
            if "invalid load key" in str(e) or "unsupported pickle protocol" in str(e):
                logger.error(f"Corrupted pickle file {model_name}, skipping (needs regeneration)")
            else:
                logger.error(f"Failed to load sklearn model {model_name}: {e}")
            return None
    
    def load_all_models(self) -> Dict[str, Any]:
        """
        Load all 6 AI models
        
        Returns:
            Dictionary of loaded models
        """
        logger.info("Loading all AI models...")
        
        # Load metadata and feature info
        self.load_metadata()
        self.load_feature_info()
        
        # Get input size from metadata or default
        input_size = 587
        if self.metadata:
            disease_meta = self.metadata.get('disease_risk', {})
            input_size = disease_meta.get('input_features', 587)
        
        # Load Disease Risk models
        self.models['disease_risk_nn'] = self.load_pytorch_model(
            'nn_disease_risk.pth',
            DiseaseRiskNN,
            input_size=input_size
        )
        self.models['disease_risk_rf'] = self.load_sklearn_model('rf_disease_risk.pkl')
        self.models['disease_risk_xgb'] = self.load_sklearn_model('xgb_disease_risk.pkl')
        
        # Load Drug Response models
        self.models['drug_response_nn'] = self.load_pytorch_model(
            'nn_drug_response.pth',
            DrugResponseNN,
            input_size=input_size
        )
        self.models['drug_response_rf'] = self.load_sklearn_model('rf_drug_response.pkl')
        self.models['drug_response_xgb'] = self.load_sklearn_model('xgb_drug_response.pkl')
        
        # Count successfully loaded models
        loaded_count = sum(1 for model in self.models.values() if model is not None)
        
        logger.info(f"✅ Successfully loaded {loaded_count}/6 models")
        
        # Log which models failed to load
        for name, model in self.models.items():
            if model is None:
                logger.warning(f"⚠️ Model not loaded: {name}")
        
        return self.models
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Get a specific loaded model
        
        Args:
            model_name: Name of model (e.g., 'disease_risk_nn')
        
        Returns:
            Model or None if not loaded
        """
        return self.models.get(model_name)
    
    def is_loaded(self, model_name: str) -> bool:
        """Check if a model is loaded"""
        return model_name in self.models and self.models[model_name] is not None
    
    def get_loaded_models(self) -> Dict[str, bool]:
        """Get status of all models"""
        return {
            name: (model is not None)
            for name, model in self.models.items()
        }
    
    def get_input_size(self) -> int:
        """Get expected input feature size"""
        if self.metadata:
            return self.metadata.get('disease_risk', {}).get('input_features', 587)
        return 587
    
    def validate_input(self, features: np.ndarray) -> bool:
        """
        Validate input features
        
        Args:
            features: Feature array
        
        Returns:
            True if valid, False otherwise
        """
        expected_size = self.get_input_size()
        
        if features.shape[-1] != expected_size:
            logger.error(
                f"Invalid input size: expected {expected_size}, got {features.shape[-1]}"
            )
            return False
        
        # Check for NaN or Inf
        if np.any(np.isnan(features)) or np.any(np.isinf(features)):
            logger.error("Input contains NaN or Inf values")
            return False
        
        return True
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        info = {
            "models_directory": str(self.models_dir),
            "device": str(self.device),
            "input_features": self.get_input_size(),
            "loaded_models": self.get_loaded_models(),
            "metadata": self.metadata,
            "feature_count": len(self.feature_info.get('names', [])),
            "selected_genes_count": len(self.feature_info.get('selected_genes', []))
        }
        return info


if __name__ == "__main__":
    # Test model loading
    print("🧬 Testing Model Loader...")
    
    loader = ModelLoader()
    models = loader.load_all_models()
    
    print("\n📊 Model Loading Results:")
    for name, loaded in loader.get_loaded_models().items():
        status = "✅" if loaded else "❌"
        print(f"  {status} {name}")
    
    print("\n📈 Model Info:")
    info = loader.get_model_info()
    print(f"  Input Features: {info['input_features']}")
    print(f"  Feature Count: {info['feature_count']}")
    print(f"  Selected Genes: {info['selected_genes_count']}")
    print(f"  Device: {info['device']}")
