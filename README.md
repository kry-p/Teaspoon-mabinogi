# Teaspoon-mabinogi
<p>
   <img src="https://img.shields.io/badge/using-Python%203.x-%233776AB?style=flat-square&logo=python"/>&nbsp
   <img src="https://img.shields.io/badge/using-PySide6-%2341CD52?style=flat-square&logo=qt"/>&nbsp
</p>   


마비노기의 요리 관련 부가기능을 제공하는 애드온 프로그램입니다.

## 🔑 설치 / 사용 방법

### 일반
1. [Releases 페이지](https://github.com/kry-p/Teaspoon-mabinogi/releases)에서 최신 버전을 다운로드합니다.  
   DB 파일도 ```Spoon.exe``` 파일과 같은 경로에 저장하셔야 정상적으로 실행됩니다.

2. ```Spoon.exe``` 파일을 실행합니다.

### 고급 (Python 관련 지식이 있을 경우, 권장하지 않음)  
1. 이 저장소를 다운로드합니다. (master branch)

2. [Python을 다운로드](https://www.python.org/downloads/) 후 설치합니다.
  + 3.9 이상 버전을 권장합니다.  
  + Anaconda와 같은 가상 환경에서도 실행은 가능하나, 예기치 못한 문제가 생길 수 있습니다.  
  + PATH에 추가 옵션을 설정하고 설치할 것을 권장합니다.

3. pip 명령으로 PySide6을 설치합니다.  
cmd 또는 PowerShell으로 아래 명령을 실행해 주세요.  
```
pip install PySide6
```

4. ```Spoon.py``` 파일을 실행합니다.

## 알려진 문제
+ 검색 창에서 입력 칸에 포커스가 있을 때 Backspace로 이전 레시피로 돌아가기 기능이 지원되지 않음

## FAQ - ⚠ 문제가 있으면 여기부터 읽어 주세요 ⚠

+ Qt platform plugin 문제  
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.  
  
  해당 프로그램에 사용된 Qt 프레임워크의 Windows용 DLL 링크가 잘못되어 발생하는 문제입니다.

  클린 설치된 Windows에서는 해당 문제가 발생하지 않으며, Python이 기 설치된 환경에서 간혹 문제가 발생하는 것을 확인하였습니다.  
  해당 메시지가 발생할 경우 아래 시스템 변수를 추가하면 해결됩니다.

    + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH  
    + 변수 값 : (Python이 설치된 경로)\Lib\site-packages\PySide6\plugins\platforms

  Python을 설치한 적이 없는데 해당 문제가 발생한 경우, Release의 platform.zip 파일의 압축을 폴더 이름으로 풀어 아래와 같이 시스템 변수로 추가합니다.

    + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH  
    + 변수 값 : (압축을 푼 경로)/platforms

  위 조치 후에도 문제가 발생하는 경우 개발자에게 문의해 주세요.
 
+ 설정 백업이나 초기화는 어떻게 하나요?    
  ```(사용자)/AppData/Local/Yuzu/Spoon``` 경로에 ```settings.ini``` 파일이 있습니다.  
  이 파일을 백업하거나 삭제하시면 됩니다.


## QnA
해당 애드온 프로그램과 관련하여 문제나 궁금한 점이 있을 경우 jhjung.dev@gmail.com 이나 이 저장소의 Issues 란에 질문해 주세요.  
답변에는 수 일이 소요될 수 있습니다.

질문이나 버그 제보 시에는 구동 환경을 **상세히** 적어 주세요. 충분한 정보가 있을수록 빠른 해결에 도움이 됩니다.

## 🚧 Todos 🚧

 + 설정 저장 / 불러오기, 초기화 기능 구현 

## 라이선스
이 애드온 프로그램은 LGPL 라이선스 하에 사용 가능합니다.
