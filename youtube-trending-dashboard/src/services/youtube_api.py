"""
YouTube Data API v3 서비스
"""
import time
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config.settings import settings
from ..utils.logger import get_logger, log_api_request, log_api_error, log_performance
from ..utils.validators import validate_api_key, validate_region_code, validate_category_id

logger = get_logger(__name__)


class YouTubeAPIService:
    """YouTube Data API v3 서비스 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        YouTube API 서비스 초기화
        
        Args:
            api_key: YouTube API 키 (없으면 설정에서 가져옴)
        """
        self.api_key = api_key or settings.YOUTUBE_API_KEY
        
        if not validate_api_key(self.api_key):
            raise ValueError("유효하지 않은 YouTube API 키입니다.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.request_count = 0
        self.last_request_time = 0
        
    def _rate_limit_check(self) -> None:
        """API 요청 제한 확인"""
        if not settings.ENABLE_RATE_LIMITING:
            return
            
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        # 최소 1초 간격으로 요청
        if time_since_last_request < 1.0:
            time.sleep(1.0 - time_since_last_request)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HttpError, ConnectionError, TimeoutError))
    )
    def _make_request(self, request_func, *args, **kwargs) -> Dict[str, Any]:
        """
        API 요청 실행 (재시도 로직 포함)
        
        Args:
            request_func: 실행할 요청 함수
            *args: 위치 인수
            **kwargs: 키워드 인수
            
        Returns:
            API 응답 데이터
        """
        self._rate_limit_check()
        
        start_time = time.time()
        try:
            response = request_func(*args, **kwargs).execute()
            duration = time.time() - start_time
            
            log_performance("API Request", duration)
            log_api_request("YouTube API", kwargs, 200)
            
            return response
            
        except HttpError as e:
            log_api_error("YouTube API", e)
            
            if e.resp.status == 403:
                error_msg = "API 할당량을 초과했습니다. 잠시 후 다시 시도해주세요."
            elif e.resp.status == 400:
                error_msg = "잘못된 요청입니다. 파라미터를 확인해주세요."
            elif e.resp.status == 404:
                error_msg = "요청한 리소스를 찾을 수 없습니다."
            else:
                error_msg = f"API 요청 중 오류가 발생했습니다: {e.resp.status}"
            
            raise Exception(error_msg) from e
            
        except Exception as e:
            log_api_error("YouTube API", e)
            raise
    
    def get_trending_videos(
        self,
        region_code: str = "KR",
        category_id: int = 0,
        max_results: int = 30,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        인기 동영상 목록 조회
        
        Args:
            region_code: 지역 코드 (기본값: KR)
            category_id: 카테고리 ID (기본값: 0 = 전체)
            max_results: 최대 결과 수 (기본값: 30)
            page_token: 페이지 토큰 (페이지네이션용)
            
        Returns:
            인기 동영상 목록과 메타데이터
        """
        if not validate_region_code(region_code):
            raise ValueError(f"유효하지 않은 지역 코드입니다: {region_code}")
        
        if not validate_category_id(category_id):
            raise ValueError(f"유효하지 않은 카테고리 ID입니다: {category_id}")
        
        # API 요청 파라미터 구성
        request_params = {
            'part': 'snippet,statistics,contentDetails',
            'chart': 'mostPopular',
            'regionCode': region_code,
            'maxResults': min(max_results, 50),  # API 최대 제한
        }
        
        if category_id > 0:
            request_params['videoCategoryId'] = category_id
        
        if page_token:
            request_params['pageToken'] = page_token
        
        # API 요청 실행
        response = self._make_request(
            self.youtube.videos().list,
            **request_params
        )
        
        return response
    
    def get_video_details(self, video_ids: List[str]) -> Dict[str, Any]:
        """
        동영상 상세 정보 조회
        
        Args:
            video_ids: 동영상 ID 목록
            
        Returns:
            동영상 상세 정보
        """
        if not video_ids:
            return {"items": []}
        
        # API 요청 파라미터 구성
        request_params = {
            'part': 'snippet,statistics,contentDetails',
            'id': ','.join(video_ids[:50])  # API 최대 제한
        }
        
        # API 요청 실행
        response = self._make_request(
            self.youtube.videos().list,
            **request_params
        )
        
        return response
    
    def get_channel_details(self, channel_ids: List[str]) -> Dict[str, Any]:
        """
        채널 상세 정보 조회
        
        Args:
            channel_ids: 채널 ID 목록
            
        Returns:
            채널 상세 정보
        """
        if not channel_ids:
            return {"items": []}
        
        # API 요청 파라미터 구성
        request_params = {
            'part': 'snippet,statistics',
            'id': ','.join(channel_ids[:50])  # API 최대 제한
        }
        
        # API 요청 실행
        response = self._make_request(
            self.youtube.channels().list,
            **request_params
        )
        
        return response
    
    def search_videos(
        self,
        query: str,
        max_results: int = 30,
        order: str = "relevance",
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        동영상 검색
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
            order: 정렬 순서 (relevance, date, rating, viewCount, title)
            page_token: 페이지 토큰
            
        Returns:
            검색 결과
        """
        if not query.strip():
            raise ValueError("검색 쿼리를 입력해주세요.")
        
        # API 요청 파라미터 구성
        request_params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': min(max_results, 50),
            'order': order
        }
        
        if page_token:
            request_params['pageToken'] = page_token
        
        # API 요청 실행
        response = self._make_request(
            self.youtube.search().list,
            **request_params
        )
        
        return response
    
    def get_video_categories(self, region_code: str = "KR") -> Dict[str, Any]:
        """
        동영상 카테고리 목록 조회
        
        Args:
            region_code: 지역 코드
            
        Returns:
            카테고리 목록
        """
        if not validate_region_code(region_code):
            raise ValueError(f"유효하지 않은 지역 코드입니다: {region_code}")
        
        # API 요청 파라미터 구성
        request_params = {
            'part': 'snippet',
            'regionCode': region_code
        }
        
        # API 요청 실행
        response = self._make_request(
            self.youtube.videoCategories().list,
            **request_params
        )
        
        return response
    
    def get_api_quota_usage(self) -> Dict[str, Any]:
        """
        API 할당량 사용량 조회 (대략적)
        
        Returns:
            API 할당량 사용 정보
        """
        return {
            "request_count": self.request_count,
            "last_request_time": self.last_request_time,
            "estimated_quota_used": self.request_count * 100,  # 대략적 계산
            "quota_limit": 10000  # 일일 할당량
        }
