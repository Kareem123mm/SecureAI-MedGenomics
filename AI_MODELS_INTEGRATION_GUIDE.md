# 🤖 AI Models Integration Guide

**How to Add 6 AI Models to SecureAI-MedGenomics**

Version: 1.0  
Date: November 5, 2025  
Difficulty: ⭐⭐⭐ (Easy to Moderate)

---

## ✅ Good News: Your System is Ready!

Your platform **already has the infrastructure** needed to integrate multiple AI models:

### **What You Already Have:**

✅ **Backend Framework**: FastAPI with async support  
✅ **AI Pipeline**: `analyze_genomic_data()` function exists  
✅ **Feature Extraction**: K-mer extraction (3-mers, 21-mers)  
✅ **Sequence Parsing**: FASTA/FASTQ parsing working  
✅ **Database Storage**: SQLite with `analysis_results` column  
✅ **Frontend Display**: Dynamic results rendering  
✅ **Processing Time Tracking**: Layer timing infrastructure  

---

## 📊 Integration Complexity Assessment

| Task | Difficulty | Time Estimate | Status |
|------|------------|---------------|---------|
| **Model Loading** | Easy ⭐ | 1 hour | Infrastructure ready |
| **Feature Preparation** | Easy ⭐ | 2 hours | Partially done |
| **Model Inference** | Easy ⭐ | 3 hours | Straightforward |
| **Pipeline Integration** | Moderate ⭐⭐ | 4 hours | Need modifications |
| **Frontend Display** | Easy ⭐ | 2 hours | Dynamic already |
| **Testing** | Moderate ⭐⭐ | 4 hours | Validation needed |
| **TOTAL** | **Easy-Moderate** | **16 hours** | **2 days work** |

---

## 🎯 Three Integration Strategies

### **Strategy 1: Sequential Execution (Simplest)**

**Best for**: Small models, CPU-only, prototyping

```python
# Run models one after another
results = {}
results['model1'] = model1.predict(features)  # 100ms
results['model2'] = model2.predict(features)  # 150ms
results['model3'] = model3.predict(features)  # 120ms
results['model4'] = model4.predict(features)  # 200ms
results['model5'] = model5.predict(features)  # 180ms
results['model6'] = model6.predict(features)  # 100ms

Total time: 850ms (sum of all)
```

**Pros**:
- Simple to implement ✅
- Low memory usage ✅
- Easy to debug ✅

**Cons**:
- Slower (sum of all models) ❌
- Blocks processing ❌

---

### **Strategy 2: Parallel Execution (Fastest)**

**Best for**: GPU available, production deployment

```python
import asyncio

# Run all models simultaneously
async def run_all_models(features):
    tasks = [
        asyncio.create_task(run_model1(features)),
        asyncio.create_task(run_model2(features)),
        asyncio.create_task(run_model3(features)),
        asyncio.create_task(run_model4(features)),
        asyncio.create_task(run_model5(features)),
        asyncio.create_task(run_model6(features))
    ]
    
    results = await asyncio.gather(*tasks)
    return results

Total time: 200ms (max of all models)
```

**Pros**:
- Fastest (3-4x speedup) ✅
- Efficient GPU usage ✅
- Better UX (faster results) ✅

**Cons**:
- Higher memory (all models in RAM) ❌
- More complex code ❌
- Requires GPU for best performance ❌

---

### **Strategy 3: On-Demand Loading (Memory Efficient)**

**Best for**: Large models, limited RAM, cloud deployment

```python
def run_model_on_demand(model_name, features):
    # Load model
    model = load_model(model_name)  # 500ms
    
    # Predict
    result = model.predict(features)  # 100ms
    
    # Unload model
    del model
    torch.cuda.empty_cache()  # Free GPU memory
    
    return result

Total time: 3600ms (6 models × 600ms)
Memory: Low (only 1 model at a time)
```

**Pros**:
- Low memory usage ✅
- Can handle large models ✅
- Flexible (load only needed models) ✅

**Cons**:
- Slowest (loading overhead) ❌
- More disk I/O ❌

---

## 🔧 Step-by-Step Integration Guide

