"""Keyword + trend analysis over fetched posts."""
import re
from collections import Counter, defaultdict

import config

WORD = re.compile(r"[a-z][a-z\-']{2,}")


def tokens(text):
    return [w.strip("-'") for w in WORD.findall(text.lower()) if w not in config.STOPWORDS]


def terms(post):
    """Unigrams + bigrams of title/body, plus phrase hits from the topic taxonomy."""
    text = f"{post.get('title', '')} {post.get('selftext', '')[:1500]}".lower()
    toks = tokens(text)
    found = set(toks) | {f"{a} {b}" for a, b in zip(toks, toks[1:])}
    for words in config.TOPICS.values():
        found |= {w for w in words if w in text}
    return found


def weight(p):
    return 1 + p.get("score", 0) ** 0.5 + 2 * p.get("num_comments", 0) ** 0.5


def tag_topics(post):
    text = f"{post.get('title', '')} {post.get('selftext', '')[:1500]}".lower()
    return [t for t, words in config.TOPICS.items() if any(w in text for w in words)]


def analyze(posts, now):
    """posts: list of dicts with created_utc, score, num_comments, title, subreddit, permalink."""
    cut = now - config.RECENT_HOURS * 3600
    recent = [p for p in posts if p["created_utc"] >= cut]
    older = [p for p in posts if p["created_utc"] < cut]
    freq_r, freq_o, hot = Counter(), Counter(), defaultdict(float)
    for p in recent:
        for t in terms(p):
            freq_r[t] += 1
    for p in older:
        for t in terms(p):
            freq_o[t] += 1
    for p in posts:
        for t in terms(p):
            hot[t] += weight(p)

    def keep(t):  # drop noise: single short words that appear once
        return len(t) > 3 and (" " in t or len(t) > 4)

    rising = []
    nr, no = max(len(recent), 1), max(len(older), 1)
    for t, c in freq_r.items():
        if c >= 3 and keep(t):
            ratio = (c / nr) / ((freq_o.get(t, 0) + 0.5) / no)
            rising.append((t, c, round(ratio, 1), freq_o.get(t, 0)))
    rising.sort(key=lambda x: (x[2] * x[1]), reverse=True)

    doc = Counter()
    for p in posts:
        for t in terms(p):
            doc[t] += 1
    hot_kw = sorted([(t, round(w), doc[t]) for t, w in hot.items() if keep(t) and doc[t] >= 3],
                    key=lambda x: x[1], reverse=True)

    topic_counts = Counter()
    topic_posts = defaultdict(list)
    for p in posts:
        for t in tag_topics(p):
            topic_counts[t] += 1
            topic_posts[t].append(p)
    topic_top = {t: sorted(v, key=weight, reverse=True)[:3] for t, v in topic_posts.items()}

    most_commented = sorted(posts, key=lambda p: p.get("num_comments", 0), reverse=True)[:10]
    top_scored = sorted(posts, key=lambda p: p.get("score", 0), reverse=True)[:5]
    by_sub = Counter(p["subreddit"] for p in posts)
    return {
        "n_posts": len(posts), "n_recent": len(recent), "by_sub": by_sub,
        "rising": rising[:15], "hot": hot_kw[:15], "topics": topic_counts, "topic_top": topic_top,
        "most_commented": most_commented, "top_scored": top_scored,
    }
