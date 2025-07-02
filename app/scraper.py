# app/scraper.py

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 실제 브라우저처럼 보이기 위한 User-Agent 설정
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_static_site(url):
    """Tier 1: 정적 웹사이트 크롤링"""
    print(f"정적 사이트 크롤링 시작: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = 
        quotes = soup.select('div.quote')
        for quote in quotes:
            text = quote.select_one('span.text').get_text(strip=True)
            author = quote.select_one('small.author').get_text(strip=True)
            items.append({'quote': text, 'author': author})
        
        print(f"총 {len(items)}개의 아이템을 찾았습니다.")
        return items

    except requests.exceptions.RequestException as e:
        print(f"정적 사이트 크롤링 오류: {e}")
        return None

def scrape_dynamic_site(url, login_credentials=None):
    """Tier 2 & 3: 동적 웹사이트 및 로그인 처리"""
    print(f"동적 사이트 크롤링 시작: {url}")
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("lang=ko_KR") 

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        if login_credentials:
            print("로그인 시도 중...")
            # 실제 사이트의 ID, 비밀번호 필드, 로그인 버튼의 선택자로 변경해야 합니다.
            driver.find_element(By.ID, 'username').send_keys(login_credentials['username'])
            driver.find_element(By.ID, 'password').send_keys(login_credentials['password'])
            driver.find_element(By.ID, 'login_button').click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-profile-element"))
            )
            print("로그인 성공.")

        # 동적 콘텐츠가 로드될 때까지 대기 (예: 영상 목록)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        items =
        videos = soup.select("div#details")
        for video in videos:
            title_tag = video.select_one("a#video-title-link")
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'
            link = "https://www.youtube.com" + title_tag['href'] if title_tag else 'N/A'
            
            meta_block = video.select_one("div#meta")
            views = meta_block.select_one("span.inline-metadata-item").get_text(strip=True) if meta_block else 'N/A'
            
            items.append({'title': title, 'link': link, 'views': views})

        print(f"총 {len(items)}개의 아이템을 찾았습니다.")
        return items

    except Exception as e:
        print(f"동적 사이트 크롤링 오류: {e}")
        return None
    finally:
        if driver:
            driver.quit()