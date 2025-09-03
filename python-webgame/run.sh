#!/bin/bash

# Mirror Maze 게임 서버 실행 스크립트

echo "🎮 Mirror Maze - 빛의 미로 서버를 시작합니다..."
echo "="*50

# 가상환경 확인 및 활성화
if [ -d "venv" ]; then
    echo "✅ 가상환경을 활성화합니다..."
    source venv/bin/activate
else
    echo "⚠️  가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 패키지를 설치합니다..."
    pip install -r requirements.txt
fi

# 환경 변수 로드
if [ -f ".env" ]; then
    echo "✅ 환경 변수를 로드합니다..."
    export $(cat .env | grep -v '^#' | xargs)
fi

echo ""
echo "🚀 게임 서버를 시작합니다..."
echo "="*50
echo "📍 브라우저에서 http://localhost:8000 으로 접속하세요"
echo "🎯 8개의 도전적인 퍼즐이 당신을 기다립니다!"
echo "💡 Ctrl+C로 서버를 종료할 수 있습니다"
echo "="*50
echo ""

# 서버 실행
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000