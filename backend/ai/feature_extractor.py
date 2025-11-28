"""
Genomic Feature Extractor

Converts raw genomic sequences (FASTA/FASTQ) into numeric feature vectors
compatible with AI models (587 features expected)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter
import logging
import re

logger = logging.getLogger(__name__)


class GenomicFeatureExtractor:
    """
    Extract numeric features from genomic sequences for ML models
    """
    
    def __init__(self, expected_features: int = 587):
        """
        Initialize feature extractor
        
        Args:
            expected_features: Number of features models expect (default: 587)
        """
        self.expected_features = expected_features
        
        # Nucleotide mapping
        self.nucleotide_map = {'A': 0, 'T': 1, 'G': 2, 'C': 3, 'N': 4}
        
        # K-mer sizes to extract
        self.kmer_sizes = [3, 4, 5]  # 3-mers, 4-mers, 5-mers
        
        logger.info(f"Feature extractor initialized (target: {expected_features} features)")
    
    def parse_fasta(self, content: bytes) -> List[Tuple[str, str]]:
        """
        Parse FASTA format file
        
        Args:
            content: Raw file bytes
        
        Returns:
            List of (header, sequence) tuples
        """
        try:
            text = content.decode('utf-8', errors='ignore')
            sequences = []
            current_header = None
            current_seq = []
            
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('>'):
                    # Save previous sequence
                    if current_header:
                        sequences.append((current_header, ''.join(current_seq)))
                    
                    # Start new sequence
                    current_header = line[1:]  # Remove '>'
                    current_seq = []
                else:
                    current_seq.append(line.upper())
            
            # Don't forget last sequence
            if current_header:
                sequences.append((current_header, ''.join(current_seq)))
            
            logger.info(f"Parsed {len(sequences)} sequences from FASTA")
            return sequences
        
        except Exception as e:
            logger.error(f"Failed to parse FASTA: {e}")
            return []
    
    def calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content percentage"""
        if not sequence:
            return 0.0
        
        g_count = sequence.count('G')
        c_count = sequence.count('C')
        return (g_count + c_count) / len(sequence) * 100
    
    def calculate_nucleotide_frequencies(self, sequence: str) -> Dict[str, float]:
        """Calculate frequency of each nucleotide"""
        if not sequence:
            return {'A': 0, 'T': 0, 'G': 0, 'C': 0, 'N': 0}
        
        length = len(sequence)
        return {
            'A': sequence.count('A') / length,
            'T': sequence.count('T') / length,
            'G': sequence.count('G') / length,
            'C': sequence.count('C') / length,
            'N': sequence.count('N') / length
        }
    
    def extract_kmers(self, sequence: str, k: int) -> Dict[str, int]:
        """
        Extract k-mers from sequence
        
        Args:
            sequence: DNA sequence
            k: K-mer size
        
        Returns:
            Dictionary of k-mer counts
        """
        kmers = {}
        
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]
            # Only count valid k-mers (ATGC only)
            if all(c in 'ATGC' for c in kmer):
                kmers[kmer] = kmers.get(kmer, 0) + 1
        
        return kmers
    
    def calculate_kmer_diversity(self, kmers: Dict[str, int]) -> float:
        """Calculate k-mer diversity (Shannon entropy)"""
        if not kmers:
            return 0.0
        
        total = sum(kmers.values())
        entropy = 0.0
        
        for count in kmers.values():
            if count > 0:
                prob = count / total
                entropy -= prob * np.log2(prob)
        
        return entropy
    
    def calculate_cpg_islands(self, sequence: str) -> int:
        """
        Count CpG islands (regions with high CG content)
        CpG island: CG pattern appears frequently
        """
        return sequence.count('CG')
    
    def calculate_repeat_regions(self, sequence: str) -> int:
        """Count simple repeat regions (e.g., AAAA, TTTT, etc.)"""
        repeats = 0
        
        # Check for runs of 4+ same nucleotide
        for nucleotide in 'ATGC':
            pattern = nucleotide * 4
            repeats += sequence.count(pattern)
        
        return repeats
    
    def extract_sequence_features(self, sequence: str) -> np.ndarray:
        """
        Extract all features from a single sequence
        
        Returns:
            Feature vector (numpy array)
        """
        features = []
        
        # 1. Basic statistics (5 features)
        features.append(len(sequence))  # Sequence length
        features.append(self.calculate_gc_content(sequence))  # GC content
        
        # 2. Nucleotide frequencies (5 features)
        nuc_freq = self.calculate_nucleotide_frequencies(sequence)
        features.extend([nuc_freq['A'], nuc_freq['T'], nuc_freq['G'], nuc_freq['C'], nuc_freq['N']])
        
        # 3. K-mer features
        for k in self.kmer_sizes:
            kmers = self.extract_kmers(sequence, k)
            
            # K-mer count
            features.append(len(kmers))
            
            # K-mer diversity
            features.append(self.calculate_kmer_diversity(kmers))
            
            # Top 10 most common k-mers (frequency)
            if kmers:
                total_kmers = sum(kmers.values())
                most_common = sorted(kmers.items(), key=lambda x: x[1], reverse=True)[:10]
                for _, count in most_common:
                    features.append(count / total_kmers)
                # Pad if less than 10
                features.extend([0.0] * (10 - len(most_common)))
            else:
                features.extend([0.0] * 10)
        
        # 4. Special regions (2 features)
        features.append(self.calculate_cpg_islands(sequence))
        features.append(self.calculate_repeat_regions(sequence))
        
        # 5. Dinucleotide frequencies (16 features: AA, AT, AG, AC, TA, TT, ...)
        dinuc_counts = {}
        for i in range(len(sequence) - 1):
            dinuc = sequence[i:i+2]
            if all(c in 'ATGC' for c in dinuc):
                dinuc_counts[dinuc] = dinuc_counts.get(dinuc, 0) + 1
        
        total_dinuc = sum(dinuc_counts.values()) if dinuc_counts else 1
        for n1 in 'ATGC':
            for n2 in 'ATGC':
                dinuc = n1 + n2
                freq = dinuc_counts.get(dinuc, 0) / total_dinuc
                features.append(freq)
        
        return np.array(features, dtype=np.float32)
    
    def extract_features_from_file(
        self,
        content: bytes,
        aggregate: str = "mean"
    ) -> np.ndarray:
        """
        Extract features from genomic file (FASTA format)
        
        Args:
            content: Raw file bytes
            aggregate: How to combine multiple sequences ("mean", "max", "first")
        
        Returns:
            Feature vector matching model input size (587 features)
        """
        try:
            # Parse sequences
            sequences = self.parse_fasta(content)
            
            if not sequences:
                logger.warning("No sequences found in file")
                return self._get_zero_features()
            
            # Extract features from each sequence
            all_features = []
            for header, seq in sequences:
                if len(seq) > 0:  # Skip empty sequences
                    seq_features = self.extract_sequence_features(seq)
                    all_features.append(seq_features)
            
            if not all_features:
                logger.warning("No valid sequences to extract features from")
                return self._get_zero_features()
            
            # Aggregate features from multiple sequences
            if aggregate == "mean":
                combined_features = np.mean(all_features, axis=0)
            elif aggregate == "max":
                combined_features = np.max(all_features, axis=0)
            elif aggregate == "first":
                combined_features = all_features[0]
            else:
                combined_features = np.mean(all_features, axis=0)
            
            # Pad or truncate to expected size
            final_features = self._adjust_feature_size(combined_features)
            
            logger.info(f"Extracted {len(final_features)} features from {len(sequences)} sequences")
            
            return final_features
        
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            return self._get_zero_features()
    
    def _adjust_feature_size(self, features: np.ndarray) -> np.ndarray:
        """
        Adjust feature vector to match expected size
        
        Args:
            features: Current feature vector
        
        Returns:
            Feature vector of size self.expected_features
        """
        current_size = len(features)
        
        if current_size == self.expected_features:
            return features
        elif current_size < self.expected_features:
            # Pad with zeros
            padding = np.zeros(self.expected_features - current_size, dtype=np.float32)
            return np.concatenate([features, padding])
        else:
            # Truncate
            logger.warning(
                f"Truncating features from {current_size} to {self.expected_features}"
            )
            return features[:self.expected_features]
    
    def _get_zero_features(self) -> np.ndarray:
        """Return zero feature vector"""
        return np.zeros(self.expected_features, dtype=np.float32)
    
    def validate_features(self, features: np.ndarray) -> bool:
        """Validate extracted features"""
        # Check size
        if len(features) != self.expected_features:
            logger.error(f"Invalid feature size: {len(features)} != {self.expected_features}")
            return False
        
        # Check for NaN or Inf
        if np.any(np.isnan(features)) or np.any(np.isinf(features)):
            logger.error("Features contain NaN or Inf")
            return False
        
        return True
    
    def get_feature_names(self) -> List[str]:
        """Get human-readable feature names"""
        names = []
        
        # Basic stats
        names.extend(['sequence_length', 'gc_content'])
        
        # Nucleotide frequencies
        names.extend(['freq_A', 'freq_T', 'freq_G', 'freq_C', 'freq_N'])
        
        # K-mer features
        for k in self.kmer_sizes:
            names.append(f'{k}mer_count')
            names.append(f'{k}mer_diversity')
            for i in range(10):
                names.append(f'{k}mer_top{i+1}_freq')
        
        # Special regions
        names.extend(['cpg_islands', 'repeat_regions'])
        
        # Dinucleotides
        for n1 in 'ATGC':
            for n2 in 'ATGC':
                names.append(f'dinuc_{n1}{n2}')
        
        # Pad to expected size
        while len(names) < self.expected_features:
            names.append(f'feature_{len(names)}')
        
        return names[:self.expected_features]


if __name__ == "__main__":
    # Test feature extraction
    print("🧬 Testing Feature Extractor...")
    
    extractor = GenomicFeatureExtractor(expected_features=587)
    
    # Test FASTA
    test_fasta = b""">test_sequence_1
ATCGATCGATCGATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
>test_sequence_2
AAAAAATTTTTGGGGGGCCCCCCATCGATCG
"""
    
    features = extractor.extract_features_from_file(test_fasta)
    
    print(f"\n✅ Extracted {len(features)} features")
    print(f"Feature range: [{features.min():.3f}, {features.max():.3f}]")
    print(f"Valid: {extractor.validate_features(features)}")
    
    # Show first 10 features
    print("\nFirst 10 features:")
    for i, (name, value) in enumerate(zip(extractor.get_feature_names()[:10], features[:10])):
        print(f"  {name}: {value:.4f}")
