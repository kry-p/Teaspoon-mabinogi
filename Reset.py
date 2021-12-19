from modules.preferences_provider import defaultPreferences, preferences

if __name__ == '__main__':
    print('설정 초기화 스크립트입니다.')

    while True:
        print('주의: 초기화한 설정은 다시 살릴 수 없습니다. 계속하시겠습니까? (Y / N) ')
        input = input()

        if input == 'Y' or input == 'y':
            for key, value in defaultPreferences.items():
                preferences.setValue(key, value)
            print('초기화를 완료했습니다.')
            break
        elif input == 'N' or input == 'n':
            print('초기화하지 않고 종료합니다.')
            break
        else:
            print('잘못된 값을 입력했습니다. 다시 입력해 주세요.')
