"""
로깅 설정 및 유틸리티
"""
import os
import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from ..config.settings import settings


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True
) -> None:
    """
    로거 설정
    
    Args:
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 로그 파일 경로
        enable_console: 콘솔 출력 활성화 여부
    """
    # 기존 핸들러 제거
    logger.remove()
    
    # 로그 디렉토리 생성
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # 콘솔 핸들러 추가
    if enable_console:
        logger.add(
            sys.stdout,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            colorize=True
        )
    
    # 파일 핸들러 추가
    if log_file:
        logger.add(
            log_file,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                   "{name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )


def get_logger(name: str = "youtube_dashboard") -> logger:
    """
    로거 인스턴스 반환
    
    Args:
        name: 로거 이름
        
    Returns:
        로거 인스턴스
    """
    return logger.bind(name=name)


def log_api_request(endpoint: str, params: dict, response_status: int) -> None:
    """
    API 요청 로깅
    
    Args:
        endpoint: API 엔드포인트
        params: 요청 파라미터
        response_status: 응답 상태 코드
    """
    logger.info(
        f"API Request - Endpoint: {endpoint}, "
        f"Params: {params}, Status: {response_status}"
    )


def log_api_error(endpoint: str, error: Exception) -> None:
    """
    API 에러 로깅
    
    Args:
        endpoint: API 엔드포인트
        error: 발생한 에러
    """
    logger.error(f"API Error - Endpoint: {endpoint}, Error: {str(error)}")


def log_performance(operation: str, duration: float) -> None:
    """
    성능 로깅
    
    Args:
        operation: 수행한 작업
        duration: 소요 시간 (초)
    """
    logger.info(f"Performance - {operation}: {duration:.2f}s")


def log_user_action(action: str, details: Optional[dict] = None) -> None:
    """
    사용자 액션 로깅
    
    Args:
        action: 사용자 액션
        details: 추가 세부사항
    """
    if details:
        logger.info(f"User Action - {action}: {details}")
    else:
        logger.info(f"User Action - {action}")


def log_cache_operation(operation: str, key: str, hit: bool = False) -> None:
    """
    캐시 작업 로깅
    
    Args:
        operation: 캐시 작업 (get, set, delete)
        key: 캐시 키
        hit: 캐시 히트 여부
    """
    status = "HIT" if hit else "MISS"
    logger.debug(f"Cache {operation.upper()} - Key: {key}, Status: {status}")


# 애플리케이션 시작 시 로거 설정
setup_logger(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE,
    enable_console=True
)
