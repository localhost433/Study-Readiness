# Study Readiness Logger

## Overview

When I was preparing for my Linear Algebra final (working through Axler’s LADR problems), I noticed how often I’d lose motivation or struggle to stay productive. Initially, I sketched out a simple “choose‑your‑own‑adventure” survey in an Excel sheet—each answer would direct you to a new question until you arrived at a score indicating your readiness. But after reading some psychology papers, I realized pure self‑reporting isn’t objective enough. 

So I evolved the idea into a hybrid system:

1. Quantified Tasks
   — Timed arithmetic drills, reaction‑time tests, digit‑span challenges, and category‑fluency exercises  
2. Self‑Evaluation Prompts
   — Karolinska Sleepiness Scale, fluid intake, minutes since last caffeine  
3. Weighted Scoring
   — Each task and prompt carries a configurable weight; scores are aggregated into a single readiness index  
4. Contextual Feedback
   — Based on your subscores and the time of day, the tool offers suggestions  

This is still a work in progress. Some of the tests are too easy to cheat, and some are less meaningful than I have thought. Once data accumulates, I hope to uncover meaningful patterns in study readiness and productivity.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run full daily check:
```bash
python3 -m study_readiness.cli --run
```

Evaluate the latest entry:
```bash
python3 -m study_readiness.cli --evaluate
```

Plot metrics over time:
```bash
python3 -m study_readiness.cli --plot
```