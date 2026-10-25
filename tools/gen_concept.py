"""Generate concept art with the OpenAI Images API.

Usage: python tools/gen_concept.py prompts.json out_dir [--quality high] [--model gpt-image-2.5-sunburst]
prompts.json: {"name": {"prompt": "...", "size": "1536x1024"}, ...}
Reads OPENAI_API_KEY from the environment or the repo's .env.
"""
import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_key():
    key = os.environ.get("OPENAI_API_KEY")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENAI_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("OPENAI_API_KEY not set")
    return key


def generate(key, model, quality, name, spec, out_dir):
    body = json.dumps({
        "model": model,
        "prompt": spec["prompt"],
        "size": spec.get("size", "1536x1024"),
        "quality": quality,
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        return f"{name}: HTTP {e.code} {e.read().decode()[:500]}"
    path = out_dir / f"{name}.png"
    path.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    return f"{name}: {path} usage={data.get('usage')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompts")
    ap.add_argument("out_dir")
    ap.add_argument("--quality", default="high")
    ap.add_argument("--model", default="gpt-image-2.5-sunburst")
    args = ap.parse_args()

    key = load_key()
    prompts = json.loads(pathlib.Path(args.prompts).read_text(encoding="utf-8"))
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(generate, key, args.model, args.quality, n, s, out_dir) for n, s in prompts.items()]
        for f in futures:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
