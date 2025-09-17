#!/usr/bin/env python3
"""
YouTube 인기 동영상 대시보드 실행 스크립트
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """메인 실행 함수"""
    try:
        # 환경 변수 확인
        if not os.getenv('YOUTUBE_API_KEY'):
            print("❌ 오류: YOUTUBE_API_KEY 환경 변수가 설정되지 않았습니다.")
            print("💡 해결 방법:")
            print("   1. .env 파일을 생성하고 YOUTUBE_API_KEY를 설정하세요")
            print("   2. 또는 환경 변수로 직접 설정하세요: export YOUTUBE_API_KEY='your_key'")
            sys.exit(1)
        
        # Streamlit 앱 실행
        import streamlit.web.cli as stcli
        import streamlit as st
        
        # Streamlit 설정
        sys.argv = [
            "streamlit",
            "run",
            str(project_root / "src" / "streamlit_app.py"),
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ]
        
        print("🚀 YouTube 인기 동영상 대시보드를 시작합니다...")
        print("📺 브라우저에서 http://localhost:8501 을 열어주세요")
        
        # Streamlit 실행
        stcli.main()
        
    except KeyboardInterrupt:
        print("\n👋 애플리케이션을 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
