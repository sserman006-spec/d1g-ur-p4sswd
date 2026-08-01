"""
digurpasswd.py
---------
D1G UR P4SSWD - Account Security Checker CLI

Combines three checks into one tool:
  1. Breach check       - has this password leaked before? (HIBP k-anonymity)
  2. Strength scoring   - how hard would this be to guess/crack?
  3. Passphrase generator - need a new one? get a secure, memorable one

Pure Python standard library - no external dependencies, no pip install.
Colors are plain ANSI escape codes - work natively on Linux/Mac terminals
and modern Windows terminals. No library needed.

Nothing entered here is stored, logged, or saved to disk. Everything
lives only in memory for the duration of a single run.
"""

import os
import random
import re
import shutil
import sys
import threading
import time

from password_checker import check_password_pwned
from strength_checker import score_password_strength
from passphrase_generator import generate_passphrase


class C:
    """Plain ANSI color/style codes - no external library required."""
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"
    GREY = "\033[90m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


WIDTH = 58


ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def visible_width(text):
    """
    Real on-screen width of a string, ignoring ANSI color codes
    (invisible but counted by len()). Emoji are deliberately kept out
    of bordered/padded content elsewhere in this file, since terminal
    emoji width isn't consistent across terminals (VS Code, Kali's
    default terminal, etc. disagree) and can't be reliably solved
    without an external library.
    """
    return len(ANSI_RE.sub("", text))


def box_top():
    print(center_line(C.CYAN + "┌" + "─" * (WIDTH - 2) + "┐" + C.RESET))


def box_bottom():
    print(center_line(C.CYAN + "└" + "─" * (WIDTH - 2) + "┘" + C.RESET))


def box_line(text=""):
    pad = WIDTH - 4 - visible_width(text)
    print(center_line(C.CYAN + "│ " + C.RESET + text + " " * max(pad, 0) + C.CYAN + " │" + C.RESET))


def clear_screen():
    print("\033[H\033[J", end="")


