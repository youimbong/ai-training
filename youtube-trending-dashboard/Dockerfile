# 멀티 스테이지 빌드를 사용한 최적화된 Docker 이미지
FROM python:3.10-slim as builder

# 시스템 패키지 업데이트 및 필요한 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 프로덕션 스테이지
FROM python:3.10-slim

# 시스템 패키지 업데이트 및 필요한 런타임 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 사용자 생성 (보안을 위해 root 사용자 사용 방지)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 작업 디렉토리 설정
WORKDIR /app

# 빌드 스테이지에서 Python 패키지 복사
COPY --from=builder /root/.local /home/appuser/.local

# 애플리케이션 코드 복사
COPY . .

# 로그 디렉토리 생성
RUN mkdir -p logs && chown -R appuser:appuser logs

# 사용자 권한 설정
RUN chown -R appuser:appuser /app
USER appuser

# Python 경로 설정
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app

# 포트 노출
EXPOSE 8501

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# 애플리케이션 실행
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
