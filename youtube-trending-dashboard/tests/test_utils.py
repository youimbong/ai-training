"""
유틸리티 함수 테스트
"""
import pytest
from src.utils.formatters import (
    format_view_count, format_duration, format_relative_time,
    format_channel_title, format_video_title
)
from src.utils.validators import (
    validate_api_key, validate_region_code, validate_category_id,
    validate_max_results, validate_video_id, validate_channel_id
)


class TestFormatters:
    """포맷터 함수 테스트 클래스"""
    
    def test_format_view_count(self):
        """조회수 포맷팅 테스트"""
        assert format_view_count(0) == "조회수 없음"
        assert format_view_count(1000) == "1,000회"
        assert format_view_count(15000) == "1.5만회"
        assert format_view_count(150000000) == "1.5억회"
        assert format_view_count("invalid") == "조회수 없음"
    
    def test_format_duration(self):
        """동영상 길이 포맷팅 테스트"""
        assert format_duration("PT0S") == "0:00"
        assert format_duration("PT4M13S") == "4:13"
        assert format_duration("PT1H23M45S") == "1:23:45"
        assert format_duration("invalid") == "0:00"
    
    def test_format_relative_time(self):
        """상대 시간 포맷팅 테스트"""
        from datetime import datetime, timedelta
        
        # 방금 전
        now = datetime.now().isoformat()
        assert "방금 전" in format_relative_time(now)
        
        # 1시간 전
        one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
        assert "1시간 전" in format_relative_time(one_hour_ago)
        
        # 잘못된 형식
        assert format_relative_time("invalid") == "시간 정보 없음"
    
    def test_format_channel_title(self):
        """채널명 포맷팅 테스트"""
        assert format_channel_title("Short Channel") == "Short Channel"
        assert format_channel_title("Very Long Channel Name That Exceeds Limit") == "Very Long Channel Name That Exce..."
        assert format_channel_title("") == "알 수 없는 채널"
    
    def test_format_video_title(self):
        """동영상 제목 포맷팅 테스트"""
        assert format_video_title("Short Title") == "Short Title"
        assert format_video_title("Very Long Video Title That Exceeds The Maximum Length Limit") == "Very Long Video Title That Exceeds The Maximum Len..."
        assert format_video_title("") == "제목 없음"


class TestValidators:
    """검증 함수 테스트 클래스"""
    
    def test_validate_api_key(self):
        """API 키 검증 테스트"""
        assert validate_api_key("AIzaSyBvOkBwv1wKZq5Kf2v3w4x5y6z7a8b9c0d1e2f3g4h5i6") is True
        assert validate_api_key("invalid") is False
        assert validate_api_key("") is False
        assert validate_api_key(None) is False
    
    def test_validate_region_code(self):
        """지역 코드 검증 테스트"""
        assert validate_region_code("KR") is True
        assert validate_region_code("US") is True
        assert validate_region_code("INVALID") is False
        assert validate_region_code("") is False
        assert validate_region_code(None) is False
    
    def test_validate_category_id(self):
        """카테고리 ID 검증 테스트"""
        assert validate_category_id(0) is True
        assert validate_category_id(10) is True
        assert validate_category_id(-1) is False
        assert validate_category_id("invalid") is False
        assert validate_category_id(None) is False
    
    def test_validate_max_results(self):
        """최대 결과 수 검증 테스트"""
        assert validate_max_results(1) is True
        assert validate_max_results(50) is True
        assert validate_max_results(0) is False
        assert validate_max_results(51) is False
        assert validate_max_results("invalid") is False
    
    def test_validate_video_id(self):
        """동영상 ID 검증 테스트"""
        assert validate_video_id("dQw4w9WgXcQ") is True
        assert validate_video_id("invalid") is False
        assert validate_video_id("") is False
        assert validate_video_id(None) is False
    
    def test_validate_channel_id(self):
        """채널 ID 검증 테스트"""
        assert validate_channel_id("UCuAXFkgsw1L7xaCfnd5JJOw") is True
        assert validate_channel_id("invalid") is False
        assert validate_channel_id("") is False
        assert validate_channel_id(None) is False
