#!/bin/bash
# 로컬 개발 환경 설정 스크립트

echo "🚀 로컬 개발 환경 설정 중..."

# 1. 프로젝트 디렉토리로 이동
cd /workspaces/ai-training/youtube-trending-dashboard

# 2. secrets.toml 파일 확인
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "📝 secrets.toml 파일 생성 중..."
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    echo "⚠️ .streamlit/secrets.toml 파일을 편집하여 실제 API 키를 설정하세요!"
    echo "💡 로컬 개발 시에는 .streamlit/secrets.toml 파일을 사용합니다."
fi

# 3. 가상환경 생성 및 활성화
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
fi

echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 4. 의존성 설치
echo "📚 의존성 설치 중..."
pip install -r requirements.txt

# 5. 설정 확인
echo "✅ 설정 확인 중..."
python3 -c "
from src.config.settings import settings
print('설정 소스:', settings.config_source)
print('API 키 설정:', '✅' if settings.YOUTUBE_API_KEY else '❌')
"

echo "🎉 로컬 개발 환경 설정 완료!"
echo "이제 다음 명령어로 실행하세요:"
echo "source venv/bin/activate"
echo "streamlit run src/streamlit_app.py"
