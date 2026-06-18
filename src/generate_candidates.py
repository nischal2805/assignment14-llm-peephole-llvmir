#!/usr/bin/env python3

from pathlib import Path
import argparse
import os
import time

from google import genai


SYSTEM_PROMPT = """
You are an LLVM and MLIR optimization expert.

Your task is to discover a semantically equivalent
peephole optimization.

Rules:

1. Preserve semantics exactly.
2. Only perform local rewrites.
3. Do not invent new functions.
4. Keep the same function signature.
5. Output ONLY the rewritten IR.
6. If no optimization is obvious, return the original IR unchanged.
7. Do not explain anything.
"""


def read_file(path):
    return path.read_text(encoding="utf-8")


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_prompt(ir_text, ir_type):
    return f"""
Type: {ir_type}

Find a valid peephole optimization.

Input IR:

{ir_text}

Output only the optimized IR.
"""


def generate_candidate(client, ir_text, ir_type):
    prompt = build_prompt(ir_text, ir_type)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
    )

    text = response.text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def process_directory(client, case_dir, extension):
    files = sorted(
        f for f in case_dir.glob(f"*{extension}")
        if f".candidate{extension}" not in f.name
    )

    total = len(files)

    for idx, source_file in enumerate(files, start=1):

        candidate_file = source_file.with_name(
            source_file.stem + f".candidate{extension}"
        )

        print(
            f"[{idx}/{total}] "
            f"Generating candidate for {source_file.name}"
        )

        source_text = read_file(source_file)

        try:
            ir_type = "LLVM IR" if extension == ".ll" else "MLIR"

            candidate = generate_candidate(
                client,
                source_text,
                ir_type,
            )

            write_file(candidate_file, candidate)

        except Exception as e:
            print(f"ERROR: {source_file.name}: {e}")

        time.sleep(1)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--llvm-dir",
        default="testcases/llvm_ir"
    )

    parser.add_argument(
        "--mlir-dir",
        default="testcases/mlir"
    )

    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise SystemExit(
            "Please set GEMINI_API_KEY"
        )

    client = genai.Client(api_key=api_key)

    llvm_dir = Path(args.llvm_dir)
    mlir_dir = Path(args.mlir_dir)

    if llvm_dir.exists():
        process_directory(
            client,
            llvm_dir,
            ".ll"
        )

    if mlir_dir.exists():
        process_directory(
            client,
            mlir_dir,
            ".mlir"
        )

    print("\nDone.")


if __name__ == "__main__":
    main()