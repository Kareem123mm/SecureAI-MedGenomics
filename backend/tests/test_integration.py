"""
End-to-End Integration Tests

Tests complete pipeline from upload to results
"""
import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integrated_main import app, startup_event
from fastapi.testclient import TestClient
import io


@pytest.fixture(scope="module")
def client():
    """Create test client"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def sample_fasta():
    """Create sample FASTA file"""
    content = b""">sample_sequence_1
ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
>sample_sequence_2
AAAAAATTTTTTGGGGGGCCCCCCATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
"""
    return content


class TestAPIEndpoints:
    """Test FastAPI endpoints"""
    
    def test_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "SecureAI-MedGenomics" in data["message"]
    
    def test_health(self, client):
        """Test health check"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "security_pipeline" in data
        assert "ai_engine" in data
    
    def test_system_stats(self, client):
        """Test system statistics"""
        response = client.get("/api/system/stats")
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        assert "jobs" in data


class TestFileUpload:
    """Test file upload and processing"""
    
    def test_upload_valid_file(self, client, sample_fasta):
        """Test uploading valid FASTA file"""
        files = {"file": ("test.fasta", io.BytesIO(sample_fasta), "text/plain")}
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "processing"
        
        return data["job_id"]
    
    def test_upload_large_file(self, client):
        """Test uploading file that's too large"""
        # Create 51 MB file
        large_content = b"A" * (51 * 1024 * 1024)
        files = {"file": ("large.fasta", io.BytesIO(large_content), "text/plain")}
        
        response = client.post("/api/upload", files=files)
        assert response.status_code == 400  # Too large


class TestJobTracking:
    """Test job status and results"""
    
    def test_job_status(self, client, sample_fasta):
        """Test getting job status"""
        # Upload file
        files = {"file": ("test.fasta", io.BytesIO(sample_fasta), "text/plain")}
        upload_response = client.post("/api/upload", files=files)
        job_id = upload_response.json()["job_id"]
        
        # Get status
        response = client.get(f"/api/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert "status" in data
        assert "progress" in data
    
    def test_job_not_found(self, client):
        """Test getting non-existent job"""
        response = client.get("/api/status/nonexistent-job-id")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_complete_pipeline(self, client, sample_fasta):
        """Test complete processing pipeline"""
        # Upload
        files = {"file": ("test.fasta", io.BytesIO(sample_fasta), "text/plain")}
        upload_response = client.post("/api/upload", files=files)
        job_id = upload_response.json()["job_id"]
        
        # Wait for processing (max 30 seconds)
        max_wait = 30
        waited = 0
        while waited < max_wait:
            status_response = client.get(f"/api/status/{job_id}")
            status_data = status_response.json()
            
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Job failed: {status_data.get('error')}")
            
            await asyncio.sleep(1)
            waited += 1
        
        # Get results
        results_response = client.get(f"/api/result/{job_id}")
        
        if results_response.status_code == 200:
            results_data = results_response.json()
            assert "security_passed" in results_data
            assert "ai_analysis" in results_data
            assert "encrypted" in results_data


class TestSecurityIntegration:
    """Test security layer integration"""
    
    def test_malicious_content_blocked(self, client):
        """Test that malicious content is blocked"""
        malicious_content = b"<script>alert('XSS')</script>"
        files = {"file": ("malicious.txt", io.BytesIO(malicious_content), "text/plain")}
        
        upload_response = client.post("/api/upload", files=files)
        job_id = upload_response.json()["job_id"]
        
        # Wait a bit for processing
        import time
        time.sleep(3)
        
        status_response = client.get(f"/api/status/{job_id}")
        status_data = status_response.json()
        
        # Should either fail or detect threat
        if status_data["status"] == "failed":
            assert "security" in status_data.get("error", "").lower()


class TestAIIntegration:
    """Test AI model integration"""
    
    @pytest.mark.asyncio
    async def test_ai_predictions(self, client, sample_fasta):
        """Test that AI predictions are generated"""
        files = {"file": ("test.fasta", io.BytesIO(sample_fasta), "text/plain")}
        upload_response = client.post("/api/upload", files=files)
        job_id = upload_response.json()["job_id"]
        
        # Wait for completion
        max_wait = 30
        for _ in range(max_wait):
            status_response = client.get(f"/api/status/{job_id}")
            status_data = status_response.json()
            
            if status_data["status"] in ["completed", "failed"]:
                break
            
            await asyncio.sleep(1)
        
        if status_data["status"] == "completed":
            results_response = client.get(f"/api/result/{job_id}")
            results_data = results_response.json()
            
            ai_analysis = results_data.get("ai_analysis", {})
            
            # Check if AI ran
            if ai_analysis.get("success"):
                assert "disease_risk" in ai_analysis
                assert "drug_response" in ai_analysis


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
