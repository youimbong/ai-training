"""
동영상 카드 컴포넌트
"""
import streamlit as st
from typing import Dict, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VideoCard:
    """동영상 카드 컴포넌트 클래스"""
    
    @staticmethod
    def render(video_data: Dict[str, Any], show_details: bool = True) -> None:
        """
        동영상 카드 렌더링
        
        Args:
            video_data: 동영상 데이터
            show_details: 상세 정보 표시 여부
        """
        try:
            video_url = video_data.get('video_url', '#')
            
            with st.container():
                # 카드 컨테이너 (클릭 가능한 링크)
                st.markdown(
                    f"""
                    <a href="{video_url}" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="video-card">
                            <div class="video-thumbnail">
                                <img src="{video_data.get('thumbnail_url', '')}" 
                                     alt="{video_data.get('title', '')}"
                                     class="thumbnail-image"
                                     onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjE4MCIgdmlld0JveD0iMCAwIDMyMCAxODAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMjAiIGhlaWdodD0iMTgwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xMzUgNzVMMTY1IDkwTDEzNSAxMDVWNzVaIiBmaWxsPSIjNkI3MjgwIi8+Cjx0ZXh0IHg9IjE2MCIgeT0iMTQwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM2QjcyODAiPkltYWdlIG5vdCBhdmFpbGFibGU8L3RleHQ+Cjwvc3ZnPgo='"
                                     loading="lazy">
                                <div class="video-duration">{video_data.get('duration', '0:00')}</div>
                            </div>
                            <div class="video-info">
                                <h3 class="video-title" title="{video_data.get('full_title', '')}">
                                    {video_data.get('title', '제목 없음')}
                                </h3>
                                <div class="video-channel">
                                    <span class="channel-name" title="{video_data.get('full_channel_title', '')}">
                                        {video_data.get('channel_title', '알 수 없는 채널')}
                                    </span>
                                </div>
                                <div class="video-stats">
                                    <span class="view-count">{video_data.get('view_count', '0회')}</span>
                                    <span class="published-time">{video_data.get('published_at', '시간 정보 없음')}</span>
                                </div>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                
                if show_details:
                    VideoCard._render_details(video_data)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
        except Exception as e:
            logger.error(f"동영상 카드 렌더링 중 오류: {e}")
            st.error("동영상 정보를 표시할 수 없습니다.")
    
    @staticmethod
    def _render_details(video_data: Dict[str, Any]) -> None:
        """
        동영상 상세 정보 렌더링
        
        Args:
            video_data: 동영상 데이터
        """
        with st.expander("상세 정보", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**좋아요:** {video_data.get('like_count', '0')}")
                st.write(f"**댓글 수:** {video_data.get('comment_count', '0')}")
            
            with col2:
                st.write(f"**카테고리 ID:** {video_data.get('category_id', '0')}")
                st.write(f"**동영상 길이:** {video_data.get('duration', '0:00')}")
            
            # 동영상 링크
            if video_data.get('video_url'):
                st.markdown(f"[동영상 보기]({video_data['video_url']})")
            
            # 채널 링크
            if video_data.get('channel_url'):
                st.markdown(f"[채널 보기]({video_data['channel_url']})")
    
    @staticmethod
    def render_compact(video_data: Dict[str, Any]) -> None:
        """
        컴팩트한 동영상 카드 렌더링
        
        Args:
            video_data: 동영상 데이터
        """
        try:
            video_url = video_data.get('video_url', '#')
            
            with st.container():
                # 클릭 가능한 링크로 전체 컨테이너 감싸기
                st.markdown(
                    f"""
                    <a href="{video_url}" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="video-list-item">
                            <div class="video-list-thumbnail-container">
                                <img src="{video_data.get('thumbnail_url', '')}" 
                                     alt="{video_data.get('title', '')}"
                                     class="video-list-thumbnail"
                                     onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjY4IiB2aWV3Qm94PSIwIDAgMTIwIDY4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cmVjdCB3aWR0aD0iMTIwIiBoZWlnaHQ9IjY4IiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik01MCAyNEw2MCAzMkw1MCA0MFYyNFoiIGZpbGw9IiM2QjcyODAiLz4KPC9zdmc+Cg=='"
                                     loading="lazy">
                            </div>
                            <div class="video-list-info">
                                <h4 class="video-list-title" title="{video_data.get('full_title', '')}">
                                    {video_data.get('title', '제목 없음')}
                                </h4>
                                <p class="video-list-channel" title="{video_data.get('full_channel_title', '')}">
                                    {video_data.get('channel_title', '알 수 없는 채널')}
                                </p>
                                <p class="video-list-stats">
                                    {video_data.get('view_count', '0회')} • {video_data.get('published_at', '시간 정보 없음')} • {video_data.get('duration', '0:00')}
                                </p>
                            </div>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            logger.error(f"컴팩트 동영상 카드 렌더링 중 오류: {e}")
            st.error("동영상 정보를 표시할 수 없습니다.")
    
    @staticmethod
    def render_grid(videos: list, columns: int = 3) -> None:
        """
        그리드 형태로 동영상 카드들 렌더링
        
        Args:
            videos: 동영상 목록
            columns: 열 개수
        """
        if not videos:
            st.info("표시할 동영상이 없습니다.")
            return
        
        # 그리드 컬럼 생성
        cols = st.columns(columns)
        
        for i, video in enumerate(videos):
            col_index = i % columns
            with cols[col_index]:
                VideoCard.render(video, show_details=False)
    
    @staticmethod
    def render_list(videos: list) -> None:
        """
        리스트 형태로 동영상 카드들 렌더링
        
        Args:
            videos: 동영상 목록
        """
        if not videos:
            st.info("표시할 동영상이 없습니다.")
            return
        
        for video in videos:
            VideoCard.render_compact(video)
            st.divider()
