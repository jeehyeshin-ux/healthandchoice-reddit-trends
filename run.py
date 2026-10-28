#!/usr/bin/env python3
"""Reddit trend digest for Health & Choice.

  python run.py check-subs            verify candidate subreddits exist
  python run.py digest --demo         build report from synthetic data (no credentials)
  python run.py digest                fetch live, write out/digest_YYMMDD.html
  python run.py digest --send         also email recipients.txt
"""
import argparse
import datetime as dt
import os
import time

import analyze
import config
import report


def load_env(path=".env"):
    if os.path.exists(path):
        for line in open(path):
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v)


def fetch_live():
    from reddit_client import RedditClient
    rc = RedditClient()
    cutoff = time.time() - config.LOOKBACK_DAYS * 86400
    seen, posts = set(), []
    for sub in config.SUBREDDITS:
        try:
            batch = rc.listing(sub, "new", config.POSTS_PER_LISTING) + \
                rc.listing(sub, "top", config.POSTS_PER_LISTING, t="week")
        except Exception as e:  # missing/private/banned sub should not kill the run
            print(f"skip r/{sub}: {e}")
            continue
        for p in batch:
            if p["id"] not in seen and p["created_utc"] >= cutoff:
                seen.add(p["id"])
                posts.append(p)
    comments = {}
    top = sorted(posts, key=lambda p: p["num_comments"], reverse=True)[:10]
    for p in top[:config.FETCH_COMMENTS_FOR_TOP]:
        try:
            comments[p["id"]] = rc.top_comments(p["subreddit"], p["id"])
        except Exception:
            pass
    return posts, comments


def main():
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check-subs", "digest"])
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--send", action="store_true")
    args = ap.parse_args()

    if args.cmd == "check-subs":
        from reddit_client import RedditClient
        rc = RedditClient()
        for s in config.SUBREDDITS:
            try:
                d = rc.about(s)
                print(f"OK   r/{s}: {d.get('subscribers')} subscribers")
            except Exception as e:
                print(f"FAIL r/{s}: {e}")
        return

    if args.demo:
        import demo_data
        posts, comments = demo_data.posts(), {}
    else:
        posts, comments = fetch_live()
    if not posts:
        raise SystemExit("no posts fetched")
    a = analyze.analyze(posts, time.time())
    day = dt.date.today().strftime("%Y-%m-%d")
    html_body = report.render(a, day, comments)
    os.makedirs("out", exist_ok=True)
    path = f"out/digest_{dt.date.today():%y%m%d}.html"
    open(path, "w").write(html_body)
    print(f"wrote {path} ({a['n_posts']} posts)")
    if args.send:
        import mailer
        to = mailer.recipients()
        mailer.send(f"[H&C] Reddit trend digest {day}", html_body, report.render_text(a, day), to)
        print(f"sent to {len(to)} recipients")


if __name__ == "__main__":
    main()
