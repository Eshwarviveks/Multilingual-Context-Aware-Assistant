"""
╔══════════════════════════════════════════════════════╗
║         Context AI Assistant  ·  Main Pipeline       ║
║         NLP · Intent Detection · Voice Response      ║
╚══════════════════════════════════════════════════════╝
"""

import sys
from input_module    import get_text_input
from preprocess      import preprocess_text
from pos_module      import pos_tagging
from wsd_module      import get_word_sense
from intent_module   import detect_intent
from response_module import generate_response, speak_response


# ─────────────────────────────────────────
# TERMINAL STYLING HELPERS
# ─────────────────────────────────────────

class C:
    """ANSI colour codes for terminal output."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    AMBER  = "\033[33m"
    CYAN   = "\033[36m"
    GREEN  = "\033[32m"
    RED    = "\033[31m"
    WHITE  = "\033[97m"
    BLUE   = "\033[34m"


def header(title: str) -> None:
    """Print a styled section header."""
    width = 52
    print(f"\n{C.AMBER}{'─' * width}{C.RESET}")
    print(f"{C.AMBER}{C.BOLD}  {title}{C.RESET}")
    print(f"{C.AMBER}{'─' * width}{C.RESET}")


def banner() -> None:
    """Print the application banner."""
    print(f"""
{C.AMBER}{C.BOLD}
  ╔══════════════════════════════════════════════════╗
  ║        Context AI Assistant  v1.0                ║
  ║        NLP · WSD · Intent · Voice                ║
  ╚══════════════════════════════════════════════════╝
{C.RESET}{C.DIM}  Context-Aware Virtual Assistant — CLI Mode{C.RESET}
""")


def divider() -> None:
    print(f"{C.DIM}  {'·' * 48}{C.RESET}")


# ─────────────────────────────────────────
# PIPELINE STAGES
# ─────────────────────────────────────────

def stage_preprocess(text: str) -> list[str]:
    header("01 · Preprocessing")
    tokens = preprocess_text(text)
    print(f"  {C.DIM}Tokens :{C.RESET} ", end="")
    print("  ".join(f"{C.CYAN}{t}{C.RESET}" for t in tokens))
    return tokens


def stage_pos(text: str) -> list[tuple[str, str]]:
    header("02 · Part-of-Speech Tagging")
    pos_tags = pos_tagging(text)
    for word, pos in pos_tags:
        tag_color = C.GREEN if pos.startswith("N") else C.BLUE if pos.startswith("V") else C.WHITE
        print(f"  {C.WHITE}{word:<18}{C.RESET}{tag_color}{pos}{C.RESET}")
    return pos_tags


def stage_wsd(text: str, tokens: list[str]) -> None:
    header("03 · Word Sense Disambiguation")
    found = False
    for word in tokens:
        meaning = get_word_sense(text, word)
        if meaning:
            found = True
            print(f"  {C.AMBER}{C.BOLD}{word}{C.RESET}")
            print(f"  {C.DIM}↳{C.RESET} {meaning}")
            divider()
    if not found:
        print(f"  {C.DIM}No ambiguous words detected.{C.RESET}")


def stage_intent(text: str) -> str:
    header("04 · Intent Detection")
    intent = detect_intent(text)
    icons = {
        "Booking": "📅",
        "Weather":  "🌤",
        "Banking":  "🏦",
        "General":  "💬",
    }
    icon = icons.get(intent, "💬")
    print(f"  Detected Intent :  {C.GREEN}{C.BOLD}{icon}  {intent}{C.RESET}")
    return intent


def stage_response(intent: str) -> str:
    header("05 · Assistant Response")
    response = generate_response(intent)
    print(f"  {C.AMBER}Assistant :{C.RESET} {C.WHITE}{response}{C.RESET}")
    return response


# ─────────────────────────────────────────
# MAIN ENTRYPOINT
# ─────────────────────────────────────────

def main() -> None:
    banner()

    # ── Input ──
    text = get_text_input()
    if not text or not text.strip():
        print(f"\n  {C.RED}✗  No input provided. Exiting.{C.RESET}\n")
        sys.exit(1)

    print(f"\n  {C.DIM}Input received :{C.RESET} {C.WHITE}\"{text}\"{C.RESET}")

    # ── Pipeline ──
    tokens   = stage_preprocess(text)
    _        = stage_pos(text)
    stage_wsd(text, tokens)
    intent   = stage_intent(text)
    response = stage_response(intent)

    # ── Voice Output ──
    header("06 · Voice Output")
    print(f"  {C.DIM}Speaking response via TTS...{C.RESET}")
    speak_response(response)
    print(f"  {C.GREEN}✓  Done{C.RESET}")

    # ── Footer ──
    print(f"\n{C.AMBER}{'═' * 52}{C.RESET}\n")


if __name__ == "__main__":
    main()