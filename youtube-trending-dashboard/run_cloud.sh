#!/bin/bash
# 클라우드 환경에서 Streamlit 실행 스크립트

echo "🚀 YouTube Trending Dashboard 실행 중..."

# 1. 프로젝트 디렉토리로 이동
cd /workspaces/ai-training/youtube-trending-dashboard

# 2. 가상환경이 있는지 확인
if [ ! -d "venv" ]; then
    echo "📦 가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
fi

# 3. 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 4. 의존성 설치 (필요한 경우)
echo "📚 의존성 확인 중..."
pip install -r requirements.txt

# 5. Streamlit 실행
echo "🎬 Streamlit 실행 중..."
streamlit run src/streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