### **STEP 1: Prepare Model Files**

**Expected file structure:**
```
backend/
├── models/
│   ├── model1_species_classifier.pth      # Species prediction
│   ├── model2_quality_scorer.pth          # Quality assessment
│   ├── model3_mutation_detector.pth       # Variant calling
│   ├── model4_contamination_checker.pth   # Contamination detection
│   ├── model5_gc_predictor.pth            # GC content prediction
│   └── model6_length_estimator.pth        # Sequence length analysis
├── model_configs/
│   ├── model1_config.json
│   ├── model2_config.json
│   └── ...
└── real_main.py
```

**Model requirements:**
- Format: PyTorch (.pth), TensorFlow (.h5), ONNX (.onnx), or scikit-learn (.pkl)
- Size: Preferably < 100MB per model (for fast loading)
- Input: Feature vectors (should match your k-mer extraction)
- Output: Predictions + confidence scores

---

### **STEP 2: Create Model Manager Class**

**File**: `backend/ai_models/model_manager.py`

```python
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
import json
import time

class AIModelManager:
    """
    Manages multiple AI models for genomic analysis
    Handles loading, inference, and result aggregation
    """
    
    def __init__(self, models_dir="models/", device="cpu"):
        self.models_dir = Path(models_dir)
        self.device = device
        self.models = {}
        self.configs = {}
        
        # Load all models at startup
        self.load_all_models()
    
    def load_all_models(self):
        """
        Load all 6 AI models into memory
        Call this once at backend startup
        """
        
        print("Loading AI models...")
        start_time = time.time()
        
        model_files = [
            ("species_classifier", "model1_species_classifier.pth"),
            ("quality_scorer", "model2_quality_scorer.pth"),
            ("mutation_detector", "model3_mutation_detector.pth"),
            ("contamination_checker", "model4_contamination_checker.pth"),
            ("gc_predictor", "model5_gc_predictor.pth"),
            ("length_estimator", "model6_length_estimator.pth")
        ]
        
        for model_name, model_file in model_files:
            try:
                model_path = self.models_dir / model_file
                config_path = self.models_dir / f"../model_configs/{model_name}_config.json"
                
                # Load configuration
                with open(config_path, 'r') as f:
                    self.configs[model_name] = json.load(f)
                
                # Load model
                model = torch.load(model_path, map_location=self.device)
                model.eval()  # Set to evaluation mode
                self.models[model_name] = model
                
                print(f"  ✓ Loaded {model_name}")
                
            except Exception as e:
                print(f"  ✗ Failed to load {model_name}: {e}")
                self.models[model_name] = None
        
        elapsed = time.time() - start_time
        print(f"All models loaded in {elapsed:.2f}s")
    
    def predict_all(self, features):
        """
        Run all 6 models on the input features
        
        Args:
            features: Dict containing:
                - 'sequence': Raw DNA sequence
                - 'kmers': K-mer frequencies
                - 'gc_content': GC percentage
                - 'length': Sequence length
        
        Returns:
            Dict with all model predictions
        """
        
        results = {}
        timing = {}
        
        for model_name, model in self.models.items():
            if model is None:
                results[model_name] = {"error": "Model not loaded"}
                continue
            
            try:
                start = time.time()
                
                # Prepare model-specific features
                model_features = self.prepare_features(features, model_name)
                
                # Run inference
                with torch.no_grad():
                    prediction = model(model_features)
                
                # Post-process results
                results[model_name] = self.post_process(prediction, model_name)
                
                timing[model_name] = f"{(time.time() - start) * 1000:.1f}ms"
                
            except Exception as e:
                results[model_name] = {"error": str(e)}
                timing[model_name] = "0ms"
        
        return {
            "predictions": results,
            "timing": timing,
            "total_time": sum([float(t.replace('ms', '')) for t in timing.values()])
        }
    
    async def predict_all_parallel(self, features):
        """
        Run all 6 models in parallel (if GPU available)
        3-4x faster than sequential
        """
        
        import asyncio
        
        async def run_model(model_name, model):
            if model is None:
                return {"error": "Model not loaded"}
            
            try:
                start = time.time()
                
                # Prepare features
                model_features = self.prepare_features(features, model_name)
                
                # Run inference (in thread to avoid blocking)
                loop = asyncio.get_event_loop()
                prediction = await loop.run_in_executor(
                    None, 
                    lambda: model(model_features)
                )
                
                # Post-process
                result = self.post_process(prediction, model_name)
                result['time'] = f"{(time.time() - start) * 1000:.1f}ms"
                
                return result
                
            except Exception as e:
                return {"error": str(e)}
        
        # Create tasks for all models
        tasks = [
            run_model(name, model) 
            for name, model in self.models.items()
        ]
        
        # Run in parallel
        start_time = time.time()
        predictions = await asyncio.gather(*tasks)
        total_time = (time.time() - start_time) * 1000
        
        # Combine results
        results = {}
        timing = {}
        for i, (name, _) in enumerate(self.models.items()):
            results[name] = predictions[i]
            timing[name] = predictions[i].get('time', '0ms')
        
        return {
            "predictions": results,
            "timing": timing,
            "total_time": f"{total_time:.1f}ms"
        }
    
    def prepare_features(self, features, model_name):
        """
        Prepare model-specific input features
        Each model may need different feature formats
        """
        
        config = self.configs.get(model_name, {})
        input_size = config.get('input_size', 784)
        
        # Extract relevant features based on model type
        if model_name == "species_classifier":
            # Needs k-mer frequencies
            feature_vector = features['kmers']
        
        elif model_name == "quality_scorer":
            # Needs GC content + k-mers
            feature_vector = np.concatenate([
                features['kmers'],
                [features['gc_content']]
            ])
        
        elif model_name == "mutation_detector":
            # Needs full sequence features
            feature_vector = self.extract_mutation_features(features['sequence'])
        
        # ... (similar for other models)
        
        else:
            # Default: use k-mer frequencies
            feature_vector = features['kmers']
        
        # Pad or truncate to input_size
        if len(feature_vector) < input_size:
            feature_vector = np.pad(feature_vector, 
                                   (0, input_size - len(feature_vector)))
        else:
            feature_vector = feature_vector[:input_size]
        
        # Convert to tensor
        tensor = torch.tensor(feature_vector, dtype=torch.float32)
        tensor = tensor.unsqueeze(0)  # Add batch dimension
        tensor = tensor.to(self.device)
        
        return tensor
    
    def post_process(self, prediction, model_name):
        """
        Post-process model output to human-readable format
        """
        
        # Convert tensor to numpy
        if isinstance(prediction, torch.Tensor):
            prediction = prediction.cpu().numpy()
        
        if model_name == "species_classifier":
            # Multi-class classification
            classes = ["Human", "Bacterial", "Viral", "Plant", "Fungal", "Unknown"]
            probs = torch.softmax(torch.tensor(prediction), dim=-1).numpy()[0]
            
            return {
                "predicted_class": classes[np.argmax(probs)],
                "confidence": float(np.max(probs)),
                "probabilities": {
                    cls: float(prob) 
                    for cls, prob in zip(classes, probs)
                }
            }
        
        elif model_name == "quality_scorer":
            # Regression (quality score 0-100)
            score = float(prediction[0][0])
            
            return {
                "quality_score": max(0, min(100, score)),
                "quality_level": "High" if score > 90 else "Medium" if score > 70 else "Low"
            }
        
        elif model_name == "mutation_detector":
            # Binary classification
            prob = torch.sigmoid(torch.tensor(prediction)).numpy()[0][0]
            
            return {
                "has_mutations": bool(prob > 0.5),
                "mutation_probability": float(prob),
                "estimated_variants": int(prob * 100)  # Rough estimate
            }
        
        # ... (similar for other models)
        
        else:
            # Default: return raw prediction
            return {
                "prediction": prediction.tolist(),
                "note": "Raw model output (no post-processing defined)"
            }
    
    def extract_mutation_features(self, sequence):
        """
        Extract features specific to mutation detection
        """
        
        # Example features:
        # - Transition/transversion ratios
        # - Homopolymer runs
        # - Dinucleotide frequencies
        # - etc.
        
        features = []
        
        # Homopolymer runs (e.g., AAAA, TTTT)
        for base in ['A', 'T', 'C', 'G']:
            max_run = 0
            current_run = 0
            for nuc in sequence:
                if nuc == base:
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 0
            features.append(max_run / len(sequence))
        
        # Add more features as needed...
        
        return np.array(features)


# Global model manager instance
model_manager = None

def initialize_models():
    """
    Initialize model manager at backend startup
    """
    global model_manager
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model_manager = AIModelManager(device=device)
    
    return model_manager
```

