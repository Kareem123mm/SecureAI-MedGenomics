"""
Test suite for security layers
"""
import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from security.genetic_algo.optimizer import GeneticSecurityOptimizer
from security.intrusion.ids import IntrusionDetectionSystem
from security.aml_defense.defender import AMLDefender
from security_validator import SecurityPipeline


class TestGeneticOptimizer:
    """Test genetic algorithm optimizer"""
    
    def test_initialization(self):
        """Test optimizer initialization"""
        optimizer = GeneticSecurityOptimizer(
            population_size=10,
            generations=5
        )
        assert optimizer is not None
        assert optimizer.population_size == 10
        assert optimizer.generations == 5
    
    def test_create_individual(self):
        """Test individual creation"""
        optimizer = GeneticSecurityOptimizer()
        individual = optimizer._create_random_individual()
        
        assert individual is not None
        assert "aml_threshold" in individual.parameters
        assert "ids_sensitivity" in individual.parameters
        assert 0.5 <= individual.parameters["aml_threshold"] <= 0.99
    
    def test_fitness_calculation(self):
        """Test fitness calculation"""
        optimizer = GeneticSecurityOptimizer()
        individual = optimizer._create_random_individual()
        
        fitness = optimizer._calculate_fitness(individual)
        assert fitness >= 0
        assert isinstance(fitness, float)
    
    def test_optimization(self):
        """Test full optimization run"""
        optimizer = GeneticSecurityOptimizer(
            population_size=10,
            generations=5
        )
        
        best_params = optimizer.optimize()
        
        assert best_params is not None
        assert "aml_threshold" in best_params
        assert "ids_sensitivity" in best_params


class TestIntrusionDetection:
    """Test IDS functionality"""
    
    def test_initialization(self):
        """Test IDS initialization"""
        ids = IntrusionDetectionSystem(sensitivity="HIGH")
        assert ids is not None
        assert ids.is_active() == True
    
    def test_threat_patterns(self):
        """Test threat pattern loading"""
        ids = IntrusionDetectionSystem()
        patterns = ids.threat_patterns
        
        assert len(patterns) > 0
        # Check for common patterns
        pattern_strings = [p.pattern for p in patterns]
        assert any("../" in p for p in pattern_strings)  # Path traversal
    
    @pytest.mark.asyncio
    async def test_scan_clean_content(self):
        """Test scanning clean content"""
        ids = IntrusionDetectionSystem()
        
        clean_content = b">sequence1\nATCGATCGATCG\n"
        threat_detected = await ids.scan_content(
            content=clean_content,
            filename="clean.fasta"
        )
        
        assert threat_detected == False
    
    @pytest.mark.asyncio
    async def test_scan_malicious_content(self):
        """Test scanning malicious content"""
        ids = IntrusionDetectionSystem()
        
        malicious_content = b"<script>alert('XSS')</script>"
        threat_detected = await ids.scan_content(
            content=malicious_content,
            filename="malicious.txt"
        )
        
        assert threat_detected == True
    
    @pytest.mark.asyncio
    async def test_sql_injection_detection(self):
        """Test SQL injection detection"""
        ids = IntrusionDetectionSystem()
        
        sql_injection = b"' OR '1'='1"
        threat_detected = await ids.scan_content(
            content=sql_injection,
            filename="test.txt"
        )
        
        assert threat_detected == True
    
    def test_statistics(self):
        """Test statistics tracking"""
        ids = IntrusionDetectionSystem()
        stats = ids.get_statistics()
        
        assert "total_scans" in stats
        assert "threats_detected" in stats


class TestAMLDefender:
    """Test AML defense system"""
    
    def test_initialization(self):
        """Test AML defender initialization"""
        defender = AMLDefender(threshold=0.85)
        assert defender is not None
        assert defender.is_ready() == True
    
    def test_feature_extraction(self):
        """Test feature extraction from data"""
        defender = AMLDefender(feature_size=256)
        
        test_data = b"ATCGATCGATCG" * 100
        features = defender.extract_features(test_data)
        
        assert features is not None
        assert len(features) == 256
    
    def test_entropy_calculation(self):
        """Test entropy calculation"""
        defender = AMLDefender()
        
        # Low entropy data
        low_entropy = b"AAAA" * 100
        entropy_low = defender.calculate_entropy(low_entropy)
        
        # High entropy data
        import random
        high_entropy = bytes([random.randint(0, 255) for _ in range(400)])
        entropy_high = defender.calculate_entropy(high_entropy)
        
        assert entropy_low < entropy_high
    
    @pytest.mark.asyncio
    async def test_detect_adversarial(self):
        """Test adversarial detection"""
        defender = AMLDefender()
        
        # Normal data
        normal_data = b">seq\nATCGATCG\n" * 50
        is_adversarial = await defender.detect_adversarial_file(normal_data)
        
        # Should be detected or not based on model
        assert isinstance(is_adversarial, bool)
    
    def test_statistics(self):
        """Test statistics"""
        defender = AMLDefender()
        stats = defender.get_statistics()
        
        assert "total_checks" in stats
        assert "adversarial_detected" in stats


class TestSecurityPipeline:
    """Test integrated security pipeline"""
    
    def test_initialization(self):
        """Test pipeline initialization"""
        pipeline = SecurityPipeline()
        assert pipeline is not None
    
    def test_layer_status(self):
        """Test layer status"""
        pipeline = SecurityPipeline()
        status = pipeline.get_status()
        
        assert "ready" in status
        assert "layers" in status
        assert "security_score" in status
    
    @pytest.mark.asyncio
    async def test_full_security_scan(self):
        """Test complete security scan"""
        pipeline = SecurityPipeline()
        
        if not pipeline.is_ready():
            pytest.skip("Pipeline not ready")
        
        test_data = b">test\nATCGATCGATCG\n"
        report = await pipeline.full_security_scan(
            content=test_data,
            filename="test.fasta",
            job_id="test-123"
        )
        
        assert report is not None
        assert "overall_passed" in report
        assert "layers" in report
        assert "security_score" in report
    
    @pytest.mark.asyncio
    async def test_security_scan_malicious(self):
        """Test security scan with malicious content"""
        pipeline = SecurityPipeline()
        
        if not pipeline.is_ready():
            pytest.skip("Pipeline not ready")
        
        malicious_data = b"<script>alert('XSS')</script>"
        report = await pipeline.full_security_scan(
            content=malicious_data,
            filename="malicious.txt"
        )
        
        # Should fail security
        assert report["overall_passed"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
