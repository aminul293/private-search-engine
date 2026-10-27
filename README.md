# private-search-engine

A personal search engine that runs entirely on your own machine: a
small crawler, an inverted index, and BM25 ranking, with a minimal web
page to query it. Zero dependencies, standard library only, and it
works offline against a bundled sample corpus.

## Run it

```bash
python make_corpus.py    # only needed to regenerate the sample pages
python app.py --demo     # crawl, index, and print sample query results
python app.py            # web UI on http://127.0.0.1:8077
python -m pytest         # test suite
```

## Example demo output

```text
indexed 12 pages from 5 seeds (330 distinct terms)

query: 'python list sorting'
   6.30  Working With Python Lists
   4.83  Sorting Algorithms: Bubble, Merge, Quick
   ...

query: 'rocket orbit mars'
   6.61  How Rockets Reach Space
   3.23  Missions to Mars
```

## How it works

1. **Crawler.** Starts from seed pages, parses each one with a small
   HTML parser that pulls the title, the visible text, and the links,
   then follows links breadth-first. Seeds can be local files, which is
   how the offline demo works, or http URLs on your own network.
2. **Index.** Text is tokenized (lowercased, stopwords dropped) into an
   inverted index: each term maps to the documents containing it and
   how often. Document lengths are kept for normalization.
3. **Ranking.** Queries are scored with BM25, the ranking function
   that powered a generation of real search engines. It balances term
   frequency, how rare a term is across the corpus, and document
   length, so a short page that is really about your query beats a long
   page that mentions it once.
4. **UI.** A single standard-library HTTP server with a search box,
   results, scores, and snippets. No framework, no JavaScript.

## What it demonstrates

The moving parts of a real search engine (crawl, index, rank, serve)
at a size where every part can be read and understood, plus a ranking
test suite that checks the right page actually wins for sample queries.

## Honest scope

The corpus is 12 hand-written pages, the crawler is polite but simple
(no robots.txt, no JavaScript rendering, no scheduling), tokenization
is regex based with no stemming, and the index lives in memory. Point
it at a folder of your own HTML notes and it is genuinely useful;
it is not a Google replacement.
