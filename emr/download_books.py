import requests
import os

books = [
    "https://www.gutenberg.org/cache/epub/1497/pg1497.txt",
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
    "https://www.gutenberg.org/cache/epub/1513/pg1513.txt",
    "https://www.gutenberg.org/cache/epub/11/pg11.txt",
    "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
    "https://www.gutenberg.org/cache/epub/174/pg174.txt",
    "https://www.gutenberg.org/cache/epub/98/pg98.txt",
    "https://www.gutenberg.org/cache/epub/1260/pg1260.txt",
    "https://www.gutenberg.org/cache/epub/3207/pg3207.txt",
    "https://www.gutenberg.org/cache/epub/1998/pg1998.txt",
    "https://www.gutenberg.org/cache/epub/2600/pg2600.txt",
    "https://www.gutenberg.org/cache/epub/6130/pg6130.txt",
]

os.makedirs("books", exist_ok=True)

for book_url in books:
    r = requests.get(book_url)
    text = r.text.splitlines()
    book_name = "".join(c if c.isalnum() else '_' for c in text[0][len("The Project Gutenberg eBook of ")+1:]).lower()

    for i, line in enumerate(text):
        if line.startswith("*** START OF THE PROJECT GUTENBERG EBOOK"):
            break
    else:
        i = 0

    with open(f"books/{book_name}.txt", "w") as f:
        f.write("\n".join(text[i+1:]))
