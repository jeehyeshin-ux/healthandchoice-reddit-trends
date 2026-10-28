"""Render the analysis as HTML (email) and plain text."""
import datetime as dt
import html

BASE = "https://www.reddit.com"


def _link(p):
    return BASE + p["permalink"]


def _e(s):
    return html.escape(str(s))


def render(a, day, comments=None):
    comments = comments or {}
    h = [f"<div style='font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:680px;margin:auto;color:#1a1a1a'>",
         f"<h2 style='margin-bottom:4px'>HEALTH &amp; CHOICE Reddit Trend Digest</h2>",
         f"<div style='color:#666'>{day} / {a['n_posts']} posts scanned, {a['n_recent']} in last 48h / "
         + ", ".join(f"r/{_e(s)} {n}" for s, n in a["by_sub"].most_common()) + "</div>"]

    h.append("<h3>1. Rising keywords (last 48h vs earlier)</h3><ul>")
    for t, c, ratio, old in a["rising"][:10]:
        tag = "NEW" if old == 0 else f"x{ratio}"
        h.append(f"<li><b>{_e(t)}</b> {tag} ({c} recent posts)</li>")
    h.append("</ul><h3>2. Hot-issue keywords (weighted by upvotes and comments)</h3><ul>")
    for t, w, d in a["hot"][:10]:
        h.append(f"<li><b>{_e(t)}</b> in {d} posts, weight {w}</li>")
    h.append("</ul><h3>3. Topic map</h3><ul>")
    for t, n in a["topics"].most_common():
        h.append(f"<li><b>{_e(t)}</b>: {n} posts")
        h.append("<ul>" + "".join(
            f"<li><a href='{_link(p)}'>{_e(p['title'][:100])}</a> (r/{_e(p['subreddit'])}, "
            f"{p['score']} pts, {p['num_comments']} comments)</li>" for p in a["topic_top"][t]) + "</ul></li>")
    h.append("</ul><h3>4. Most-discussed posts</h3><ol>")
    for p in a["most_commented"]:
        h.append(f"<li><a href='{_link(p)}'>{_e(p['title'][:120])}</a><br>"
                 f"<span style='color:#666'>r/{_e(p['subreddit'])} / {p['num_comments']} comments / {p['score']} pts</span>")
        for c in comments.get(p["id"], [])[:2]:
            h.append(f"<div style='margin:4px 0 0 12px;color:#444;font-size:13px'>&ldquo;{_e(c['body'][:200])}&rdquo;"
                     f" ({c['score']})</div>")
        h.append("</li>")
    h.append("</ol><hr><div style='color:#888;font-size:12px'>Source: Reddit official API. "
             "Community opinion, not verified fact. Reply STOP to unsubscribe.</div></div>")
    return "\n".join(h)


def render_text(a, day):
    out = [f"HEALTH & CHOICE Reddit Trend Digest {day}", ""]
    out.append("RISING: " + ", ".join(t for t, *_ in a["rising"][:10]))
    out.append("HOT: " + ", ".join(t for t, *_ in a["hot"][:10]))
    out.append("")
    for p in a["most_commented"]:
        out.append(f"- {p['title'][:100]} ({p['num_comments']} comments)\n  {_link(p)}")
    return "\n".join(out)
