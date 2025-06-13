# download_images.py
from icrawler.builtin import GoogleImageCrawler
import os

categories = [
    'bench press',
    'squat',
    'deadlift',
    'barbell biceps curl',
    'shoulder press'
]

base_dir = 'dataset/all_images'
os.makedirs(base_dir, exist_ok=True)

num_images = 50

for category in categories:
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    crawler = GoogleImageCrawler(storage={'root_dir': category_dir})
    print(f"📥 Downloading {num_images} more images for '{category}'...")
    crawler.crawl(keyword=category + " gym", max_num=num_images)

print("✅ New images downloaded and merged into existing folders.")
