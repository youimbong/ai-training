"""
페이지네이션 컴포넌트
"""
import streamlit as st
from typing import Dict, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Pagination:
    """페이지네이션 컴포넌트 클래스"""
    
    @staticmethod
    def render(
        current_page: int,
        total_pages: int,
        total_results: int,
        results_per_page: int,
        on_page_change: callable = None
    ) -> Optional[int]:
        """
        페이지네이션 UI 렌더링
        
        Args:
            current_page: 현재 페이지 번호
            total_pages: 전체 페이지 수
            total_results: 전체 결과 수
            results_per_page: 페이지당 결과 수
            on_page_change: 페이지 변경 콜백 함수
            
        Returns:
            선택된 페이지 번호
        """
        if total_pages <= 1:
            return current_page
        
        try:
            # 페이지네이션 컨테이너
            st.markdown(
                f"""
                <div class="pagination-container">
                    <div class="pagination-info">
                        총 {total_results:,}개의 결과 중 {((current_page - 1) * results_per_page) + 1:,}-{min(current_page * results_per_page, total_results):,}개 표시
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # 페이지 버튼들
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
            
            with col1:
                if st.button("◀◀", key="first_page", disabled=current_page == 1):
                    return 1
            
            with col2:
                if st.button("◀", key="prev_page", disabled=current_page == 1):
                    return max(1, current_page - 1)
            
            with col3:
                # 페이지 번호 선택
                page_options = list(range(1, total_pages + 1))
                selected_page = st.selectbox(
                    "페이지",
                    page_options,
                    index=current_page - 1,
                    key="page_selector",
                    label_visibility="collapsed"
                )
                
                if selected_page != current_page:
                    return selected_page
            
            with col4:
                if st.button("▶", key="next_page", disabled=current_page == total_pages):
                    return min(total_pages, current_page + 1)
            
            with col5:
                if st.button("▶▶", key="last_page", disabled=current_page == total_pages):
                    return total_pages
            
            return current_page
            
        except Exception as e:
            logger.error(f"페이지네이션 렌더링 중 오류: {e}")
            return current_page
    
    @staticmethod
    def render_simple(
        current_page: int,
        total_pages: int,
        on_page_change: callable = None
    ) -> Optional[int]:
        """
        간단한 페이지네이션 UI 렌더링
        
        Args:
            current_page: 현재 페이지 번호
            total_pages: 전체 페이지 수
            on_page_change: 페이지 변경 콜백 함수
            
        Returns:
            선택된 페이지 번호
        """
        if total_pages <= 1:
            return current_page
        
        try:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("이전", disabled=current_page == 1):
                    return max(1, current_page - 1)
            
            with col2:
                st.markdown(
                    f"<div style='text-align: center; padding: 0.5rem;'>"
                    f"페이지 {current_page} / {total_pages}"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            with col3:
                if st.button("다음", disabled=current_page == total_pages):
                    return min(total_pages, current_page + 1)
            
            return current_page
            
        except Exception as e:
            logger.error(f"간단한 페이지네이션 렌더링 중 오류: {e}")
            return current_page
    
    @staticmethod
    def render_with_jump(
        current_page: int,
        total_pages: int,
        total_results: int,
        results_per_page: int
    ) -> Optional[int]:
        """
        페이지 점프 기능이 있는 페이지네이션 UI 렌더링
        
        Args:
            current_page: 현재 페이지 번호
            total_pages: 전체 페이지 수
            total_results: 전체 결과 수
            results_per_page: 페이지당 결과 수
            
        Returns:
            선택된 페이지 번호
        """
        if total_pages <= 1:
            return current_page
        
        try:
            # 결과 정보 표시
            start_result = ((current_page - 1) * results_per_page) + 1
            end_result = min(current_page * results_per_page, total_results)
            
            st.markdown(
                f"**{total_results:,}개 결과 중 {start_result:,}-{end_result:,}개 표시**"
            )
            
            # 페이지 점프 입력
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                jump_page = st.number_input(
                    "페이지로 이동",
                    min_value=1,
                    max_value=total_pages,
                    value=current_page,
                    key="jump_page_input"
                )
                
                if st.button("이동", key="jump_button"):
                    return jump_page
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # 공간 확보
            
            with col3:
                # 페이지 번호 버튼들 (최대 5개)
                page_buttons = Pagination._get_page_buttons(current_page, total_pages)
                
                for page_num in page_buttons:
                    if st.button(
                        str(page_num),
                        key=f"page_btn_{page_num}",
                        disabled=page_num == current_page
                    ):
                        return page_num
            
            return current_page
            
        except Exception as e:
            logger.error(f"점프 페이지네이션 렌더링 중 오류: {e}")
            return current_page
    
    @staticmethod
    def _get_page_buttons(current_page: int, total_pages: int, max_buttons: int = 5) -> list:
        """
        표시할 페이지 번호 버튼들 계산
        
        Args:
            current_page: 현재 페이지 번호
            total_pages: 전체 페이지 수
            max_buttons: 최대 버튼 수
            
        Returns:
            페이지 번호 리스트
        """
        if total_pages <= max_buttons:
            return list(range(1, total_pages + 1))
        
        half = max_buttons // 2
        start = max(1, current_page - half)
        end = min(total_pages, start + max_buttons - 1)
        
        if end - start + 1 < max_buttons:
            start = max(1, end - max_buttons + 1)
        
        return list(range(start, end + 1))
    
    @staticmethod
    def calculate_page_info(
        total_results: int,
        results_per_page: int,
        current_page: int
    ) -> Dict[str, int]:
        """
        페이지 정보 계산
        
        Args:
            total_results: 전체 결과 수
            results_per_page: 페이지당 결과 수
            current_page: 현재 페이지 번호
            
        Returns:
            페이지 정보 딕셔너리
        """
        total_pages = (total_results + results_per_page - 1) // results_per_page
        start_result = ((current_page - 1) * results_per_page) + 1
        end_result = min(current_page * results_per_page, total_results)
        
        return {
            "total_pages": total_pages,
            "start_result": start_result,
            "end_result": end_result,
            "has_prev": current_page > 1,
            "has_next": current_page < total_pages
        }
