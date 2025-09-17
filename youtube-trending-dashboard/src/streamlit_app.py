"""
YouTube 인기 동영상 대시보드 메인 애플리케이션
"""
import streamlit as st
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.youtube_api import YouTubeAPIService
from src.services.data_processor import DataProcessor
from src.components.video_card import VideoCard
from src.components.pagination import Pagination
from src.components.filters import Filters
from src.utils.logger import get_logger, log_user_action

# 로거 설정
logger = get_logger(__name__)

# 페이지 설정
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon=settings.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 로드
def load_css():
    """커스텀 CSS 스타일 로드"""
    css_path = Path(__file__).parent.parent / "assets" / "styles" / "custom.css"
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 세션 상태 초기화
def init_session_state():
    """세션 상태 초기화"""
    if 'videos' not in st.session_state:
        st.session_state.videos = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    if 'total_pages' not in st.session_state:
        st.session_state.total_pages = 1
    
    if 'total_results' not in st.session_state:
        st.session_state.total_results = 0
    
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = None
    
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'grid'
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False

# 헤더 렌더링
def render_header():
    """애플리케이션 헤더 렌더링"""
    st.markdown(
        f"""
        <div class="header-container">
            <h1 class="header-title">{settings.APP_TITLE}</h1>
            <p class="header-subtitle">실시간 YouTube 인기 동영상을 확인하세요</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 사이드바 렌더링
def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.title("⚙️ 설정")
        
        # API 키 확인
        if not settings.validate_config():
            st.error("⚠️ YouTube API 키가 설정되지 않았습니다.")
            st.info("환경 변수 YOUTUBE_API_KEY를 설정해주세요.")
            
            # 설정 정보 표시 (디버깅용)
            with st.expander("🔧 현재 설정 정보", expanded=False):
                config_info = settings.get_config_info()
                for key, value in config_info.items():
                    st.text(f"{key}: {value}")
            
            return False
        
        # 기본 설정만 유지
        st.subheader("⚙️ 설정")
        
        # 기본 설정값들
        region = st.selectbox(
            "지역",
            list(settings.SUPPORTED_REGIONS.keys()),
            index=list(settings.SUPPORTED_REGIONS.keys()).index(st.session_state.get('current_region', settings.DEFAULT_REGION)),
            help="인기 동영상을 조회할 지역을 선택하세요."
        )
        
        category = st.selectbox(
            "카테고리",
            list(settings.YOUTUBE_CATEGORIES.keys()),
            index=list(settings.YOUTUBE_CATEGORIES.keys()).index(st.session_state.get('current_category', settings.DEFAULT_CATEGORY)),
            help="동영상 카테고리를 선택하세요."
        )
        
        results_per_page = st.selectbox(
            "페이지당 결과 수",
            [10, 20, 30, 50],
            index=[10, 20, 30, 50].index(st.session_state.get('current_results_per_page', settings.DEFAULT_MAX_RESULTS)),
            help="한 페이지에 표시할 동영상 수를 선택하세요."
        )
        
        filters = {
            'region': region,
            'category': category,
            'sort': 'view_count',
            'results_per_page': results_per_page,
            'search_query': ''
        }
        
        advanced_filters = {}
        
        # 뷰 모드 선택
        st.subheader("👁️ 표시 옵션")
        view_mode = st.radio(
            "뷰 모드",
            ["grid", "list"],
            format_func=lambda x: "그리드" if x == "grid" else "리스트",
            index=0 if st.session_state.get('view_mode', 'grid') == 'grid' else 1
        )
        
        # 자동 새로고침
        auto_refresh = st.checkbox(
            "자동 새로고침 (5분마다)",
            value=st.session_state.get('auto_refresh', False)
        )
        
        # 새로고침 버튼
        if st.button("🔄 새로고침", type="primary", use_container_width=True):
            st.session_state.loading = True
            st.session_state.videos = []  # 기존 데이터 초기화
            st.rerun()
        
        # 설정 저장
        st.session_state.update({
            'current_region': region,
            'current_category': category,
            'current_sort': 'view_count',
            'current_results_per_page': results_per_page,
            'view_mode': view_mode,
            'auto_refresh': auto_refresh,
            'advanced_filters': advanced_filters
        })
        
        return True

# 통계 카드 렌더링
def render_stats():
    """통계 카드 렌더링"""
    if not st.session_state.videos:
        return
    
    total_videos = len(st.session_state.videos)
    total_views = sum(video.get('raw_view_count', 0) for video in st.session_state.videos)
    total_likes = sum(video.get('raw_like_count', 0) for video in st.session_state.videos)
    avg_duration = sum(
        Filters._parse_duration_to_seconds(video.get('raw_duration', 'PT0S'))
        for video in st.session_state.videos
    ) / total_videos if total_videos > 0 else 0
    
    # 평균 동영상 길이를 분:초 형식으로 변환
    avg_minutes = int(avg_duration // 60)
    avg_seconds = int(avg_duration % 60)
    avg_duration_str = f"{avg_minutes}:{avg_seconds:02d}"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 동영상", f"{total_videos:,}개")
    
    with col2:
        st.metric("총 조회수", f"{total_views:,}회")
    
    with col3:
        st.metric("총 좋아요", f"{total_likes:,}개")
    
    with col4:
        st.metric("평균 길이", avg_duration_str)

# 동영상 목록 렌더링
def render_videos():
    """동영상 목록 렌더링"""
    if not st.session_state.videos:
        st.info("표시할 동영상이 없습니다. 새로고침해주세요.")
        return
    
    # 정렬 적용 (필터 제거)
    sorted_videos = DataProcessor.sort_videos(
        st.session_state.videos,
        st.session_state.get('current_sort', 'view_count')
    )
    
    # 페이지네이션 계산
    results_per_page = st.session_state.get('current_results_per_page', settings.DEFAULT_MAX_RESULTS)
    total_pages = (len(sorted_videos) + results_per_page - 1) // results_per_page
    current_page = st.session_state.get('current_page', 1)
    
    start_idx = (current_page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    page_videos = sorted_videos[start_idx:end_idx]
    
    # 뷰 모드에 따른 렌더링
    view_mode = st.session_state.get('view_mode', 'grid')
    
    if view_mode == 'grid':
        VideoCard.render_grid(page_videos, columns=3)
    else:
        VideoCard.render_list(page_videos)
    
    # 페이지네이션
    if total_pages > 1:
        new_page = Pagination.render(
            current_page=current_page,
            total_pages=total_pages,
            total_results=len(sorted_videos),
            results_per_page=results_per_page
        )
        
        if new_page and new_page != current_page:
            st.session_state.current_page = new_page
            st.rerun()

# 데이터 로딩
@st.cache_data(ttl=settings.CACHE_TTL)
def load_trending_videos(
    region_code: str,
    category_id: int,
    max_results: int,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    인기 동영상 데이터 로딩 (캐시됨)
    
    Args:
        region_code: 지역 코드
        category_id: 카테고리 ID
        max_results: 최대 결과 수
        page_token: 페이지 토큰
        
    Returns:
        API 응답 데이터
    """
    try:
        youtube_service = YouTubeAPIService()
        response = youtube_service.get_trending_videos(
            region_code=region_code,
            category_id=category_id,
            max_results=max_results,
            page_token=page_token
        )
        
        log_user_action("load_trending_videos", {
            "region": region_code,
            "category": category_id,
            "max_results": max_results
        })
        
        return response
        
    except Exception as e:
        logger.error(f"동영상 데이터 로딩 중 오류: {e}")
        raise

# 설정 상태 표시
def render_config_status():
    """설정 로드 상태 표시"""
    status = settings.get_config_status()
    
    with st.expander("🔧 설정 로드 상태", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("설정 소스", status['config_source'])
            st.metric("로드 성공", "✅" if status['load_success'] else "❌")
        
        with col2:
            st.metric("API 키 설정", "✅" if status['api_key_set'] else "❌")
            st.metric("Secrets 사용 가능", "✅" if status['secrets_available'] else "❌")
        
        if status['load_errors']:
            st.error(f"로드 오류: {', '.join(status['load_errors'])}")
        
        # 상세 설정 정보
        if st.checkbox("상세 설정 정보 보기"):
            config_info = settings.get_config_info()
            for key, value in config_info.items():
                st.text(f"{key}: {value}")
        
        # API 키 디버깅 정보
        st.subheader("🔑 API 키 디버깅")
        api_key_display = settings.get_api_key_display(show_full=False)
        st.text(f"API 키 (부분 표시): {api_key_display}")
        
        # API 키가 플레이스홀더인지 확인
        if "your_youtube_api_key_here" in settings.YOUTUBE_API_KEY:
            st.error("❌ API 키가 설정되지 않았습니다!")
            st.info("""
            **YouTube API 키 설정 방법:**
            
            1. [Google Cloud Console](https://console.cloud.google.com/) 접속
            2. 새 프로젝트 생성 또는 기존 프로젝트 선택
            3. YouTube Data API v3 활성화
            4. API 키 생성
            5. `.streamlit/secrets.toml` 파일에서 `youtube_api_key` 값을 실제 키로 변경
            """)
        
        if st.checkbox("전체 API 키 보기 (디버깅용)"):
            full_api_key = settings.get_api_key_display(show_full=True)
            st.text(f"전체 API 키: {full_api_key}")
            st.warning("⚠️ 보안상 주의: 이 정보를 공유하지 마세요!")

# 메인 애플리케이션
def main():
    """메인 애플리케이션 함수"""
    # CSS 로드
    load_css()
    
    # 설정 상태 출력 (콘솔)
    settings.print_config_status()
    
    # 세션 상태 초기화
    init_session_state()
    
    # 헤더 렌더링
    render_header()
    
    # 설정 상태 표시
    render_config_status()
    
    # 사이드바 렌더링
    if not render_sidebar():
        st.stop()
    
    # 최초 로딩 또는 로딩 상태일 때 데이터 로드
    if st.session_state.loading or not st.session_state.videos:
        with st.spinner("동영상 데이터를 불러오는 중..."):
            try:
                # API 호출
                response = load_trending_videos(
                    region_code=st.session_state.current_region,
                    category_id=st.session_state.current_category,
                    max_results=st.session_state.current_results_per_page
                )
                
                # 데이터 처리
                videos = DataProcessor.process_trending_videos(response)
                pagination_info = DataProcessor.get_pagination_info(response)
                
                # 세션 상태 업데이트
                st.session_state.videos = videos
                st.session_state.total_results = pagination_info['total_results']
                st.session_state.total_pages = pagination_info['total_results'] // st.session_state.current_results_per_page + 1
                st.session_state.current_page = 1
                st.session_state.last_refresh = time.time()
                st.session_state.error_message = None
                
                log_user_action("data_refresh", {
                    "videos_count": len(videos),
                    "region": st.session_state.current_region,
                    "category": st.session_state.current_category
                })
                
            except Exception as e:
                st.session_state.error_message = str(e)
                logger.error(f"데이터 로딩 실패: {e}")
            
            finally:
                st.session_state.loading = False
                if st.session_state.videos:  # 데이터가 로드된 경우에만 rerun
                    st.rerun()
    
    # 에러 메시지 표시
    if st.session_state.error_message:
        st.error(f"❌ 오류가 발생했습니다: {st.session_state.error_message}")
        if st.button("다시 시도"):
            st.session_state.loading = True
            st.rerun()
        return
    
    # 통계 카드 렌더링
    render_stats()
    
    # 동영상 목록 렌더링
    render_videos()
    
    # 자동 새로고침 처리
    if st.session_state.auto_refresh:
        if st.session_state.last_refresh:
            time_since_refresh = time.time() - st.session_state.last_refresh
            if time_since_refresh >= 300:  # 5분
                st.session_state.loading = True
                st.rerun()
        
        # 다음 새로고침까지 남은 시간 표시
        if st.session_state.last_refresh:
            time_remaining = 300 - (time.time() - st.session_state.last_refresh)
            if time_remaining > 0:
                st.info(f"⏰ 다음 자동 새로고침까지 {int(time_remaining)}초 남음")
    
    # 푸터
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: var(--text-secondary); padding: 1rem;">
            <p>📺 {settings.APP_TITLE} | 마지막 업데이트: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.last_refresh)) if st.session_state.last_refresh else '없음'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
