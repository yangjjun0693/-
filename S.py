import pytesseract
import pyautogui
import cv2
import numpy as np
import time
import json
import os
import re
import traceback
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
DB_FILE = "word_memory.json"

# ==========================================
# [설정] 
BUTTON_OFFSET = 320   # 힌트 확인 완료 버튼
INPUT_OFFSET = 130    # 정답 입력창 위치
TYPING_SPEED = 0.12   # 타자 간격 (숫자가 커질수록 느려짐, 0.1~0.2 추천)
# ==========================================

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except: pass

memory_db = load_db()

def clean_text(text):
    return re.sub(r'[^가-힣a-zA-Z0-9]', '', text)

def solve_v70():
    try:
        print(f">>> [V7.0] 타자 속도 조절 모드 가동 (속도: {TYPING_SPEED})")
        print(">>> 10초 뒤 시작합니다.")
        
        for i in range(10, 0, -1):
            print(f"[{i}]..."); time.sleep(1)
        
        scr_w, scr_h = pyautogui.size()
        center_x, center_y = scr_w // 2, scr_h // 2

        while True:
            # 1. 뜻 인식 영역 캡처
            cap_x, cap_y = center_x - 300, center_y - 200
            shot = pyautogui.screenshot(region=(cap_x, cap_y, 600, 300))
            frame = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
            raw_meaning = pytesseract.image_to_string(thresh, lang='kor', config='--psm 6').strip()
            meaning_key = clean_text(raw_meaning)

            if len(meaning_key) < 2:
                time.sleep(0.5); continue

            if meaning_key in memory_db:
                answer = memory_db[meaning_key]
                print(f"[매칭] {meaning_key[:8]} -> {answer}")
                
                # 입력창 클릭
                pyautogui.click(center_x, center_y + INPUT_OFFSET) 
                time.sleep(random.uniform(0.2, 0.4)) # 사람 같은 미세 대기
                
                # 타자 속도 조절
                pyautogui.write(answer, interval=TYPING_SPEED) 
                
                pyautogui.press('enter')
                time.sleep(random.uniform(1.0, 1.2))
                pyautogui.press('space') # 결과 확인창 넘기기
                time.sleep(random.uniform(1.5, 2.0)) 
            else:
                # 2. 힌트 수집 단계
                print(f"[수집] '{meaning_key[:8]}' 힌트 확인 중...")
                pyautogui.hotkey('ctrl', 'h')
                time.sleep(1.5)
                
                h_shot = pyautogui.screenshot(region=(center_x - 300, center_y - 100, 600, 500))
                h_frame = cv2.cvtColor(np.array(h_shot), cv2.COLOR_RGB2BGR)
                hsv = cv2.cvtColor(h_frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
                
                hint_ocr = pytesseract.image_to_string(mask, lang='eng', config='--psm 7').strip()
                clean_answer = "".join([c for c in hint_ocr if c.isalpha()])

                if len(clean_answer) >= 2:
                    memory_db[meaning_key] = clean_answer
                    save_db(memory_db)
                    
                    # 힌트 확인 버튼 클릭
                    pyautogui.click(center_x, center_y + BUTTON_OFFSET) 
                    time.sleep(1.0)
                    
                    # 입력창 클릭 및 느린 타징
                    pyautogui.click(center_x, center_y + INPUT_OFFSET)
                    time.sleep(0.3)
                    pyautogui.write(clean_answer, interval=TYPING_SPEED)
                    
                    pyautogui.press('enter')
                    time.sleep(random.uniform(1.0, 1.2)); pyautogui.press('space'); time.sleep(1.8)
                else:
                    pyautogui.press('esc'); time.sleep(0.5)
                    
    except Exception:
        traceback.print_exc()
        input("\n>>> 작업 중단. 엔터를 누르면 종료됩니다...")

if __name__ == "__main__":
    solve_v70()