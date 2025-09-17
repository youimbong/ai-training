"""
입력 검증 유틸리티 함수들
"""
import re
from typing import Optional, List, Union
from .formatters import format_view_count


def validate_api_key(api_key: str) -> bool:
    """
    YouTube API 키 유효성 검사
    
    Args:
        api_key: API 키 문자열
        
    Returns:
        유효한 API 키인지 여부
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # YouTube API 키는 보통 39자리이고 영숫자와 하이픈으로 구성
    pattern = r'^[A-Za-z0-9_-]{35,40}$'
    return bool(re.match(pattern, api_key))


def validate_region_code(region_code: str) -> bool:
    """
    지역 코드 유효성 검사
    
    Args:
        region_code: 지역 코드 (예: "KR", "US")
        
    Returns:
        유효한 지역 코드인지 여부
    """
    if not region_code or not isinstance(region_code, str):
        return False
    
    # 2자리 대문자 영문자
    pattern = r'^[A-Z]{2}$'
    return bool(re.match(pattern, region_code))


def validate_category_id(category_id: Union[int, str]) -> bool:
    """
    YouTube 카테고리 ID 유효성 검사
    
    Args:
        category_id: 카테고리 ID
        
    Returns:
        유효한 카테고리 ID인지 여부
    """
    try:
        cat_id = int(category_id)
        # YouTube 카테고리 ID는 0 이상의 정수
        return cat_id >= 0
    except (ValueError, TypeError):
        return False


def validate_max_results(max_results: Union[int, str]) -> bool:
    """
    최대 결과 수 유효성 검사
    
    Args:
        max_results: 최대 결과 수
        
    Returns:
        유효한 최대 결과 수인지 여부
    """
    try:
        results = int(max_results)
        # YouTube API는 1-50 사이의 값을 허용
        return 1 <= results <= 50
    except (ValueError, TypeError):
        return False


def validate_video_id(video_id: str) -> bool:
    """
    YouTube 동영상 ID 유효성 검사
    
    Args:
        video_id: 동영상 ID
        
    Returns:
        유효한 동영상 ID인지 여부
    """
    if not video_id or not isinstance(video_id, str):
        return False
    
    # YouTube 동영상 ID는 11자리 영숫자
    pattern = r'^[A-Za-z0-9_-]{11}$'
    return bool(re.match(pattern, video_id))


def validate_channel_id(channel_id: str) -> bool:
    """
    YouTube 채널 ID 유효성 검사
    
    Args:
        channel_id: 채널 ID
        
    Returns:
        유효한 채널 ID인지 여부
    """
    if not channel_id or not isinstance(channel_id, str):
        return False
    
    # YouTube 채널 ID는 24자리 영숫자
    pattern = r'^[A-Za-z0-9_-]{24}$'
    return bool(re.match(pattern, channel_id))


def sanitize_search_query(query: str) -> str:
    """
    검색 쿼리 문자열 정리
    
    Args:
        query: 검색 쿼리
        
    Returns:
        정리된 검색 쿼리
    """
    if not query:
        return ""
    
    # 특수 문자 제거 및 공백 정리
    cleaned = re.sub(r'[^\w\s가-힣]', '', query)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned


def validate_search_query(query: str) -> bool:
    """
    검색 쿼리 유효성 검사
    
    Args:
        query: 검색 쿼리
        
    Returns:
        유효한 검색 쿼리인지 여부
    """
    if not query or not isinstance(query, str):
        return False
    
    # 최소 1자, 최대 100자
    return 1 <= len(query.strip()) <= 100


def validate_page_number(page: Union[int, str]) -> bool:
    """
    페이지 번호 유효성 검사
    
    Args:
        page: 페이지 번호
        
    Returns:
        유효한 페이지 번호인지 여부
    """
    try:
        page_num = int(page)
        return page_num >= 1
    except (ValueError, TypeError):
        return False


def validate_sort_order(sort_order: str) -> bool:
    """
    정렬 순서 유효성 검사
    
    Args:
        sort_order: 정렬 순서
        
    Returns:
        유효한 정렬 순서인지 여부
    """
    valid_orders = ["relevance", "date", "rating", "viewCount", "title"]
    return sort_order in valid_orders


def validate_boolean(value: Union[bool, str]) -> bool:
    """
    불린 값 유효성 검사
    
    Args:
        value: 검사할 값
        
    Returns:
        유효한 불린 값인지 여부
    """
    if isinstance(value, bool):
        return True
    
    if isinstance(value, str):
        return value.lower() in ["true", "false", "1", "0", "yes", "no"]
    
    return False


def convert_to_boolean(value: Union[bool, str]) -> bool:
    """
    값을 불린으로 변환
    
    Args:
        value: 변환할 값
        
    Returns:
        변환된 불린 값
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ["true", "1", "yes"]
    
    return False
