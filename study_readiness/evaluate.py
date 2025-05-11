import os
import pandas as pd

LOG_FILE = "study_readiness_log.csv"

def evaluate_logs(log_file=LOG_FILE):
    if not os.path.exists(log_file):
        print("No log to evaluate.")
        return

    df = pd.read_csv(log_file, parse_dates=['timestamp'])
    latest, history = df.iloc[-1], df.iloc[:-1]
    if history.empty:
        print("Not enough history to compute a readiness score.")
        return

    def normalize(val, avg, direction='lower'):
        """Normalize so that higher is always better (0–1)."""
        if avg == 0:
            return 0.5
        ratio = val / avg
        if direction == 'lower':
            score = 2 - ratio
        else:
            score = ratio
        return max(0, min(1, score))

    # Cognitive Processing subscores
    s_arith_time = normalize(latest['T_arith'], history['T_arith'].mean(), 'lower')
    s_arith_err  = normalize(latest['E_arith'], history['E_arith'].mean(), 'lower')
    s_rt         = normalize(latest['RT'],    history['RT'].mean(),    'lower')

    # Memory & Executive subscores
    s_stroop     = normalize(latest['stroop'],     history['stroop'].mean(),     'higher')
    s_two_back   = normalize(latest['two_back'],   history['two_back'].mean(),   'higher')
    s_word_pair  = normalize(latest['word_pair'],  history['word_pair'].mean(),  'higher')

    # Well‑Being & Regulation subscores
    s_kss        = max(0, min(1, 1 - (latest['KSS'] - 1) / 8))
    s_sleep_q    = latest['sleep_q'] / 5.0
    s_stress     = max(0, min(1, 1 - (latest['stress'] - 1) / 9))
    s_caffeine   = max(0, min(1, 1 - min(latest['caffeine_min'], 360) / 360))

    # Apply overall weights
    readiness_score = (
        0.12 * s_arith_time   +
        0.10 * s_arith_err    +
        0.13 * s_rt           +
        0.10 * s_stroop       +
        0.115 * s_two_back     +
        0.115 * s_word_pair    +
        0.06 * s_kss          +
        0.10 * s_sleep_q      +
        0.09 * s_stress       +
        0.07 * s_caffeine
    )

    # Build advice broken down by domain
    adv_cog = []
    adv_mem = []
    adv_well = []

    hour = pd.to_datetime(latest['timestamp']).hour

    # Time-based flags
    is_morning = 6 <= hour < 11
    is_midday = 11 <= hour < 14
    is_afternoon = 14 <= hour < 18
    is_evening = 18 <= hour < 22
    is_late = hour >= 22 or hour < 6

    # --- Cognitive Advice ---
    if latest['T_arith'] > history['T_arith'].mean() * 1.2:
        if is_morning:
            adv_cog.append("Arithmetic is slow this morning—wait 30–60 minutes for natural alertness to rise.")
        elif is_afternoon:
            adv_cog.append("Afternoon slowdown in arithmetic—try a short break or hydration.")
        elif is_evening or is_late:
            adv_cog.append("Evening arithmetic decline—consider saving logical tasks for tomorrow.")
        else:
            adv_cog.append("Arithmetic slower than usual—consider a brief break.")
    elif latest['E_arith'] > history['E_arith'].mean() + 1:
        adv_cog.append("Arithmetic errors are elevated—warm up with simpler calculations.")
    if latest['RT'] > history['RT'].mean() * 1.2:
        if is_morning:
            adv_cog.append("Reaction time is low this morning—use light, caffeine, or movement to boost alertness.")
        elif is_afternoon:
            adv_cog.append("Afternoon drop in reaction time—consider stepping outside briefly.")
        elif is_late:
            adv_cog.append("Reaction time is poor at night—limit demanding decisions or work.")
        else:
            adv_cog.append("Reaction time is slower—reduce distractions before continuing.")
    if not adv_cog:
        adv_cog.append("Cognitive processing is on par with your historical performance.")

    # --- Memory & Executive ---
    if latest['stroop'] < 0.6 or latest['two_back'] < 0.6:
        if is_morning:
            adv_mem.append("Early cognitive control is weak—start your day with planning or light admin.")
        elif is_evening or is_late:
            adv_mem.append("Reduced executive function at this hour—do creative or passive review tasks instead.")
    if latest['stroop'] < 0.6:
        adv_mem.append("Stroop performance is low—focus exercises may help attention control.")
    if latest['two_back'] < 0.6:
        adv_mem.append("2‑Back score suggests working memory strain—short rest could help.")
    if latest['word_pair'] < 0.6:
        adv_mem.append("Word‑pair recall is weaker—try a quick verbal memory drill.")
    if not adv_mem:
        adv_mem.append("Memory and executive function are consistent with your norms.")

    # --- Well-Being & Regulation ---
    if latest['KSS'] >= 7:
        if is_morning:
            adv_well.append("High morning sleepiness—light exposure or brief movement might help.")
        elif is_afternoon:
            adv_well.append("Afternoon drowsiness—consider a short walk or stretch.")
        elif is_evening:
            adv_well.append("Evening fatigue—prepare for restful sleep soon.")
        else:
            adv_well.append("You’re very sleepy this morning—delay demanding work until fully alert.")
    if latest['sleep_q'] <= 2:
        adv_well.append("Sleep quality was poor—review sleep hygiene routines tonight.")
    if latest['stress'] >= 8:
        adv_well.append("Stress is high—try 5 minutes of paced breathing or mindfulness.")
    elif latest['stress'] >= 5:
        adv_well.append("Stress is moderate—monitor workload and take short pauses.")
    if latest['caffeine_min'] > 240:
        if is_morning:
            adv_well.append("No caffeine yet this morning—consider a small dose if needed.")
        else:
            adv_well.append("No caffeine for several hours—plan intake to avoid dips.")
    elif latest['caffeine_min'] < 30:
        if is_afternoon or is_evening:
            adv_well.append("Caffeine intake was recent and it’s already afternoon—watch for sleep disruption.")
        else:
            adv_well.append("Very recent caffeine—be aware of potential overstimulation.")
    if not adv_well:
        adv_well.append("Physiological state is within normal ranges.")


    # Print results
    print("\nStudy Readiness Evaluation")
    print(f"Overall Score: {readiness_score * 100:.1f}/100\n")

    print("Cognitive Processing:")
    print(f"  Subscore: {(0.12 * s_arith_time + 0.10 * s_arith_err + 0.13 * s_rt) / 0.35 * 100:.1f}/100")
    for msg in adv_cog:
        print(f"  - {msg}")

    print("\nMemory & Executive Function:")
    print(f"  Subscore: {(0.10 * s_stroop + 0.115 * s_two_back + 0.115 * s_word_pair) / 0.33 * 100:.1f}/100")
    for msg in adv_mem:
        print(f"  - {msg}")

    print("\nWell-Being & Regulation:")
    print(f"  Subscore: {(0.06 * s_kss + 0.10 * s_sleep_q + 0.09 * s_stress + 0.07 * s_caffeine) / 0.32 * 100:.1f}/100")
    for msg in adv_well:
        print(f"  - {msg}")
