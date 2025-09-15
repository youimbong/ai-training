"""
AI Chatbot Core Module
깔끔하고 단순한 챗봇 핵심 로직
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Generator, Any
from datetime import datetime
import openai
import anthropic
from dotenv import load_dotenv

load_dotenv()

class ChatbotCore:
    """챗봇 핵심 클래스 - 모든 AI 상호작용 처리"""
    
    def __init__(self, config_path: str = "config/chatbot_settings.json"):
        self.config = self._load_config(config_path)
        self.setup_ai_clients()
        
    def _load_config(self, config_path: str) -> Dict:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 환경 변수로 오버라이드
            ai_config = config.get('ai', {})
            ai_config['provider'] = os.getenv('AI_PROVIDER', ai_config.get('provider', 'openai'))
            ai_config['model'] = os.getenv('AI_MODEL', ai_config.get('model', 'gpt-3.5-turbo'))
            ai_config['temperature'] = float(os.getenv('AI_TEMPERATURE', ai_config.get('temperature', 0.7)))
            ai_config['max_tokens'] = int(os.getenv('AI_MAX_TOKENS', ai_config.get('max_tokens', 2000)))
            
            return config
        except Exception as e:
            print(f"설정 파일 로드 오류: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """기본 설정 반환"""
        return {
            'ai': {
                'provider': 'openai',
                'model': 'gpt-3.5-turbo',
                'temperature': 0.7,
                'max_tokens': 2000,
                'stream': True,
                'system_prompt': 'You are a helpful AI assistant.'
            },
            'chat': {
                'welcome_message': 'Hello! How can I help you?',
                'error_message': 'An error occurred. Please try again.'
            }
        }
    
    def setup_ai_clients(self):
        """AI 클라이언트 초기화"""
        self.openai_client = None
        self.anthropic_client = None
        
        # OpenAI 설정
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and not openai_key.startswith('sk-proj-YOUR'):
            self.openai_client = openai.OpenAI(api_key=openai_key)
            
        # Anthropic 설정
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and not anthropic_key.startswith('sk-ant-YOUR'):
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
    
    def is_available(self) -> bool:
        """AI 서비스 사용 가능 여부 확인"""
        provider = self.config['ai']['provider']
        if provider == 'openai':
            return self.openai_client is not None
        elif provider == 'anthropic':
            return self.anthropic_client is not None
        return False
    
    def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록 반환"""
        provider = self.config['ai']['provider']
        models_config = self.config.get('models', {})
        return models_config.get(provider, {}).get('available', [])
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        stream: bool = None
    ) -> Generator[str, None, None]:
        """AI 응답 생성"""
        ai_config = self.config['ai']
        provider = ai_config['provider']
        model = ai_config['model']
        temperature = ai_config['temperature']
        max_tokens = ai_config['max_tokens']
        
        if stream is None:
            stream = ai_config.get('stream', True)
        
        try:
            if provider == 'openai':
                yield from self._generate_openai_response(
                    messages, model, temperature, max_tokens, stream
                )
            elif provider == 'anthropic':
                yield from self._generate_anthropic_response(
                    messages, model, temperature, max_tokens, stream
                )
            else:
                yield self.config['chat']['error_message']
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def _generate_openai_response(
        self, messages, model, temperature, max_tokens, stream
    ) -> Generator[str, None, None]:
        """OpenAI 응답 생성"""
        if not self.openai_client:
            yield "OpenAI API key not configured"
            return
            
        try:
            if stream:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            else:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                yield response.choices[0].message.content
        except Exception as e:
            yield f"OpenAI Error: {str(e)}"
    
    def _generate_anthropic_response(
        self, messages, model, temperature, max_tokens, stream
    ) -> Generator[str, None, None]:
        """Anthropic 응답 생성"""
        if not self.anthropic_client:
            yield "Anthropic API key not configured"
            return
            
        try:
            # 시스템 프롬프트 추출
            system_prompt = ""
            conversation = []
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_prompt = msg['content']
                else:
                    conversation.append(msg)
            
            if stream:
                with self.anthropic_client.messages.stream(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else None,
                    messages=conversation
                ) as stream:
                    for text in stream.text_stream:
                        yield text
            else:
                response = self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else None,
                    messages=conversation
                )
                yield response.content[0].text
        except Exception as e:
            yield f"Anthropic Error: {str(e)}"
    
    def prepare_messages(
        self, 
        conversation_history: List[Dict[str, str]], 
        user_input: str
    ) -> List[Dict[str, str]]:
        """메시지 준비 및 포맷팅"""
        messages = []
        
        # 시스템 프롬프트 추가
        system_prompt = self.config['ai'].get('system_prompt', '')
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 대화 기록 추가 (메모리 제한 적용)
        memory_limit = self.config['ai'].get('conversation_memory', 20)
        if conversation_history:
            recent_history = conversation_history[-memory_limit:]
            messages.extend(recent_history)
        
        # 현재 사용자 입력 추가
        messages.append({"role": "user", "content": user_input})
        
        return messages