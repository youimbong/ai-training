"""
컴포넌트 테스트
"""
import pytest
from unittest.mock import Mock, patch
from src.components.video_card import VideoCard
from src.components.pagination import Pagination
from src.components.filters import Filters


class TestVideoCard:
    """동영상 카드 컴포넌트 테스트 클래스"""
    
    @pytest.fixture
    def sample_video_data(self):
        """샘플 동영상 데이터"""
        return {
            'video_id': 'test_video_123',
            'title': 'Test Video Title',
            'full_title': 'Test Video Title - Full Version',
            'description': 'This is a test video description',
            'channel_title': 'Test Channel',
            'full_channel_title': 'Test Channel - Official',
            'channel_id': 'test_channel_123',
            'thumbnail_url': 'https://example.com/thumbnail.jpg',
            'view_count': '1.2만회',
            'raw_view_count': 12000,
            'like_count': '500회',
            'raw_like_count': 500,
            'comment_count': '100회',
            'raw_comment_count': 100,
            'duration': '4:30',
            'raw_duration': 'PT4M30S',
            'published_at': '2시간 전',
            'raw_published_at': '2023-01-01T00:00:00Z',
            'category_id': 10,
            'video_url': 'https://www.youtube.com/watch?v=test_video_123',
            'channel_url': 'https://www.youtube.com/channel/test_channel_123'
        }
    
    def test_render_with_valid_data(self, sample_video_data):
        """유효한 데이터로 렌더링 테스트"""
        # Streamlit 모킹
        with patch('streamlit.container'), \
             patch('streamlit.markdown') as mock_markdown:
            
            VideoCard.render(sample_video_data)
            
            # HTML이 포함된 markdown 호출 확인
            assert mock_markdown.called
            call_args = mock_markdown.call_args[0][0]
            assert 'video-card' in call_args
            assert sample_video_data['title'] in call_args
            assert sample_video_data['channel_title'] in call_args
    
    def test_render_compact_with_valid_data(self, sample_video_data):
        """유효한 데이터로 컴팩트 렌더링 테스트"""
        with patch('streamlit.container'), \
             patch('streamlit.columns'), \
             patch('streamlit.image'), \
             patch('streamlit.markdown'), \
             patch('streamlit.caption'):
            
            VideoCard.render_compact(sample_video_data)
    
    def test_render_grid_with_empty_list(self):
        """빈 목록으로 그리드 렌더링 테스트"""
        with patch('streamlit.info') as mock_info:
            VideoCard.render_grid([])
            mock_info.assert_called_with("표시할 동영상이 없습니다.")
    
    def test_render_list_with_empty_list(self):
        """빈 목록으로 리스트 렌더링 테스트"""
        with patch('streamlit.info') as mock_info:
            VideoCard.render_list([])
            mock_info.assert_called_with("표시할 동영상이 없습니다.")


class TestPagination:
    """페이지네이션 컴포넌트 테스트 클래스"""
    
    def test_render_single_page(self):
        """단일 페이지 렌더링 테스트"""
        with patch('streamlit.markdown') as mock_markdown:
            result = Pagination.render(
                current_page=1,
                total_pages=1,
                total_results=10,
                results_per_page=10
            )
            
            assert result == 1
            # 단일 페이지에서는 페이지네이션 UI가 표시되지 않음
            assert not mock_markdown.called
    
    def test_render_multiple_pages(self):
        """다중 페이지 렌더링 테스트"""
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.selectbox') as mock_selectbox:
            
            # 모의 컬럼과 버튼 설정
            mock_columns.return_value = [Mock(), Mock(), Mock(), Mock(), Mock()]
            mock_button.return_value = False
            mock_selectbox.return_value = 2
            
            result = Pagination.render(
                current_page=1,
                total_pages=5,
                total_results=100,
                results_per_page=20
            )
            
            assert result == 1  # 페이지 변경 없음
    
    def test_render_simple(self):
        """간단한 페이지네이션 렌더링 테스트"""
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.markdown'):
            
            mock_columns.return_value = [Mock(), Mock(), Mock()]
            mock_button.return_value = False
            
            result = Pagination.render_simple(
                current_page=1,
                total_pages=3
            )
            
            assert result == 1
    
    def test_calculate_page_info(self):
        """페이지 정보 계산 테스트"""
        info = Pagination.calculate_page_info(
            total_results=100,
            results_per_page=20,
            current_page=2
        )
        
        assert info['total_pages'] == 5
        assert info['start_result'] == 21
        assert info['end_result'] == 40
        assert info['has_prev'] is True
        assert info['has_next'] is True
    
    def test_get_page_buttons(self):
        """페이지 버튼 계산 테스트"""
        # 5개 이하 페이지
        buttons = Pagination._get_page_buttons(1, 3)
        assert buttons == [1, 2, 3]
        
        # 5개 초과 페이지
        buttons = Pagination._get_page_buttons(3, 10)
        assert len(buttons) == 5
        assert 3 in buttons


