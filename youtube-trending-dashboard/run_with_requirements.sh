#!/bin/bash
# requirements.txt를 사용하여 실행

echo "🚀 requirements.txt 기반 실행"

# 프로젝트 디렉토리로 이동
cd /workspaces/ai-training/youtube-trending-dashboard

# 가상환경 생성 및 활성화
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
fi

echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# requirements.txt로 설치
echo "📚 requirements.txt에서 설치 중..."
pip install -r requirements.txt

# 의존성 확인
echo "🔍 의존성 확인 중..."
python3 check_dependencies.py

# Streamlit 실행
echo "🎬 Streamlit 실행 중..."
streamlit run src/streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
