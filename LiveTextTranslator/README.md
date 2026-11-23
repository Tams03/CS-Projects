# LiveTextTranslator

A team project for multilingual text chat. The original Python prototype pairs clients over FastAPI WebSockets and translates messages using NLLB-200.

## My contribution

I worked on the FastAPI/WebSocket backend, integrated NLLB-200, built the Streamlit interaction demo and tested different languages and longer text inputs.

## Public demo

The [Streamlit source](./Demo_Page/streamlit_app.py) illustrates the interaction using Google Translate through `deep-translator`. It runs separately from the original NLLB/WebSocket backend, whose source is private.

```sh
python -m pip install streamlit deep-translator
python -m streamlit run LiveTextTranslator/Demo_Page/streamlit_app.py
```

The demo requires network access to translate. The prototype does not establish production latency or translation accuracy.

[Course presentation](./Deep_Learning.pdf)
