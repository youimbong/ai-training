"""
클라우드 환경용 설정 관리 모듈 (dotenv 없이)
"""
import os
import streamlit as st
from typing import Optional, Any, Dict

class CloudSettings:
    """클라우드 환경용 설정 클래스"""
    
    def __init__(self):
        """설정 초기화"""
        self.config_source = None
        self.load_success = False
        self.load_errors = []
        self._load_config()
    
    def _load_config(self):
        """설정 로드"""
        try:
            # Streamlit Secrets 우선
            if hasattr(st, 'secrets') and st.secrets:
                self.config_source = "Streamlit Secrets"
                self._load_from_streamlit_secrets()
            else:
                # 환경 변수 사용
                self.config_source = "Environment Variables"
                self._load_from_env_vars()
            
            self.load_success = True
            print(f"✅ 설정 로드 성공: {self.config_source}")
            
        except Exception as e:
            self.load_success = False
            self.load_errors.append(str(e))
            print(f"❌ 설정 로드 실패: {e}")
            self._load_defaults()
    
    def _load_from_streamlit_secrets(self):
        """Streamlit Secrets에서 설정 로드"""
        self.YOUTUBE_API_KEY = st.secrets.get("youtube_api_key", "")
        self.APP_TITLE = st.secrets.get("app_title", "YouTube 인기 동영상 대시보드")
        self.APP_ICON = st.secrets.get("app_icon", "📺")
        self.DEFAULT_REGION = st.secrets.get("default_region", "KR")
        self.DEFAULT_CATEGORY = int(st.secrets.get("default_category", "0"))
        self.DEFAULT_MAX_RESULTS = int(st.secrets.get("default_max_results", "30"))
        self.CACHE_TTL = int(st.secrets.get("cache_ttl", "300"))
        self.ENABLE_CACHE = st.secrets.get("enable_cache", True)
        self.LOG_LEVEL = st.secrets.get("log_level", "INFO")
        self.LOG_FILE = st.secrets.get("log_file", "logs/app.log")
        self.DEFAULT_THEME = st.secrets.get("default_theme", "light")
        self.ENABLE_DARK_MODE = st.secrets.get("enable_dark_mode", True)
        self.ITEMS_PER_PAGE = int(st.secrets.get("items_per_page", "30"))
        self.MAX_RETRIES = int(st.secrets.get("max_retries", "3"))
        self.REQUEST_TIMEOUT = int(st.secrets.get("request_timeout", "30"))
        self.ENABLE_LAZY_LOADING = st.secrets.get("enable_lazy_loading", True)
        self.ENABLE_RATE_LIMITING = st.secrets.get("enable_rate_limiting", True)
        self.MAX_REQUESTS_PER_MINUTE = int(st.secrets.get("max_requests_per_minute", "100"))
    
    def _load_from_env_vars(self):
        """환경 변수에서 설정 로드"""
        self.YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
        self.APP_TITLE = os.getenv("APP_TITLE", "YouTube 인기 동영상 대시보드")
        self.APP_ICON = os.getenv("APP_ICON", "📺")
        self.DEFAULT_REGION = os.getenv("DEFAULT_REGION", "KR")
        self.DEFAULT_CATEGORY = int(os.getenv("DEFAULT_CATEGORY", "0"))
        self.DEFAULT_MAX_RESULTS = int(os.getenv("DEFAULT_MAX_RESULTS", "30"))
        self.CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
        self.ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
        self.DEFAULT_THEME = os.getenv("DEFAULT_THEME", "light")
        self.ENABLE_DARK_MODE = os.getenv("ENABLE_DARK_MODE", "true").lower() == "true"
        self.ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", "30"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
        self.ENABLE_LAZY_LOADING = os.getenv("ENABLE_LAZY_LOADING", "true").lower() == "true"
        self.ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        self.MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "100"))
    
    def _load_defaults(self):
        """기본값으로 설정 로드"""
        self.YOUTUBE_API_KEY = ""
        self.APP_TITLE = "YouTube 인기 동영상 대시보드"
        self.APP_ICON = "📺"
        self.DEFAULT_REGION = "KR"
        self.DEFAULT_CATEGORY = 0
        self.DEFAULT_MAX_RESULTS = 30
        self.CACHE_TTL = 300
        self.ENABLE_CACHE = True
        self.LOG_LEVEL = "INFO"
        self.LOG_FILE = "logs/app.log"
        self.DEFAULT_THEME = "light"
        self.ENABLE_DARK_MODE = True
        self.ITEMS_PER_PAGE = 30
        self.MAX_RETRIES = 3
        self.REQUEST_TIMEOUT = 30
        self.ENABLE_LAZY_LOADING = True
        self.ENABLE_RATE_LIMITING = True
        self.MAX_REQUESTS_PER_MINUTE = 100
    
    # 클래스 속성들
    YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    SUPPORTED_REGIONS = {
        "KR": "대한민국", "US": "미국", "JP": "일본", "GB": "영국",
        "CA": "캐나다", "AU": "호주", "DE": "독일", "FR": "프랑스",
        "IN": "인도", "BR": "브라질"
    }
    
    YOUTUBE_CATEGORIES = {
        0: "전체", 1: "영화 및 애니메이션", 2: "자동차 및 차량",
        10: "음악", 15: "애완동물 및 동물", 17: "스포츠",
        18: "짧은 영화", 19: "여행 및 이벤트", 20: "게임",
        21: "비디오 블로그", 22: "사람 및 블로그", 23: "코미디",
        24: "엔터테인먼트", 25: "뉴스 및 정치", 26: "Howto & Style",
        27: "교육", 28: "과학 및 기술"
    }
    
    def validate_config(self) -> bool:
        """설정 유효성 검사"""
        return bool(self.YOUTUBE_API_KEY)
    
    def get_region_name(self, region_code: str) -> str:
        """지역 코드로부터 지역명 반환"""
        return self.SUPPORTED_REGIONS.get(region_code, region_code)
    
    def get_category_name(self, category_id: int) -> str:
        """카테고리 ID로부터 카테고리명 반환"""
        return self.YOUTUBE_CATEGORIES.get(category_id, "알 수 없음")
    
    def get_config_status(self) -> Dict[str, Any]:
        """설정 로드 상태 정보 반환"""
        return {
            "config_source": self.config_source,
            "load_success": self.load_success,
            "load_errors": self.load_errors,
            "api_key_set": bool(self.YOUTUBE_API_KEY),
            "secrets_available": hasattr(st, 'secrets') and bool(st.secrets) if 'st' in globals() else False
        }
    
    def print_config_status(self):
        """설정 상태를 콘솔에 출력"""
        status = self.get_config_status()
        print("\n" + "="*50)
        print("🔧 클라우드 설정 로드 상태")
        print("="*50)
        print(f"설정 소스: {status['config_source']}")
        print(f"로드 성공: {'✅' if status['load_success'] else '❌'}")
        print(f"API 키 설정: {'✅' if status['api_key_set'] else '❌'}")
        print(f"Secrets 사용 가능: {'✅' if status['secrets_available'] else '❌'}")
        
        if status['load_errors']:
            print(f"오류: {', '.join(status['load_errors'])}")
        
        print("="*50)

# 전역 설정 인스턴스
settings = CloudSettings()