class TestFilters:
    """필터 컴포넌트 테스트 클래스"""
    
    def test_render_region_filter(self):
        """지역 필터 렌더링 테스트"""
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "KR - 대한민국"
            
            result = Filters.render_region_filter("KR")
            
            assert result == "KR"
            mock_selectbox.assert_called_once()
    
    def test_render_category_filter(self):
        """카테고리 필터 렌더링 테스트"""
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "음악"
            
            result = Filters.render_category_filter(10)
            
            assert result == 10
            mock_selectbox.assert_called_once()
    
    def test_render_sort_filter(self):
        """정렬 필터 렌더링 테스트"""
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "조회수 높은 순"
            
            result = Filters.render_sort_filter("view_count")
            
            assert result == "view_count"
            mock_selectbox.assert_called_once()
    
    def test_render_results_per_page_filter(self):
        """결과 수 필터 렌더링 테스트"""
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "30개"
            
            result = Filters.render_results_per_page_filter(30)
            
            assert result == 30
            mock_selectbox.assert_called_once()
    
    def test_render_search_filter(self):
        """검색 필터 렌더링 테스트"""
        with patch('streamlit.text_input') as mock_text_input:
            mock_text_input.return_value = "test query"
            
            result = Filters.render_search_filter()
            
            assert result == "test query"
            mock_text_input.assert_called_once()
    
    def test_apply_filters(self):
        """필터 적용 테스트"""
        videos = [
            {
                'raw_view_count': 1000,
                'raw_like_count': 100,
                'raw_duration': 'PT2M30S',
                'raw_published_at': '2023-01-01T00:00:00Z'
            },
            {
                'raw_view_count': 5000,
                'raw_like_count': 500,
                'raw_duration': 'PT5M00S',
                'raw_published_at': '2023-01-02T00:00:00Z'
            }
        ]
        
        filters = {
            'min_views': 2000,
            'min_likes': 200
        }
        
        filtered_videos = Filters.apply_filters(videos, filters)
        
        assert len(filtered_videos) == 1
        assert filtered_videos[0]['raw_view_count'] == 5000
    
    def test_parse_duration_to_seconds(self):
        """동영상 길이 파싱 테스트"""
        # 분:초 형식
        assert Filters._parse_duration_to_seconds('PT2M30S') == 150
        
        # 시간:분:초 형식
        assert Filters._parse_duration_to_seconds('PT1H30M45S') == 5445
        
        # 초만 있는 형식
        assert Filters._parse_duration_to_seconds('PT45S') == 45
        
        # 빈 문자열
        assert Filters._parse_duration_to_seconds('') == 0
        
        # 잘못된 형식
        assert Filters._parse_duration_to_seconds('INVALID') == 0
    
    def test_is_within_period(self):
        """업로드 기간 확인 테스트"""
        from datetime import datetime, timedelta
        
        # 오늘 업로드된 동영상
        today = datetime.now().isoformat()
        assert Filters._is_within_period(today, "오늘") is True
        
        # 어제 업로드된 동영상
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        assert Filters._is_within_period(yesterday, "오늘") is False
        
        # 잘못된 형식
        assert Filters._is_within_period("invalid", "오늘") is True
