"""Web UI and offline demo for the private search engine.

    python app.py            serve the search page on http://127.0.0.1:8077
    python app.py --demo     crawl the corpus, run sample queries, print results
"""

import html
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from search import Index, crawl, snippet

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")
SEEDS = [os.path.join(CORPUS, name) for name in
         ("python-basics.html", "gardening-herbs.html", "space-rockets.html",
          "coffee-brewing.html", "web-servers.html")]

INDEX = Index().build(crawl(SEEDS))


def page(query="", results=None):
    rows = ""
    if results is not None:
        if not results:
            rows = "<p>No results. Try other words.</p>"
        for doc, score in results:
            rows += (f'<div class="hit"><a href="file://{html.escape(doc["url"])}">'
                     f'{html.escape(doc["title"])}</a>'
                     f'<span class="score">score {score:.2f}</span>'
                     f'<p>{html.escape(snippet(doc, query))}</p></div>')
    return f"""<!doctype html><html><head><title>private search</title>
<style>body{{font-family:system-ui;margin:2rem auto;max-width:44rem;padding:0 1rem}}
input{{width:70%;padding:.5rem;font-size:1rem}} button{{padding:.5rem 1rem}}
.hit{{margin:1.2rem 0}} .score{{color:#888;margin-left:.6rem;font-size:.85rem}}
a{{font-size:1.05rem}}</style></head><body>
<h1>private search</h1>
<p>Searching {len(INDEX.docs)} locally crawled pages. Nothing leaves this machine.</p>
<form action="/search"><input name="q" value="{html.escape(query)}" autofocus>
<button>Search</button></form>{rows}</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/search":
            q = parse_qs(parsed.query).get("q", [""])[0]
            body = page(q, INDEX.search(q)).encode()
        elif parsed.path == "/":
            body = page().encode()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def demo():
    print(f"indexed {len(INDEX.docs)} pages from {len(SEEDS)} seeds "
          f"({len(INDEX.postings)} distinct terms)")
    for q in ("python list sorting", "grow tomatoes water", "rocket orbit mars",
              "coffee water ratio", "router wifi password"):
        print(f"\nquery: {q!r}")
        for doc, score in INDEX.search(q, k=3):
            print(f"  {score:5.2f}  {doc['title']}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        print("serving on http://127.0.0.1:8077 (ctrl+c to stop)")
        HTTPServer(("127.0.0.1", 8077), Handler).serve_forever()
