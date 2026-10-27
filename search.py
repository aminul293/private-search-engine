"""A small personal search engine: crawler, inverted index, BM25.

Pipeline:
  crawl(seeds)   fetch pages (local files or http), pull out title,
                 visible text, and links, then follow links BFS-style.
  Index          inverted index over tokenized text with document
                 lengths stored for BM25 normalization.
  Index.search   BM25 ranking, the same family of scoring that powered
                 a generation of real search engines.

Everything is standard library. No dependencies, runs fully offline
against the bundled corpus.
"""

import math
import os
import re
import urllib.request
from collections import deque
from html.parser import HTMLParser

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "is", "it", "for",
    "on", "with", "as", "by", "at", "from", "this", "that", "are", "was",
    "be", "you", "your", "we", "how", "can", "all", "one", "two",
}

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return [t for t in TOKEN_RE.findall(text.lower())
            if t not in STOPWORDS and len(t) > 1]


# ------------------------------------------------------------- crawling

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self._skip = 0
        self.chunks = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.chunks.append(data)

    @property
    def text(self):
        return " ".join(" ".join(self.chunks).split())


def fetch(url):
    if url.startswith(("http://", "https://")):
        req = urllib.request.Request(url, headers={"User-Agent": "private-search/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")
    with open(url, encoding="utf-8") as fh:
        return fh.read()


def resolve(base, href):
    if href.startswith(("http://", "https://")):
        return href
    if base.startswith(("http://", "https://")):
        from urllib.parse import urljoin
        return urljoin(base, href)
    return os.path.normpath(os.path.join(os.path.dirname(base), href))


def crawl(seeds, max_pages=100):
    """BFS from seed URLs/paths. Returns (url, title, text) tuples."""
    seen, queue, pages = set(), deque(seeds), []
    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        try:
            html = fetch(url)
        except (OSError, ValueError):
            continue
        parser = PageParser()
        parser.feed(html)
        pages.append((url, parser.title.strip() or url, parser.text))
        for href in parser.links:
            if href.startswith(("#", "mailto:")):
                continue
            nxt = resolve(url, href)
            if nxt not in seen:
                queue.append(nxt)
    return pages


# ------------------------------------------------------------- index

class Index:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = {}        # doc_id -> {url, title, text, length}
        self.postings = {}    # term -> {doc_id: term frequency}
        self.total_length = 0

    def add(self, doc_id, url, title, text):
        tokens = tokenize(text)
        self.docs[doc_id] = {"url": url, "title": title, "text": text,
                             "length": len(tokens)}
        self.total_length += len(tokens)
        for tok in tokens:
            self.postings.setdefault(tok, {})
            self.postings[tok][doc_id] = self.postings[tok].get(doc_id, 0) + 1

    def build(self, pages):
        for i, (url, title, text) in enumerate(pages):
            self.add(i, url, title, text)
        return self

    def search(self, query, k=10):
        terms = tokenize(query)
        if not terms or not self.docs:
            return []
        n = len(self.docs)
        avgdl = self.total_length / n
        scores = {}
        for term in terms:
            posting = self.postings.get(term)
            if not posting:
                continue
            df = len(posting)
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            for doc_id, tf in posting.items():
                dl = self.docs[doc_id]["length"]
                denom = tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
                scores[doc_id] = scores.get(doc_id, 0.0) + idf * tf * (self.k1 + 1) / denom
        ranked = sorted(scores.items(), key=lambda kv: -kv[1])
        return [(self.docs[d], s) for d, s in ranked[:k] if s > 0]


def snippet(doc, query, width=180):
    text = doc["text"]
    low = text.lower()
    pos = min((low.find(t) for t in tokenize(query) if low.find(t) >= 0),
              default=0)
    start = max(0, pos - 40)
    out = text[start:start + width].strip()
    return ("..." if start else "") + out + "..."
