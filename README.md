# Teaspoon-mabinogi
마비노기의 요리 관련 부가기능을 제공하는 애드온 프로그램입니다.

## 설치 방법

1. 최신 Release를 다운로드해 주세요.

2. Python을 설치합니다. 3.9 이상 버전을 권장합니다.  
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
해당 메시지가 발생할 경우 해당 시스템 변수를 추가하면 해결됩니다.

  + 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH  
  + 변수 값 : (Python이 설치된 경로)\Lib\site-packages\PySide6\plugins\platforms


## Todos

 + 레시피 목록 구현
 + 즐겨찾기 기능 구현
 + 설정 저장 / 불러오기, 초기화 기능 구현
 + 설치 과정 자동화
