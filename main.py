# main.py

import sys
import argparse
from app import scraper, data_handler, config

def run_tier1():
    print("--- Tier 1: 스타터 데이터 추출 실행 ---")
    data = scraper.scrape_static_site(config.STATIC_URL)
    if data:
        data_handler.save_data(data, 'csv', 'tier1_output')

def run_tier2():
    print("--- Tier 2: 프로 자동화 봇 실행 (Tkinter GUI) ---")
    try:
        from app.gui_tkinter import TkinterApp
        app = TkinterApp()
        app.mainloop()
    except ImportError:
        print("Tkinter를 실행할 수 없습니다. GUI 환경이 아닐 수 있습니다.")
    except Exception as e:
        print(f"Tier 2 실행 중 오류 발생: {e}")

def run_tier3():
    print("--- Tier 3: 엔터프라이즈 맞춤 솔루션 실행 (PyQt GUI) ---")
    try:
        from app.gui_pyqt import PyQtApp
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        ex = PyQtApp()
        ex.show()
        sys.exit(app.exec_())
    except ImportError:
        print("PyQt5를 찾을 수 없습니다. 'pip install PyQt5'로 설치해주세요.")
    except Exception as e:
        print(f"Tier 3 실행 중 오류 발생: {e}")

def main():
    parser = argparse.ArgumentParser(description="범용 웹 크롤러. --tier 옵션 없이 실행 시 Tier 3 GUI를 기본으로 실행합니다.")
    parser.add_argument('--tier', type=int, choices=[1, 2, 3], help="실행할 서비스 등급 (1, 2, 3)")
    args = parser.parse_args()

    if args.tier == 1:
        run_tier1()
    elif args.tier == 2:
        run_tier2()
    elif args.tier == 3:
        run_tier3()
    else:
        # 인자 없이 실행 시 기본값으로 Tier 3 실행
        run_tier3()

if __name__ == "__main__":
    main()