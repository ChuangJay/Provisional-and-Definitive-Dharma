import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin, urlparse

def download_image(url, save_dir):
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            if not filename: filename = "image.jpg"
            save_path = os.path.join(save_dir, filename)
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024): f.write(chunk)
            return os.path.join("images", filename)
    except: pass
    return url

def fetch_and_convert(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # 使用 html5lib 以更好地處理非標準標籤如 <session>
    soup = BeautifulSoup(response.text, 'html5lib')

    page_title = soup.title.text.split('-')[-1].strip()
    tag_answer = soup.find(id="taganswer")
    if not tag_answer: return page_title, "Content not found"

    output_dir = page_title
    os.makedirs(output_dir, exist_ok=True)

    output = [f"# {page_title}\n"]
    image_dir = os.path.join(output_dir, "images")
    
    # 封面
    content_div = soup.find('div', class_='publicationtext')
    if content_div:
        cover_img = content_div.find('img', alt='封面')
        if cover_img:
            src = cover_img.get('src')
            local = download_image(urljoin(url, src), image_dir)
            output.append(f"![封面]({local})\n")

    # 1. 抓取目錄結構
    sections = []
    current_h2 = None
    # 在 html5lib 中，標籤名會變成小寫
    for el in tag_answer.find_all(True, recursive=False):
        style = el.get('style', '').lower()
        if 'color:#dc875a' in style or 'color: #dc875a' in style:
            current_h2 = el.get_text(strip=True)
        elif el.name == 'ul':
            links = el.find_all('a')
            for a in links:
                sections.append({
                    'h2': current_h2,
                    'h3': a.get_text(strip=True),
                    'id': a.get('href', '').replace('#', '')
                })

    # 2. 抓取正文
    # 獲取整個頁面中所有的 publicationass div
    ass_divs = soup.find_all('div', class_='publicationass')
    
    last_h2 = None
    for sec in sections:
        h2 = sec['h2']
        h3 = sec['h3']
        
        if h2 != last_h2:
            output.append(f"\n## {h2}\n")
            last_h2 = h2
        
        output.append(f"\n### {h3}\n")
        
        # 尋找內容
        target_div = None
        for div in ass_divs:
            div_text = div.get_text()
            if h3 in div_text and len(div_text) > 100:
                target_div = div
                break
        
        if target_div:
            # 提取文字
            raw_text = target_div.get_text('\n')
            lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
            for line in lines:
                if line == h3 or line == "目錄": continue
                if '整理' in line or '編輯部' in line or '講授' in line or line in ['蓮心', '心爾']:
                    if len(line) < 60:
                        output.append(f"\n*{line}*\n")
                        continue
                if '問：' in line or '答：' in line:
                    line = line.replace('問：', '\n**問：** ').replace('答：', '\n**答：** ')
                    output.append(f"{line}\n")
                else:
                    output.append(f"\n{line}\n")
            
            # 圖片
            for img in target_div.find_all('img'):
                src = img.get('src')
                local = download_image(urljoin(url, src), image_dir)
                output.append(f"\n![圖片]({local})\n")

    result = "".join(output)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return page_title, result.replace('加入學習計畫', '')

if __name__ == "__main__":
    with open("urlList", "r") as f:
        urls = [line.strip().strip('"') for line in f if line.strip()]

    for i, url in enumerate(urls, 1):
        try:
            title, md = fetch_and_convert(url)
            output_path = os.path.join(title, "output.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"[{i}/{len(urls)}] Done → {title}/")
        except Exception as e:
            print(f"[{i}/{len(urls)}] Failed → {url} ({e})")
