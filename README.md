# Teaspoon-mabinogi

<p>
   <img src="https://img.shields.io/badge/using-Python%203.x-%233776AB?style=flat-square&logo=python"/>&nbsp
   <img src="https://img.shields.io/badge/using-PyQt5-%2341CD52?style=flat-square&logo=qt"/>&nbsp
</p>

마비노기의 요리 관련 부가기능을 제공하는 애드온 프로그램입니다.

## 🔑 설치 / 사용 방법

### 일반

1. [Releases 페이지](https://github.com/kry-p/Teaspoon-mabinogi/releases)에서 최신 버전을 다운로드합니다.  
   DB 파일도 `Spoon.exe` 파일과 같은 경로에 저장하셔야 정상적으로 실행됩니다.

2. `Spoon.exe` 파일을 실행합니다.

### 고급 (Python 관련 지식이 있을 경우, 권장하지 않음)

#### 인터프리터로 직접 실행

1. 이 저장소를 다운로드합니다. (master branch)

2. [Python을 다운로드](https://www.python.org/downloads/) 후 설치합니다.

- 3.9 이상 버전을 권장합니다.
- Anaconda와 같은 가상 환경에서도 실행은 가능하나, 예기치 못한 문제가 생길 수 있습니다.
- PATH에 추가 옵션을 설정하고 설치할 것을 권장합니다.

3. pip 명령으로 PyQt5을 설치합니다.  
   cmd 또는 PowerShell으로 아래 명령을 실행해 주세요.

```
pip install PyQt5
```

4. `Spoon.py` 파일을 실행합니다.

#### PyInstaller로 빌드

```pyinstaller``` 를 사용하여 단독 실행 파일로 작성할 수 있습니다. 동봉된 ```Spoon.spec``` 파일을 사용해 주세요.

## 알려진 문제

- PyQt5에서 실수배 HiDPI가 정상 대응되지 않음  
  Qt 6에서 한국어 오토마타가 비정상적으로 작동하여(Shift 키를 떼면 다음 글자로 넘어감) 임시방편으로 HiDPI Scaling이 불완전한 구 버전을 사용 중이며, 해당 문제가 해결되는 대로 Qt 6으로 이행 예정입니다.

## FAQ - ⚠ 문제가 있으면 여기부터 읽어 주세요 ⚠

- 컴퓨터에 ```api-ms-win-core-path-l1-1-0.dll``` 이 없음

  프로그램이 Windows 7 이전 버전과 호환되지 않는 Python 3.9 이상 버전을 이용, 작성되어 발생하는 문제입니다.  
  Windows 8 이상 버전으로 업데이트 후 프로그램을 실행해 주실 것을 요청드리며, 구 버전 OS에 대응 업데이트를 하지는 않을 예정인 점 양해 부탁드립니다.  
  
  Python 버전을 낮추어 직접 빌드하여 사용하는 방법으로 해결할 수 있으나, 예기치 못한 문제가 발생할 수 있으므로 권장하지 않습니다.

- Qt platform plugin 문제  

  This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

  해당 프로그램에 사용된 Qt 프레임워크의 Windows용 DLL 링크가 잘못되어 발생하는 문제입니다.

  클린 설치된 Windows에서는 해당 문제가 발생하지 않으며, Python이 기 설치된 환경에서 간혹 문제가 발생하는 것을 확인하였습니다.  
   해당 메시지가 발생할 경우 아래 시스템 변수를 추가하면 해결됩니다.

      + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH
      + 변수 값 : (Python이 설치된 경로)\Lib\site-packages\PyQt5\plugins\platforms

  Python을 설치한 적이 없는데 해당 문제가 발생한 경우, Release의 platform.zip 파일의 압축을 폴더 이름으로 풀어 아래와 같이 시스템 변수로 추가합니다.

      + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH
      + 변수 값 : (압축을 푼 경로)/platforms

  위 조치 후에도 문제가 발생하는 경우 개발자에게 문의해 주세요.

- 설정 백업이나 초기화는 어떻게 하나요?  

  `(사용자)/AppData/Local/Yuzu/Spoon` 경로에 `settings.ini` 파일이 있습니다.  
  이 파일을 백업하거나 삭제하시면 됩니다.
  
- 프로그램이 왜 이렇게 무겁나요?  

  Python이 무겁습니다. 차후 여유가 있다면 Electron 프레임워크로 이식이 이루어질 수 있으나, 언제일지는 아무도 모릅니다.
  
- SmartScreen 경고는 왜 뜨나요?  

  실행 파일에 디지털 서명을 하지 않아서입니다. 인증서가 비싸요..  
  진위 여부가 의심될 경우 릴리즈 노트의 MD5 해시를 확인해 주세요. Windows 10 이상을 사용 중이라면 certutil 명령으로 빠르게 확인할 수 있습니다.

## QnA

해당 애드온 프로그램과 관련하여 문제나 궁금한 점이 있을 경우 jhjung.dev@gmail.com 이나 이 저장소의 Issues 란에 질문해 주세요.  
답변에는 수 일이 소요될 수 있습니다.

질문이나 버그 제보 시에는 구동 환경을 **상세히** 적어 주세요. 충분한 정보가 있을수록 빠른 해결에 도움이 됩니다.

## 라이선스

이 애드온 프로그램은 GPL 라이선스 하에  가능합니다.
