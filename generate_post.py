import os
import json
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6LEmT1Hjz6O_td-z4dJvIodJcwLHa59G1X6xVjce6_bQw")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

prompt = """
Lütfen yazılım, teknoloji, yapay zeka veya dijital trendler hakkında dikkat çekici, SEO dostu Türkçe bir blog yazısı oluştur.
Yanıtını YALNIZCA aşağıdaki JSON formatında ver, başka hiçbir açıklama ekleme:

{
  "title": "Başlık",
  "summary": "1-2 cümlelik kısa özet",
  "content": "HTML formatında paragraflar, <h3> alt başlıklar ve liste elemanları barındıran detaylı içerik",
  "category": "Teknoloji"
}
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}]
}

response = requests.post(URL, json=payload)
data = response.json()

try:
    text_response = data['candidates'][0]['content']['parts'][0]['text']
    # JSON kod bloğu temizleme
    if "```json" in text_response:
        text_response = text_response.split("```json")[1].split("```")[0].strip()
    elif "```" in text_response:
        text_response = text_response.split("```")[1].split("```")[0].strip()
    
    post_data = json.loads(text_response)
    post_data["id"] = int(datetime.now().timestamp())
    post_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Var olan içerikleri oku
    posts_file = "posts.json"
    if os.path.exists(posts_file):
        with open(posts_file, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except:
                posts = []
    else:
        posts = []

    # Yeni yazıyı başa ekle
    posts.insert(0, post_data)

    # Dosyaya kaydet
    with open(posts_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print("Yeni makale başarıyla üretildi ve eklendi.")

except Exception as e:
    print("Hata oluştu:", e)
    print("API Yanıtı:", data)
