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
from src.utils.auth import AuthManager

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
    # 인증 상태 초기화
    AuthManager.initialize_auth_state()

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
            <div class="header-content">
                <div class="header-logo">
                    <span class="logo-icon">🎬</span>
                </div>
                <div class="header-text">
                    <h1 class="header-title">
                        <span class="title-icon">📺</span>
                        {settings.APP_TITLE}
                    </h1>
                    <p class="header-subtitle">
                        <span class="subtitle-icon">✨</span>
                        실시간으로 업데이트되는 YouTube 트렌딩 동영상을 만나보세요
                    </p>
                </div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <span class="stat-icon">🌐</span>
                    <span class="stat-label">글로벌 트렌드</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">⚡</span>
                    <span class="stat-label">실시간 업데이트</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">🎯</span>
                    <span class="stat-label">맞춤 필터링</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 사이드바 렌더링
def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        # 사이드바 헤더
        st.markdown(
            """
            <div style="text-align: center; padding: 20px 0;">
                <h2 style="margin: 0; font-size: 24px;">
                    <span style="font-size: 32px;">🎯</span><br>
                    트렌드 필터
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 로그아웃 버튼 (인증이 활성화된 경우만)
        if settings.ENABLE_PASSWORD_AUTH and settings.APP_PASSWORD:
            AuthManager.render_logout_button()
            st.markdown("---")

        # API 키 확인
        if not settings.validate_config():
            st.error("⚠️ YouTube API 키가 설정되지 않았습니다.")
            st.info("환경 변수 YOUTUBE_API_KEY를 설정해주세요.")
            return False

        # 지역 선택 섹션
        st.markdown("### 🌍 지역 선택")
        region = st.selectbox(
            "어느 지역의 트렌드를 보시겠어요?",
            list(settings.SUPPORTED_REGIONS.keys()),
            index=list(settings.SUPPORTED_REGIONS.keys()).index(st.session_state.get('current_region', settings.DEFAULT_REGION)),
            format_func=lambda x: f"{settings.SUPPORTED_REGIONS[x]}",
            help="선택한 지역의 인기 동영상을 보여드립니다"
        )

        # 카테고리 선택 섹션
        st.markdown("### 🎬 카테고리")
        category = st.selectbox(
            "관심있는 주제를 선택하세요",
            list(settings.YOUTUBE_CATEGORIES.keys()),
            index=list(settings.YOUTUBE_CATEGORIES.keys()).index(st.session_state.get('current_category', settings.DEFAULT_CATEGORY)),
            format_func=lambda x: f"{settings.YOUTUBE_CATEGORIES[x]}",
            help="특정 카테고리의 동영상만 필터링합니다"
        )

        # 디스플레이 옵션
        st.markdown("### ✨ 표시 설정")

        col1, col2 = st.columns(2)
        with col1:
            view_mode = st.radio(
                "📱 레이아웃",
                ["grid", "list"],
                format_func=lambda x: "카드형" if x == "grid" else "목록형",
                index=0 if st.session_state.get('view_mode', 'grid') == 'grid' else 1
            )

        with col2:
            results_per_page = st.select_slider(
                "📊 표시 개수",
                options=[10, 20, 30, 50],
                value=st.session_state.get('current_results_per_page', settings.DEFAULT_MAX_RESULTS)
            )

        # 고급 옵션
        st.markdown("### ⚙️ 고급 설정")

        # 정렬 옵션
        sort_by = st.selectbox(
            "🔀 정렬 기준",
            ["view_count", "published_at", "like_count"],
            format_func=lambda x: {"view_count": "조회수 순", "published_at": "최신 순", "like_count": "좋아요 순"}.get(x, x),
            index=0
        )

        # 자동 새로고침
        auto_refresh = st.checkbox(
            "🔄 자동 새로고침 (5분마다)",
            value=st.session_state.get('auto_refresh', False),
            help="5분마다 자동으로 최신 동영상을 불러옵니다"
        )
        
        # 액션 버튼
        st.markdown("### 🚀 실행")

        # 새로고침 버튼
        if st.button("✨ 트렌드 업데이트", type="primary", use_container_width=True):
            st.session_state.loading = True
            st.session_state.videos = []  # 기존 데이터 초기화
            st.rerun()

        # 마지막 업데이트 시간 표시
        if st.session_state.get('last_refresh'):
            import time
            time_str = time.strftime('%H:%M:%S', time.localtime(st.session_state.last_refresh))
            st.caption(f"⏰ 마지막 업데이트: {time_str}")

        # 설정 저장
        st.session_state.update({
            'current_region': region,
            'current_category': category,
            'current_sort': sort_by,
            'current_results_per_page': results_per_page,
            'view_mode': view_mode,
            'auto_refresh': auto_refresh
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

    # 애니메이션과 함께 통계 카드 표시
    st.markdown('<div class="stats-container fade-in">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card scale-in">
                <div class="stat-card-icon">📹</div>
                <div class="stat-card-value">{total_videos:,}개</div>
                <div class="stat-card-label">총 동영상</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card scale-in" style="animation-delay: 0.1s;">
                <div class="stat-card-icon">👁️</div>
                <div class="stat-card-value">{total_views:,}회</div>
                <div class="stat-card-label">총 조회수</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card scale-in" style="animation-delay: 0.2s;">
                <div class="stat-card-icon">👍</div>
                <div class="stat-card-value">{total_likes:,}개</div>
                <div class="stat-card-label">총 좋아요</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card scale-in" style="animation-delay: 0.3s;">
                <div class="stat-card-icon">⏱️</div>
                <div class="stat-card-value">{avg_duration_str}</div>
                <div class="stat-card-label">평균 길이</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # CSS 스타일 추가 (한 번만)
    st.markdown(
        """
        <style>
        .stats-container {
            margin: 2rem 0;
        }

        .stat-card {
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-lg);
            padding: 1.5rem;
            text-align: center;
            transition: var(--transition-medium);
            box-shadow: var(--shadow-sm);
            height: 100%;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-light);
        }

        .stat-card-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }

        .stat-card-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }

        .stat-card-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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

