# Teaspoon-mabinogi
마비노기의 요리 관련 부가기능을 제공하는 애드온 프로그램입니다.

## 설치 방법

### 일반  
1. 최신 Release를 다운로드해 주세요. (Spoon.exe)

2. [Python을 다운로드](https://www.python.org/downloads/) 후 설치합니다.
  + 3.9 이상 버전을 권장합니다.  
  + Anaconda와 같은 가상 환경에서도 실행은 가능하나, 예기치 못한 문제가 생길 수 있습니다.  
  + PATH에 추가 옵션을 설정하고 설치할 것을 권장합니다.

3. pip 명령으로 PySide6을 설치합니다.  
cmd 또는 PowerShell으로 아래 명령을 실행해 주세요.  
```
pip install PySide6
```

4. 1.에서 다운로드한 파일의 압축을 풀어 Spoon.exe 파일을 사용합니다.

## FAQ

+ Qt platform plugin 문제  
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.  
해당 메시지가 발생할 경우 아래 시스템 변수를 추가하면 해결됩니다.

  + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH  
  + 변수 값 : (Python이 설치된 경로)\Lib\site-packages\PySide6\plugins\platforms

## QnA
해당 애드온 프로그램과 관련하여 문제나 궁금한 점이 있을 경우 jhjung.dev@gmail.com 이나 이 저장소의 Issues 란에 질문해 주세요.  
답변에는 수 일이 소요될 수 있습니다.

질문이나 버그 제보 시에는 구동 환경을 **상세히** 적어 주세요. 충분한 정보가 있을수록 빠른 해결에 도움이 됩니다.

## Todos

 + 레시피 목록 구현
 + 즐겨찾기 기능 구현
 + 설정 저장 / 불러오기, 초기화 기능 구현
 + 설치 과정 자동화

## 라이선스
이 애드온 프로그램은 LGPL 라이선스 하에 사용 가능합니다.
