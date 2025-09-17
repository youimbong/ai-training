#!/usr/bin/env python3
"""
의존성 설치 확인 스크립트
"""
import subprocess
import sys

def check_package(package_name, import_name=None):
    """패키지 설치 및 import 확인"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} ({import_name}) - 설치됨")
        return True
    except ImportError:
        print(f"❌ {package_name} ({import_name}) - 설치되지 않음")
        return False

def install_package(package_name):
    """패키지 설치"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} 설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} 설치 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🔍 의존성 확인 중...")
    
    # 확인할 패키지들
    packages = [
        ("streamlit", "streamlit"),
        ("python-dotenv", "dotenv"),
        ("google-api-python-client", "googleapiclient"),
        ("google-auth", "google.auth"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("requests", "requests"),
        ("tenacity", "tenacity"),
    ]
    
    missing_packages = []
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 누락된 패키지: {', '.join(missing_packages)}")
        print("🔧 설치 중...")
        
        for package in missing_packages:
            install_package(package)
        
        print("\n🔍 재확인 중...")
        all_installed = True
        for package_name, import_name in packages:
            if not check_package(package_name, import_name):
                all_installed = False
        
        if all_installed:
            print("\n🎉 모든 의존성 설치 완료!")
        else:
            print("\n⚠️ 일부 패키지 설치에 실패했습니다.")
    else:
        print("\n🎉 모든 의존성이 이미 설치되어 있습니다!")

if __name__ == "__main__":
    main()
