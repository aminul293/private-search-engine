import os

from search import Index, PageParser, crawl, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")


def test_tokenize_drops_stopwords():
    assert tokenize("The Quick Brown Fox") == ["quick", "brown", "fox"]
    assert tokenize("Python, python! PYTHON?") == ["python", "python", "python"]


def test_parser_extracts_title_text_links():
    p = PageParser()
    p.feed("<html><head><title>My Page</title></head><body>"
           "<p>Hello <b>world</b></p><a href='other.html'>go</a>"
           "<script>var secret = 1;</script></body></html>")
    assert p.title == "My Page"
    assert "Hello world" in p.text
    assert "secret" not in p.text
    assert p.links == ["other.html"]


def test_crawler_follows_links(tmp_path):
    (tmp_path / "a.html").write_text(
        "<html><head><title>A</title></head><body>alpha page "
        "<a href='b.html'>b</a></body></html>")
    (tmp_path / "b.html").write_text(
        "<html><head><title>B</title></head><body>beta page</body></html>")
    pages = crawl([str(tmp_path / "a.html")])
    titles = sorted(t for _u, t, _x in pages)
    assert titles == ["A", "B"]


def corpus_index():
    seeds = [os.path.join(CORPUS, "python-basics.html"),
             os.path.join(CORPUS, "gardening-herbs.html"),
             os.path.join(CORPUS, "space-rockets.html"),
             os.path.join(CORPUS, "coffee-brewing.html"),
             os.path.join(CORPUS, "web-servers.html")]
    return Index().build(crawl(seeds))


def test_corpus_crawl_covers_all_pages():
    idx = corpus_index()
    assert len(idx.docs) == 12


def test_bm25_ranks_relevant_page_first():
    idx = corpus_index()
    top = idx.search("how do i sort a python list", k=1)[0][0]
    assert "Sorting" in top["title"] or "List" in top["title"]
    top = idx.search("tomato plants water sun", k=1)[0][0]
    assert "Tomato" in top["title"]
    top = idx.search("coffee beans grind water", k=1)[0][0]
    assert "Coffee" in top["title"]
    top = idx.search("rocket orbit fuel stages", k=1)[0][0]
    assert "Rocket" in top["title"]


def test_search_no_match_returns_empty():
    idx = corpus_index()
    assert idx.search("zzzqqq nonexistent") == []
