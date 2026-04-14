
## ※ 본 툴은 학습용으로 사용시 발생하는 문제에 대한 책임은 모두 사용자 본인에게 있습니다.

본 툴은 클래스카드의 암기, 리콜, 스펠 학습을 자동화하는 툴입니다.

``` R.py (리콜) 사용시 https://chromewebstore.google.com/detail/classcard-auto/ddhailnbodajnflekpkmkpglocmendfp 에서 extension 다운로드 후 리콜 가이드 켜주세요.```

**설명**
- S.py : 스펠 학습
  - OCR 인식으로 단어를 학습하여 DB에 저장 한 후 단어가 다시 나타나면 입력.
- R.py : 리콜 학습
  - 크롬 확장프로그램의 파란 테두리를 인식하여 번호 입력.
    - 4개가 제일 안정합니다.
- M.py
  - 암기 스페이스 키 반복.

**요구 라이브러리**
```
- pyautogui
- pytesseract
-numpy
-opencv-python
```

## Tesseract OCR
- S.py 사용 시 화면 글자 인식을 위하여 Tesseract OCR 프로그램을 다운로드 해 주세요.
