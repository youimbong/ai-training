#!/bin/bash
# 클라우드 환경 설정 스크립트

echo "🚀 클라우드 환경 설정 시작..."

# 1. 프로젝트 디렉토리로 이동
cd /workspaces/ai-training/youtube-trending-dashboard

# 2. 가상환경 생성
echo "📦 가상환경 생성 중..."
python3 -m venv venv

# 3. 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 4. pip 업그레이드
echo "⬆️ pip 업그레이드 중..."
pip install --upgrade pip

# 5. 의존성 설치
echo "📚 의존성 설치 중..."
pip install -r requirements.txt

# 6. 설치 확인
echo "✅ 설치 확인 중..."
python -c "import dotenv; print('✅ python-dotenv 설치 완료')"
python -c "import streamlit; print('✅ streamlit 설치 완료')"

echo "🎉 설정 완료! 이제 다음 명령어로 실행하세요:"
echo "cd /workspaces/ai-training/youtube-trending-dashboard"
echo "source venv/bin/activate"
echo "streamlit run src/streamlit_app.py"
