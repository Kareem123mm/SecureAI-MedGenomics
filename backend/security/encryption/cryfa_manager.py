"""
Cryfa Manager - Genomic Data Encryption and Compression

Cryfa is a specialized tool for FASTA/FASTQ file compression and encryption.
It provides better compression ratios than general-purpose tools while maintaining security.

Features:
- Optimized for genomic data (FASTA, FASTQ, VCF)
- High compression ratios (10-20x for FASTA files)
- AES-256 encryption
- Fast encryption/decryption

Note: Requires Cryfa to be installed on the system
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple
import hashlib
import time
import shutil


logger = logging.getLogger(__name__)


class CryfaManager:
    """
    Manager for Cryfa encryption/decryption operations
    """
    
    def __init__(self, cryfa_path: Optional[str] = None):
        """
        Initialize Cryfa manager
        
        Args:
            cryfa_path: Path to cryfa executable. If None, assumes cryfa is in PATH
        """
        self.cryfa_path = cryfa_path or "cryfa"
        self._check_availability()
        
        # Statistics
        self.stats = {
            "total_encryptions": 0,
            "total_decryptions": 0,
            "total_bytes_processed": 0,
            "total_time": 0.0
        }
    
    def _check_availability(self) -> bool:
        """Check if Cryfa is available on the system"""
        try:
            result = subprocess.run(
                [self.cryfa_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Cryfa found: {result.stdout.strip()}")
                return True
            else:
                logger.warning("Cryfa command failed")
                return False
        except FileNotFoundError:
            logger.warning(
                "Cryfa not found. Please install: "
                "https://github.com/cobilab/cryfa"
            )
            return False
        except Exception as e:
            logger.error(f"Error checking Cryfa availability: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Cryfa is available"""
        return self._check_availability()
    
    async def encrypt_file(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        password: Optional[str] = None,
        verbose: bool = False
    ) -> str:
        """
        Encrypt a file using Cryfa
        
        Args:
            input_file: Path to input file
            output_file: Path to output file (auto-generated if None)
            password: Encryption password
            verbose: Show verbose output
        
        Returns:
            Path to encrypted file
        """
        start_time = time.time()
        
        try:
            input_path = Path(input_file)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            # Generate output filename if not provided
            if output_file is None:
                output_file = str(input_path.parent / f"{input_path.stem}.cryfa")
            
            output_path = Path(output_file)
            
            # Get file size before encryption
            input_size = input_path.stat().st_size
            
            # Build Cryfa command
            cmd = [self.cryfa_path, "-e"]  # -e for encryption
            
            if password:
                cmd.extend(["-k", password])  # -k for password
            
            if verbose:
                cmd.append("-v")  # -v for verbose
            
            cmd.extend([str(input_path), "-o", str(output_path)])
            
            # Execute Cryfa
            logger.info(f"Encrypting {input_file}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Cryfa encryption failed: {result.stderr}")
                raise RuntimeError(f"Encryption failed: {result.stderr}")
            
            if not output_path.exists():
                raise RuntimeError("Encrypted file was not created")
            
            # Get output file size
            output_size = output_path.stat().st_size
            compression_ratio = input_size / output_size if output_size > 0 else 0
            
            # Update statistics
            elapsed_time = time.time() - start_time
            self.stats["total_encryptions"] += 1
            self.stats["total_bytes_processed"] += input_size
            self.stats["total_time"] += elapsed_time
            
            logger.info(
                f"Encryption complete: {input_file} -> {output_file} "
                f"(Compression ratio: {compression_ratio:.2f}x, "
                f"Time: {elapsed_time:.2f}s)"
            )
            
            return str(output_path)
            
        except subprocess.TimeoutExpired:
            logger.error("Cryfa encryption timed out")
            raise RuntimeError("Encryption timed out")
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    async def decrypt_file(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        password: Optional[str] = None,
        verbose: bool = False
    ) -> str:
        """
        Decrypt a Cryfa-encrypted file
        
        Args:
            input_file: Path to encrypted file
            output_file: Path to decrypted output file
            password: Decryption password
            verbose: Show verbose output
        
        Returns:
            Path to decrypted file
        """
        start_time = time.time()
        
        try:
            input_path = Path(input_file)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            # Generate output filename if not provided
            if output_file is None:
                # Remove .cryfa extension or add _decrypted
                if input_path.suffix == ".cryfa":
                    output_file = str(input_path.with_suffix(""))
                else:
                    output_file = str(input_path.parent / f"{input_path.stem}_decrypted{input_path.suffix}")
            
            output_path = Path(output_file)
            
            # Build Cryfa command
            cmd = [self.cryfa_path, "-d"]  # -d for decryption
            
            if password:
                cmd.extend(["-k", password])
            
            if verbose:
                cmd.append("-v")
            
            cmd.extend([str(input_path), "-o", str(output_path)])
            
            # Execute Cryfa
            logger.info(f"Decrypting {input_file}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                logger.error(f"Cryfa decryption failed: {result.stderr}")
                raise RuntimeError(f"Decryption failed: {result.stderr}")
            
            if not output_path.exists():
                raise RuntimeError("Decrypted file was not created")
            
            # Update statistics
            elapsed_time = time.time() - start_time
            self.stats["total_decryptions"] += 1
            self.stats["total_time"] += elapsed_time
            
            logger.info(
                f"Decryption complete: {input_file} -> {output_file} "
                f"(Time: {elapsed_time:.2f}s)"
            )
            
            return str(output_path)
            
        except subprocess.TimeoutExpired:
            logger.error("Cryfa decryption timed out")
            raise RuntimeError("Decryption timed out")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def get_compression_ratio(self, encrypted_file: str, original_file: str) -> float:
        """
        Calculate compression ratio between original and encrypted files
        
        Returns:
            Compression ratio (original_size / encrypted_size)
        """
        try:
            original_size = Path(original_file).stat().st_size
            encrypted_size = Path(encrypted_file).stat().st_size
            
            return original_size / encrypted_size if encrypted_size > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Failed to calculate compression ratio: {e}")
            return 0.0
    
    def verify_integrity(self, file_path: str) -> Tuple[bool, str]:
        """
        Verify file integrity using checksum
        
        Returns:
            (is_valid, checksum_hash)
        """
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
                
                checksum = file_hash.hexdigest()
                return True, checksum
                
        except Exception as e:
            logger.error(f"Integrity verification failed: {e}")
            return False, ""
    
    def get_statistics(self) -> dict:
        """Get encryption/decryption statistics"""
        return {
            **self.stats,
            "average_time": (
                self.stats["total_time"] / 
                (self.stats["total_encryptions"] + self.stats["total_decryptions"])
                if (self.stats["total_encryptions"] + self.stats["total_decryptions"]) > 0
                else 0.0
            )
        }


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

async def encrypt_genomic_data(
    input_file: str,
    password: str,
    output_dir: Optional[str] = None
) -> Tuple[str, float]:
    """
    Convenient function to encrypt genomic data
    
    Returns:
        (encrypted_file_path, compression_ratio)
    """
    manager = CryfaManager()
    
    if not manager.is_available():
        raise RuntimeError("Cryfa is not available on this system")
    
    # Set output directory
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_file = str(Path(output_dir) / Path(input_file).with_suffix(".cryfa").name)
    else:
        output_file = None
    
    # Encrypt
    encrypted_path = await manager.encrypt_file(
        input_file=input_file,
        output_file=output_file,
        password=password
    )
    
    # Calculate compression ratio
    ratio = manager.get_compression_ratio(encrypted_path, input_file)
    
    return encrypted_path, ratio


async def decrypt_genomic_data(
    encrypted_file: str,
    password: str,
    output_dir: Optional[str] = None
) -> str:
    """
    Convenient function to decrypt genomic data
    
    Returns:
        Decrypted file path
    """
    manager = CryfaManager()
    
    if not manager.is_available():
        raise RuntimeError("Cryfa is not available on this system")
    
    # Set output directory
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_file = str(Path(output_dir) / Path(encrypted_file).stem)
    else:
        output_file = None
    
    # Decrypt
    decrypted_path = await manager.decrypt_file(
        input_file=encrypted_file,
        output_file=output_file,
        password=password
    )
    
    return decrypted_path


if __name__ == "__main__":
    import asyncio
    
    # Example usage
    print("🔐 Cryfa Manager Test")
    
    manager = CryfaManager()
    
    if manager.is_available():
        print("✅ Cryfa is available")
        
        # Create test file
        test_file = "test_genome.fasta"
        with open(test_file, "w") as f:
            f.write(">test_sequence\n")
            f.write("ATGCGTACGTAGCTAGCTAGCTAGCTA\n" * 100)
        
        print(f"\nTest file created: {test_file}")
        
        # Test encryption
        print("\nTesting encryption...")
        encrypted = asyncio.run(manager.encrypt_file(
            input_file=test_file,
            password="TestPassword123"
        ))
        print(f"Encrypted: {encrypted}")
        
        # Test decryption
        print("\nTesting decryption...")
        decrypted = asyncio.run(manager.decrypt_file(
            input_file=encrypted,
            password="TestPassword123"
        ))
        print(f"Decrypted: {decrypted}")
        
        # Show stats
        print("\nStatistics:")
        print(manager.get_statistics())
        
        # Cleanup
        Path(test_file).unlink(missing_ok=True)
        Path(encrypted).unlink(missing_ok=True)
        Path(decrypted).unlink(missing_ok=True)
        
    else:
        print("❌ Cryfa is not available")
        print("Install with: sudo apt-get install cryfa")
        print("Or download from: https://github.com/cobilab/cryfa")
