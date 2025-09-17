#!/bin/bash
# requirements.txt를 사용하여 환경 설정 및 실행

echo "🚀 YouTube Trending Dashboard 설정 및 실행"

# 1. 프로젝트 디렉토리로 이동
cd /workspaces/ai-training/youtube-trending-dashboard

# 2. 가상환경 생성 (없는 경우)
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
fi

# 3. 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 4. pip 업그레이드
echo "⬆️ pip 업그레이드 중..."
pip install --upgrade pip

# 5. requirements.txt로 의존성 설치
echo "📚 requirements.txt에서 의존성 설치 중..."
pip install -r requirements.txt

# 6. 설치 확인
echo "✅ 설치 확인 중..."
python -c "
import streamlit
import googleapiclient
import dotenv
import pandas
import numpy
print('✅ 모든 의존성 설치 완료!')
"

# 7. Streamlit 실행
echo "🎬 Streamlit 실행 중..."
streamlit run src/streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
