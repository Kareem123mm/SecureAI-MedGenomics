"""
Metrics Collector for Security Monitoring
Exports metrics to Prometheus/Grafana
"""

import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
from prometheus_client import Counter, Gauge, Histogram, Summary
from collections import defaultdict
import threading


logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collects and exports security metrics
    """
    
    def __init__(self):
        # Prometheus metrics
        self.request_counter = Counter(
            'api_requests_total',
            'Total number of API requests',
            ['endpoint', 'method', 'status']
        )
        
        self.aml_detections_counter = Counter(
            'aml_detections_total',
            'Total number of adversarial inputs detected'
        )
        
        self.intrusion_attempts_counter = Counter(
            'intrusion_attempts_total',
            'Total number of intrusion attempts detected',
            ['severity']
        )
        
        self.encryption_operations_counter = Counter(
            'encryption_operations_total',
            'Total number of encryption operations',
            ['operation_type']
        )
        
        self.file_uploads_counter = Counter(
            'file_uploads_total',
            'Total number of file uploads',
            ['file_type']
        )
        
        self.response_time_histogram = Histogram(
            'response_time_seconds',
            'API response time in seconds',
            ['endpoint']
        )
        
        self.security_score_gauge = Gauge(
            'security_score',
            'Current security score (0-100)'
        )
        
        self.active_jobs_gauge = Gauge(
            'active_jobs',
            'Number of currently active jobs'
        )
        
        # In-memory metrics (for quick access)
        self.metrics = {
            "total_requests": 0,
            "aml_detections": 0,
            "intrusion_attempts": 0,
            "encryption_operations": 0,
            "file_uploads": 0,
            "errors": 0,
            "avg_response_time": 0.0,
            "security_score": 100.0,
            "threat_level": "low"
        }
        
        # Thread-safe lock
        self.lock = threading.Lock()
        
        # Start time
        self.start_time = time.time()
        
        logger.info("Metrics collector initialized")
    
    def is_collecting(self) -> bool:
        """Check if metrics collection is active"""
        return True
    
    def increment(self, metric_name: str, value: int = 1, labels: Optional[Dict] = None):
        """Increment a counter metric"""
        with self.lock:
            if metric_name in self.metrics:
                self.metrics[metric_name] += value
            
            # Update Prometheus metrics
            if metric_name == "aml_detections":
                self.aml_detections_counter.inc(value)
            elif metric_name == "intrusion_attempts":
                severity = labels.get("severity", "unknown") if labels else "unknown"
                self.intrusion_attempts_counter.labels(severity=severity).inc(value)
            elif metric_name == "encryption_operations":
                op_type = labels.get("operation_type", "unknown") if labels else "unknown"
                self.encryption_operations_counter.labels(operation_type=op_type).inc(value)
            elif metric_name == "errors":
                self.metrics["errors"] += value
    
    def record_request(
        self,
        endpoint: str,
        method: str,
        status: int,
        response_time: float
    ):
        """Record API request metrics"""
        with self.lock:
            self.metrics["total_requests"] += 1
            
            # Update average response time
            total = self.metrics["total_requests"]
            current_avg = self.metrics["avg_response_time"]
            self.metrics["avg_response_time"] = (
                (current_avg * (total - 1) + response_time) / total
            )
            
            # Update Prometheus metrics
            self.request_counter.labels(
                endpoint=endpoint,
                method=method,
                status=str(status)
            ).inc()
            
            self.response_time_histogram.labels(endpoint=endpoint).observe(response_time)
    
    def record_upload(self, job_id: str, filename: str, file_size: int):
        """Record file upload metrics"""
        with self.lock:
            self.metrics["file_uploads"] += 1
            
            # Determine file type
            if filename.endswith(('.fasta', '.fa')):
                file_type = 'fasta'
            elif filename.endswith('.vcf'):
                file_type = 'vcf'
            elif filename.endswith('.txt'):
                file_type = 'txt'
            else:
                file_type = 'other'
            
            self.file_uploads_counter.labels(file_type=file_type).inc()
    
    def update_security_score(self, score: float):
        """Update security score (0-100)"""
        with self.lock:
            self.metrics["security_score"] = max(0.0, min(100.0, score))
            self.security_score_gauge.set(score)
            
            # Update threat level based on score
            if score >= 90:
                self.metrics["threat_level"] = "low"
            elif score >= 70:
                self.metrics["threat_level"] = "medium"
            elif score >= 50:
                self.metrics["threat_level"] = "high"
            else:
                self.metrics["threat_level"] = "critical"
    
    def update_active_jobs(self, count: int):
        """Update active jobs count"""
        with self.lock:
            self.active_jobs_gauge.set(count)
    
    def get_current_metrics(self) -> Dict:
        """Get current metrics snapshot"""
        with self.lock:
            return {
                **self.metrics,
                "uptime_seconds": int(time.time() - self.start_time),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def export_final_metrics(self):
        """Export final metrics before shutdown"""
        logger.info("Exporting final metrics...")
        metrics = self.get_current_metrics()
        
        # Log summary
        logger.info(f"Final metrics: {metrics}")
        
        # Could save to file or database here
        return metrics


if __name__ == "__main__":
    # Test
    collector = MetricsCollector()
    
    # Simulate some activity
    collector.increment("aml_detections", 5)
    collector.increment("intrusion_attempts", 3, {"severity": "high"})
    collector.increment("encryption_operations", 10, {"operation_type": "cryfa"})
    collector.record_request("/api/upload", "POST", 200, 0.5)
    collector.record_upload("job123", "test.fasta", 1024)
    collector.update_security_score(95.5)
    
    print("📊 Metrics:")
    print(collector.get_current_metrics())
