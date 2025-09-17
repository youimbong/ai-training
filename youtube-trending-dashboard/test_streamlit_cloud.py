#!/usr/bin/env python3
"""
Streamlit Cloud 배포 테스트 스크립트
이 스크립트는 Streamlit Cloud에서 애플리케이션이 올바르게 작동하는지 테스트합니다.
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_imports():
    """필수 모듈 import 테스트"""
    try:
        import streamlit as st
        print("✅ Streamlit import 성공")
        
        from src.config.settings import settings
        print("✅ Settings import 성공")
        
        from src.services.youtube_api import YouTubeAPIService
        print("✅ YouTube API Service import 성공")
        
        from src.services.data_processor import DataProcessor
        print("✅ Data Processor import 성공")
        
        from src.components.video_card import VideoCard
        print("✅ Video Card import 성공")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        return False

def test_settings():
    """설정 로드 테스트"""
    try:
        from src.config.settings import settings
        
        print(f"✅ 앱 제목: {settings.APP_TITLE}")
        print(f"✅ 기본 지역: {settings.DEFAULT_REGION}")
        print(f"✅ 기본 카테고리: {settings.DEFAULT_CATEGORY}")
        print(f"✅ 최대 결과 수: {settings.DEFAULT_MAX_RESULTS}")
        
        # API 키 확인
        if settings.YOUTUBE_API_KEY:
            print("✅ YouTube API 키가 설정되어 있습니다")
        else:
            print("⚠️ YouTube API 키가 설정되지 않았습니다")
        
        return True
        
    except Exception as e:
        print(f"❌ 설정 테스트 오류: {e}")
        return False

def test_streamlit_secrets():
    """Streamlit Secrets 테스트"""
    try:
        import streamlit as st
        
        if hasattr(st, 'secrets') and st.secrets:
            print("✅ Streamlit Secrets 사용 가능")
            
            # 주요 설정 확인
            secrets_to_check = [
                'youtube_api_key',
                'app_title',
                'default_region',
                'default_category',
                'max_results'
            ]
            
            for secret in secrets_to_check:
                if secret in st.secrets:
                    print(f"✅ {secret}: 설정됨")
                else:
                    print(f"⚠️ {secret}: 설정되지 않음")
        else:
            print("⚠️ Streamlit Secrets를 사용할 수 없습니다 (로컬 환경)")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit Secrets 테스트 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 Streamlit Cloud 배포 테스트 시작\n")
    
    tests = [
        ("모듈 Import 테스트", test_imports),
        ("설정 로드 테스트", test_settings),
        ("Streamlit Secrets 테스트", test_streamlit_secrets)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} 통과")
        else:
            print(f"❌ {test_name} 실패")
    
    print(f"\n📊 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 통과했습니다! Streamlit Cloud 배포 준비 완료")
        return 0
    else:
        print("⚠️ 일부 테스트가 실패했습니다. 설정을 확인해주세요.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