# API 키 확인 (개발 디버깅 제거)
def check_api_key():
    """API 키가 설정되었는지 확인"""
    if not settings.YOUTUBE_API_KEY or "your_youtube_api_key_here" in settings.YOUTUBE_API_KEY:
        st.error("❌ YouTube API 키가 설정되지 않았습니다!")
        st.info("""
        **YouTube API 키 설정 방법:**

        1. [Google Cloud Console](https://console.cloud.google.com/) 접속
        2. 새 프로젝트 생성 또는 기존 프로젝트 선택
        3. YouTube Data API v3 활성화
        4. API 키 생성
        5. `.streamlit/secrets.toml` 파일에서 `youtube_api_key` 값을 실제 키로 변경
        """)
        return False
    return True

# 메인 애플리케이션
def main():
    """메인 애플리케이션 함수"""
    # CSS 로드
    load_css()

    # 세션 상태 초기화
    init_session_state()

    # 인증 체크
    if not AuthManager.is_authenticated():
        AuthManager.render_login_page()
        st.stop()

    # 헤더 렌더링
    render_header()

    # API 키 확인
    if not check_api_key():
        st.stop()

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
                    max_results=st.session_state.get('current_results_per_page', settings.DEFAULT_MAX_RESULTS)
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
    st.markdown(
        f"""
        <div class="footer-container fade-in">
            <div class="footer-divider"></div>
            <div class="footer-content">
                <div class="footer-info">
                    <span class="footer-icon">📺</span>
                    <span class="footer-text">{settings.APP_TITLE}</span>
                </div>
                <div class="footer-separator">|</div>
                <div class="footer-info">
                    <span class="footer-icon">⏱️</span>
                    <span class="footer-text">마지막 업데이트: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_refresh)) if st.session_state.last_refresh else '없음'}</span>
                </div>
                <div class="footer-separator">|</div>
                <div class="footer-info">
                    <span class="footer-icon">🌟</span>
                    <span class="footer-text">실시간 트렌드</span>
                </div>
            </div>
            <div class="footer-copyright">
                <p>Made with ❤️ using YouTube Data API v3</p>
            </div>
        </div>

        <style>
        .footer-container {{
            margin-top: 3rem;
            padding: 2rem 0 1rem 0;
        }}

        .footer-divider {{
            height: 1px;
            background: linear-gradient(to right, transparent, var(--border-color) 20%, var(--border-color) 80%, transparent);
            margin-bottom: 2rem;
        }}

        .footer-content {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }}

        .footer-info {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        .footer-icon {{
            font-size: 1rem;
            opacity: 0.8;
        }}

        .footer-text {{
            font-weight: 500;
        }}

        .footer-separator {{
            color: var(--text-tertiary);
            opacity: 0.5;
        }}

        .footer-copyright {{
            text-align: center;
            color: var(--text-tertiary);
            font-size: 0.75rem;
            opacity: 0.8;
            margin-top: 1rem;
        }}

        .footer-copyright p {{
            margin: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
