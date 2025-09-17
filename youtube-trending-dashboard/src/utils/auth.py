"""
비밀번호 인증 관리 모듈
"""
import streamlit as st
import hashlib
import time
from typing import Optional
from ..config.settings import settings
from .logger import get_logger

logger = get_logger(__name__)


class AuthManager:
    """비밀번호 인증 관리 클래스"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        비밀번호를 SHA256으로 해시화

        Args:
            password: 평문 비밀번호

        Returns:
            해시화된 비밀번호
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def initialize_auth_state():
        """인증 세션 상태 초기화"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False

        if 'auth_time' not in st.session_state:
            st.session_state.auth_time = None

        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0

        if 'locked_until' not in st.session_state:
            st.session_state.locked_until = None

    @staticmethod
    def is_authenticated() -> bool:
        """
        현재 세션이 인증되었는지 확인

        Returns:
            인증 여부
        """
        # 비밀번호 인증이 비활성화되어 있으면 항상 True
        if not settings.ENABLE_PASSWORD_AUTH:
            return True

        # 비밀번호가 설정되지 않았으면 인증 비활성화
        if not settings.APP_PASSWORD:
            return True

        # 세션 상태 확인
        if not st.session_state.get('authenticated', False):
            return False

        # 세션 타임아웃 확인
        auth_time = st.session_state.get('auth_time')
        if auth_time:
            elapsed = time.time() - auth_time
            if elapsed > settings.AUTH_SESSION_TIMEOUT:
                # 세션 만료
                AuthManager.logout()
                return False

        return True

    @staticmethod
    def is_locked() -> tuple[bool, Optional[int]]:
        """
        계정이 잠겨있는지 확인

        Returns:
            (잠김 여부, 남은 시간(초))
        """
        locked_until = st.session_state.get('locked_until')
        if locked_until:
            remaining = locked_until - time.time()
            if remaining > 0:
                return True, int(remaining)
            else:
                # 잠금 해제
                st.session_state.locked_until = None
                st.session_state.login_attempts = 0
        return False, None

    @staticmethod
    def verify_password(input_password: str) -> bool:
        """
        입력된 비밀번호 검증

        Args:
            input_password: 사용자가 입력한 비밀번호

        Returns:
            비밀번호 일치 여부
        """
        # 잠금 상태 확인
        is_locked, _ = AuthManager.is_locked()
        if is_locked:
            return False

        # 비밀번호 비교 (해시화된 값으로 비교하면 더 안전하지만,
        # secrets.toml에 평문으로 저장하는 경우를 고려하여 직접 비교)
        if input_password == settings.APP_PASSWORD:
            # 로그인 성공
            st.session_state.authenticated = True
            st.session_state.auth_time = time.time()
            st.session_state.login_attempts = 0
            logger.info("Authentication successful")
            return True
        else:
            # 로그인 실패
            st.session_state.login_attempts += 1

            # 5회 실패 시 5분 동안 잠금
            if st.session_state.login_attempts >= 5:
                st.session_state.locked_until = time.time() + 300  # 5분
                logger.warning(f"Account locked after {st.session_state.login_attempts} failed attempts")

            logger.warning(f"Authentication failed - attempt {st.session_state.login_attempts}")
            return False

    @staticmethod
    def logout():
        """로그아웃 처리"""
        st.session_state.authenticated = False
        st.session_state.auth_time = None
        logger.info("User logged out")

    @staticmethod
    def render_login_page():
        """로그인 페이지 렌더링"""
        # 화면 정중앙에 작고 단순한 로그인 폼 배치
        st.markdown(
            """
            <style>
            /* Streamlit 기본 패딩 제거 */
            .block-container {
                padding-top: 3rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # 상단 여백
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        # 중앙 정렬 컨테이너
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            # 로그인 카드
            st.markdown(
                """
                <div style="
                    text-align: center;
                    padding: 2rem;
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔐</div>
                    <h3 style="margin: 0 0 0.5rem 0; color: #333;">YouTube 트렌딩</h3>
                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;">비밀번호를 입력하세요</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 잠금 상태 확인
            is_locked, remaining = AuthManager.is_locked()

            if is_locked:
                minutes = remaining // 60
                seconds = remaining % 60
                st.error(f"⏳ 잠금 상태: {minutes}분 {seconds}초 후 재시도")
                time.sleep(1)
                st.rerun()
            else:
                # 비밀번호 입력 폼
                with st.form("login_form", clear_on_submit=True):
                    password = st.text_input(
                        "비밀번호",
                        type="password",
                        placeholder="비밀번호 입력",
                        label_visibility="collapsed"
                    )

                    submit = st.form_submit_button(
                        "로그인",
                        use_container_width=True,
                        type="primary"
                    )

                    if submit:
                        if password:
                            if AuthManager.verify_password(password):
                                st.success("✅ 로그인 성공")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                attempts_left = 5 - st.session_state.login_attempts
                                if attempts_left > 0:
                                    st.error(f"올바르지 않은 비밀번호 (남은 시도: {attempts_left})")
                                else:
                                    st.error("계정이 잠겼습니다")
                        else:
                            st.warning("비밀번호를 입력하세요")

            # 도움말 링크
            st.markdown(
                """
                <div style="text-align: center; margin-top: 1rem;">
                    <small style="color: #999;">비밀번호를 잊으셨나요?</small>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("도움말", expanded=False):
                st.caption(
                    "**재설정 방법**: `.streamlit/secrets.toml`에서 `app_password` 변경"
                )

    @staticmethod
    def render_logout_button():
        """로그아웃 버튼 렌더링"""
        if st.session_state.get('authenticated', False):
            if st.button("🚪 로그아웃", key="logout_btn"):
                AuthManager.logout()
                st.rerun()