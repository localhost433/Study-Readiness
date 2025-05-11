import csv
import os
from datetime import datetime
import pandas as pd

LOG_FILE = 'study_readiness_log.csv'


def init_log(log_file=LOG_FILE):
    """
    Initialize the log file if it doesn't exist.
    """
    if not os.path.exists(log_file):
        try:
            with open(log_file, 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow([
                    'timestamp', 'T_arith', 'E_arith', 'RT',
                    'stroop', 'two_back', 'word_pair',
                    'KSS', 'caffeine_min', 'sleep_q', 'stress'
                ])
            print(f"Log file initialized: {log_file}")
        except IOError as e:
            print(f"Error initializing log file: {e}")


def log_results(results, log_file=LOG_FILE):
    """
    Log the results to the CSV file.
    """
    init_log(log_file)
    try:
        with open(log_file, 'a', newline='') as f:
            w = csv.writer(f)
            timestamp = datetime.now().isoformat()
            w.writerow([
                timestamp,
                results.get('T_arith', None),
                results.get('E_arith', None),
                results.get('RT', None),
                results.get('stroop', None),
                results.get('two_back', None),
                results.get('word_pair', None),
                results.get('KSS', None),
                results.get('caffeine_min', None),
                results.get('sleep_q', None),
                results.get('stress', None)
            ])
        print(f"Results logged to {log_file}")
    except IOError as e:
        print(f"Error logging results: {e}")


def show_logs(n=5, log_file=LOG_FILE):
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return

    if pd:
        try:
            df = pd.read_csv(log_file)
            print(df.tail(n).to_string(index=False))
        except Exception as e:
            print(f"Error reading log file: {e}")
    else:
        print("Pandas not installed. Cannot display logs.")

def clear_logs(log_file=LOG_FILE):
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
            print(f"Log file cleared: {log_file}")
        except IOError as e:
            print(f"Error clearing log file: {e}")
    else:
        print(f"Log file does not exist: {log_file}")

def parse_caffeine_time(input_str: str) -> int:
    s = input_str.strip().lower()
    if s in {"none", "n/a", "never"}:
        return 36 * 60
    if s.endswith('h'):
        try:
            return int(float(s[:-1]) * 60)
        except ValueError:
            pass
    try:
        return int(s)
    except ValueError:
        print("Invalid input. Use '45', '2h', or 'none'.")
        return parse_caffeine_time(input("Try again: "))

def log_prompts():
    """
    Prompt user for manual inputs:
      - KSS
      - Caffeine (minutes since)
      - Sleep quality
      - Stress level
    """
    try:
        print("\nManual Check-ins:")
        kss = int(input("Karolinska Sleepiness Scale (1=Very alert to 9=Very sleepy): ").strip())
        caffeine_raw = input("When was your last caffeine intake? (e.g., 45, 2h, none): ").strip()
        caffeine_min = parse_caffeine_time(caffeine_raw)
        sleep_q = int(input("How would you rate your sleep quality? (1=Terrible to 5=Excellent): ").strip())
        stress = int(input("Current stress level (1=Relaxed to 10=Very stressed): ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return log_prompts()

    # Clamp values
    kss = max(1, min(kss, 9))
    sleep_q = max(1, min(sleep_q, 5))
    stress = max(1, min(stress, 10))
    caffeine_min = max(0, caffeine_min)

    return kss, caffeine_min, sleep_q, stress
