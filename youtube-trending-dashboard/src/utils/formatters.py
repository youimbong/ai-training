"""
데이터 포맷팅 유틸리티 함수들
"""
from datetime import datetime, timedelta
from typing import Union
import re


def format_view_count(view_count: Union[int, str]) -> str:
    """
    조회수를 한국어 형식으로 포맷팅
    
    Args:
        view_count: 조회수 (정수 또는 문자열)
        
    Returns:
        포맷팅된 조회수 문자열 (예: "1.2만회", "3.4억회")
    """
    try:
        count = int(view_count)
    except (ValueError, TypeError):
        return "조회수 없음"
    
    if count == 0:
        return "조회수 없음"
    elif count < 10000:
        return f"{count:,}회"
    elif count < 100000000:  # 1억 미만
        return f"{count/10000:.1f}만회"
    else:  # 1억 이상
        return f"{count/100000000:.1f}억회"


def format_duration(duration: str) -> str:
    """
    ISO 8601 duration을 읽기 쉬운 형식으로 변환
    
    Args:
        duration: ISO 8601 duration 문자열 (예: "PT4M13S")
        
    Returns:
        포맷팅된 시간 문자열 (예: "4:13", "1:23:45")
    """
    if not duration or duration == "PT0S":
        return "0:00"
    
    # PT4M13S -> 4:13
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration)
    
    if not match:
        return "0:00"
    
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def format_relative_time(published_at: str) -> str:
    """
    업로드 시간을 상대 시간으로 포맷팅
    
    Args:
        published_at: ISO 8601 datetime 문자열
        
    Returns:
        상대 시간 문자열 (예: "2시간 전", "3일 전", "1주 전")
    """
    try:
        # ISO 8601 형식 파싱
        if published_at.endswith('Z'):
            published_at = published_at[:-1] + '+00:00'
        
        pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.now()
        
        diff = now - pub_time
        
        if diff.days > 0:
            if diff.days == 1:
                return "1일 전"
            elif diff.days < 7:
                return f"{diff.days}일 전"
            elif diff.days < 30:
                weeks = diff.days // 7
                return f"{weeks}주 전"
            elif diff.days < 365:
                months = diff.days // 30
                return f"{months}개월 전"
            else:
                years = diff.days // 365
                return f"{years}년 전"
        else:
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            if hours > 0:
                return f"{hours}시간 전"
            elif minutes > 0:
                return f"{minutes}분 전"
            else:
                return "방금 전"
                
    except (ValueError, TypeError, AttributeError):
        return "시간 정보 없음"


def format_channel_title(channel_title: str, max_length: int = 30) -> str:
    """
    채널명을 지정된 길이로 자르고 말줄임 처리
    
    Args:
        channel_title: 채널명
        max_length: 최대 길이
        
    Returns:
        포맷팅된 채널명
    """
    if not channel_title:
        return "알 수 없는 채널"
    
    if len(channel_title) <= max_length:
        return channel_title
    
    return channel_title[:max_length-3] + "..."


def format_video_title(video_title: str, max_length: int = 50) -> str:
    """
    동영상 제목을 지정된 길이로 자르고 말줄임 처리
    
    Args:
        video_title: 동영상 제목
        max_length: 최대 길이
        
    Returns:
        포맷팅된 동영상 제목
    """
    if not video_title:
        return "제목 없음"
    
    if len(video_title) <= max_length:
        return video_title
    
    return video_title[:max_length-3] + "..."


def format_number_with_commas(number: Union[int, str]) -> str:
    """
    숫자에 천 단위 구분자 추가
    
    Args:
        number: 숫자
        
    Returns:
        천 단위 구분자가 추가된 문자열
    """
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return "0"
