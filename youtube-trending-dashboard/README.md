# 📺 YouTube 인기 동영상 대시보드

YouTube Data API v3를 활용하여 실시간 인기 동영상을 모니터링할 수 있는 Streamlit 기반 웹 애플리케이션입니다.

## ✨ 주요 기능

### 핵심 기능
- 🎬 **실시간 인기 동영상 조회**: YouTube Data API v3를 통한 실시간 데이터
- 🎯 **다양한 필터링**: 지역별, 카테고리별, 정렬 옵션
- 🔍 **검색 기능**: 키워드 기반 동영상 검색
- 📱 **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원
- 🌙 **다크모드 지원**: 사용자 선호에 따른 테마 변경
- ⚡ **자동 새로고침**: 설정 가능한 자동 데이터 업데이트

### 고급 기능
- 📊 **통계 대시보드**: 조회수, 좋아요, 댓글 수 등 상세 통계
- 🎨 **커스터마이징**: 그리드/리스트 뷰, 페이지당 결과 수 조정
- 🔄 **캐싱 시스템**: 성능 최적화를 위한 스마트 캐싱
- 📝 **로깅 시스템**: 상세한 로그 및 에러 추적
- 🛡️ **에러 처리**: 사용자 친화적인 에러 메시지

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/youtube-trending-dashboard.git
cd youtube-trending-dashboard
```

### 2. 환경 설정

**Streamlit Secrets 사용 (권장)**
```bash
# 자동 설정 스크립트 실행
./setup_local_dev.sh

# secrets.toml 파일 편집하여 YouTube API 키 설정
nano .streamlit/secrets.toml
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
streamlit run src/streamlit_app.py
```

## 🐳 Docker를 사용한 실행

### Docker Compose 사용 (권장)
```bash
# 환경 변수 설정
export YOUTUBE_API_KEY="your_api_key_here"

# 애플리케이션 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### Docker 직접 실행
```bash
# 이미지 빌드
docker build -t youtube-dashboard .

# 컨테이너 실행
docker run -p 8501:8501 \
  -e YOUTUBE_API_KEY="your_api_key_here" \
  youtube-dashboard
```

## ⚙️ 설정

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `YOUTUBE_API_KEY` | - | YouTube Data API v3 키 (필수) |
| `APP_TITLE` | "YouTube 인기 동영상 대시보드" | 애플리케이션 제목 |
| `DEFAULT_REGION` | "KR" | 기본 지역 코드 |
| `DEFAULT_CATEGORY` | 0 | 기본 카테고리 ID (0=전체) |
| `DEFAULT_MAX_RESULTS` | 30 | 기본 결과 수 |
| `CACHE_TTL` | 300 | 캐시 유지 시간 (초) |
| `LOG_LEVEL` | "INFO" | 로그 레벨 |
| `DEFAULT_THEME` | "light" | 기본 테마 |

### YouTube API 키 발급

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. YouTube Data API v3 활성화
4. API 키 생성 및 제한 설정
5. 생성된 API 키를 `.env` 파일에 설정

## 📁 프로젝트 구조

```
youtube-trending-dashboard/
├── 📁 src/
│   ├── 📄 streamlit_app.py          # 메인 애플리케이션
│   ├── 📁 components/               # UI 컴포넌트
│   │   ├── 📄 video_card.py         # 동영상 카드
│   │   ├── 📄 pagination.py         # 페이지네이션
│   │   └── 📄 filters.py            # 필터 컴포넌트
│   ├── 📁 services/                 # 비즈니스 로직
│   │   ├── 📄 youtube_api.py        # YouTube API 래퍼
│   │   └── 📄 data_processor.py     # 데이터 처리
│   ├── 📁 utils/                    # 유틸리티
│   │   ├── 📄 formatters.py         # 데이터 포맷터
│   │   ├── 📄 validators.py         # 입력 검증
│   │   └── 📄 logger.py             # 로깅
│   └── 📁 config/                   # 설정
│       └── 📄 settings.py           # 앱 설정
├── 📁 tests/                        # 테스트 코드
├── 📁 assets/                       # 정적 자원
│   └── 📁 styles/
│       └── 📄 custom.css            # 커스텀 스타일
├── 📄 requirements.txt              # Python 의존성
├── 📄 Dockerfile                    # Docker 설정
├── 📄 docker-compose.yml            # Docker Compose 설정
├── 📄 .env.example                  # 환경 변수 예시
└── 📄 README.md                     # 프로젝트 문서
```

