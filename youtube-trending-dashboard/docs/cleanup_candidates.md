# 🧹 프로젝트 정리 대상 파일 리스트

> 생성일: 2025-09-17
> 목적: 프로젝트 구조 최적화 및 불필요한 파일 정리

## 📋 삭제 대상 파일 목록

### 1. 중복된 실행 스크립트 (7개)
**위치**: 루트 디렉토리

| 파일명 | 삭제 이유 | 우선순위 |
|--------|-----------|----------|
| `run.py` | run_app.sh와 기능 중복, 가상환경 미지원 | 🔴 높음 |
| `run_cloud.sh` | Streamlit Cloud에서 불필요 (자동 실행) | 🔴 높음 |
| `run_with_requirements.sh` | run_app.sh와 기능 중복 | 🔴 높음 |
| `setup_and_run.sh` | setup_local_dev.sh와 기능 중복 | 🔴 높음 |
| `setup_cloud_environment.sh` | Streamlit Cloud에서 불필요 | 🔴 높음 |
| `install_dependencies.py` | pip install -r requirements.txt로 충분 | 🟡 중간 |
| `check_dependencies.py` | 테스트 목적 스크립트, 프로덕션에서 불필요 | 🟡 중간 |

**보존할 파일**:
- ✅ `run_app.sh` - 로컬 실행용 메인 스크립트
- ✅ `setup_local_dev.sh` - 로컬 개발 환경 설정

### 2. 테스트/디버깅 파일 (1개)
**위치**: 루트 디렉토리

| 파일명 | 삭제 이유 | 우선순위 |
|--------|-----------|----------|
| `test_streamlit_cloud.py` | 개발 중 테스트 목적, 프로덕션에서 불필요 | 🟡 중간 |

### 3. 사용하지 않는 설정 파일 (1개)
**위치**: src/utils/

| 파일명 | 삭제 이유 | 우선순위 |
|--------|-----------|----------|
| `src/utils/toml_config.py` | Streamlit Secrets 사용으로 불필요 | 🔴 높음 |

### 4. Docker 관련 파일 (조건부)
**위치**: 루트 디렉토리

| 파일명 | 삭제 이유 | 우선순위 |
|--------|-----------|----------|
| `Dockerfile.cloud` | Streamlit Cloud는 Docker 미사용 | 🟢 낮음 |

**참고**: `Dockerfile`과 `docker-compose.yml`은 로컬 Docker 환경이나 다른 클라우드 플랫폼 배포시 필요하므로 유지

### 5. 테스트 디렉토리 (조건부)
**위치**: tests/

| 디렉토리 | 삭제 이유 | 우선순위 |
|----------|-----------|----------|
| `tests/` | 현재 테스트 코드가 구현되지 않음 | 🟢 낮음 |

**참고**: 향후 테스트 코드 작성 계획이 있다면 유지 권장

## 📊 정리 효과

### 파일 수 감소
- **현재**: 32개 파일 (루트 레벨)
- **정리 후**: 22개 파일 (약 31% 감소)

### 코드 복잡도 감소
- 중복 스크립트 제거로 유지보수 포인트 감소
- 명확한 단일 진입점 제공 (`run_app.sh`)
- 설정 관리 일원화 (Streamlit Secrets)

## 🎯 권장 작업 순서

### Phase 1 - 즉시 삭제 (높은 우선순위)
```bash
# 중복 실행 스크립트 삭제
rm run.py
rm run_cloud.sh
rm run_with_requirements.sh
rm setup_and_run.sh
rm setup_cloud_environment.sh

# 사용하지 않는 설정 파일 삭제
rm src/utils/toml_config.py
```

### Phase 2 - 검토 후 삭제 (중간 우선순위)
```bash
# 테스트/디버깅 스크립트
rm test_streamlit_cloud.py
rm check_dependencies.py
rm install_dependencies.py
```

### Phase 3 - 선택적 삭제 (낮은 우선순위)
```bash
# Docker 관련 (Streamlit Cloud 전용 사용시)
rm Dockerfile.cloud

# 테스트 디렉토리 (테스트 계획 없을시)
rm -rf tests/
```

## ⚠️ 삭제 전 체크리스트

- [ ] 현재 실행 중인 프로세스 확인
- [ ] Git에 모든 변경사항 커밋
- [ ] 백업 브랜치 생성
- [ ] 팀원과 삭제 계획 공유
- [ ] CI/CD 파이프라인 영향 검토

## 🔍 추가 최적화 제안

### 코드 레벨 개선
1. **settings.py 정리**
   - 환경변수 관련 코드 제거 (Streamlit Secrets 전용)
   - 불필요한 fallback 로직 단순화

2. **Import 정리**
   - 사용하지 않는 import 제거
   - 조건부 import 정리

3. **주석 정리**
   - 구식 주석 및 TODO 제거
   - 디버깅용 print문 제거

### 구조 개선
1. **스크립트 통합**
   - `run_app.sh` 하나로 모든 실행 옵션 통합
   - 환경별 설정을 플래그로 처리

2. **문서화**
   - README.md 업데이트 (삭제된 파일 참조 제거)
   - 단순화된 실행 방법 문서화

## 📝 삭제 명령어 스크립트

전체 정리를 한번에 수행하려면:

```bash
#!/bin/bash
# cleanup.sh - 프로젝트 정리 스크립트

echo "🧹 프로젝트 정리 시작..."

# Phase 1 - 중복 스크립트 삭제
echo "Phase 1: 중복 스크립트 삭제 중..."
rm -f run.py
rm -f run_cloud.sh
rm -f run_with_requirements.sh
rm -f setup_and_run.sh
rm -f setup_cloud_environment.sh
rm -f src/utils/toml_config.py

# Phase 2 - 테스트 스크립트 삭제
echo "Phase 2: 테스트 스크립트 삭제 중..."
rm -f test_streamlit_cloud.py
rm -f check_dependencies.py
rm -f install_dependencies.py

# Phase 3 - 선택적 삭제 (주석 해제하여 사용)
# echo "Phase 3: 선택적 파일 삭제 중..."
# rm -f Dockerfile.cloud
# rm -rf tests/

echo "✅ 정리 완료!"
echo "삭제된 파일은 git을 통해 복구 가능합니다."
```

## 💡 참고사항

1. **Git 이력 보존**: 삭제 전 반드시 커밋하여 필요시 복구 가능하도록 함
2. **단계적 접근**: 한번에 모든 파일을 삭제하지 말고 단계별로 진행
3. **팀 공유**: 다른 개발자가 사용 중일 수 있으므로 사전 공지
4. **문서 업데이트**: 삭제 후 관련 문서 업데이트 필수

---

*이 문서는 프로젝트 정리를 위한 가이드이며, 실제 삭제는 팀의 검토 후 진행하시기 바랍니다.*