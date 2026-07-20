"""Verify local DeepSeek configuration without exposing secrets.

Run with --live only when a local DEEPSEEK_API_KEY has been configured.
"""

import argparse
import asyncio

from app.core.config import get_settings
from app.llm.errors import LLMError
from app.llm.factory import create_llm_provider
from app.llm.types import LLMMessage, LLMRequest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate local DeepSeek configuration and optionally send one test request."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Send one small request to DeepSeek. This may consume API quota.",
    )
    return parser.parse_args()


async def run_live_check() -> int:
    provider = create_llm_provider()
    response = await provider.generate(
        LLMRequest(
            messages=[
                LLMMessage(
                    role="user",
                    content="Reply with exactly: DeepSeek connection OK",
                )
            ],
            temperature=0,
        )
    )
    print(f"DeepSeek live check succeeded (provider={response.provider}, model={response.model}).")
    return 0


def main() -> int:
    args = parse_args()
    get_settings.cache_clear()
    settings = get_settings()

    if not settings.deepseek_api_key:
        print("DeepSeek API key is not configured. Add DEEPSEEK_API_KEY to the repository-root .env file.")
        return 2

    print(f"DeepSeek configuration found (base URL={settings.deepseek_base_url}, model={settings.deepseek_model}).")
    if not args.live:
        print("Configuration-only check passed. Re-run with --live to send one small API request.")
        return 0

    try:
        return asyncio.run(run_live_check())
    except LLMError as error:
        print(f"DeepSeek live check failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
