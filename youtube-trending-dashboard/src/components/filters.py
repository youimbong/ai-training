"""
필터 컴포넌트
"""
import streamlit as st
from typing import Dict, Any, List, Optional, Union
from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Filters:
    """필터 컴포넌트 클래스"""
    
    @staticmethod
    def render_region_filter(
        current_region: str = "KR",
        key: str = "region_filter"
    ) -> str:
        """
        지역 필터 렌더링
        
        Args:
            current_region: 현재 선택된 지역 코드
            key: Streamlit 위젯 키
            
        Returns:
            선택된 지역 코드
        """
        try:
            region_options = list(settings.SUPPORTED_REGIONS.keys())
            region_labels = [f"{code} - {settings.get_region_name(code)}" for code in region_options]
            
            selected_index = region_options.index(current_region) if current_region in region_options else 0
            
            selected_label = st.selectbox(
                "지역 선택",
                region_labels,
                index=selected_index,
                key=key,
                help="인기 동영상을 조회할 지역을 선택하세요."
            )
            
            # 선택된 라벨에서 지역 코드 추출
            selected_region = selected_label.split(" - ")[0]
            return selected_region
            
        except Exception as e:
            logger.error(f"지역 필터 렌더링 중 오류: {e}")
            return current_region
    
    @staticmethod
    def render_category_filter(
        current_category: int = 0,
        key: str = "category_filter"
    ) -> int:
        """
        카테고리 필터 렌더링
        
        Args:
            current_category: 현재 선택된 카테고리 ID
            key: Streamlit 위젯 키
            
        Returns:
            선택된 카테고리 ID
        """
        try:
            category_options = list(settings.YOUTUBE_CATEGORIES.keys())
            category_labels = [settings.get_category_name(cat_id) for cat_id in category_options]
            
            selected_index = category_options.index(current_category) if current_category in category_options else 0
            
            selected_label = st.selectbox(
                "카테고리 선택",
                category_labels,
                index=selected_index,
                key=key,
                help="동영상 카테고리를 선택하세요."
            )
            
            # 선택된 라벨에서 카테고리 ID 추출
            selected_category = category_options[category_labels.index(selected_label)]
            return selected_category
            
        except Exception as e:
            logger.error(f"카테고리 필터 렌더링 중 오류: {e}")
            return current_category
    
    @staticmethod
    def render_sort_filter(
        current_sort: str = "view_count",
        key: str = "sort_filter"
    ) -> str:
        """
        정렬 필터 렌더링
        
        Args:
            current_sort: 현재 선택된 정렬 기준
            key: Streamlit 위젯 키
            
        Returns:
            선택된 정렬 기준
        """
        try:
            sort_options = {
                "view_count": "조회수 높은 순",
                "published_at": "최신순",
                "title": "제목순",
                "like_count": "좋아요 많은 순",
                "comment_count": "댓글 많은 순"
            }
            
            sort_labels = list(sort_options.values())
            sort_values = list(sort_options.keys())
            
            selected_index = sort_values.index(current_sort) if current_sort in sort_values else 0
            
            selected_label = st.selectbox(
                "정렬 기준",
                sort_labels,
                index=selected_index,
                key=key,
                help="동영상 정렬 기준을 선택하세요."
            )
            
            # 선택된 라벨에서 정렬 기준 추출
            selected_sort = sort_values[sort_labels.index(selected_label)]
            return selected_sort
            
        except Exception as e:
            logger.error(f"정렬 필터 렌더링 중 오류: {e}")
            return current_sort
    
    @staticmethod
    def render_results_per_page_filter(
        current_count: int = 30,
        key: str = "results_per_page_filter"
    ) -> int:
        """
        페이지당 결과 수 필터 렌더링
        
        Args:
            current_count: 현재 선택된 결과 수
            key: Streamlit 위젯 키
            
        Returns:
            선택된 결과 수
        """
        try:
            options = [10, 20, 30, 50]
            labels = [f"{count}개" for count in options]
            
            selected_index = options.index(current_count) if current_count in options else 2
            
            selected_label = st.selectbox(
                "페이지당 결과 수",
                labels,
                index=selected_index,
                key=key,
                help="한 페이지에 표시할 동영상 수를 선택하세요."
            )
            
            # 선택된 라벨에서 결과 수 추출
            selected_count = options[labels.index(selected_label)]
            return selected_count
            
        except Exception as e:
            logger.error(f"결과 수 필터 렌더링 중 오류: {e}")
            return current_count
    
    @staticmethod
    def render_search_filter(
        placeholder: str = "동영상 검색...",
        key: str = "search_filter"
    ) -> str:
        """
        검색 필터 렌더링
        
        Args:
            placeholder: 검색 입력창 플레이스홀더
            key: Streamlit 위젯 키
            
        Returns:
            검색 쿼리
        """
        try:
            search_query = st.text_input(
                "검색",
                placeholder=placeholder,
                key=key,
                help="동영상 제목이나 채널명으로 검색하세요."
            )
            
            return search_query.strip()
            
        except Exception as e:
            logger.error(f"검색 필터 렌더링 중 오류: {e}")
            return ""
    
    @staticmethod
    def render_advanced_filters(
        current_filters: Dict[str, Any] = None,
        key_prefix: str = "advanced"
    ) -> Dict[str, Any]:
        """
        고급 필터 렌더링
        
        Args:
            current_filters: 현재 필터 설정
            key_prefix: 위젯 키 접두사
            
        Returns:
            필터 설정 딕셔너리
        """
        if current_filters is None:
            current_filters = {}
        
        try:
            with st.expander("고급 필터", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    # 최소 조회수 필터
                    min_views = st.number_input(
                        "최소 조회수",
                        min_value=0,
                        value=current_filters.get("min_views", 0),
                        key=f"{key_prefix}_min_views",
                        help="최소 조회수를 설정하세요."
                    )
                    
                    # 최소 좋아요 수 필터
                    min_likes = st.number_input(
                        "최소 좋아요 수",
                        min_value=0,
                        value=current_filters.get("min_likes", 0),
                        key=f"{key_prefix}_min_likes",
                        help="최소 좋아요 수를 설정하세요."
                    )
                
                with col2:
                    # 최대 동영상 길이 필터 (분)
                    max_duration_minutes = st.number_input(
                        "최대 동영상 길이 (분)",
                        min_value=0,
                        value=current_filters.get("max_duration_minutes", 0),
                        key=f"{key_prefix}_max_duration",
                        help="최대 동영상 길이를 분 단위로 설정하세요. 0은 제한 없음입니다."
                    )
                    
                    # 업로드 기간 필터
                    upload_period = st.selectbox(
                        "업로드 기간",
                        ["전체", "오늘", "이번 주", "이번 달", "올해"],
                        index=current_filters.get("upload_period_index", 0),
                        key=f"{key_prefix}_upload_period",
                        help="동영상 업로드 기간을 선택하세요."
                    )
                
                return {
                    "min_views": min_views,
                    "min_likes": min_likes,
                    "max_duration_minutes": max_duration_minutes,
                    "upload_period": upload_period
                }
                
        except Exception as e:
            logger.error(f"고급 필터 렌더링 중 오류: {e}")
            return current_filters
    
    @staticmethod
    def render_main_filters(
        current_region: str = "KR",
        current_category: int = 0,
        current_sort: str = "view_count",
        current_results_per_page: int = 30,
        show_search: bool = True
    ) -> Dict[str, Any]:
        """
        메인 필터들 렌더링
        
        Args:
            current_region: 현재 지역 코드
            current_category: 현재 카테고리 ID
            current_sort: 현재 정렬 기준
            current_results_per_page: 현재 페이지당 결과 수
            show_search: 검색 필터 표시 여부
            
        Returns:
            필터 설정 딕셔너리
        """
        try:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                region = Filters.render_region_filter(current_region)
            
            with col2:
                category = Filters.render_category_filter(current_category)
            
            with col3:
                sort = Filters.render_sort_filter(current_sort)
            
            with col4:
                results_per_page = Filters.render_results_per_page_filter(current_results_per_page)
            
            search_query = ""
            if show_search:
                search_query = Filters.render_search_filter()
            
            return {
                "region": region,
                "category": category,
                "sort": sort,
                "results_per_page": results_per_page,
                "search_query": search_query
            }
            
        except Exception as e:
            logger.error(f"메인 필터 렌더링 중 오류: {e}")
            return {
                "region": current_region,
                "category": current_category,
                "sort": current_sort,
                "results_per_page": current_results_per_page,
                "search_query": ""
            }
    
    @staticmethod
    def apply_filters(
        videos: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        동영상 목록에 필터 적용
        
        Args:
            videos: 동영상 목록
            filters: 필터 설정
            
        Returns:
            필터링된 동영상 목록
        """
        try:
            filtered_videos = videos.copy()
            
            # 최소 조회수 필터
            if filters.get("min_views", 0) > 0:
                filtered_videos = [
                    video for video in filtered_videos
                    if video.get("raw_view_count", 0) >= filters["min_views"]
                ]
            
            # 최소 좋아요 수 필터
            if filters.get("min_likes", 0) > 0:
                filtered_videos = [
                    video for video in filtered_videos
                    if video.get("raw_like_count", 0) >= filters["min_likes"]
                ]
            
            # 최대 동영상 길이 필터
            if filters.get("max_duration_minutes", 0) > 0:
                max_seconds = filters["max_duration_minutes"] * 60
                filtered_videos = [
                    video for video in filtered_videos
                    if Filters._parse_duration_to_seconds(video.get("raw_duration", "PT0S")) <= max_seconds
                ]
            
            # 업로드 기간 필터
            upload_period = filters.get("upload_period", "전체")
            if upload_period != "전체":
                filtered_videos = [
                    video for video in filtered_videos
                    if Filters._is_within_period(video.get("raw_published_at", ""), upload_period)
                ]
            
            return filtered_videos
            
        except Exception as e:
            logger.error(f"필터 적용 중 오류: {e}")
            return videos
    
    @staticmethod
    def _parse_duration_to_seconds(duration: str) -> int:
        """
        ISO 8601 duration을 초 단위로 변환
        
        Args:
            duration: ISO 8601 duration 문자열
            
        Returns:
            초 단위 시간
        """
        import re
        
        if not duration or duration == "PT0S":
            return 0
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)
        
        if not match:
            return 0
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        return hours * 3600 + minutes * 60 + seconds
    
    @staticmethod
    def _is_within_period(published_at: str, period: str) -> bool:
        """
        업로드 시간이 지정된 기간 내에 있는지 확인
        
        Args:
            published_at: 업로드 시간 (ISO 8601)
            period: 기간 ("오늘", "이번 주", "이번 달", "올해")
            
        Returns:
            기간 내 여부
        """
        from datetime import datetime, timedelta
        
        try:
            if published_at.endswith('Z'):
                published_at = published_at[:-1] + '+00:00'
            
            pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.now()
            
            if period == "오늘":
                return pub_time.date() == now.date()
            elif period == "이번 주":
                week_start = now - timedelta(days=now.weekday())
                return pub_time >= week_start
            elif period == "이번 달":
                return pub_time.month == now.month and pub_time.year == now.year
            elif period == "올해":
                return pub_time.year == now.year
            
            return True
            
        except Exception:
            return True
