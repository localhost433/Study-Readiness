import argparse
import datetime
import time
from study_readiness.tests import (
    arithmetic_test,
    reaction_time_test,
    stroop_test,
    two_back_test,
    word_pair_test
)
from study_readiness.logger import log_results, log_prompts, show_logs
from study_readiness.evaluate import evaluate_logs
from study_readiness.plot import plot_logs

def main():
    parser = argparse.ArgumentParser('Study Readiness Logger')
    parser.add_argument('--run', action='store_true', help="Run the full cognitive test battery")
    parser.add_argument('--show', type=int, metavar='N', help="Show the last N logged sessions")
    parser.add_argument('--plot', action='store_true', help="Plot logged metrics over time")
    parser.add_argument('--evaluate', action='store_true', help="Evaluate the logged data for readiness score")
    args = parser.parse_args()

    if args.run:
        print("Running full test battery...\n")
        T_arith, E_arith = arithmetic_test()
        print("Arithmetic test completed.\n")
        time.sleep(1)
        RT = reaction_time_test()
        print("Reaction time test completed.\n")
        time.sleep(1)
        stroop = stroop_test()
        print("Stroop test completed.\n")
        time.sleep(1)
        two_back = two_back_test()
        print("Two-back test completed.\n")
        time.sleep(1)
        word_pair = word_pair_test()
        print("Word pair test completed.\n")
        time.sleep(1)
        KSS, caffeine_min, sleep_q, stress = log_prompts()


        results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'T_arith': round(T_arith, 3),
            'E_arith': E_arith,
            'RT': round(RT, 3),
            'stroop': stroop,
            'two_back': two_back,
            'word_pair': word_pair,
            'KSS': KSS,
            'caffeine_min': caffeine_min,
            'sleep_q': sleep_q,
            'stress': stress
        }
        log_results(results)

    elif args.show:
        show_logs(args.show)

    elif args.evaluate:
        evaluate_logs()

    elif args.plot:
        plot_logs()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()