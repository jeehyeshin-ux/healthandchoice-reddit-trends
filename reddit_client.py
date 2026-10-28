"""Minimal Reddit client using the official OAuth API (app-only). No scraping, no UA spoofing."""
import base64
import os
import time

import requests

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API = "https://oauth.reddit.com"


class RedditClient:
    def __init__(self):
        self.cid = os.environ.get("REDDIT_CLIENT_ID")
        self.secret = os.environ.get("REDDIT_CLIENT_SECRET")
        if not (self.cid and self.secret):
            raise SystemExit("REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not set (see README, .env).")
        self.ua = os.environ.get("REDDIT_USER_AGENT", "script:healthandchoice-trends:0.1 (by /u/your_username)")
        self._token, self._exp = None, 0

    def _auth(self):
        if self._token and time.time() < self._exp - 60:
            return
        basic = base64.b64encode(f"{self.cid}:{self.secret}".encode()).decode()
        r = requests.post(TOKEN_URL, data={"grant_type": "client_credentials"},
                          headers={"Authorization": f"Basic {basic}", "User-Agent": self.ua}, timeout=30)
        r.raise_for_status()
        j = r.json()
        self._token, self._exp = j["access_token"], time.time() + j.get("expires_in", 3600)

    def get(self, path, **params):
        self._auth()
        for attempt in range(3):
            r = requests.get(API + path, params=params, timeout=30,
                             headers={"Authorization": f"bearer {self._token}", "User-Agent": self.ua})
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 5)))
                continue
            r.raise_for_status()
            time.sleep(0.7)  # stay well under the rate limit
            return r.json()
        raise RuntimeError(f"rate limited: {path}")

    def about(self, sub):
        return self.get(f"/r/{sub}/about", raw_json=1)["data"]

    def listing(self, sub, kind, limit=100, **extra):
        data = self.get(f"/r/{sub}/{kind}", limit=limit, raw_json=1, **extra)["data"]["children"]
        return [c["data"] for c in data]

    def top_comments(self, sub, post_id, n=3):
        j = self.get(f"/r/{sub}/comments/{post_id}", limit=30, sort="top", raw_json=1)
        kids = j[1]["data"]["children"]
        out = [c["data"] for c in kids if c["kind"] == "t1"]
        return sorted(out, key=lambda c: c.get("score", 0), reverse=True)[:n]
