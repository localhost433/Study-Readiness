import time, random, os
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    _COLORAMA = True
except ImportError:
    _COLORAMA = False

import time
import random
import operator

def arithmetic_test(n=5):
    """
    Presents n three‐operand integer problems whose answers
    always lie in [–200, 800]. Times the session and counts errors.
    Returns (time_taken_seconds, error_count).
    """
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul
    }
    symbols = list(ops.keys())

    errors = 0
    start = time.perf_counter()

    for _ in range(n):
        # keep sampling until we get an answer in the desired range
        while True:
            a = random.randint(0, 200)
            b = random.randint(0, 200)
            c = random.randint(0, 200)
            op1 = random.choice(symbols)
            op2 = random.choice(symbols)

            # left‐associative evaluation
            intermediate = ops[op1](a, b)
            answer = ops[op2](intermediate, c)

            if -200 <= answer <= 800:
                expr = f"{a} {op1} {b} {op2} {c}"
                break

        # prompt the user
        try:
            resp = int(input(f"{expr} = ? "))
            if resp != answer:
                errors += 1
        except ValueError:
            errors += 1

    end = time.perf_counter()
    return end - start, errors

def reaction_time_test(trials=5):
    """
    Simple reaction time: waits random interval, then prompts Enter.
    Returns average reaction time in seconds.
    """
    import sys
    # platform‐specific import for input‐flush
    try:
        import termios
    except ImportError:
        termios = None
    msvcrt = None
    if sys.platform.startswith('win'):
        import msvcrt

    times = []
    print("\nReaction time test: Press Enter as soon as you see 'GO!'\n")
    i = 0
    while i < trials:
        wait = random.uniform(1.0, 3.0)
        time.sleep(wait)
        print("GO!", end=' ', flush=True)

        # --- flush any prior keypresses ---
        if termios:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        elif msvcrt:
            while msvcrt.kbhit():
                msvcrt.getch()

        # --- measure reaction ---
        t0 = time.perf_counter()
        input()
        rt = time.perf_counter() - t0

        # --- reject false starts ---
        if rt < 0.07:
            print("  False start (too quick). Let’s try again.")
            continue

        times.append(rt)
        print(f"  Trial {i+1}: {rt:.3f}s")
        i += 1

    avg = sum(times) / len(times)
    print(f"Average reaction time: {avg:.3f}s\n")
    return avg

def stroop_test(trials=5):
    """
    Show color words in mismatched ink; user must type ink color.
    If colorama is installed, the word is printed in that color.
    Returns proportion correct.
    """
    print("\nStroop Test: Type the INK color, not the word\n")
    colors = ['red','green','blue','yellow','pink','white']
    correct = 0

    for i in range(trials):
        word = random.choice(colors)
        ink  = random.choice([c for c in colors if c!=word])
        display = word.upper()
        if _COLORAMA and hasattr(Fore, ink.upper()):
            display = getattr(Fore, ink.upper()) + display + Style.RESET_ALL

        print(display)
        ans = input("Ink color: ").strip().lower()
        if ans == ink:
            correct += 1

    score = correct / trials
    print(f"Stroop score: {score:.2f}\n")
    return round(score,2)

def two_back_test(seq_len=10, display_time=1.0):
    """
    2‑back test: show letter briefly, clear, then ask if it matches
    the one two steps earlier. Returns proportion correct.
    """
    print("\n2‑Back Test: Press Y if letter matches 2 back, N otherwise\n")
    letters = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(seq_len)]
    correct, total = 0, 0

    for i, let in enumerate(letters):
        print(f"  {let}", end='', flush=True)
        time.sleep(display_time)
        # clear the line
        print("\r" + " " * (len(let)+2) + "\r", end='', flush=True)

        if i >= 2:
            ans = input("Match 2‑back? (Y/N): ").strip().lower()
            match = (letters[i] == letters[i-2])
            if (ans=='y' and match) or (ans=='n' and not match):
                correct += 1
            total += 1

    score = correct / total if total else 0
    print(f"\n2‑Back score: {score:.2f}\n")
    return round(score,2)

def word_pair_test(view_time=5):
    """
    User sees word pairs, then must recall second word.
    Returns percent correct.
    """
    print("\nWord Pair Test: Remember the second word in each pair")
    pool = [
        "sol", "mela", "nubes", "potio", "penna", "herba", "piscis", "luna", "stella", "flumen",
        "arbor", "lapis", "mons", "oceanus", "flos", "avis", "caelum", "silva", "pluvia",
        "ventus", "ignis", "terra", "aqua", "lux", "umbra", "folium", "ramus", "semen",
        "fructus", "arena", "unda", "concha", "aura", "tempestas", "nix", "glacies", "nebula", "ros",
        "pratum", "vallis", "collis", "rivus", "spelunca", "rupes", "insula", "litus", "desertum",
        "vulcanus", "glaciarium", "stagnum", "laguna", "obex", "canyon", "planities", "savanna", "silva", "tundra",
        "lucus", "pomarium", "vinea", "cortex", "petalum", "radix", "cataracta", "arcus", "occasus", "aurora",
        "gutta", "mare", "fons", "semita", "rus", "vicus", "urbs", "via", "pons", "turris",
        "castrum", "palatium", "hortus", "parcus", "fons", "statua", "forum", "mercatus", "theatrum", "bibliotheca",
        "museum", "ecclesia", "cathedralis", "monasterium", "abbatia", "arx", "molendinum", "pharus", "portus", "navis",
        "templum", "arena", "circus", "amphitheatrum", "thermae", "aquaeductus", "domus", "insulae", "villa", "atrium",
        "taberna", "caupona", "popina", "macellum", "pistrinum", "officina", "horreum", "granarium", "carcer", "curia",
        "basilica", "rostrum", "comitium", "templum", "porticus", "arcus triumphalis", "columna", "obeliscus", "statio", "via sacra",
        "campus", "horti", "palus", "lacus", "stagnum", "fluctus", "scopulus", "promontorium", "sinus", "fretum"
    ]
    pairs = []
    while len(pairs) < 4:
        a, b = random.sample(pool, 2)
        pair = (a, b)
        if pair not in pairs:
            pairs.append(pair)

    for a, b in pairs:
        print(f"  {a} – {b}")
    time.sleep(view_time)

    # clear screen
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')

    print("Recall time:\n")
    correct = 0
    for a, b in pairs:
        ans = input(f"{a} = ? ").strip().lower()
        if ans == b.lower():
            correct += 1

    score = correct / len(pairs)
    print(f"\nWord Pair score: {score:.2f}\n")
    return round(score,2)