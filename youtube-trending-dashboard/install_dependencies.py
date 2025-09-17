#!/usr/bin/env python3
"""
클라우드 환경에서 의존성을 자동으로 설치하는 스크립트
"""
import subprocess
import sys
import os

def run_command(command, description):
    """명령어 실행 및 결과 출력"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False

def main():
    """메인 함수"""
    print("🚀 클라우드 환경 의존성 설치 시작...")
    
    # 1. 프로젝트 디렉토리로 이동
    project_dir = "/workspaces/ai-training/youtube-trending-dashboard"
    if os.path.exists(project_dir):
        os.chdir(project_dir)
        print(f"📁 프로젝트 디렉토리로 이동: {project_dir}")
    else:
        print(f"❌ 프로젝트 디렉토리를 찾을 수 없습니다: {project_dir}")
        return False
    
    # 2. 가상환경 생성
    if not os.path.exists("venv"):
        if not run_command("python3 -m venv venv", "가상환경 생성"):
            return False
    else:
        print("✅ 가상환경이 이미 존재합니다")
    
    # 3. 가상환경 활성화 및 pip 업그레이드
    activate_cmd = "source venv/bin/activate && pip install --upgrade pip"
    if not run_command(activate_cmd, "pip 업그레이드"):
        return False
    
    # 4. 의존성 설치
    install_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    if not run_command(install_cmd, "의존성 설치"):
        return False
    
    # 5. 설치 확인
    test_cmd = "source venv/bin/activate && python -c \"import dotenv, streamlit; print('✅ 모든 의존성 설치 완료')\""
    if not run_command(test_cmd, "설치 확인"):
        return False
    
    print("\n🎉 설정 완료!")
    print("이제 다음 명령어로 실행하세요:")
    print("cd /workspaces/ai-training/youtube-trending-dashboard")
    print("source venv/bin/activate")
    print("streamlit run src/streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
