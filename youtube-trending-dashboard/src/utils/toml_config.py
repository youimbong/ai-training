"""
TOML 설정 파일 로더
"""
import toml
from pathlib import Path
from typing import Dict, Any, Optional


def load_toml_config(config_path: str = "config.toml") -> Dict[str, Any]:
    """
    TOML 설정 파일 로드
    
    Args:
        config_path: TOML 설정 파일 경로
        
    Returns:
        설정 딕셔너리
    """
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        
        return config
        
    except Exception as e:
        print(f"TOML 설정 파일 로드 중 오류: {e}")
        return {}


def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    중첩된 설정 값 가져오기
    
    Args:
        config: 설정 딕셔너리
        key_path: 키 경로 (예: "youtube_api.key")
        default: 기본값
        
    Returns:
        설정 값 또는 기본값
    """
    try:
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            value = value[key]
        
        return value
        
    except (KeyError, TypeError):
        return default


def merge_with_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    환경 변수와 TOML 설정 병합
    
    Args:
        config: TOML 설정 딕셔너리
        
    Returns:
        병합된 설정 딕셔너리
    """
    import os
    
    # 환경 변수에서 값 가져오기
    env_mappings = {
        'YOUTUBE_API_KEY': 'youtube_api.key',
        'DEFAULT_REGION': 'youtube_api.default_region',
        'DEFAULT_CATEGORY': 'youtube_api.default_category',
        'DEFAULT_MAX_RESULTS': 'youtube_api.max_results',
        'CACHE_TTL': 'cache.ttl',
        'ENABLE_CACHE': 'cache.enabled',
        'LOG_LEVEL': 'logging.level',
        'LOG_FILE': 'logging.file',
        'DEFAULT_THEME': 'ui.default_theme',
        'ENABLE_DARK_MODE': 'ui.enable_dark_mode',
        'ITEMS_PER_PAGE': 'ui.items_per_page',
        'MAX_RETRIES': 'performance.max_retries',
        'REQUEST_TIMEOUT': 'performance.request_timeout',
        'ENABLE_LAZY_LOADING': 'performance.enable_lazy_loading',
        'ENABLE_RATE_LIMITING': 'security.enable_rate_limiting',
        'MAX_REQUESTS_PER_MINUTE': 'security.max_requests_per_minute'
    }
    
    # 환경 변수 값으로 TOML 설정 덮어쓰기
    for env_key, config_path in env_mappings.items():
        env_value = os.getenv(env_key)
        if env_value is not None:
            set_nested_value(config, config_path, env_value)
    
    return config


def set_nested_value(config: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    중첩된 설정 값 설정
    
    Args:
        config: 설정 딕셔너리
        key_path: 키 경로 (예: "youtube_api.key")
        value: 설정할 값
    """
    keys = key_path.split('.')
    current = config
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # 값 변환
    if isinstance(value, str):
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '').isdigit():
            value = float(value)
    
    current[keys[-1]] = value
