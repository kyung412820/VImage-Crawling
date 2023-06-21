import os
import random
import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, unquote, urljoin
from uuid import uuid4


def download_resource(url, save_dir, min_size):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    content_length = int(response.headers.get("Content-Length", 0))
    if content_length < min_size:
        return False

    # 파일명 생성
    ext = os.path.splitext(urlparse(url).path)[1]
    file_name = str(uuid4()) + ext
    file_path = os.path.join(save_dir, file_name)

    # 파일 다운로드
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    return True


# 크롤링할 웹 사이트의 URL
url = input("URL을 입력하세요: ")

javascript = 0  # html의 javascript 요청이 필요하면 1 아니면 0
if javascript == 1:
    # ChromeDriver 경로 설정
    chromedriver_path = "/path/to/chromedriver"  # 자신의 환경에 맞게 수정

    # ChromeDriver 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 브라우저 창을 띄우지 않음

    # ChromeDriver 객체 생성
    driver = webdriver.Chrome(chromedriver_path, options=options)

    # 웹 페이지 접속
    driver.get(url)

    # JavaScript 코드가 실행될 때까지 대기
    driver.implicitly_wait(5)

    # HTML 문서 다운로드
    html = driver.page_source
    """
    # 가장 높은 화질의 영상 URL 추출
    video_urls = re.findall(r'"(https://.*?\.mp4)"', html)

    # 영상 다운로드
    if video_urls:
        video_url = video_urls[0]
        print("Video URL:", video_url)
    else:
        print("No video URL found.")"""
else:
    response = requests.get(url)
    html = response.text

# ChromeDriver 종료
if javascript == 1:
    driver.quit()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html, "html.parser")

# HTML 문서의 title 태그 추출
title_tag = soup.find("title")
title = title_tag.text.strip()  # title 문자열 추출 및 공백 제거

# 유효하지 않은 문자 제거 및 유효한 폴더 이름 생성
invalid_chars = r'\/:*?"<>|'
for char in invalid_chars:
    title = title.replace(char, "")

# 자원을 저장할 로컬 폴더 경로
save_dir = os.path.join(r"C:\Users\user\Desktop\Result", title)

# 로컬 폴더가 없다면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 태그 추출
image_tags = soup.find_all("img")

# 이미지 다운로드
count = 0
for img_tag in image_tags:
    img_url = img_tag.get("src")  # 이미지 URL 추출

    try:
        if img_url.startswith("//"):  # URL이 //로 시작할 경우 https:를 추가하여 유효한 URL로 변환
            img_url = "https:" + img_url
        elif not img_url.startswith("http"):  # URL이 상대 경로일 경우 절대 경로로 변환
            img_url = urljoin(url, img_url)

        if download_resource(img_url, save_dir, 30 * 1024):  # 이미지의 최소 크기를 30KB로 지정 (30 * 1024 bytes)
            print(f"{img_url} 다운로드 완료")
            count += 1
    except Exception as e:
        print(f"다운로드 오류: {img_url}")
        print(e)

# 이미지 크롤링이 완료되었습니다.
print(f"이미지 크롤링이 완료되었습니다. (다운로드된 이미지 수: {count})")

# 동영상을 저장할 로컬 폴더 경로
save_dir = os.path.join(r"C:\Users\user\Desktop\Result", title)

# 로컬 폴더가 없다면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 동영상 태그 추출
video_tags = soup.find_all("video")

# 동영상 다운로드
count = 0
for video_tag in video_tags:
    video_url = video_tag.get("src")  # 동영상 URL 추출
    print(video_url)
    try:
        if video_url.startswith("//"):  # URL이 //로 시작할 경우 https:를 추가하여 유효한 URL로 변환
            video_url = "https:" + video_url
        elif not video_url.startswith("http"):  # URL이 상대 경로일 경우 절대 경로로 변환
            video_url = urljoin(url, video_url)

        if download_resource(video_url, save_dir, 1 * 1024 * 1024):  # 영상의 최소 크기를 1MB로 지정 (1 * 1024 * 1024 bytes)
            print(f"{video_url} 다운로드 완료")
            count += 1
    except Exception as e:
        print(f"다운로드 오류: {video_url}")
        print(e)

# 동영상 크롤링이 완료되었습니다.
print(f"동영상 크롤링이 완료되었습니다. (다운로드된 동영상 수: {count})")
