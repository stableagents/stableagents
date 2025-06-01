import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any


class LogManager:
    """Manages agent logs"""
    
    def __init__(self, logs_dir: Optional[str] = None):
        self.logs_dir = logs_dir or os.path.join(
            os.path.dirname(__file__), "data", "logs"
        )
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir, exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger("stableagents")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = os.path.join(self.logs_dir, f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message"""
        if extra:
            self.logger.info(message, extra=extra)
        else:
            self.logger.info(message)
    
    def log_warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        if extra:
            self.logger.warning(message, extra=extra)
        else:
            self.logger.warning(message)
    
    def log_error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log error message"""
        if extra:
            self.logger.error(message, extra=extra)
        else:
            self.logger.error(message)
    
    def log_debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message"""
        if extra:
            self.logger.debug(message, extra=extra)
        else:
            self.logger.debug(message)
            
    def get_logs(self, log_file: Optional[str] = None) -> List[str]:
        """Get logs from a specific file or the latest file"""
        if not log_file:
            # Get the most recent log file
            log_files = [f for f in os.listdir(self.logs_dir) if f.endswith('.log')]
            if not log_files:
                return []
            log_file = max(log_files, key=lambda x: os.path.getctime(os.path.join(self.logs_dir, x)))
        
        log_path = os.path.join(self.logs_dir, log_file)
        if not os.path.exists(log_path):
            return []
            
        with open(log_path, 'r') as f:
            return f.readlines() 