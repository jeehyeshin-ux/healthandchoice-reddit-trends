"""Subreddit list and keyword taxonomy for the Health & Choice trend digest."""

# Candidate subreddits (from web search; run `python run.py check-subs` to verify they exist).
SUBREDDITS = {
    "SeoulPlasticSurgery": "Korean plastic surgery, core",
    "KoreaSeoulBeauty": "Seoul clinics/skin/surgery",
    "KoreaTravelBeauty": "beauty during Korea trips",
    "MedTourismAesthetic": "aesthetic medical tourism, small",
    "medicaltourism": "general medical tourism",
    "PlasticSurgery": "global plastic surgery, big",
    "koreanbeauty": "K-beauty and derm trends",
    "koreatravel": "visitor questions, visa/tax refund",
    "AsianBeauty": "skincare, derm procedures",
}

LOOKBACK_DAYS = 7          # window for top posts
RECENT_HOURS = 48          # "rising" = frequent in last 48h vs older posts
POSTS_PER_LISTING = 100
FETCH_COMMENTS_FOR_TOP = 5  # per subreddit, top comment threads to read

# Topic buckets: label -> trigger terms (lowercase). Used to tag posts and count themes.
TOPICS = {
    "시술/수술": ["rhinoplasty", "blepharoplasty", "double eyelid", "eyelid", "jaw", "v-line", "facelift",
               "breast", "liposuction", "fat graft", "botox", "filler", "thread lift", "laser",
               "skin booster", "salmon dna", "rejuran", "ulthera", "shurink", "thermage", "juvelook",
               "lip", "nose job", "orthognathic"],
    "병원/코디네이터": ["clinic", "hospital", "coordinator", "agency", "broker", "consultation", "surgeon",
                  "doctor", "gangnam", "apgujeong", "sinsa", "id hospital", "banobagi", "grand", "view"],
    "가격/비용": ["price", "cost", "quote", "expensive", "cheap", "budget", "deposit", "tax refund", "vat"],
    "안전/부작용": ["complication", "revision", "infection", "botched", "regret", "safe", "risk",
               "recovery", "swelling", "bruising", "anesthesia", "scam", "illegal", "lawsuit"],
    "여행/행정": ["visa", "k-eta", "flight", "hotel", "airbnb", "recovery stay", "interpreter",
              "translator", "insurance", "passport", "stay", "itinerary"],
    "국가 비교": ["thailand", "turkey", "japan", "china", "mexico", "colombia", "vietnam", "taiwan"],
}

STOPWORDS = set("""a about above after again all also am an and any are as at be because been before being below
between both but by can could did do does doing down during each few for from further had has have having he her
here hers him his how i if in into is it its just me more most my no nor not of off on once only or other our out
over own same she should so some such than that the their them then there these they this those through to too
under until up very was we were what when where which while who whom why will with would you your yours
like get got im ive dont cant one two really much even still know think want need anyone anything thing things
post posts reddit please thanks thank help question questions looking going go back day days week weeks month months
year years time first im also would new good best make made see seen ask asking people someone""".split())