def _type_out(text, color=C.WHITE, delay=0.02):
    for ch in text:
        sys.stdout.write(color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def anim_decrypt():
    """Scrambled characters gradually resolve into the tool name."""
    target = "D1G UR P4SSWD"
    charset = "!@#$%^&*<>?/\\|=+-01"
    clear_screen()
    print(C.GREY + "  booting security console...\n" + C.RESET)
    for step in range(10):
        guess = "".join(
            ch if random.random() < step / 9 or ch == " " else random.choice(charset)
            for ch in target
        )
        sys.stdout.write("\r  " + C.MAGENTA + C.BOLD + guess + C.RESET)
        sys.stdout.flush()
        time.sleep(0.09)
    print("\r  " + C.MAGENTA + C.BOLD + target + C.RESET + "\n")
    time.sleep(0.2)


def anim_radar():
    """A small spinning radar sweep, like scanning for threats."""
    clear_screen()
    frames = ["|", "/", "-", "\\"]
    labels = ["checking known breach sources", "loading strength heuristics", "priming secure RNG"]
    print(C.CYAN + C.BOLD + "  D1G UR P4SSWD" + C.RESET + C.GREY + "  — initializing\n" + C.RESET)
    for label in labels:
        for i in range(8):
            sys.stdout.write(f"\r  {C.CYAN}{frames[i % 4]}{C.RESET}  {label}...")
            sys.stdout.flush()
            time.sleep(0.06)
        print(f"\r  {C.GREEN}✓{C.RESET}  {label}... done" + " " * 10)
    time.sleep(0.15)


def anim_matrix_rain():
    """A brief burst of falling-character 'matrix' noise before the banner."""
    clear_screen()
    chars = "01"
    width = 50
    print(C.GREEN + "  establishing secure session...\n" + C.RESET)
    for _ in range(10):
        line = "".join(random.choice(chars) if random.random() > 0.5 else " " for _ in range(width))
        print(C.GREEN + C.DIM + line + C.RESET)
        time.sleep(0.05)
    time.sleep(0.15)


def anim_lock():
    """A small padlock 'unlocking' animation."""
    clear_screen()
    locked = r"""
        _____
       /     \
      | () () |
       \  ^  /
      [ █████ ]   LOCKED
"""
    unlocked = r"""
        _____
       /     \
      |       |
       \  ^  /
      [ █████ ]   UNLOCKED
"""
    print(C.RED + locked + C.RESET)
    time.sleep(0.5)
    sys.stdout.write("\033[6A")  # move cursor up to overwrite
    print(C.GREEN + unlocked + C.RESET)
    print(C.GREY + "  session ready.\n" + C.RESET)
    time.sleep(0.3)


def anim_firewall():
    """Simulated firewall rule sweep."""
    clear_screen()
    print(C.BLUE + C.BOLD + "  D1G UR P4SSWD" + C.RESET + C.GREY + "  — firewall check\n" + C.RESET)
    rules = ["inbound: default deny", "outbound: HTTPS allowed", "port 443: open", "port 22: filtered"]
    for rule in rules:
        sys.stdout.write(C.GREY + "  scanning: " + rule + C.RESET)
        sys.stdout.flush()
        time.sleep(0.18)
        print("\r  " + C.GREEN + "✓ " + rule + " " * 10 + C.RESET)
    time.sleep(0.15)


def anim_fingerprint():
    """ASCII fingerprint scan effect."""
    clear_screen()
    print(C.CYAN + "  identity verification...\n" + C.RESET)
    art = ["  ╭─────╮", "  │ ┊┊┊ │", "  │ ┊┊┊ │", "  │ ┊┊┊ │", "  ╰─────╯"]
    for i in range(len(art) + 1):
        clear_screen()
        print(C.CYAN + "  identity verification...\n" + C.RESET)
        for line in art[:i]:
            print(C.GREEN + line + C.RESET)
        time.sleep(0.12)
    print(C.GREEN + C.BOLD + "\n  scan complete\n" + C.RESET)
    time.sleep(0.2)


def anim_handshake():
    """A simulated TLS-style handshake sequence."""
    clear_screen()
    print(C.MAGENTA + C.BOLD + "  D1G UR P4SSWD" + C.RESET + C.GREY + "  — secure handshake\n" + C.RESET)
    steps = ["CLIENT HELLO", "SERVER HELLO", "KEY EXCHANGE", "SESSION ESTABLISHED"]
    for step in steps:
        sys.stdout.write(C.GREY + f"  {step}..." + C.RESET)
        sys.stdout.flush()
        time.sleep(0.2)
        print("\r  " + C.GREEN + f"{step} ✓" + " " * 10 + C.RESET)
    time.sleep(0.15)


def anim_shield():
    """A shield icon that 'raises' line by line."""
    clear_screen()
    lines = [
        "     .---.",
        "    / ~~~ \\",
        "   | SECURE |",
        "    \\ ~~~ /",
        "     '---'",
    ]
    print(C.YELLOW + "  raising defenses...\n" + C.RESET)
    for line in lines:
        print(C.YELLOW + line + C.RESET)
        time.sleep(0.1)
    time.sleep(0.2)


def anim_boot_sequence():
    """A fake system boot log, hacker-movie style."""
    clear_screen()
    logs = [
        "loading kernel modules",
        "mounting encrypted volume",
        "verifying checksums",
        "starting D1G UR P4SSWD daemon",
        "all systems nominal",
    ]
    for log in logs:
        print(C.GREEN + "[ OK ] " + C.WHITE + log + C.RESET)
        time.sleep(0.15)
    time.sleep(0.2)


def play_intro_animation():
    animations = [
        anim_decrypt, anim_radar, anim_matrix_rain, anim_lock,
        anim_firewall, anim_fingerprint, anim_handshake, anim_shield,
        anim_boot_sequence,
    ]
    random.choice(animations)()
    clear_screen()


class Spinner:
    """
    Reusable live spinner that runs in a background thread while a
    slower operation (like the breach-check network call) completes.
    Used so the CLI never just 'hangs' silently during the HIBP lookup.
    """
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)

    def _spin(self):
        i = 0
        while not self._stop_event.is_set():
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r  {C.MAGENTA}{frame}{C.RESET}  {self.message}...")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self):
        self._thread.start()

    def stop(self, final_message=None):
        self._stop_event.set()
        self._thread.join()
        clear_line = "\r" + " " * (len(self.message) + 12) + "\r"
        sys.stdout.write(clear_line)
        if final_message:
            print(final_message)


RAINBOW = [C.RED, C.YELLOW, C.GREEN, C.CYAN, C.BLUE, C.MAGENTA]


def _gradient(text):
    return "".join(RAINBOW[i % len(RAINBOW)] + ch for i, ch in enumerate(text)) + C.RESET


