# 🚀 포트폴리오 웹사이트 제작 프롬프트 가이드

이 가이드는 AI를 활용하여 전문적인 포트폴리오 웹사이트를 제작하기 위한 단계별 프롬프트를 제공합니다.

## 📋 목차
1. [프로젝트 초기 설정](#1-프로젝트-초기-설정)
2. [HTML 구조 생성](#2-html-구조-생성)
3. [CSS 스타일링](#3-css-스타일링)
4. [JavaScript 인터랙션](#4-javascript-인터랙션)
5. [콘텐츠 개인화](#5-콘텐츠-개인화)
6. [이미지 추가](#6-이미지-추가)

---

## 1. 프로젝트 초기 설정

### 프롬프트 1: 폴더 구조 생성
```
portfolio 폴더를 생성해서 나의 포트폴리오 홈페이지를 세련되게 작성해줘. 
이력 부분은 적당히 꾸며서 작성해주면 돼.
```

**예상 결과:**
- `portfolio/` 메인 폴더 생성
- `css/`, `js/`, `assets/images/` 하위 폴더 구조
- 기본 파일 생성 (index.html, style.css, script.js)

---

## 2. HTML 구조 생성

### 프롬프트 2: HTML 템플릿 생성
```
포트폴리오 HTML 파일을 작성해줘. 다음 섹션들을 포함해줘:
- 네비게이션 바
- 히어로 섹션 (자기소개)
- 소개 섹션
- 기술 스택 섹션
- 경력 및 교육 섹션
- 프로젝트 포트폴리오 섹션
- 연락처 섹션
- 푸터
```

### HTML 기본 구조 예시:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[이름] | Full Stack Developer Portfolio</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- 네비게이션 -->
    <nav class="navbar">
        <!-- 네비게이션 내용 -->
    </nav>
    
    <!-- 히어로 섹션 -->
    <section id="home" class="hero">
        <!-- 자기소개 내용 -->
    </section>
    
    <!-- 기타 섹션들 -->
</body>
</html>
```

---

## 3. CSS 스타일링

### 프롬프트 3: 모던 CSS 스타일 적용
```
포트폴리오를 세련되게 만들어줘. CSS를 이용해서:
- 다크 테마 디자인
- 그라데이션 효과
- 부드러운 애니메이션
- 반응형 디자인 (모바일, 태블릿, 데스크톱)
- 호버 효과
- 스크롤 애니메이션
```

### 핵심 CSS 변수 설정:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --dark: #0f172a;
    --dark-light: #1e293b;
    --text-light: #94a3b8;
    --text-dark: #e2e8f0;
    --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 4. JavaScript 인터랙션

### 프롬프트 4: 동적 기능 추가
```
JavaScript로 다음 기능들을 구현해줘:
- 스크롤 시 네비게이션 바 스타일 변경
- 부드러운 스크롤 이동
- 타이핑 애니메이션 효과
- 스킬바 애니메이션
- 카운터 애니메이션 (숫자 증가 효과)
- 모바일 햄버거 메뉴
- 스크롤 투 탑 버튼
```

### JavaScript 기능 예시:
```javascript
// 스크롤 시 네비게이션 변경
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// 타이핑 효과
const textArray = ['Full Stack Developer', 'Web Designer', 'Problem Solver'];
// 타이핑 로직 구현
```

---

## 5. 콘텐츠 개인화

### 프롬프트 5: 개인 정보 커스터마이징
```
포트폴리오를 업데이트할 거야. 다음 정보로 변경해줘:
- 이름: [영어 이름 또는 닉네임]
- 직책: [원하는 직책]
- 위치: [도시, 국가]
- 이메일: [이메일 주소]
- 전화번호: [전화번호]
- 학력: [학교명, 전공]
- 경력: [회사명, 기간, 역할]
```

### 프롬프트 5-1: 언어 설정
```
이름만 영어로 하고 내용은 모두 한글로 바꿔줘.
```

---

## 6. 이미지 추가

### 프롬프트 6: 실제 이미지 적용
```
샘플 이미지를 찾아서 다운받아서 적용할 수 있을까?
```

### 이미지 소스 추천:
- **Unsplash** (무료 고품질 이미지): https://unsplash.com
- **Pexels** (무료 스톡 사진): https://www.pexels.com
- **Pixabay** (무료 이미지): https://pixabay.com

### 이미지 다운로드 및 적용 예시:
```bash
# 이미지 폴더 생성
mkdir -p portfolio/assets/images

# Unsplash에서 이미지 다운로드 (curl 사용)
curl -L -o profile.jpg "https://images.unsplash.com/photo-[ID]?w=400&h=400&fit=crop"
```

---

## 🎨 추가 커스터마이징 프롬프트

### 색상 테마 변경
```
포트폴리오의 색상 테마를 [원하는 색상]으로 변경해줘.
```

### 폰트 변경
```
폰트를 [Montserrat/Roboto/Noto Sans KR 등]으로 변경해줘.
```

### 섹션 추가/삭제
```
[블로그/수상 경력/자격증] 섹션을 추가해줘.
```

### 애니메이션 효과 추가
```
AOS (Animate On Scroll) 라이브러리를 추가해서 스크롤 애니메이션을 더 화려하게 만들어줘.
```

---

## 📦 최종 파일 구조

```
portfolio/
├── index.html              # 메인 HTML 파일
├── css/
│   └── style.css          # 스타일시트
├── js/
│   └── script.js          # JavaScript 파일
└── assets/
    └── images/            # 이미지 폴더
        ├── profile.jpg    # 프로필 사진
        ├── project1.jpg   # 프로젝트 이미지들
        └── ...
```

---

## ✅ 체크리스트

- [ ] 폴더 구조 생성 완료
- [ ] HTML 구조 작성 완료
- [ ] CSS 스타일링 완료
- [ ] JavaScript 기능 구현 완료
- [ ] 반응형 디자인 확인
- [ ] 개인 정보 커스터마이징 완료
- [ ] 이미지 추가 완료
- [ ] 크로스 브라우저 테스트
- [ ] 모바일 테스트
- [ ] 성능 최적화

---

## 🚀 배포 옵션

### GitHub Pages (무료)
```
1. GitHub 저장소 생성
2. 코드 업로드
3. Settings > Pages에서 배포 설정
4. https://[username].github.io/[repository-name]
```

### Netlify (무료)
```
1. netlify.com 가입
2. GitHub 연동 또는 직접 업로드
3. 자동 배포 설정
```

### Vercel (무료)
```
1. vercel.com 가입
2. GitHub 연동
3. 프로젝트 import
4. 자동 배포
```

---

## 💡 팁과 트릭

1. **성능 최적화**
   - 이미지 압축 (TinyPNG, Squoosh)
   - CSS/JS 파일 최소화
   - Lazy Loading 적용

2. **SEO 최적화**
   - 메타 태그 추가
   - Open Graph 태그
   - 구조화된 데이터 (Schema.org)

3. **접근성**
   - Alt 텍스트 추가
   - ARIA 레이블
   - 키보드 네비게이션

4. **보안**
   - HTTPS 사용
   - 이메일 주소 보호
   - 폼 검증

---

## 📚 참고 자료

- [MDN Web Docs](https://developer.mozilla.org)
- [W3Schools](https://www.w3schools.com)
- [CSS-Tricks](https://css-tricks.com)
- [JavaScript.info](https://javascript.info)
- [Font Awesome Icons](https://fontawesome.com)
- [Google Fonts](https://fonts.google.com)

---

## 🤝 기여 및 피드백

이 가이드가 도움이 되셨다면 GitHub에서 Star를 주세요! 
개선 사항이나 제안이 있으시면 Issue를 생성해주세요.

---

**작성일**: 2024년 1월
**작성자**: AI Assistant with Alex Chen
**버전**: 1.0.0

---

### 라이선스
이 가이드는 MIT 라이선스 하에 배포됩니다. 자유롭게 사용하고 수정하실 수 있습니다.