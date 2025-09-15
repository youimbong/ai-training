"""
Streamlit UI Module
깔끔하고 현대적인 챗봇 UI
"""

import streamlit as st
import json
from datetime import datetime
import time
from typing import Dict, List

class ChatUI:
    """챗봇 UI 클래스 - 순수 채팅 인터페이스"""
    
    def __init__(self, chatbot_core):
        self.chatbot = chatbot_core
        self.config = chatbot_core.config
        self.setup_page()
        self.apply_custom_css()
        
    def setup_page(self):
        """페이지 설정"""
        app_config = self.config.get('app', {})
        st.set_page_config(
            page_title=app_config.get('page_title', '🤖 AI Assistant'),
            page_icon=app_config.get('page_icon', '🤖'),
            layout=app_config.get('layout', 'centered'),
            initial_sidebar_state='collapsed'  # 사이드바 숨김
        )
    
    def apply_custom_css(self):
        """커스텀 CSS 적용"""
        ui_theme = self.config.get('ui', {}).get('theme', {})
        ui_layout = self.config.get('ui', {}).get('layout', {})
        
        css = f"""
        <style>
        /* 메인 컨테이너 스타일 */
        .main {{
            max-width: {ui_layout.get('max_width', '800px')};
            margin: 0 auto;
            padding: {ui_layout.get('padding', '2rem')};
        }}
        
        /* 채팅 메시지 스타일 */
        .stChatMessage {{
            margin-bottom: {ui_layout.get('message_spacing', '1rem')};
            border-radius: {ui_layout.get('border_radius', '10px')};
            animation: fadeIn 0.3s ease-in;
        }}
        
        /* 사용자 메시지 */
        [data-testid="chat-message-user"] {{
            background-color: {ui_theme.get('chat_bubble_user', '#262730')};
        }}
        
        /* AI 메시지 */
        [data-testid="chat-message-assistant"] {{
            background-color: {ui_theme.get('chat_bubble_assistant', '#1A1A1F')};
        }}
        
        /* 입력 필드 스타일 */
        .stChatInputContainer {{
            border-top: 1px solid #333;
            padding-top: 1rem;
            background: linear-gradient(to top, #0E1117, transparent);
        }}
        
        /* 버튼 스타일 */
        .stButton > button {{
            background-color: {ui_theme.get('primary_color', '#FF6B6B')};
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.5rem 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        }}
        
        /* 애니메이션 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* 타이핑 인디케이터 */
        .typing-indicator {{
            display: inline-block;
            padding: 10px;
        }}
        
        .typing-indicator span {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: {ui_theme.get('primary_color', '#FF6B6B')};
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }}
        
        .typing-indicator span:nth-child(2) {{
            animation-delay: 0.2s;
        }}
        
        .typing-indicator span:nth-child(3) {{
            animation-delay: 0.4s;
        }}
        
        @keyframes typing {{
            0%, 60%, 100% {{
                transform: translateY(0);
                opacity: 0.7;
            }}
            30% {{
                transform: translateY(-10px);
                opacity: 1;
            }}
        }}
        
        /* 스크롤바 스타일 */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #1E1E1E;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {ui_theme.get('primary_color', '#FF6B6B')};
            border-radius: 4px;
        }}
        
        /* 헤더 숨기기 */
        header {{
            visibility: hidden;
            height: 0;
        }}
        
        /* 푸터 숨기기 */
        footer {{
            visibility: hidden;
            height: 0;
        }}
        
        /* Streamlit 브랜딩 숨기기 */
        .viewerBadge_container__1QSob {{
            display: none;
        }}
        
        #MainMenu {{
            visibility: hidden;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'input_key' not in st.session_state:
            st.session_state.input_key = 0
            
    def render_header(self):
        """헤더 렌더링"""
        col1, col2 = st.columns([6, 1])
        
        with col1:
            st.markdown(f"### {self.config['app'].get('title', 'AI Assistant')}")
        
        with col2:
            if self.config['features'].get('clear_chat_button', True):
                if st.button("🗑️", help="대화 초기화", key="clear_btn"):
                    st.session_state.messages = []
                    st.session_state.input_key += 1
                    st.rerun()
    
    def render_welcome_message(self):
        """환영 메시지 표시"""
        if not st.session_state.messages:
            welcome_msg = self.config['chat'].get('welcome_message', 'Hello!')
            
            # 제안 프롬프트 표시
            if self.config['features'].get('suggested_prompts', True):
                st.markdown("#### 💡 무엇을 도와드릴까요?")
                
                suggested = self.config.get('suggested_prompts', [])
                cols = st.columns(min(len(suggested), 3))
                
                for idx, prompt in enumerate(suggested[:3]):
                    with cols[idx]:
                        if st.button(
                            prompt, 
                            key=f"suggest_{idx}",
                            use_container_width=True
                        ):
                            st.session_state.prompt_input = prompt
                            st.rerun()
            
            st.markdown("---")
            st.markdown(f"💬 {welcome_msg}")
    
    def render_messages(self):
        """메시지 히스토리 렌더링"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # 복사 버튼 (선택적)
                if self.config['chat'].get('show_copy_button', True):
                    if st.button("📋", key=f"copy_{id(message)}", help="복사"):
                        st.write("Copied!")  # 실제로는 JS로 구현 필요
    
    def render_chat_input(self):
        """채팅 입력 처리"""
        chat_config = self.config.get('chat', {})
        
        # 프롬프트 입력
        if hasattr(st.session_state, 'prompt_input'):
            prompt = st.session_state.prompt_input
            del st.session_state.prompt_input
        else:
            prompt = st.chat_input(
                placeholder=chat_config.get('placeholder', 'Type your message...'),
                key=f"chat_input_{st.session_state.input_key}"
            )
        
        if prompt:
            # 사용자 메시지 추가
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # 사용자 메시지 표시
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI 응답 생성
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 타이핑 인디케이터
                if self.config['features'].get('typing_indicator', True):
                    thinking = chat_config.get('thinking_indicator', '💭 Thinking...')
                    message_placeholder.markdown(thinking)
                    time.sleep(0.5)
                
                # 메시지 준비
                messages = self.chatbot.prepare_messages(
                    st.session_state.messages[:-1],  # 현재 메시지 제외
                    prompt
                )
                
                # 응답 스트리밍
                for chunk in self.chatbot.generate_response(messages):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # AI 응답 저장
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
    
    def render_status_bar(self):
        """상태 바 (선택적)"""
        if self.config['features'].get('show_status', False):
            st.caption(f"Model: {self.config['ai']['model']} | Messages: {len(st.session_state.messages)}")
    
    def run(self):
        """UI 실행"""
        self.initialize_session_state()
        
        # 메인 컨테이너
        with st.container():
            self.render_header()
            
            # 채팅 영역
            chat_container = st.container()
            with chat_container:
                self.render_welcome_message()
                self.render_messages()
            
            # 입력 영역
            self.render_chat_input()
            
            # 상태 바 (선택적)
            self.render_status_bar()