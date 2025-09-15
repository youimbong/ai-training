# 🤖 AI Chatbot

깔끔하고 현대적인 AI 챗봇 애플리케이션입니다.
모든 설정은 JSON 파일로 관리되며, UI는 순수 채팅에만 집중합니다.

## ✨ 주요 특징

- **깔끔한 UI**: 설정 패널 없이 순수 채팅 인터페이스만 제공
- **JSON 기반 설정**: 모든 설정을 `config/chatbot_settings.json`에서 중앙 관리
- **간소화된 구조**: 핵심 모듈만 유지 (app/ 폴더)
- **현대적 디자인**: 애니메이션, 그라데이션, 다크 테마
- **스마트 기능**: 제안 프롬프트, 타이핑 인디케이터, 자동 스크롤

## 📁 폴더 구조

```
chat-bot/
├── app/                      # 핵심 애플리케이션 모듈
│   ├── __init__.py
│   ├── chatbot.py           # AI 처리 로직
│   └── ui.py                # Streamlit UI
├── config/                   
│   └── chatbot_settings.json # 모든 설정 (UI, AI, 기능)
├── streamlit_app.py  # 메인 진입점
├── .env                      # API 키 및 환경 변수
└── run.sh            # 실행 스크립트
```

## 🚀 빠른 시작

### 1. 설치

```bash
# 의존성 설치 (이미 설치된 경우 건너뛰기)
pip install streamlit openai anthropic python-dotenv
```

### 2. API 키 설정

`.env` 파일 편집:
```env
# 최소 하나의 API 키 필요
OPENAI_API_KEY=your-actual-key-here
# 또는
ANTHROPIC_API_KEY=your-actual-key-here
```

### 3. 실행

```bash
./run.sh
# 또는
streamlit run streamlit_app.py
```

## ⚙️ 설정 구조

### config/chatbot_settings.json

```json
{
  "app": {
    "title": "AI Assistant",
    "layout": "centered"
  },
  
  "chat": {
    "welcome_message": "안녕하세요! 😊",
    "placeholder": "메시지를 입력하세요...",
    "thinking_indicator": "💭 생각 중..."
  },
  
  "ai": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 2000,
    "stream": true,
    "system_prompt": "You are a helpful AI assistant."
  },
  
  "ui": {
    "theme": {
      "primary_color": "#FF6B6B",
      "chat_bubble_user": "#262730",
      "chat_bubble_assistant": "#1A1A1F"
    }
  },
  
  "features": {
    "clear_chat_button": true,
    "suggested_prompts": true,
    "typing_indicator": true
  }
}
```

### 환경 변수 오버라이드

JSON 설정을 환경 변수로 오버라이드 가능:

```bash
export AI_PROVIDER=anthropic
export AI_MODEL=claude-3-sonnet-20240229
export AI_TEMPERATURE=0.5
export AI_MAX_TOKENS=3000
```

## 🎨 UI 특징

### 제거된 요소
- ❌ 사이드바 설정 패널
- ❌ 모델 선택 드롭다운
- ❌ Temperature 슬라이더
- ❌ Max tokens 슬라이더
- ❌ 복잡한 설정 옵션들

### 유지된 핵심 기능
- ✅ 깔끔한 채팅 인터페이스
- ✅ 제안 프롬프트
- ✅ 대화 초기화 버튼
- ✅ 타이핑 인디케이터
- ✅ 스트리밍 응답
- ✅ 마크다운 지원

## 🎯 사용자 경험

1. **시작**: 앱 실행 시 환영 메시지와 제안 프롬프트 표시
2. **대화**: 메시지 입력하면 즉시 AI가 응답
3. **초기화**: 우측 상단 🗑️ 버튼으로 대화 초기화
4. **설정 변경**: JSON 파일 수정 후 앱 재시작

## 🛠️ 커스터마이징

### UI 테마 변경
`config/chatbot_settings.json`의 `ui.theme` 섹션 수정:
```json
"theme": {
  "primary_color": "#00D4FF",
  "chat_bubble_user": "#1A2332",
  "chat_bubble_assistant": "#0D1117"
}
```

### 제안 프롬프트 수정
`suggested_prompts` 배열 수정:
```json
"suggested_prompts": [
  "코드 리뷰 도와주세요",
  "아이디어 브레인스토밍",
  "문서 작성 도와주세요"
]
```

### AI 동작 변경
`ai` 섹션에서 모델, 온도, 토큰 수 조정:
```json
"ai": {
  "model": "gpt-4",
  "temperature": 0.3,
  "max_tokens": 3000
}
```

## 📝 주요 개선 사항

1. **UI 단순화**: 모든 설정을 JSON으로 이동, 화면은 채팅만
2. **구조 개선**: src/ 대신 app/ 폴더로 간소화
3. **설정 중앙화**: 하나의 JSON 파일로 모든 설정 관리
4. **현대적 디자인**: CSS 애니메이션, 그라데이션, 부드러운 전환
5. **성능 최적화**: 불필요한 의존성 제거, 핵심 기능만 유지

## 🔧 문제 해결

### API 키 오류
`.env` 파일에 올바른 API 키가 설정되었는지 확인

### 설정이 적용되지 않음
1. `config/chatbot_settings.json` 문법 확인
2. 앱 재시작 필요

### 가상환경 문제
```bash
python3 -m venv venv_new
source venv_new/bin/activate
pip install streamlit openai anthropic python-dotenv
```

---

**즐거운 대화 되세요!** 🚀