# AI 챗봇 API 및 인터페이스 설계

## 1. API 설계 개요

### 1.1 설계 원칙
- **RESTful 원칙 준수**: 표준 HTTP 메서드 활용
- **일관성**: 통일된 응답 형식과 에러 처리
- **확장성**: 버전 관리 및 하위 호환성
- **보안**: 인증/인가 메커니즘
- **성능**: 효율적인 데이터 전송

## 2. 내부 API 인터페이스

### 2.1 AI 서비스 인터페이스

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Generator, Optional
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    """지원되는 AI 모델 타입"""
    OPENAI_GPT4 = "gpt-4"
    OPENAI_GPT35 = "gpt-3.5-turbo"
    CLAUDE_3 = "claude-3"
    CUSTOM = "custom"

@dataclass
class Message:
    """대화 메시지 구조"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: float
    metadata: Optional[Dict] = None

@dataclass
class ChatConfig:
    """채팅 설정 구조"""
    model: ModelType
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    stream: bool = True
    system_prompt: Optional[str] = None

class AIServiceInterface(ABC):
    """AI 서비스 공통 인터페이스"""
    
    @abstractmethod
    async def initialize(self, api_key: str) -> bool:
        """서비스 초기화 및 API 키 검증"""
        pass
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Message],
        config: ChatConfig
    ) -> Message:
        """동기 응답 생성"""
        pass
    
    @abstractmethod
    async def stream_response(
        self,
        messages: List[Message],
        config: ChatConfig
    ) -> Generator[str, None, None]:
        """스트리밍 응답 생성"""
        pass
    
    @abstractmethod
    async def validate_config(self, config: ChatConfig) -> bool:
        """설정 유효성 검증"""
        pass
    
    @abstractmethod
    def get_token_count(self, messages: List[Message]) -> int:
        """토큰 수 계산"""
        pass
```

### 2.2 세션 관리 인터페이스

```python
@dataclass
class SessionData:
    """세션 데이터 구조"""
    session_id: str
    user_id: Optional[str]
    created_at: float
    last_activity: float
    conversation_history: List[Message]
    settings: ChatConfig
    metadata: Dict

class SessionManagerInterface(ABC):
    """세션 관리 인터페이스"""
    
    @abstractmethod
    async def create_session(self, user_id: Optional[str] = None) -> SessionData:
        """새 세션 생성"""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """세션 조회"""
        pass
    
    @abstractmethod
    async def update_session(self, session_id: str, data: SessionData) -> bool:
        """세션 업데이트"""
        pass
    
    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        pass
    
    @abstractmethod
    async def cleanup_expired_sessions(self, ttl_seconds: int = 3600) -> int:
        """만료된 세션 정리"""
        pass
```

### 2.3 대화 관리 인터페이스

```python
from typing import Tuple

class ConversationManagerInterface(ABC):
    """대화 관리 인터페이스"""
    
    @abstractmethod
    async def add_message(
        self, 
        session_id: str, 
        message: Message
    ) -> bool:
        """메시지 추가"""
        pass
    
    @abstractmethod
    async def get_conversation(
        self, 
        session_id: str,
        limit: int = 50
    ) -> List[Message]:
        """대화 내역 조회"""
        pass
    
    @abstractmethod
    async def clear_conversation(self, session_id: str) -> bool:
        """대화 내역 초기화"""
        pass
    
    @abstractmethod
    async def get_context_window(
        self,
        session_id: str,
        max_tokens: int = 4000
    ) -> List[Message]:
        """컨텍스트 윈도우 내 메시지 조회"""
        pass
    
    @abstractmethod
    async def export_conversation(
        self,
        session_id: str,
        format: str = "json"
    ) -> str:
        """대화 내역 내보내기"""
        pass
```

## 3. 외부 API 엔드포인트

### 3.1 REST API 엔드포인트 (옵션)

Streamlit 앱 외에 REST API로 노출이 필요한 경우:

```yaml
# API 엔드포인트 명세

/api/v1/chat:
  post:
    summary: "채팅 메시지 전송"
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              session_id:
                type: string
              message:
                type: string
              config:
                $ref: '#/components/schemas/ChatConfig'
    responses:
      200:
        description: "성공"
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatResponse'

/api/v1/sessions:
  post:
    summary: "새 세션 생성"
    responses:
      201:
        description: "세션 생성됨"
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SessionData'
  
  get:
    summary: "세션 목록 조회"
    parameters:
      - name: user_id
        in: query
        schema:
          type: string
    responses:
      200:
        description: "세션 목록"

/api/v1/sessions/{session_id}:
  get:
    summary: "세션 상세 조회"
  
  delete:
    summary: "세션 삭제"

/api/v1/sessions/{session_id}/messages:
  get:
    summary: "대화 내역 조회"
    parameters:
      - name: limit
        in: query
        schema:
          type: integer
          default: 50
  
  delete:
    summary: "대화 내역 초기화"

/api/v1/models:
  get:
    summary: "사용 가능한 모델 목록"
    responses:
      200:
        description: "모델 목록"
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ModelInfo'
```

## 4. Streamlit 컴포넌트 인터페이스

### 4.1 UI 컴포넌트 구조

```python
# UI 컴포넌트 인터페이스

class ChatUIComponent:
    """채팅 UI 컴포넌트"""
    
    def render_message(self, message: Message) -> None:
        """단일 메시지 렌더링"""
        pass
    
    def render_conversation(self, messages: List[Message]) -> None:
        """전체 대화 렌더링"""
        pass
    
    def render_input_area(self) -> str:
        """입력 영역 렌더링 및 입력값 반환"""
        pass
    
    def render_typing_indicator(self) -> None:
        """타이핑 인디케이터 표시"""
        pass

class SidebarComponent:
    """사이드바 컴포넌트"""
    
    def render_model_selector(self) -> ModelType:
        """모델 선택기"""
        pass
    
    def render_settings(self) -> ChatConfig:
        """설정 패널"""
        pass
    
    def render_conversation_controls(self) -> Dict:
        """대화 제어 버튼"""
        pass

class SettingsComponent:
    """설정 컴포넌트"""
    
    def render_api_key_input(self) -> str:
        """API 키 입력"""
        pass
    
    def render_theme_selector(self) -> str:
        """테마 선택기"""
        pass
    
    def render_language_selector(self) -> str:
        """언어 선택기"""
        pass
```

### 4.2 Streamlit 상태 관리

```python
# Streamlit SessionState 구조

class StreamlitState:
    """Streamlit 세션 상태 관리"""
    
    # 세션 데이터
    session_id: str
    messages: List[Message]
    
    # UI 상태
    is_typing: bool = False
    show_settings: bool = False
    
    # 설정
    current_model: ModelType
    chat_config: ChatConfig
    api_keys: Dict[str, str]
    
    # 캐시
    response_cache: Dict[str, str]
    
    def initialize(self):
        """상태 초기화"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = generate_session_id()
            st.session_state.messages = []
            st.session_state.current_model = ModelType.OPENAI_GPT35
            # ... 기타 초기화
