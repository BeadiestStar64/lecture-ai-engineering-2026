"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import time
from typing import Iterator

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai.chats import Chat
from google.genai.types import GenerateContentResponse, GenerateContentResponseUsageMetadata

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat: Chat, question: str):
    response: Iterator[GenerateContentResponse] = chat.send_message_stream(question)

    for message in response:
        metadata: GenerateContentResponseUsageMetadata | None = message.usage_metadata
        output: str | None = message.text

        if output is None or metadata is None:
            return output, None, None

        # https://ai.google.dev/gemini-api/docs/generate-content/tokens?hl=ja
        input_token: int | None = metadata.prompt_token_count
        output_token: int | None = metadata.candidates_token_count

        yield output, input_token, output_token


def main() -> None:
    load_dotenv(override=True)

    # マルチターン会話での初期化
    client = genai.Client(api_key=get_api_key())
    chat: Chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")

    while True:
        prompt = input("プロンプトを入力(終了はqを入力) > ")
        if not prompt:
            prompt = DEFAULT_QUESTION

        # 終了判定
        if prompt == "q":
            break

        try:
            print(f"\n{'-' * 50}\n")
            print(f"[回答]")

            in_count: int | None = None
            out_count: int = 0
            start_time: float = time.perf_counter()
            # Time to First Token
            ttft: float | None = None
            # Token per second
            tps: float | None = None
            # First Token Time
            ftt: float | None = None

            for message in ask(chat, prompt):
                response, in_c, out_c = message
                print(response, end="")
                in_count = in_c
                out_count = out_c if out_c is not None else 0

                if ftt is None:
                    ftt = time.perf_counter()
                    ttft = ftt - start_time

            end_time = time.perf_counter()

            if ftt is not None:
                tps = out_count / (end_time - ftt)
            
            print(f"\n{'-' * 50}\n")
            print(f"[Input Token] {in_count} Token")
            print(f"[Output Token] {out_count} Token")
            print(f"[TTFT] {ttft} sec")
            print(f"[TPS] {tps} token/sec")
            print(f"\n{'-' * 50}\n")
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))  # type: ignore
            raise SystemExit(1)


if __name__ == "__main__":
    main()
