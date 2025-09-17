# 🚀 Streamlit Cloud 배포 가이드

이 문서는 YouTube 인기 동영상 대시보드를 Streamlit Cloud에 배포하는 방법을 설명합니다.

## 📋 사전 준비사항

### 1. GitHub 저장소 준비
- [ ] GitHub 계정 생성
- [ ] 새 저장소 생성 또는 기존 저장소 사용
- [ ] 코드를 GitHub에 푸시

### 2. YouTube API 키 발급
- [ ] [Google Cloud Console](https://console.cloud.google.com/) 접속
- [ ] 새 프로젝트 생성 또는 기존 프로젝트 선택
- [ ] YouTube Data API v3 활성화
- [ ] API 키 생성 및 제한 설정

## 🚀 배포 단계

### 1단계: GitHub에 코드 푸시

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/youtube-trending-dashboard

# Git 초기화 (필요한 경우)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Add Streamlit Cloud support"

# GitHub 저장소에 푸시
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 2단계: Streamlit Cloud에서 앱 생성

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. "New app" 버튼 클릭
3. GitHub 계정으로 로그인
4. 저장소 선택: `your-username/your-repo`
5. 브랜치 선택: `main`
6. 메인 파일 경로: `src/streamlit_app.py`
7. "Deploy!" 버튼 클릭

### 3단계: Secrets 설정

배포가 시작되면 "Advanced settings"로 이동하여 다음 설정을 추가:

```toml
# 필수 설정
youtube_api_key = "your_youtube_api_key_here"

# 애플리케이션 설정
app_title = "YouTube 인기 동영상 대시보드"
app_icon = "📺"
default_region = "KR"
default_category = 0
default_max_results = 30
max_results = 30

# 캐시 설정
cache_ttl = 300
enable_cache = true

# 로깅 설정
log_level = "INFO"
log_file = "logs/app.log"

# UI 설정
default_theme = "light"
enable_dark_mode = true
items_per_page = 30

# 성능 설정
max_retries = 3
request_timeout = 30
enable_lazy_loading = true

# 보안 설정
enable_rate_limiting = true
max_requests_per_minute = 100
```

### 4단계: 배포 확인

1. 배포 상태 모니터링
2. 로그 확인 (문제 발생 시)
3. 앱 URL로 접속하여 정상 작동 확인

## 🔧 설정 옵션

### 필수 설정
- `youtube_api_key`: YouTube Data API v3 키 (반드시 설정)

### 선택적 설정
- `app_title`: 애플리케이션 제목
- `default_region`: 기본 지역 (KR, US, JP 등)
- `default_category`: 기본 카테고리 (0=전체)
- `max_results`: 페이지당 결과 수
- `cache_ttl`: 캐시 유지 시간 (초)
- `log_level`: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)

## 🐛 문제 해결

### 일반적인 문제

**1. API 키 오류**
```
❌ YouTube API 키가 설정되지 않았습니다.
```
- **해결방법**: Secrets에서 `youtube_api_key` 설정 확인

**2. 모듈 import 오류**
```
❌ Import 오류: No module named 'streamlit'
```
- **해결방법**: `requirements.txt`에 필요한 패키지가 모두 포함되어 있는지 확인

**3. 배포 실패**
- **해결방법**: 
  - 로그 확인
  - `packages.txt` 파일 확인
  - 메인 파일 경로 확인 (`src/streamlit_app.py`)

### 로그 확인 방법

1. Streamlit Cloud 대시보드에서 "Logs" 탭 클릭
2. 오류 메시지 확인
3. 필요시 로컬에서 테스트: `python3 test_streamlit_cloud.py`

## 📊 성능 최적화

### 캐시 설정
```toml
cache_ttl = 300  # 5분
enable_cache = true
```

### Rate Limiting
```toml
enable_rate_limiting = true
max_requests_per_minute = 100
```

### 결과 수 제한
```toml
max_results = 30  # 한 번에 가져올 최대 결과 수
```

## 🔄 업데이트 배포

코드 변경 후 재배포:

```bash
# 변경사항 커밋
git add .
git commit -m "Update app"

# GitHub에 푸시
git push origin main

# Streamlit Cloud에서 자동 재배포 확인
```

## 📱 앱 접근

배포 완료 후:
- **URL**: `https://your-app-name.streamlit.app`
- **관리**: Streamlit Cloud 대시보드에서 설정 변경 가능

## 🆘 지원

문제가 발생하면:
1. 로그 확인
2. 로컬 테스트 실행: `python3 test_streamlit_cloud.py`
3. GitHub Issues에 문제 보고

---

🎉 **배포 완료!** 이제 전 세계 어디서나 YouTube 인기 동영상 대시보드에 접근할 수 있습니다!