---

### **STEP 3: Integrate with Existing Backend**

**File**: `backend/real_main.py`

**Update the initialization:**

```python
# Add at top of file
from ai_models.model_manager import initialize_models, model_manager

# After app initialization
@app.on_event("startup")
async def startup_event():
    """
    Initialize AI models when backend starts
    """
    print("🚀 Starting SecureAI-MedGenomics backend...")
    
    # Initialize database
    init_database()
    
    # Initialize AI models (NEW!)
    initialize_models()
    
    print("✅ Backend ready!")
```

**Update the `analyze_genomic_data()` function:**

```python
async def analyze_genomic_data(content: bytes) -> dict:
    """
    Layer 4: AI-based Genomic Analysis using 6 AI models
    NOW WITH MULTIPLE MODELS!
    """
    try:
        # Parse FASTA sequences (existing code)
        sequences = []
        current_seq = ""
        
        lines = content.decode('utf-8', errors='ignore').split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append(current_seq)
                    current_seq = ""
            else:
                current_seq += line
        
        if current_seq:
            sequences.append(current_seq)
        
        # Calculate basic features (existing code)
        total_bases = sum(len(seq) for seq in sequences)
        gc_count = sum(seq.count('G') + seq.count('C') for seq in sequences)
        gc_content = (gc_count / total_bases * 100) if total_bases > 0 else 0
        
        # K-mer analysis (existing code)
        kmers = {}
        for seq in sequences:
            for i in range(len(seq) - 2):
                kmer = seq[i:i+3]
                if all(c in 'ACGT' for c in kmer):
                    kmers[kmer] = kmers.get(kmer, 0) + 1
        
        # Prepare features for AI models (NEW!)
        kmer_frequencies = []
        all_kmers = [
            a + b + c 
            for a in 'ATCG' 
            for b in 'ATCG' 
            for c in 'ATCG'
        ]
        total_kmers = sum(kmers.values())
        for kmer in all_kmers:
            freq = kmers.get(kmer, 0) / total_kmers if total_kmers > 0 else 0
            kmer_frequencies.append(freq)
        
        features = {
            'sequence': sequences[0] if sequences else "",
            'kmers': np.array(kmer_frequencies),
            'gc_content': gc_content,
            'length': total_bases
        }
        
        # Run all 6 AI models (NEW!)
        print("Running 6 AI models...")
        ai_results = await model_manager.predict_all_parallel(features)
        
        # Combine results
        return {
            # Basic analysis (existing)
            "sequences_analyzed": len(sequences),
            "total_bases": total_bases,
            "gc_content": round(gc_content, 2),
            "unique_kmers": len(kmers),
            "most_common_kmer": max(kmers, key=kmers.get) if kmers else "N/A",
            
            # AI model predictions (NEW!)
            "ai_models": ai_results['predictions'],
            "model_timing": ai_results['timing'],
            "total_model_time": ai_results['total_time'],
            
            # Legacy fields for compatibility
            "species_prediction": ai_results['predictions']['species_classifier'].get('predicted_class', 'Unknown'),
            "quality_score": ai_results['predictions']['quality_scorer'].get('quality_score', 0),
            "analysis_method": "6 AI Models + K-mer analysis"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "sequences_analyzed": 0,
            "total_bases": 0
        }
```

