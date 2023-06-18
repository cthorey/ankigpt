import streamlit as st
import os
import openai
from box import Box

if "OPENAI_API_KEY" not in os.environ:
    raise RuntimeError("You need to provide an OPENAI_API_KEY!")
openai.organization = os.getenv("OPENAI_ORG").strip()
openai.api_key = os.getenv("OPENAI_API_KEY").strip()

with open("/workdir/config.yaml", "r") as f:
    cfg = Box.from_yaml(f)


def generate_cards(
    txt: str,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0.7,
    max_tokens: int = 5000,
):
    with open("/workdir/app/prompt.txt", "r") as f:
        content = f.read().format(INFO=txt)
    messages = [
        {"role": "system", "content": "You are a very HELPFUL assistant."},
        {"role": "user", "content": content},
    ]

    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    flashcards = response["choices"][0]["message"]["content"]
    with open("/workdir/data/flashcards.txt", "w") as f:
        f.write(flashcards)

    return flashcards


st.title("Anki GPT :sunglasses:")

txt = st.text_area(
    "Copy/paste some text",
    "",
    height=cfg.height,
)
if txt:
    with st.spinner("Wait for it..."):
        cards = generate_cards(txt, **cfg.openai)
    st.write("FlashCards :sunglasses:")
    st.write(cards)