## 🧪 테스트

### 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=src --cov-report=html

# 특정 테스트 파일 실행
pytest tests/test_youtube_api.py

# 특정 테스트 함수 실행
pytest tests/test_utils.py::TestFormatters::test_format_view_count
```

### 테스트 커버리지
```bash
# HTML 리포트 생성
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 🚀 배포

### Streamlit Community Cloud (권장)

1. **GitHub 저장소 준비**
   ```bash
   git add .
   git commit -m "Add Streamlit Cloud support"
   git push origin main
   ```

2. **Streamlit Cloud에서 배포**
   - [share.streamlit.io](https://share.streamlit.io) 접속
   - "New app" 클릭
   - GitHub 저장소 연결
   - 메인 파일 경로: `src/streamlit_app.py`
   - 브랜치: `main`

3. **Secrets 설정**
   Streamlit Cloud 대시보드에서 "Advanced settings"로 이동하여 다음 설정 추가:
   ```toml
   # 필수 설정
   youtube_api_key = "your_youtube_api_key_here"
   
   # 선택적 설정
   app_title = "YouTube 인기 동영상 대시보드"
   default_region = "KR"
   default_category = 0
   max_results = 30
   ```

4. **배포 완료**
   - 자동으로 배포가 시작됩니다
   - 배포 상태는 대시보드에서 확인 가능합니다
   - 배포 완료 후 제공되는 URL로 접속 가능합니다

### AWS/GCP/Azure
```bash
# Docker 이미지 빌드
docker build -t youtube-dashboard .

# 클라우드 레지스트리에 푸시
docker tag youtube-dashboard your-registry/youtube-dashboard
docker push your-registry/youtube-dashboard

# 클라우드에서 컨테이너 실행
```

### 로컬 프로덕션 실행
```bash
# Gunicorn 사용
gunicorn -w 4 -b 0.0.0.0:8501 src.streamlit_app:main

# 또는 Streamlit 직접 실행
streamlit run src/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```

## 📊 성능 최적화

### 캐싱
- Streamlit의 `@st.cache_data` 데코레이터 사용
- 설정 가능한 TTL (Time To Live)
- 메모리 효율적인 캐시 관리

### API 최적화
- Rate limiting 구현
- 재시도 로직 (Exponential Backoff)
- 배치 요청 최적화

### UI/UX 최적화
- Lazy loading 구현
- 반응형 디자인
- 스켈레톤 스크린

## 🛠️ 개발

### 개발 환경 설정
```bash
# 개발 의존성 설치
pip install -r requirements.txt

# 코드 포맷팅
black src/ tests/

# 린팅
flake8 src/ tests/

# 타입 체크
mypy src/
```

### 코드 스타일
- PEP 8 준수
- Type hints 사용
- Google 스타일 docstring
- 의미있는 변수/함수명

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🆘 문제 해결

### 일반적인 문제

**Q: API 키 오류가 발생합니다**
A: `.env` 파일에 올바른 YouTube API 키가 설정되어 있는지 확인하세요.

**Q: 동영상이 표시되지 않습니다**
A: API 할당량을 확인하고, 네트워크 연결을 점검하세요.

**Q: Docker 컨테이너가 시작되지 않습니다**
A: 포트 8501이 사용 중인지 확인하고, 다른 포트를 사용해보세요.

### 로그 확인
```bash
# Docker 로그 확인
docker-compose logs -f

# 애플리케이션 로그 확인
tail -f logs/app.log
```

## 📞 지원

- 🐛 버그 리포트: [Issues](https://github.com/your-username/youtube-trending-dashboard/issues)
- 💡 기능 요청: [Discussions](https://github.com/your-username/youtube-trending-dashboard/discussions)
- 📧 이메일: your-email@example.com

## 🙏 감사의 말

- [Streamlit](https://streamlit.io/) - 웹 애플리케이션 프레임워크
- [YouTube Data API v3](https://developers.google.com/youtube/v3) - 데이터 소스
- [Google Cloud Platform](https://cloud.google.com/) - API 서비스

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
