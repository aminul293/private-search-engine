"""Generate the bundled sample corpus: 12 small interlinked pages.

Run once:  python make_corpus.py
The pages are committed under corpus/ so the demo works offline
without regenerating anything.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")

PAGES = {
    "python-basics.html": (
        "Python Basics for Beginners",
        "Python is a friendly programming language known for readable code. "
        "You write python programs in plain text files and run them with the "
        "python interpreter. Variables hold values, functions group reusable "
        "steps, and loops repeat work. Beginners like python because the "
        "syntax stays close to everyday language.",
        ["python-lists.html", "data-structures.html"],
    ),
    "python-lists.html": (
        "Working With Python Lists",
        "A python list is an ordered collection that can hold numbers, "
        "strings, or other lists. You append items to a list, slice a list "
        "to copy part of it, and sort a list with the sorted function. List "
        "comprehensions build a new list in one readable line.",
        ["python-basics.html", "sorting-algorithms.html"],
    ),
    "data-structures.html": (
        "Data Structures Explained Simply",
        "Data structures are ways of organizing information so programs can "
        "find it quickly. Arrays store items in order, hash maps connect "
        "keys to values, trees branch like family trees, and queues line "
        "items up first in first out. Choosing the right data structure "
        "often matters more than clever code.",
        ["sorting-algorithms.html", "python-basics.html"],
    ),
    "sorting-algorithms.html": (
        "Sorting Algorithms: Bubble, Merge, Quick",
        "Sorting puts a list in order. Bubble sort swaps neighbors again "
        "and again and is slow on big lists. Merge sort splits the list in "
        "half, sorts each half, and merges them back together. Quick sort "
        "picks a pivot and partitions around it. Merge sort and quick sort "
        "are the practical choices for large data.",
        ["data-structures.html", "python-lists.html"],
    ),
    "web-servers.html": (
        "How Web Servers Work",
        "A web server waits for requests from browsers and sends back "
        "pages. When you type an address, your browser asks a server for "
        "the page, and the server responds with HTML. Servers also handle "
        "images, forms, and logins. Popular web servers run on Linux and "
        "can answer thousands of requests every second.",
        ["home-networks.html", "python-basics.html"],
    ),
    "home-networks.html": (
        "Setting Up a Home Network",
        "A home network starts with a modem and a router. The router "
        "creates your wifi network and gives each device an address. Place "
        "the router in the center of the home for the best signal. Use a "
        "strong wifi password and update the router firmware to keep the "
        "network safe.",
        ["web-servers.html"],
    ),
    "gardening-herbs.html": (
        "Growing Herbs in a Small Garden",
        "Herbs are the easiest plants for a new garden. Basil loves warm "
        "sun, mint spreads fast and needs its own pot, and rosemary likes "
        "dry soil. Water herbs in the morning, pinch the tips to keep them "
        "bushy, and harvest a little at a time so the plant keeps growing.",
        ["tomato-guide.html"],
    ),
    "tomato-guide.html": (
        "A Tomato Growing Guide",
        "Tomatoes need full sun, rich soil, and steady water. Start tomato "
        "seeds indoors six weeks before the last frost, then move the "
        "plants outside. Support each tomato plant with a stake or cage, "
        "feed it every two weeks, and watch for yellow leaves, which often "
        "mean the plant needs more water or food.",
        ["gardening-herbs.html"],
    ),
    "space-rockets.html": (
        "How Rockets Reach Space",
        "Rockets carry fuel and oxygen and push exhaust down so the rocket "
        "moves up. Most rockets fly in stages, dropping empty tanks to save "
        "weight. To stay in orbit a rocket must reach about 28,000 "
        "kilometers per hour sideways. Reusable rockets land their first "
        "stage back on Earth to fly again.",
        ["mars-missions.html"],
    ),
    "mars-missions.html": (
        "Missions to Mars",
        "Mars is the most explored planet beyond Earth. Rovers have driven "
        "across the Mars surface studying rocks and searching for signs of "
        "past water. A trip to Mars takes about seven months. Future "
        "missions hope to bring Mars samples home and one day send people.",
        ["space-rockets.html"],
    ),
    "coffee-brewing.html": (
        "Brewing Better Coffee at Home",
        "Great coffee starts with fresh beans and clean water. Grind the "
        "coffee just before brewing, use water just below boiling, and "
        "keep the ratio near one part coffee to sixteen parts water. A "
        "pour over dripper gives a clean cup, while a french press makes "
        "coffee that tastes richer and heavier.",
        ["bread-baking.html"],
    ),
    "bread-baking.html": (
        "Baking Your First Loaf of Bread",
        "Bread needs only flour, water, yeast, and salt. Mix the dough, let "
        "it rise until it doubles, shape the loaf, and bake it in a hot "
        "oven until the crust is deep golden. The bread is done when the "
        "inside sounds hollow as you tap the bottom of the loaf.",
        ["coffee-brewing.html"],
    ),
}


def main():
    os.makedirs(CORPUS, exist_ok=True)
    for fname, (title, body, links) in PAGES.items():
        link_html = " ".join(f'<a href="{h}">{h}</a>' for h in links)
        html = (f"<html><head><title>{title}</title></head><body>"
                f"<h1>{title}</h1><p>{body}</p>"
                f"<nav>{link_html}</nav></body></html>")
        with open(os.path.join(CORPUS, fname), "w") as fh:
            fh.write(html)
    print(f"wrote {len(PAGES)} pages to {CORPUS}")


if __name__ == "__main__":
    main()