```

## 5. 이벤트 처리 인터페이스

### 5.1 이벤트 핸들러

```python
from typing import Callable, Any

class EventHandler:
    """이벤트 처리 시스템"""
    
    def on_message_sent(self, callback: Callable[[Message], None]):
        """메시지 전송 이벤트"""
        pass
    
    def on_response_received(self, callback: Callable[[Message], None]):
        """응답 수신 이벤트"""
        pass
    
    def on_error(self, callback: Callable[[Exception], None]):
        """오류 발생 이벤트"""
        pass
    
    def on_session_created(self, callback: Callable[[SessionData], None]):
        """세션 생성 이벤트"""
        pass
    
    def on_settings_changed(self, callback: Callable[[ChatConfig], None]):
        """설정 변경 이벤트"""
        pass
```

## 6. 데이터 검증 인터페이스

### 6.1 입력 검증

```python
class InputValidator:
    """입력 검증 클래스"""
    
    @staticmethod
    def validate_message(message: str) -> Tuple[bool, Optional[str]]:
        """메시지 유효성 검증"""
        if not message or len(message.strip()) == 0:
            return False, "메시지를 입력해주세요."
        
        if len(message) > 10000:
            return False, "메시지가 너무 깁니다. (최대 10000자)"
        
        # 악성 콘텐츠 검사
        if contains_malicious_content(message):
            return False, "부적절한 내용이 포함되어 있습니다."
        
        return True, None
    
    @staticmethod
    def validate_api_key(api_key: str, model_type: ModelType) -> bool:
        """API 키 유효성 검증"""
        if model_type == ModelType.OPENAI_GPT4:
            return api_key.startswith("sk-") and len(api_key) > 20
        # ... 다른 모델 검증
        return False
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """입력 텍스트 살균"""
        # XSS 방지
        text = html.escape(text)
        # SQL 인젝션 방지
        text = text.replace("'", "''")
        return text
