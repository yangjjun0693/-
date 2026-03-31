import pyautogui
import numpy as np
import time
from PIL import ImageGrab

def capture_screen():
    shot = ImageGrab.grab()
    return np.array(shot)  # RGB 형태

def find_blue_line_y(img_np):
    h, w = img_np.shape[:2]
    
    r = img_np[:, :, 0].astype(int)
    g = img_np[:, :, 1].astype(int)
    b = img_np[:, :, 2].astype(int)

    # #4B56ED = RGB(75, 86, 237) 기준으로 넓게 잡음 (안티앨리어싱 & 스케일링 대비)
    blue_mask = (b > r + 20) & (b > g + 20) & (b > 80)

    x_start = w // 4
    x_end   = w * 3 // 4
    blue_in_center = blue_mask[:, x_start:x_end]

    blue_counts = blue_in_center.sum(axis=1)

    # 임계값을 30으로 낮춤 (얇은 테두리, 스케일링 환경 대비)
    candidate_ys = np.where(blue_counts > 30)[0]

    if len(candidate_ys) == 0:
        return None

    blue_line_ys = []
    prev = -99
    for y in candidate_ys:
        if y - prev > 5:
            blue_line_ys.append(y)
        prev = y

    return blue_line_ys


def get_option_number(blue_line_ys, screen_h):
    if not blue_line_ys:
        return None

    card_ys = [y for y in blue_line_ys if y > screen_h * 0.4]

    if not card_ys:
        return None

    blue_y = card_ys[0]

    option_h = screen_h * (49 / 1080)

    # 각 선택지 하단 경계선 y (1080p 기준: 583, 632, 681, 730)
    option_bottoms = [
        screen_h * (583 / 1080),
        screen_h * (632 / 1080),
        screen_h * (681 / 1080),
        screen_h * (730 / 1080),
    ]

    # 산술 계산 대신 가장 가까운 선택지로 매핑
    dists = [abs(blue_y - b) for b in option_bottoms]
    best = int(np.argmin(dists)) + 1

    if min(dists) > option_h * 1.5:
        return None

    return best


def press_blue_option():
    img = capture_screen()
    h, w = img.shape[:2]

    blue_ys = find_blue_line_y(img)
    print(f"🔵 파란선 후보 y좌표: {blue_ys}")

    if not blue_ys:
        print("❌ 파란 테두리를 찾지 못했습니다.")
        return False

    option_num = get_option_number(blue_ys, h)
    print(f"   화면 높이: {h}px")

    if option_num is None or not (1 <= option_num <= 4):
        print(f"⚠️  번호 추정 실패 (option_num={option_num})")
        return False

    print(f"✅ {option_num}번 키 입력!")
    pyautogui.press(str(option_num))
    return True


if __name__ == "__main__":
    print("3초 후 시작합니다. 브라우저 창을 활성화하세요.")
    time.sleep(3)

    while True:
        print("\n--- 탐색 중 ---")
        press_blue_option()
        time.sleep(1.5)