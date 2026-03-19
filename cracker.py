import zipfile
import rarfile
import PyPDF2
import itertools
import string
import threading
import time
from pathlib import Path

class ArchiveCracker:
    def __init__(self, archive_path, timeout=10):
        """
        Initialize the archive cracker
        
        Args:
            archive_path: Path to the archive file
            timeout: Timeout for each password attempt (seconds)
        """
        self.archive_path = archive_path
        self.timeout = timeout
        self.found_password = None
        self.is_cracking = False
        self.attempts = 0
        self.start_time = None
        
    def get_archive_type(self):
        """Detect archive type based on file extension"""
        path = Path(self.archive_path)
        extension = path.suffix.lower()
        
        if extension == '.zip':
            return 'zip'
        elif extension == '.rar':
            return 'rar'
        elif extension == '.pdf':
            return 'pdf'
        else:
            raise ValueError(f"Unsupported archive type: {extension}")
    
    def test_password_zip(self, password):
        """Test password for ZIP archive"""
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
                zip_ref.testzip()
            return True
        except RuntimeError:
            return False
        except Exception as e:
            return False
    
    def test_password_rar(self, password):
        """Test password for RAR archive"""
        try:
            with rarfile.RarFile(self.archive_path) as rar_ref:
                rar_ref.testrar()
            return True
        except rarfile.BadRarFile:
            return False
        except Exception:
            return False
    
    def test_password_pdf(self, password):
        """Test password for PDF"""
        try:
            with open(self.archive_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                if pdf_reader.is_encrypted:
                    return pdf_reader.decrypt(password)
                return True
        except Exception:
            return False
    
    def test_password(self, password):
        """Test password with the appropriate method based on archive type"""
        archive_type = self.get_archive_type()
        
        self.attempts += 1
        
        if archive_type == 'zip':
            return self.test_password_zip(password)
        elif archive_type == 'rar':
            return self.test_password_rar(password)
        elif archive_type == 'pdf':
            return self.test_password_pdf(password)
    
    def brute_force(self, charset=None, max_length=6, callback=None):
        """
        Brute force attack using all possible combinations
        
        Args:
            charset: Characters to use (default: ascii_letters + digits + punctuation)
            max_length: Maximum password length to try
            callback: Function to call with progress updates
        """
        if charset is None:
            charset = string.ascii_letters + string.digits + string.punctuation
        
        self.is_cracking = True
        self.start_time = time.time()
        
        try:
            for length in range(1, max_length + 1):
                if not self.is_cracking:
                    break
                
                for password_tuple in itertools.product(charset, repeat=length):
                    if not self.is_cracking:
                        break
                    
                    password = ''.join(password_tuple)
                    
                    if self.test_password(password):
                        self.found_password = password
                        if callback:
                            callback('found', password, self.attempts)
                        return password
                    
                    if callback and self.attempts % 100 == 0:
                        elapsed = time.time() - self.start_time
                        callback('progress', password, self.attempts, elapsed)
        
        finally:
            self.is_cracking = False
        
        return None
    
    def dictionary_attack(self, wordlist_path, callback=None):
        """Dictionary attack using a wordlist
        
        Args:
            wordlist_path: Path to the wordlist file
            callback: Function to call with progress updates
        """
        self.is_cracking = True
        self.start_time = time.time()
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
                for password in wordlist:
                    if not self.is_cracking:
                        break
                    
                    password = password.strip()
                    
                    if self.test_password(password):
                        self.found_password = password
                        if callback:
                            callback('found', password, self.attempts)
                        return password
                    
                    if callback and self.attempts % 100 == 0:
                        elapsed = time.time() - self.start_time
                        callback('progress', password, self.attempts, elapsed)
        
        finally:
            self.is_cracking = False
        
        return None
    
    def stop_cracking(self):
        """Stop the cracking process"""
        self.is_cracking = False
    
    def get_stats(self):
        """Get cracking statistics"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            'attempts': self.attempts,
            'elapsed_time': elapsed,
            'passwords_per_second': self.attempts / elapsed if elapsed > 0 else 0,
            'found': self.found_password is not None,
            'password': self.found_password
        }