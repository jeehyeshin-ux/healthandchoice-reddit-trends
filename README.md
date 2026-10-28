# Reddit Trend Digest (Health & Choice)

Collects Korea medical tourism / aesthetics posts from Reddit, extracts rising and hot keywords,
lists the most-discussed posts with links, and emails an HTML digest.

## Setup
1. Create a Reddit "script" app at https://www.reddit.com/prefs/apps (free). Copy client id and secret.
2. `cp .env.example .env` and fill in Reddit and SMTP values (Gmail needs an app password).
3. `cp recipients.example.txt recipients.txt` and list the mailing list.
4. `pip install -r requirements.txt`

## Run
- `python run.py check-subs` verify the subreddits in `config.py`
- `python run.py digest --demo` test with synthetic data
- `python run.py digest` live run, writes `out/digest_YYMMDD.html`
- `python run.py digest --send` also emails the list

Weekly schedule: `0 9 * * 1 cd <this dir> && python3 run.py digest --send`

## Notes
- Uses the official API only. Anonymous scraping returns 403.
- Reddit API terms restrict commercial use without approval; check before using output in paid client work.
- Edit `config.py` to change subreddits and topic taxonomy.
