"""
Logger utility for Pegasus OSINT
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name='pegasus', level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        default_log_file = log_dir / f'pegasus_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(default_log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
