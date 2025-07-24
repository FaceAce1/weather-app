import logging
import logging.handlers
import os
from pathlib import Path

def setup_logger(config):
    """
    设置日志记录器
    
    Args:
        config (dict): 配置字典
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志目录
    log_file = config.get('log', {}).get('file', 'logs/app.log')
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # 获取日志等级
    log_level = getattr(logging, 
                        config.get('log', {}).get('level', 'INFO').upper(), 
                        logging.INFO)
    
    # 获取根日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 添加文件处理器（带轮转）
    max_bytes = config.get('log', {}).get('max_bytes', 10485760)  # 10MB
    backup_count = config.get('log', {}).get('backup_count', 5)
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger