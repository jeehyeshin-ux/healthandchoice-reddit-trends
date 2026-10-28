"""Synthetic posts for testing the pipeline without Reddit credentials."""
import random
import time

TITLES = [
    ("SeoulPlasticSurgery", "Rhinoplasty in Gangnam: clinic quote vs coordinator fee, is it a scam?"),
    ("SeoulPlasticSurgery", "Revision rhinoplasty after botched surgery, need a safe surgeon"),
    ("SeoulPlasticSurgery", "Double eyelid surgery recovery swelling week 2"),
    ("KoreaSeoulBeauty", "Skin booster rejuran vs salmon dna price in Seoul"),
    ("KoreaSeoulBeauty", "Tax refund for medical tourists VAT clinic Seoul"),
    ("KoreaTravelBeauty", "Botox filler and laser trip itinerary, hotel near Apgujeong"),
    ("MedTourismAesthetic", "Korea vs Turkey vs Thailand for facelift cost"),
    ("medicaltourism", "Interpreter and translator at Korean hospital, insurance for complications"),
    ("PlasticSurgery", "Jaw surgery V-line orthognathic Korea regret"),
    ("koreatravel", "K-ETA visa for medical stay and recovery stay airbnb"),
]


def posts(n=120, seed=1):
    rnd = random.Random(seed)
    now = time.time()
    out = []
    for i in range(n):
        sub, title = TITLES[i % len(TITLES)]
        age = rnd.uniform(0, 7 * 86400)
        if i % 4 == 0:  # make some terms rise
            title += " ulthera shurink thread lift"
            age = rnd.uniform(0, 40 * 3600)
        out.append({"id": f"d{i}", "subreddit": sub, "title": title, "selftext": "",
                    "created_utc": now - age, "score": rnd.randint(1, 400),
                    "num_comments": rnd.randint(0, 150), "permalink": f"/r/{sub}/comments/d{i}/demo/"})
    return out