def term_width():
    """Actual terminal column count, with a sane fallback when not a real tty."""
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def center_line(text):
    """
    Centers a line against the REAL terminal width (not against its own
    box width - centering something within its own footprint does
    nothing, since padding would always be zero). Uses visible_width so
    invisible ANSI color codes never throw off the math.
    """
    vw = visible_width(text)
    left = max((term_width() - vw) // 2, 0)
    return " " * left + text


def print_banner():
    title = "D1G UR P4SSWD"
    spaced = "  ".join(title)
    border = "═" * (len(spaced) + 4)

    print()
    print(center_line(C.MAGENTA + C.BOLD + f"╔{border}╗" + C.RESET))
    print(center_line(
        C.MAGENTA + C.BOLD + "║  " + C.RESET + _gradient(spaced) + C.MAGENTA + C.BOLD + "  ║" + C.RESET
    ))
    print(center_line(C.MAGENTA + C.BOLD + f"╚{border}╝" + C.RESET))
    print(center_line(C.CYAN + C.BOLD + "Account Security Checker" + C.RESET))

    # Feature badge row - hooks the user with what makes this tool trustworthy
    badges = [
        (C.GREEN, "🐍 PURE PYTHON"),
        (C.YELLOW, "🔓 ZERO DEPENDENCIES"),
        (C.CYAN, "🔒 PRIVACY-FIRST"),
    ]
    badge_line = "   ".join(f"{color}{C.BOLD}[{label}]{C.RESET}" for color, label in badges)
    print(center_line(badge_line))

    # Stylish author credit badge
    print()
    author_text = " Author: SERMAN AKA N4MR3S "
    author_border = "─" * len(author_text)
    print(center_line(C.GREY + "╭" + author_border + "╮" + C.RESET))
    print(center_line(C.GREY + "│" + C.RESET + C.MAGENTA + C.BOLD + author_text + C.RESET + C.GREY + "│" + C.RESET))
    print(center_line(C.GREY + "╰" + author_border + "╯" + C.RESET))
    print()


    LINKEDIN_POST_URL = "https://www.linkedin.com/in/serman-muthu-sundaresh-b-9412b8329"  
    print(center_line(C.YELLOW + "⚠ Passwords entered here are NEVER stored, logged, or transmitted." + C.RESET))
    print(center_line(C.GREY + f"  Details: {LINKEDIN_POST_URL}" + C.RESET))
    print()


def print_section(title, color=C.YELLOW):
    print()
    box_top()
    box_line(color + C.BOLD + title + C.RESET)
    box_bottom()


def bar(score, width=24):
    filled = int(width * score / 100)
    color = C.GREEN if score >= 80 else C.YELLOW if score >= 50 else C.RED
    return color + "█" * filled + C.GREY + "░" * (width - filled) + C.RESET


def run_scan():
    print()
    password = input(C.CYAN + "▶ Enter a password to scan: " + C.RESET)
    if not password:
        print(C.RED + "No password entered." + C.RESET)
        return

    print_section("BREACH CHECK", C.MAGENTA)
    spinner = Spinner("querying breach database")
    spinner.start()
    try:
        count = check_password_pwned(password)
        spinner.stop()
        if count > 0:
            print(C.RED + C.BOLD + f"  ✗ BREACH FOUND" + C.RESET + C.RED + f" — seen {count:,} times in known breach dumps" + C.RESET)
            print(C.RED + "    Do not use this password anywhere." + C.RESET)
        else:
            print(C.GREEN + C.BOLD + "  ✓ CLEAN" + C.RESET + C.GREEN + " — not found in known breach data" + C.RESET)
    except Exception as exc:
        spinner.stop()
        print(C.YELLOW + f"  ⚠ Breach check unavailable ({exc})" + C.RESET)

    print_section("STRENGTH SCORE", C.BLUE)
    result = score_password_strength(password)
    rating_color = {
        "Strong": C.GREEN,
        "Moderate": C.YELLOW,
        "Weak": C.YELLOW,
        "Very Weak": C.RED,
    }.get(result["rating"], C.WHITE)

    print(f"  {bar(result['score'])}  " + rating_color + C.BOLD + f"{result['rating']}" + C.RESET + C.GREY + f" ({result['score']}/100)" + C.RESET)
    print(C.CYAN + f"  ⏱  crack time: " + C.WHITE + result["estimated_crack_time"] + C.RESET)
    print()
    for reason in result["reasons"]:
        print(C.GREY + f"    · {reason}" + C.RESET)


def run_generate():
    print_section("NEW PASSPHRASE", C.GREEN)
    passphrase = generate_passphrase()
    print(C.GREEN + C.BOLD + f"  {passphrase}" + C.RESET)
    print(C.GREY + "  Generated fresh — not stored or logged anywhere." + C.RESET)


def print_menu():
    print()
    box_top()
    box_line(C.BOLD + C.WHITE + "MAIN MENU" + C.RESET)
    box_line(C.CYAN + C.BOLD + "1" + C.RESET + "  ▸ " + C.WHITE + "Scan a password" + C.RESET)
    box_line(C.GREEN + C.BOLD + "2" + C.RESET + "  ▸ " + C.WHITE + "Generate a new passphrase" + C.RESET)
    box_line(C.RED + C.BOLD + "3" + C.RESET + "  ▸ " + C.WHITE + "Exit" + C.RESET)
    box_bottom()


def main():
    play_intro_animation()
    print_banner()
    while True:
        print_menu()
        choice = input(C.MAGENTA + "▶ " + C.RESET).strip()

        if choice == "1":
            run_scan()
        elif choice == "2":
            run_generate()
        elif choice == "3":
            print(C.MAGENTA + "\nD1G UR P4SSWD signing off. Stay safe out there.\n" + C.RESET)
            break
        else:
            print(C.RED + "Invalid choice, pick 1, 2, or 3." + C.RESET)


if __name__ == "__main__":
    main()