---

### **STEP 4: Update Frontend to Display All Models**

**File**: `frontend/index.html`

Add a new results card:

```html
<!-- After existing Analysis Results card -->
<div class="result-card">
    <h2 class="card-title">🤖 AI Model Predictions</h2>
    <div id="ai-models-results" class="ai-models-grid">
        <!-- Will be populated dynamically -->
    </div>
</div>
```

**File**: `frontend/app.js`

Update `initResultsPage()`:

```javascript
function initResultsPage() {
  // ... existing code ...
  
  // Display AI model results (NEW!)
  if (state.currentJob.ai_models) {
    displayAIModelResults(state.currentJob.ai_models, 
                          state.currentJob.model_timing);
  }
}

function displayAIModelResults(models, timing) {
  const container = document.getElementById('ai-models-results');
  container.innerHTML = '';
  
  const modelIcons = {
    'species_classifier': '🧬',
    'quality_scorer': '⭐',
    'mutation_detector': '🔬',
    'contamination_checker': '🛡️',
    'gc_predictor': '📊',
    'length_estimator': '📏'
  };
  
  const modelNames = {
    'species_classifier': 'Species Classification',
    'quality_scorer': 'Quality Assessment',
    'mutation_detector': 'Mutation Detection',
    'contamination_checker': 'Contamination Check',
    'gc_predictor': 'GC Content Prediction',
    'length_estimator': 'Length Analysis'
  };
  
  Object.entries(models).forEach(([modelName, result]) => {
    const card = document.createElement('div');
    card.className = 'ai-model-card';
    card.innerHTML = `
      <div class="model-header">
        <span class="model-icon">${modelIcons[modelName] || '🤖'}</span>
        <span class="model-name">${modelNames[modelName] || modelName}</span>
        <span class="model-time">${timing[modelName]}</span>
      </div>
      <div class="model-result">
        ${formatModelResult(modelName, result)}
      </div>
    `;
    container.appendChild(card);
  });
}

function formatModelResult(modelName, result) {
  if (result.error) {
    return `<span class="error">⚠️ ${result.error}</span>`;
  }
  
  if (modelName === 'species_classifier') {
    return `
      <div class="prediction-main">${result.predicted_class}</div>
      <div class="prediction-confidence">Confidence: ${(result.confidence * 100).toFixed(1)}%</div>
    `;
  }
  
  if (modelName === 'quality_scorer') {
    return `
      <div class="prediction-main">Score: ${result.quality_score.toFixed(1)}/100</div>
      <div class="prediction-level">${result.quality_level} Quality</div>
    `;
  }
  
  if (modelName === 'mutation_detector') {
    return `
      <div class="prediction-main">${result.has_mutations ? '✓ Mutations Detected' : '✗ No Mutations'}</div>
      <div class="prediction-confidence">Probability: ${(result.mutation_probability * 100).toFixed(1)}%</div>
    `;
  }
  
  // ... similar for other models ...
  
  return `<pre>${JSON.stringify(result, null, 2)}</pre>`;
}
```

