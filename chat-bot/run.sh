#!/bin/bash

# AI 챗봇 실행 스크립트

echo "🤖 AI Chatbot Starting..."
echo ""

# 색상 코드
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 환경 확인
echo -e "${YELLOW}Checking environment...${NC}"

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found${NC}"
    exit 1
fi

# 가상환경 활성화
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Using existing virtual environment${NC}"
    source venv/bin/activate
elif [ -d "venv_simple" ]; then
    echo -e "${GREEN}✅ Using simple virtual environment${NC}"
    source venv_simple/bin/activate
else
    echo -e "${YELLOW}Creating new virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q streamlit openai anthropic python-dotenv
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo -e "${YELLOW}Creating from template...${NC}"
    cat > .env << EOF
# API Keys (at least one required)
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE

# AI Settings (optional - override JSON config)
AI_PROVIDER=openai
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
EOF
    echo -e "${YELLOW}📝 Please edit .env and add your API keys${NC}"
fi

# 설정 파일 확인
if [ ! -f "config/chatbot_settings.json" ]; then
    echo -e "${RED}❌ Configuration file not found${NC}"
    exit 1
fi

# 실행
echo ""
echo -e "${GREEN}🚀 Launching AI Chatbot...${NC}"
echo -e "${YELLOW}📍 URL: http://localhost:8501${NC}"
echo -e "${YELLOW}📖 Press Ctrl+C to stop${NC}"
echo ""

streamlit run streamlit_app.py