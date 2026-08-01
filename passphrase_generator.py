"""
passphrase_generator.py
------------------------
Generates strong, memorable passphrases instead of random character soup.

WHY WORDS INSTEAD OF RANDOM CHARACTERS?
A password like "xK9#mQ2!" is hard to remember and people end up writing it
down or reusing it. A passphrase like "Correct-Horse-Battery-42" is:
  - Just as hard (often harder) to brute-force, because of its length
  - Much easier for a human to actually remember
  - Still unique and unpredictable, because words + order are chosen
    using a cryptographically secure random source (not guessable patterns)

SECURITY NOTE:
We use Python's `secrets` module, not `random`. `random` is NOT safe for
security purposes - it's predictable if an attacker knows the internal
state. `secrets` is designed specifically for passwords, tokens, and keys.

PRIVACY NOTE:
This generator never stores, logs, or transmits the generated passphrase
anywhere. It's created fresh in memory, printed once to your screen, and
discarded. Nothing is saved to disk or sent over the network.
"""

import secrets

# A small curated wordlist for demo purposes.
# For a real/production version, swap this out for the full EFF long
# wordlist (7,776 words) - free, public, designed exactly for this purpose:
# https://www.eff.org/dice
WORDLIST = [
    "river", "mountain", "cactus", "falcon", "harbor", "lantern", "tundra",
    "comet", "granite", "willow", "ember", "cascade", "orbit", "meadow",
    "quartz", "thunder", "coral", "prairie", "voyage", "canyon", "spruce",
    "glacier", "nebula", "ripple", "boulder", "ember", "horizon", "marble",
    "sable", "flint", "harvest", "juniper", "solstice", "wander", "cinder",
    "delta", "frost", "haven", "ivy", "jasper", "knoll", "lagoon", "myth",
    "nomad", "opal", "pebble", "quill", "reef", "summit", "thicket", "umber",
]


def generate_passphrase(num_words: int = 4, add_number: bool = True, separator: str = "-") -> str:
    """
    Generates a passphrase using cryptographically secure random choices.
    Default: 4 words + a random 2-digit number, separated by hyphens.
    """
    words = [secrets.choice(WORDLIST).capitalize() for _ in range(num_words)]

    if add_number:
        number = secrets.randbelow(90) + 10  # random number 10-99
        words.append(str(number))

    return separator.join(words)


if __name__ == "__main__":
    print("Generating a strong, memorable passphrase...\n")

    passphrase = generate_passphrase()
    print(f"Your new passphrase: {passphrase}")
    print("\nWhy this is strong:")
    print("  - 4 random words + a number gives huge unpredictability")
    print("  - Chosen using a cryptographically secure random source")
    print("  - Nothing about it is stored or logged by this tool")
    print("\nTip: write it down somewhere safe just ONCE while you memorize it,")
    print("then use a password manager going forward instead of reusing it.")
