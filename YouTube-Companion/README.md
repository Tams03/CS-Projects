# YouTube Companion

A solo Python project I expanded for my Python Data Analysis course. The public Streamlit app uses the YouTube Data API to look up and compare channels and suggest a related channel using search results.

## What the demo shows

- Channel lookup by handle, ID, channel URL or exact channel name.
- Subscriber count, cumulative views and video count where supplied by YouTube.
- Views per subscriber, calculated as cumulative views divided by the current subscriber count. The ratio is unavailable when the subscriber count is hidden or zero.
- A category and upload cadence estimate from up to 50 recent uploads, plus a related-channel suggestion based on keyword search.

The public version uses Python, Streamlit and Google’s Python API client. The original coursework notebook is private.

[Streamlit source](./Demo_Page/streamlit_app.py) · [Python backend](./Demo_Page/backend.py)

## Run the Streamlit demo locally

From the repository root, install the dependencies and start the app:

```sh
python -m pip install streamlit google-api-python-client
python -m streamlit run YouTube-Companion/Demo_Page/streamlit_app.py
```

Before starting the app, set `YOUTUBE_API_KEY` in your environment or create
`.streamlit/secrets.toml` at the repository root with a top-level entry:

```toml
YOUTUBE_API_KEY = "YOUR_YOUTUBE_DATA_API_KEY"
```

For Streamlit Community Cloud, add the same top-level entry in the app’s
Secrets settings before deploying. Keep real keys out of the repository.
