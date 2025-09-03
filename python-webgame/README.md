# Mirror Maze - 빛의 미로 🎮

빛과 거울을 이용한 퍼즐 게임입니다. 거울, 프리즘, 필터 등 다양한 도구를 사용해 빛을 목표 지점까지 유도하세요!

## 🎯 게임 특징

- **8개의 도전적인 레벨**: Easy부터 Expert까지 점진적 난이도
- **다양한 게임 도구**:
  - 🪞 거울 (왼쪽/오른쪽): 빛을 90도 반사
  - ➕ 빔 분할기: 빛을 두 방향으로 분할
  - 🔺 프리즘: 백색광을 RGB로 분리
  - 🔴🟢🔵 색상 필터: 특정 색상만 통과
- **별점 시스템**: 최소 이동 수로 클리어 시 3성 획득
- **힌트 시스템**: 막힐 때 도움을 받을 수 있습니다

## 🚀 실행 방법

### 1. 의존성 설치

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
# 개발 서버 실행
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 또는
python -m uvicorn backend.main:app --reload
```

### 3. 게임 플레이

브라우저에서 `http://localhost:8000` 접속

## 🎮 게임 방법

### 기본 조작

1. **도구 선택**: 왼쪽 패널에서 사용할 도구 클릭
2. **배치**: 게임 보드의 원하는 위치 클릭
3. **회전**: R키 또는 회전 버튼 → 거울 클릭
4. **제거**: Delete키 또는 제거 버튼 → 조각 클릭
5. **확인**: ✨ 확인 버튼으로 솔루션 체크

### 단축키

- **R**: 회전 모드
- **Delete/Backspace**: 제거 모드
- **Escape**: 선택 취소

## 🧩 레벨 소개

### Level 1: 첫 번째 빛 (Easy)
- 기본 거울 사용법 학습
- 빛을 목표까지 유도

### Level 2: 색깔 필터 (Easy)
- 필터를 사용해 색상 변경
- 특정 색상 목표 달성

### Level 3: 빔 분할 (Medium)
- 빔 분할기로 여러 목표 동시 달성
- 전략적 배치 필요

### Level 4: 프리즘의 마법 (Medium)
- 백색광을 RGB로 분리
- 각 색상을 올바른 목표로 유도

### Level 5: 복잡한 미로 (Hard)
- 모든 도구 활용
- 복잡한 퍼즐 해결

### Level 6: 색상 혼합 (Hard)
- 여러 색상을 혼합해 새로운 색 생성
- Red + Green = Yellow

### Level 7: 정밀한 각도 (Expert)
- 좁은 통로 통과
- 정확한 거울 배치 필요

### Level 8: 다중 프리즘 (Expert)
- 여러 프리즘 연쇄 사용
- 최고 난이도 도전

## 🏆 점수 시스템

- ⭐⭐⭐ 3성: 최소 이동 수 이하로 클리어
- ⭐⭐ 2성: 최소 이동 수의 1.5배 이하
- ⭐ 1성: 클리어

## 📁 프로젝트 구조

```
python-webgame/
├── backend/
│   ├── main.py              # FastAPI 서버
│   ├── core/
│   │   ├── game_engine.py   # 게임 로직
│   │   └── level_manager.py # 레벨 관리
│   └── models/
│       └── game_models.py   # 데이터 모델
├── frontend/
│   ├── index.html           # 메인 페이지
│   ├── css/
│   │   ├── style.css       # 기본 스타일
│   │   └── game.css        # 게임 스타일
│   └── js/
│       ├── game.js         # 게임 로직
│       ├── renderer.js     # 캔버스 렌더링
│       ├── ui.js           # UI 관리
│       └── main.js         # 진입점
├── requirements.txt         # Python 의존성
└── README.md               # 문서
```

## 🛠️ 기술 스택

- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: HTML5 Canvas, Vanilla JavaScript, CSS3
- **게임 엔진**: 커스텀 빛 추적 알고리즘
- **저장**: LocalStorage (진행상황)

## 🎨 게임 메커니즘

### 빛 반사 규칙
- `\` 거울: 오른쪽→아래, 왼쪽→위, 아래→오른쪽, 위→왼쪽
- `/` 거울: 오른쪽→위, 왼쪽→아래, 아래→왼쪽, 위→오른쪽

### 색상 혼합
- White = Red + Green + Blue
- Yellow = Red + Green
- Cyan = Blue + Green
- Magenta = Red + Blue

### 프리즘 동작
- 백색광 입력 → RGB 3방향 분리
- 각도별로 색상 분산

## 🔧 개발 모드

```bash
# 테스트 실행
pytest tests/

# 코드 포맷팅
black backend/

# 린팅
flake8 backend/
```

## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**즐거운 게임 되세요! 🎮✨**