---

## 🚀 Quick Start (Minimum Viable Integration)

If you want to get started **quickly** (1-2 hours):

### **Option A: Mock Models (For Testing)**

```python
# backend/ai_models/mock_models.py

class MockModelManager:
    """
    Mock AI models for testing
    Replace with real models later
    """
    
    async def predict_all_parallel(self, features):
        import asyncio
        await asyncio.sleep(0.2)  # Simulate processing
        
        return {
            "predictions": {
                "species_classifier": {
                    "predicted_class": "Human",
                    "confidence": 0.95
                },
                "quality_scorer": {
                    "quality_score": 89.5,
                    "quality_level": "High"
                },
                "mutation_detector": {
                    "has_mutations": True,
                    "mutation_probability": 0.67
                },
                "contamination_checker": {
                    "is_contaminated": False,
                    "contamination_score": 0.05
                },
                "gc_predictor": {
                    "predicted_gc": 45.2,
                    "actual_gc": features['gc_content']
                },
                "length_estimator": {
                    "estimated_length": features['length'],
                    "length_category": "Medium"
                }
            },
            "timing": {
                "species_classifier": "50ms",
                "quality_scorer": "45ms",
                "mutation_detector": "60ms",
                "contamination_checker": "40ms",
                "gc_predictor": "35ms",
                "length_estimator": "30ms"
            },
            "total_time": "200ms"
        }

model_manager = MockModelManager()
```