```

## 7. 에러 처리 인터페이스

### 7.1 에러 타입 정의

```python
class ChatbotError(Exception):
    """챗봇 기본 에러"""
    pass

class APIError(ChatbotError):
    """API 관련 에러"""
    def __init__(self, message: str, status_code: int = 500):
        self.status_code = status_code
        super().__init__(message)

class ValidationError(ChatbotError):
    """검증 에러"""
    pass

class SessionError(ChatbotError):
    """세션 관련 에러"""
    pass

class RateLimitError(ChatbotError):
    """Rate Limit 에러"""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")
```

### 7.2 에러 핸들러

```python
class ErrorHandler:
    """에러 처리 클래스"""
    
    @staticmethod
    def handle_api_error(error: APIError) -> Dict:
        """API 에러 처리"""
        return {
            "error": True,
            "message": str(error),
            "status_code": error.status_code,
            "type": "api_error"
        }
    
    @staticmethod
    def handle_validation_error(error: ValidationError) -> Dict:
        """검증 에러 처리"""
        return {
            "error": True,
            "message": str(error),
            "type": "validation_error"
        }
    
    @staticmethod
    def get_user_friendly_message(error: Exception) -> str:
        """사용자 친화적 에러 메시지"""
        error_messages = {
            APIError: "AI 서비스 연결에 문제가 발생했습니다.",
            ValidationError: "입력값을 확인해주세요.",
            SessionError: "세션이 만료되었습니다. 새로고침해주세요.",
            RateLimitError: "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
        }
        return error_messages.get(type(error), "예상치 못한 오류가 발생했습니다.")
```

## 8. 캐싱 인터페이스

### 8.1 캐시 관리

```python
from functools import lru_cache
import hashlib

class CacheManager:
    """캐시 관리 클래스"""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.cache = {}
    
    def get_cache_key(self, messages: List[Message], config: ChatConfig) -> str:
        """캐시 키 생성"""
        content = json.dumps([m.__dict__ for m in messages])
        content += json.dumps(config.__dict__)
        return hashlib.md5(content.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        if key in self.cache:
            item, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return item
            del self.cache[key]
        return None
    
    async def set(self, key: str, value: Any) -> None:
        """캐시 저장"""
        self.cache[key] = (value, time.time())
    
    async def clear(self) -> None:
        """캐시 초기화"""
        self.cache.clear()
```

## 9. 로깅 인터페이스

### 9.1 구조화된 로깅

```python
import logging
from typing import Any

class StructuredLogger:
    """구조화된 로깅 클래스"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
    
    def log_api_request(self, endpoint: str, params: Dict) -> None:
        """API 요청 로깅"""
        self.logger.info({
            "event": "api_request",
            "endpoint": endpoint,
            "params": params,
            "timestamp": time.time()
        })
    
    def log_api_response(self, endpoint: str, status: int, duration: float) -> None:
        """API 응답 로깅"""
        self.logger.info({
            "event": "api_response",
            "endpoint": endpoint,
            "status": status,
            "duration_ms": duration * 1000,
            "timestamp": time.time()
        })
    
    def log_error(self, error: Exception, context: Dict = None) -> None:
        """에러 로깅"""
        self.logger.error({
            "event": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": time.time()
        })
```

## 10. 테스트 인터페이스

### 10.1 테스트 픽스처

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_ai_service():
    """AI 서비스 목 객체"""
    service = Mock(spec=AIServiceInterface)
    service.generate_response = AsyncMock(return_value=Message(
        role="assistant",
        content="Test response",
        timestamp=time.time()
    ))
    return service

@pytest.fixture
def sample_messages():
    """샘플 메시지 리스트"""
    return [
        Message(role="user", content="Hello", timestamp=time.time()),
        Message(role="assistant", content="Hi there!", timestamp=time.time())
    ]

@pytest.fixture
def chat_config():
    """테스트용 채팅 설정"""
    return ChatConfig(
        model=ModelType.OPENAI_GPT35,
        temperature=0.7,
        max_tokens=1000
    )
```