// ===== 네비게이션 스크롤 효과 =====
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section');

// 스크롤 시 네비게이션 배경 변경
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    // 현재 섹션에 따른 네비게이션 활성화
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// ===== 모바일 메뉴 토글 =====
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// 메뉴 링크 클릭 시 모바일 메뉴 닫기
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// ===== 부드러운 스크롤 =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 70;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===== 스킬바 애니메이션 =====
const skillBars = document.querySelectorAll('.skill-progress');
const animateSkillBars = () => {
    skillBars.forEach(bar => {
        const skillValue = bar.getAttribute('data-skill');
        bar.style.width = skillValue + '%';
    });
};

// 스킬 섹션이 뷰포트에 들어왔을 때 애니메이션 실행
const skillsSection = document.querySelector('.skills');
const skillsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateSkillBars();
            skillsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

if (skillsSection) {
    skillsObserver.observe(skillsSection);
}

// ===== 카운터 애니메이션 =====
const counters = document.querySelectorAll('.stat-number');
const speed = 200;

const animateCounters = () => {
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-count');
        const increment = target / speed;
        
        const updateCount = () => {
            const count = +counter.innerText;
            
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };
        
        updateCount();
    });
};

// About 섹션이 뷰포트에 들어왔을 때 카운터 애니메이션 실행
const aboutSection = document.querySelector('.about');
const aboutObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            aboutObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

if (aboutSection) {
    aboutObserver.observe(aboutSection);
}

// ===== 타이핑 효과 =====
const typingText = document.querySelector('.hero-subtitle');
const textArray = ['Full Stack Developer', 'Web Designer', 'Problem Solver', 'Tech Enthusiast'];
let textArrayIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
    if (typingText) {
        const currentText = textArray[textArrayIndex];
        
        if (isDeleting) {
            typingText.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingText.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        }
        
        let typeSpeed = isDeleting ? 50 : 100;
        
        if (!isDeleting && charIndex === currentText.length) {
            typeSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textArrayIndex++;
            if (textArrayIndex === textArray.length) {
                textArrayIndex = 0;
            }
        }
        
        setTimeout(typeEffect, typeSpeed);
    }
}

// 페이지 로드 후 타이핑 효과 시작
window.addEventListener('load', () => {
    setTimeout(typeEffect, 500);
});

// ===== 스크롤 투 탑 버튼 =====
const scrollToTopBtn = document.getElementById('scrollToTop');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollToTopBtn.classList.add('active');
    } else {
        scrollToTopBtn.classList.remove('active');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===== 프로젝트 필터링 (옵션) =====
const projectCards = document.querySelectorAll('.project-card');
let currentFilter = 'all';

// 프로젝트 호버 효과 개선
projectCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) rotateX(2deg)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) rotateX(0)';
    });
});

// ===== 폼 제출 처리 =====
const contactForm = document.querySelector('.contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // 폼 데이터 수집
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // 여기에서 실제 이메일 전송 로직 구현 (백엔드 필요)
        console.log('Form submitted:', data);
        
        // 성공 메시지 표시
        alert('메시지가 성공적으로 전송되었습니다!');
        contactForm.reset();
    });
}

// ===== 페이지 로드 애니메이션 =====
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    
    // 각 요소에 순차적 애니메이션 적용
    const animateElements = document.querySelectorAll('[data-aos]');
    animateElements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('aos-animate');
        }, index * 100);
    });
});

// ===== Intersection Observer를 이용한 스크롤 애니메이션 =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// 모든 섹션에 관찰자 적용
sections.forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(30px)';
    section.style.transition = 'all 0.6s ease';
    scrollObserver.observe(section);
});

// ===== 마우스 커서 효과 (선택사항) =====
const cursor = document.createElement('div');
cursor.className = 'cursor';
document.body.appendChild(cursor);

document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
});

// 링크 호버 시 커서 크기 변경
const links = document.querySelectorAll('a, button');
links.forEach(link => {
    link.addEventListener('mouseenter', () => {
        cursor.style.transform = 'scale(1.5)';
    });
    link.addEventListener('mouseleave', () => {
        cursor.style.transform = 'scale(1)';
    });
});

// ===== 다크/라이트 모드 토글 (선택사항) =====
const themeToggle = document.createElement('button');
themeToggle.className = 'theme-toggle';
themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
document.body.appendChild(themeToggle);

let isDarkMode = true;

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('light-mode');
    themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
});

// ===== 스타일 추가 (커서 및 테마 토글 버튼) =====
const style = document.createElement('style');
style.textContent = `
    .cursor {
        width: 20px;
        height: 20px;
        border: 2px solid #6366f1;
        border-radius: 50%;
        position: fixed;
        pointer-events: none;
        transition: all 0.1s ease;
        z-index: 9999;
        mix-blend-mode: difference;
    }
    
    .theme-toggle {
        position: fixed;
        top: 100px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--gradient);
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        z-index: 1001;
        transition: all 0.3s ease;
        display: none; /* 기본적으로 숨김 - 필요시 display: flex로 변경 */
        align-items: center;
        justify-content: center;
    }
    
    .theme-toggle:hover {
        transform: rotate(180deg);
    }
    
    body.light-mode {
        --dark: #ffffff;
        --dark-light: #f3f4f6;
        --text-light: #6b7280;
        --text-dark: #1f2937;
    }
`;
document.head.appendChild(style);

console.log('Portfolio website loaded successfully!');