"""
데이터 처리 및 변환 서비스
"""
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime

from ..utils.formatters import (
    format_view_count, format_duration, format_relative_time,
    format_channel_title, format_video_title
)
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """데이터 처리 및 변환 클래스"""
    
    @staticmethod
    def process_trending_videos(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        인기 동영상 API 응답을 처리하여 표시용 데이터로 변환
        
        Args:
            api_response: YouTube API 응답 데이터
            
        Returns:
            처리된 동영상 목록
        """
        if not api_response or 'items' not in api_response:
            return []
        
        processed_videos = []
        
        for item in api_response['items']:
            try:
                video_data = DataProcessor._process_single_video(item)
                processed_videos.append(video_data)
            except Exception as e:
                logger.error(f"동영상 데이터 처리 중 오류: {e}")
                continue
        
        return processed_videos
    
    @staticmethod
    def _process_single_video(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        단일 동영상 데이터 처리
        
        Args:
            item: API 응답의 단일 동영상 아이템
            
        Returns:
            처리된 동영상 데이터
        """
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        # 기본 정보
        video_id = item.get('id', '')
        title = snippet.get('title', '제목 없음')
        description = snippet.get('description', '')
        channel_title = snippet.get('channelTitle', '알 수 없는 채널')
        channel_id = snippet.get('channelId', '')
        published_at = snippet.get('publishedAt', '')
        
        # 썸네일 정보
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = DataProcessor._get_best_thumbnail(thumbnails)
        
        # 통계 정보
        view_count = statistics.get('viewCount', '0')
        like_count = statistics.get('likeCount', '0')
        comment_count = statistics.get('commentCount', '0')
        
        # 동영상 길이
        duration = content_details.get('duration', 'PT0S')
        
        # 카테고리 정보
        category_id = snippet.get('categoryId', '0')
        
        return {
            'video_id': video_id,
            'title': format_video_title(title),
            'full_title': title,
            'description': description[:200] + '...' if len(description) > 200 else description,
            'channel_title': format_channel_title(channel_title),
            'full_channel_title': channel_title,
            'channel_id': channel_id,
            'thumbnail_url': thumbnail_url,
            'view_count': format_view_count(view_count),
            'raw_view_count': int(view_count) if view_count.isdigit() else 0,
            'like_count': format_view_count(like_count),
            'raw_like_count': int(like_count) if like_count.isdigit() else 0,
            'comment_count': format_view_count(comment_count),
            'raw_comment_count': int(comment_count) if comment_count.isdigit() else 0,
            'duration': format_duration(duration),
            'raw_duration': duration,
            'published_at': format_relative_time(published_at),
            'raw_published_at': published_at,
            'category_id': int(category_id) if category_id.isdigit() else 0,
            'video_url': f"https://www.youtube.com/watch?v={video_id}",
            'channel_url': f"https://www.youtube.com/channel/{channel_id}"
        }
    
    @staticmethod
    def _get_best_thumbnail(thumbnails: Dict[str, Any]) -> str:
        """
        최적의 썸네일 URL 선택
        
        Args:
            thumbnails: 썸네일 정보 딕셔너리
            
        Returns:
            최적의 썸네일 URL
        """
        # 우선순위: high > medium > default
        for quality in ['high', 'medium', 'default']:
            if quality in thumbnails:
                return thumbnails[quality].get('url', '')
        
        return ''
    
    @staticmethod
    def process_search_results(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        검색 결과 API 응답을 처리
        
        Args:
            api_response: YouTube API 검색 응답 데이터
            
        Returns:
            처리된 검색 결과 목록
        """
        if not api_response or 'items' not in api_response:
            return []
        
        processed_results = []
        
        for item in api_response['items']:
            try:
                result_data = DataProcessor._process_search_item(item)
                processed_results.append(result_data)
            except Exception as e:
                logger.error(f"검색 결과 처리 중 오류: {e}")
                continue
        
        return processed_results
    
    @staticmethod
    def _process_search_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        단일 검색 결과 아이템 처리
        
        Args:
            item: API 응답의 단일 검색 아이템
            
        Returns:
            처리된 검색 결과 데이터
        """
        snippet = item.get('snippet', {})
        video_id = item.get('id', {}).get('videoId', '')
        
        return {
            'video_id': video_id,
            'title': format_video_title(snippet.get('title', '제목 없음')),
            'full_title': snippet.get('title', '제목 없음'),
            'description': snippet.get('description', ''),
            'channel_title': format_channel_title(snippet.get('channelTitle', '알 수 없는 채널')),
            'full_channel_title': snippet.get('channelTitle', '알 수 없는 채널'),
            'channel_id': snippet.get('channelId', ''),
            'thumbnail_url': DataProcessor._get_best_thumbnail(snippet.get('thumbnails', {})),
            'published_at': format_relative_time(snippet.get('publishedAt', '')),
            'raw_published_at': snippet.get('publishedAt', ''),
            'video_url': f"https://www.youtube.com/watch?v={video_id}",
            'channel_url': f"https://www.youtube.com/channel/{snippet.get('channelId', '')}"
        }
    
    @staticmethod
    def process_channel_data(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        채널 데이터 API 응답을 처리
        
        Args:
            api_response: YouTube API 채널 응답 데이터
            
        Returns:
            처리된 채널 데이터
        """
        if not api_response or 'items' not in api_response or not api_response['items']:
            return {}
        
        item = api_response['items'][0]
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        
        return {
            'channel_id': item.get('id', ''),
            'title': snippet.get('title', '알 수 없는 채널'),
            'description': snippet.get('description', ''),
            'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
            'subscriber_count': format_view_count(statistics.get('subscriberCount', '0')),
            'raw_subscriber_count': int(statistics.get('subscriberCount', '0')) if statistics.get('subscriberCount', '0').isdigit() else 0,
            'video_count': format_view_count(statistics.get('videoCount', '0')),
            'view_count': format_view_count(statistics.get('viewCount', '0')),
            'channel_url': f"https://www.youtube.com/channel/{item.get('id', '')}"
        }
    
    @staticmethod
    def create_dataframe(videos: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        동영상 목록을 pandas DataFrame으로 변환
        
        Args:
            videos: 동영상 목록
            
        Returns:
            pandas DataFrame
        """
        if not videos:
            return pd.DataFrame()
        
        df = pd.DataFrame(videos)
        
        # 정렬을 위한 컬럼 추가
        df['sort_key'] = df['raw_view_count']
        
        return df
    
    @staticmethod
    def sort_videos(videos: List[Dict[str, Any]], sort_by: str = 'view_count') -> List[Dict[str, Any]]:
        """
        동영상 목록 정렬
        
        Args:
            videos: 동영상 목록
            sort_by: 정렬 기준 (view_count, published_at, title)
            
        Returns:
            정렬된 동영상 목록
        """
        if not videos:
            return []
        
        reverse = True  # 기본적으로 내림차순
        
        if sort_by == 'title':
            reverse = False  # 제목은 오름차순
        
        try:
            if sort_by == 'view_count':
                return sorted(videos, key=lambda x: x.get('raw_view_count', 0), reverse=reverse)
            elif sort_by == 'published_at':
                return sorted(videos, key=lambda x: x.get('raw_published_at', ''), reverse=reverse)
            elif sort_by == 'title':
                return sorted(videos, key=lambda x: x.get('title', ''), reverse=reverse)
            else:
                return videos
        except Exception as e:
            logger.error(f"정렬 중 오류: {e}")
            return videos
    
    @staticmethod
    def filter_videos_by_category(videos: List[Dict[str, Any]], category_id: int) -> List[Dict[str, Any]]:
        """
        카테고리별 동영상 필터링
        
        Args:
            videos: 동영상 목록
            category_id: 카테고리 ID (0은 전체)
            
        Returns:
            필터링된 동영상 목록
        """
        if category_id == 0:
            return videos
        
        return [video for video in videos if video.get('category_id') == category_id]
    
    @staticmethod
    def get_pagination_info(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        페이지네이션 정보 추출
        
        Args:
            api_response: API 응답 데이터
            
        Returns:
            페이지네이션 정보
        """
        return {
            'total_results': api_response.get('pageInfo', {}).get('totalResults', 0),
            'results_per_page': api_response.get('pageInfo', {}).get('resultsPerPage', 0),
            'next_page_token': api_response.get('nextPageToken'),
            'prev_page_token': api_response.get('prevPageToken')
        }