Use this to test the integration **before** your team's models are ready!

---

## 📊 Expected Performance

| Metric | Sequential | Parallel | On-Demand |
|--------|------------|----------|-----------|
| **Processing Time** | 600-1200ms | 200-400ms | 1500-3000ms |
| **Memory Usage** | 500MB-1GB | 500MB-1GB | 100-200MB |
| **GPU Required** | No | Recommended | No |
| **Code Complexity** | Low | Medium | Medium |
| **Best For** | Prototyping | Production | Limited resources |

---

## ⚠️ Common Issues & Solutions

### **Issue 1: Models Too Large (>100MB each)**

**Problem**: Slow startup, high memory usage

**Solution**:
```python
# Use model quantization
import torch.quantization

# Quantize model to 8-bit (reduces size by 4x)
model_quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

### **Issue 2: Slow Inference (>500ms per model)**

**Problem**: Poor user experience

**Solution**:
- Use GPU if available
- Run models in parallel
- Cache results for identical inputs
- Use smaller models or model distillation

### **Issue 3: Different Model Frameworks**

**Problem**: Some models in PyTorch, others in TensorFlow

**Solution**:
```python
# Unified model wrapper
class UnifiedModel:
    def __init__(self, model_path, framework):
        self.framework = framework
        
        if framework == "pytorch":
            self.model = torch.load(model_path)
        elif framework == "tensorflow":
            self.model = tf.keras.models.load_model(model_path)
        elif framework == "onnx":
            self.model = onnxruntime.InferenceSession(model_path)
    
    def predict(self, features):
        if self.framework == "pytorch":
            return self.model(features)
        elif self.framework == "tensorflow":
            return self.model.predict(features)
        # ... etc
```

---

## 🎓 Recommendations

### **For Your Team:**

1. **Start with Mock Models**: Test integration first
2. **One Model at a Time**: Add incrementally (don't add all 6 at once)
3. **Profile Performance**: Measure each model's time/memory
4. **Use Parallel Execution**: If GPU available (3-4x speedup)
5. **Version Your Models**: Save model versions (v1, v2, etc.)
6. **Document Model Inputs**: What features does each model need?

### **Best Practice Order:**

```
Week 1: Setup infrastructure (model_manager.py)
Week 2: Integrate Model 1 (species classifier)
Week 3: Integrate Models 2-3 (quality + mutation)
Week 4: Integrate Models 4-6 (rest)
Week 5: Optimize & test
```

---

## 📋 Checklist

Before integrating models, ensure:

- [ ] Models are trained and exported (.pth/.h5/.onnx)
- [ ] Model input/output formats documented
- [ ] Feature extraction code matches model training
- [ ] Model size is reasonable (<100MB preferred)
- [ ] Backend has required dependencies (PyTorch/TensorFlow)
- [ ] Testing data available for validation
- [ ] Frontend UI designed for 6 model outputs
- [ ] Database schema updated for new results
- [ ] Error handling in place for model failures

---

## 💡 Final Answer to Your Question

### **Is it easy?**

**YES!** ✅

Your architecture is **already prepared** for multi-model integration:

✅ Backend supports async operations  
✅ Feature extraction infrastructure exists  
✅ Database can store model results  
✅ Frontend displays results dynamically  
✅ Processing time tracking ready  

### **Estimated effort:**

- **Junior Developer**: 2-3 days (16-24 hours)
- **Senior Developer**: 4-6 hours

### **Key advantage:**

You have a **well-structured foundation**. Adding models is just:
1. Load models at startup (1 hour)
2. Call `model.predict()` (2 hours)
3. Update frontend (2 hours)
4. Test (3 hours)

**Total**: ~8 hours of focused work!

---

**Ready to integrate? Start with the Mock Models approach, then replace with real models one at a time!** 🚀

---

**Last Updated**: November 5, 2025  
**Difficulty Rating**: ⭐⭐⭐ (Easy to Moderate)  
**Estimated Time**: 8-16 hours
