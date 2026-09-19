# cgjunghelpdesk.github.io

The Jung Helpdesk app's website.

- `/` — the landing page. **When the app is live, paste its App Store link into
  the first line of `site.js`** (`APP_STORE_URL`); every "Coming soon" button on
  every page becomes "Download on the App Store".
- `/e/NNN` (optionally `?t=seconds`) — one page per episode. Opens the episode
  in the app via universal links; everyone else sees the episode and the app
  pitch. Regenerate after a new episode: `python3 tools/build_episodes.py`
- `/privacy.html`, `/support.html` — linked from the App Store listing.
- `/.well-known/apple-app-site-association` tells iOS the app may claim the
  `/e/` links. Don't rename or move it.
- `img/` — web-sized copies of the store screenshots (source:
  `guided-listening/docs/appstore/`).
