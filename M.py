import pyautogui
import time
import sys
import ctypes

class ContinuousAutomator:
    def __init__(self, interval=0.15):
        # 마우스 커서를 화면 모서리(0,0)로 던지면 강제 종료
        pyautogui.FAILSAFE = True
        self.interval = interval
        # 다음 카드로 넘어가는 렌더링 대기 시간 (최적값 0.7s)
        self.cooldown = 0.7 

    def prevent_sleep(self):
        """실행 중 시스템 절전 모드 진입 방지 (Windows 전용)"""
        if sys.platform == 'win32':
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

    def start(self):
        print("무한 루프 모드 활성화.")
        print("중단하려면 화면 구석으로 마우스를 옮기거나 Ctrl+C를 누르세요.")
        time.sleep(3) # 포커스 전환 대기

        try:
            while True:
                # 1단계: 카드 뒤집기 (SPACE)
                pyautogui.press('space')
                
                # 2단계: 요청하신 0.15초 정밀 대기
                time.sleep(self.interval)
                
                # 3단계: '이제 알아요' (SHIFT + SPACE)
                pyautogui.keyDown('shift')
                pyautogui.press('space')
                pyautogui.keyUp('shift')
                
                # 4단계: 다음 카드 로딩 대기
                time.sleep(self.cooldown)
                
        except KeyboardInterrupt:
            print("\n사용자에 의해 중단되었습니다.")

if __name__ == "__main__":
    automator = ContinuousAutomator(interval=0.15)
    automator.prevent_sleep()
    automator.start()