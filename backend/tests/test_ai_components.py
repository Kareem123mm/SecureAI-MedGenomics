"""
Test suite for AI components
"""
import pytest
import numpy as np
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.model_loader import ModelLoader
from ai.feature_extractor import GenomicFeatureExtractor
from ai.prediction_engine import PredictionEngine


class TestModelLoader:
    """Test model loading functionality"""
    
    def test_initialization(self):
        """Test model loader initialization"""
        loader = ModelLoader()
        assert loader is not None
        assert loader.models_dir.name == "models_export"
    
    def test_load_all_models(self):
        """Test loading all models"""
        loader = ModelLoader()
        models = loader.load_all_models()
        
        # Should attempt to load 6 models
        assert len(models) == 6
        
        # Check model names
        expected_models = [
            'disease_risk_nn', 'disease_risk_rf', 'disease_risk_xgb',
            'drug_response_nn', 'drug_response_rf', 'drug_response_xgb'
        ]
        for model_name in expected_models:
            assert model_name in models
    
    def test_get_input_size(self):
        """Test getting input size"""
        loader = ModelLoader()
        loader.load_metadata()
        
        input_size = loader.get_input_size()
        assert input_size == 587  # Expected from metadata


class TestFeatureExtractor:
    """Test feature extraction"""
    
    def test_initialization(self):
        """Test feature extractor initialization"""
        extractor = GenomicFeatureExtractor(expected_features=587)
        assert extractor is not None
        assert extractor.expected_features == 587
    
    def test_parse_fasta(self):
        """Test FASTA parsing"""
        extractor = GenomicFeatureExtractor()
        
        fasta_content = b">seq1\nATCGATCG\n>seq2\nGCTAGCTA\n"
        sequences = extractor.parse_fasta(fasta_content)
        
        assert len(sequences) == 2
        assert sequences[0][0] == "seq1"
        assert sequences[0][1] == "ATCGATCG"
    
    def test_calculate_gc_content(self):
        """Test GC content calculation"""
        extractor = GenomicFeatureExtractor()
        
        # 50% GC content
        sequence = "ATGC"
        gc = extractor.calculate_gc_content(sequence)
        assert gc == 50.0
    
    def test_extract_kmers(self):
        """Test k-mer extraction"""
        extractor = GenomicFeatureExtractor()
        
        sequence = "ATCGATCG"
        kmers = extractor.extract_kmers(sequence, k=3)
        
        assert len(kmers) > 0
        assert "ATC" in kmers
        assert "TCG" in kmers
    
    def test_feature_extraction(self):
        """Test complete feature extraction"""
        extractor = GenomicFeatureExtractor(expected_features=587)
        
        fasta_content = b">test\nATCGATCGATCGATCG\n"
        features = extractor.extract_features_from_file(fasta_content)
        
        assert features is not None
        assert len(features) == 587
        assert extractor.validate_features(features)
    
    def test_feature_validation(self):
        """Test feature validation"""
        extractor = GenomicFeatureExtractor(expected_features=587)
        
        # Valid features
        valid_features = np.random.rand(587)
        assert extractor.validate_features(valid_features) == True
        
        # Invalid size
        invalid_features = np.random.rand(100)
        assert extractor.validate_features(invalid_features) == False
        
        # NaN values
        nan_features = np.full(587, np.nan)
        assert extractor.validate_features(nan_features) == False


class TestPredictionEngine:
    """Test prediction engine"""
    
    def test_initialization(self):
        """Test prediction engine initialization"""
        engine = PredictionEngine()
        assert engine is not None
        assert engine.model_loader is not None
        assert engine.feature_extractor is not None
    
    def test_extract_features(self):
        """Test feature extraction through engine"""
        engine = PredictionEngine()
        
        fasta_content = b">test\nATCGATCGATCGATCG\n"
        features = engine.extract_features(fasta_content)
        
        assert features is not None
        assert len(features) == 587
    
    def test_predict_from_file(self):
        """Test complete prediction pipeline"""
        engine = PredictionEngine()
        
        if not engine.is_ready():
            pytest.skip("No models loaded")
        
        fasta_content = b">test\nATCGATCGATCGATCG\n"
        result = engine.predict_from_file(fasta_content)
        
        assert result is not None
        assert "success" in result
        
        if result["success"]:
            assert "disease_risk" in result
            assert "drug_response" in result
    
    def test_ensemble_disease_risk(self):
        """Test disease risk ensemble"""
        engine = PredictionEngine()
        
        if not engine.is_ready():
            pytest.skip("No models loaded")
        
        # Random features
        features = np.random.rand(587).astype(np.float32)
        result = engine.ensemble_disease_risk(features)
        
        assert "risk_probability" in result
        assert "risk_level" in result
        assert "confidence" in result
        assert 0 <= result["risk_probability"] <= 1
    
    def test_ensemble_drug_response(self):
        """Test drug response ensemble"""
        engine = PredictionEngine()
        
        if not engine.is_ready():
            pytest.skip("No models loaded")
        
        # Random features
        features = np.random.rand(587).astype(np.float32)
        result = engine.ensemble_drug_response(features)
        
        assert "response_value" in result
        assert "response_category" in result
        assert "confidence" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
