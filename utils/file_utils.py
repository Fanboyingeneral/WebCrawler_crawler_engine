import re

def sanitize_filename(url):
    return re.sub(r'[\/:*?"<>|&]', '_', url)

def save_to_file(url, content):
    filename = f"{sanitize_filename(url)}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"URL: {url}\nContent:\n{content or 'No content retrieved'}\n")
    print(f"Data saved to {filename}.")
