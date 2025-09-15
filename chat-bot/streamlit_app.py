"""
AI Chatbot Application
심플하고 깔끔한 챗봇 애플리케이션
모든 설정은 JSON과 환경 변수로 관리
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.chatbot import ChatbotCore
from app.ui import ChatUI

def main():
    """메인 애플리케이션"""
    try:
        # 챗봇 코어 초기화
        chatbot = ChatbotCore()
        
        # API 키 체크
        if not chatbot.is_available():
            import streamlit as st
            st.error("⚠️ API 키가 설정되지 않았습니다!")
            st.info("`.env` 파일에 다음 중 하나를 설정해주세요:")
            st.code("""
OPENAI_API_KEY=your-openai-key
# 또는
ANTHROPIC_API_KEY=your-anthropic-key
            """)
            st.stop()
        
        # UI 초기화 및 실행
        ui = ChatUI(chatbot)
        ui.run()
        
    except Exception as e:
        import streamlit as st
        st.error(f"애플리케이션 오류: {str(e)}")
        st.info("설정 파일과 환경 변수를 확인해주세요.")

if __name__ == "__main__":
    main()