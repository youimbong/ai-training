"""
YouTube API 서비스 테스트
"""
import pytest
from unittest.mock import Mock, patch
from src.services.youtube_api import YouTubeAPIService
from src.config.settings import settings


class TestYouTubeAPIService:
    """YouTube API 서비스 테스트 클래스"""
    
    @pytest.fixture
    def mock_api_key(self):
        """모의 API 키"""
        return "test_api_key_123456789012345678901234567890123456789"
    
    @pytest.fixture
    def youtube_service(self, mock_api_key):
        """YouTube API 서비스 인스턴스"""
        with patch('src.services.youtube_api.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            return YouTubeAPIService(api_key=mock_api_key)
    
    def test_init_with_valid_api_key(self, mock_api_key):
        """유효한 API 키로 초기화 테스트"""
        with patch('src.services.youtube_api.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            service = YouTubeAPIService(api_key=mock_api_key)
            assert service.api_key == mock_api_key
            assert service.youtube == mock_youtube
    
    def test_init_with_invalid_api_key(self):
        """유효하지 않은 API 키로 초기화 테스트"""
        with pytest.raises(ValueError, match="유효하지 않은 YouTube API 키입니다"):
            YouTubeAPIService(api_key="invalid_key")
    
    def test_init_without_api_key(self):
        """API 키 없이 초기화 테스트"""
        with patch('src.config.settings.settings.YOUTUBE_API_KEY', ''):
            with pytest.raises(ValueError, match="유효하지 않은 YouTube API 키입니다"):
                YouTubeAPIService()
    
    @patch('src.services.youtube_api.time.sleep')
    def test_rate_limit_check(self, mock_sleep, youtube_service):
        """API 요청 제한 확인 테스트"""
        # 첫 번째 요청
        youtube_service._rate_limit_check()
        assert youtube_service.request_count == 1
        
        # 두 번째 요청 (1초 미만 간격)
        youtube_service._rate_limit_check()
        assert youtube_service.request_count == 2
        mock_sleep.assert_called()
    
    def test_get_trending_videos_success(self, youtube_service):
        """인기 동영상 조회 성공 테스트"""
        # 모의 API 응답
        mock_response = {
            'items': [
                {
                    'id': 'test_video_id',
                    'snippet': {
                        'title': 'Test Video',
                        'channelTitle': 'Test Channel',
                        'publishedAt': '2023-01-01T00:00:00Z'
                    },
                    'statistics': {
                        'viewCount': '1000',
                        'likeCount': '100'
                    }
                }
            ],
            'pageInfo': {
                'totalResults': 1,
                'resultsPerPage': 1
            }
        }
        
        # 모의 API 호출
        youtube_service.youtube.videos().list().execute.return_value = mock_response
        
        # API 호출
        response = youtube_service.get_trending_videos(
            region_code="KR",
            category_id=0,
            max_results=30
        )
        
        assert response == mock_response
        assert youtube_service.request_count == 1
    
    def test_get_trending_videos_invalid_region(self, youtube_service):
        """유효하지 않은 지역 코드로 인기 동영상 조회 테스트"""
        with pytest.raises(ValueError, match="유효하지 않은 지역 코드입니다"):
            youtube_service.get_trending_videos(region_code="INVALID")
    
    def test_get_trending_videos_invalid_category(self, youtube_service):
        """유효하지 않은 카테고리 ID로 인기 동영상 조회 테스트"""
        with pytest.raises(ValueError, match="유효하지 않은 카테고리 ID입니다"):
            youtube_service.get_trending_videos(category_id=-1)
    
    def test_get_video_details_success(self, youtube_service):
        """동영상 상세 정보 조회 성공 테스트"""
        mock_response = {
            'items': [
                {
                    'id': 'test_video_id',
                    'snippet': {
                        'title': 'Test Video',
                        'description': 'Test Description'
                    }
                }
            ]
        }
        
        youtube_service.youtube.videos().list().execute.return_value = mock_response
        
        response = youtube_service.get_video_details(['test_video_id'])
        
        assert response == mock_response
    
    def test_get_video_details_empty_list(self, youtube_service):
        """빈 동영상 ID 목록으로 상세 정보 조회 테스트"""
        response = youtube_service.get_video_details([])
        assert response == {'items': []}
    
    def test_get_channel_details_success(self, youtube_service):
        """채널 상세 정보 조회 성공 테스트"""
        mock_response = {
            'items': [
                {
                    'id': 'test_channel_id',
                    'snippet': {
                        'title': 'Test Channel',
                        'description': 'Test Channel Description'
                    }
                }
            ]
        }
        
        youtube_service.youtube.channels().list().execute.return_value = mock_response
        
        response = youtube_service.get_channel_details(['test_channel_id'])
        
        assert response == mock_response
    
    def test_search_videos_success(self, youtube_service):
        """동영상 검색 성공 테스트"""
        mock_response = {
            'items': [
                {
                    'id': {'videoId': 'test_video_id'},
                    'snippet': {
                        'title': 'Search Result',
                        'channelTitle': 'Test Channel'
                    }
                }
            ]
        }
        
        youtube_service.youtube.search().list().execute.return_value = mock_response
        
        response = youtube_service.search_videos("test query")
        
        assert response == mock_response
    
    def test_search_videos_empty_query(self, youtube_service):
        """빈 검색 쿼리로 검색 테스트"""
        with pytest.raises(ValueError, match="검색 쿼리를 입력해주세요"):
            youtube_service.search_videos("")
    
    def test_get_video_categories_success(self, youtube_service):
        """동영상 카테고리 조회 성공 테스트"""
        mock_response = {
            'items': [
                {
                    'id': '1',
                    'snippet': {
                        'title': 'Film & Animation'
                    }
                }
            ]
        }
        
        youtube_service.youtube.videoCategories().list().execute.return_value = mock_response
        
        response = youtube_service.get_video_categories("KR")
        
        assert response == mock_response
    
    def test_get_video_categories_invalid_region(self, youtube_service):
        """유효하지 않은 지역 코드로 카테고리 조회 테스트"""
        with pytest.raises(ValueError, match="유효하지 않은 지역 코드입니다"):
            youtube_service.get_video_categories("INVALID")
    
    def test_get_api_quota_usage(self, youtube_service):
        """API 할당량 사용량 조회 테스트"""
        youtube_service.request_count = 5
        youtube_service.last_request_time = 1234567890
        
        quota_info = youtube_service.get_api_quota_usage()
        
        assert quota_info['request_count'] == 5
        assert quota_info['last_request_time'] == 1234567890
        assert quota_info['estimated_quota_used'] == 500
        assert quota_info['quota_limit'] == 10000
