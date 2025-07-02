# app/gui_tkinter.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from. import scraper, data_handler, config

class TkinterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tier 2: 프로 자동화 봇")
        self.geometry("500x300")

        self.url_label = ttk.Label(self, text="타겟 URL:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self, width=60)
        self.url_entry.pack(pady=5, padx=10)
        self.url_entry.insert(0, config.DYNAMIC_URL)

        self.scrape_button = ttk.Button(self, text="크롤링 시작", command=self.start_scraping_thread)
        self.scrape_button.pack(pady=20)

        self.status_label = ttk.Label(self, text="상태: 대기 중")
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="indeterminate")
        self.progress.pack(pady=10)

    def start_scraping_thread(self):
        self.scrape_button.config(state="disabled")
        self.status_label.config(text="상태: 크롤링 진행 중...")
        self.progress.start(10)
        
        url = self.url_entry.get()
        thread = threading.Thread(target=self.run_scraping, args=(url,), daemon=True)
        thread.start()

    def run_scraping(self, url):
        scraped_data = scraper.scrape_dynamic_site(url)
        
        if scraped_data:
            saved = data_handler.save_data(scraped_data, 'excel', 'pro_bot_output')
            if saved:
                self.after(0, lambda: messagebox.showinfo("완료", "크롤링이 완료되었고, 'output' 폴더에 Excel 파일로 저장되었습니다."))
            else:
                self.after(0, lambda: messagebox.showerror("오류", "데이터 저장에 실패했습니다."))
        else:
            self.after(0, lambda: messagebox.showerror("오류", "크롤링에 실패했습니다."))

        self.after(0, self.scraping_done)

    def scraping_done(self):
        self.progress.stop()
        self.status_label.config(text="상태: 대기 중")
        self.scrape_button.config(state="normal")