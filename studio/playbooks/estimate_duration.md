# Playbook: Estimate durations and place work blocks

## 1. Pick an estimate
1. Exact match in `memory/estimates.yaml` → use `current_min`.
2. Close match → use it, scaled (e.g., 2 papers vs 1 → add `per_paper_min`).
3. No match → estimate from the description using the heuristics below,
   **show your reasoning in one line**, and add a new entry with
   `source: guessed`.

Heuristics (starting points, not truths):
- Reading a research paper carefully: 45–90 min. A textbook chapter: 60–120.
- Short written response (≤ 500 words): 30–60 min after reading.
- Slides for a 5–10 min team talk: 4–8 h total across the team, plus 1 h rehearsal.
- Problem set: 3–6 h. Exam prep: 8–12 h, spread over a week.
- Report (5–10 pages): 12–20 h, spread over 2+ weeks.
- Anything "with your team": add a 30–60 min coordination block.

## 2. Place the blocks
- Work backward from `due − buffer_before_deadline_hours`.
- Split into `max_block_minutes` chunks; space multi-block tasks over
  multiple days.
- Only in free time inside `working_hours`.
- Respect `max_work_hours_per_day` across *all* courses.
- Prefer slots listed in `work_blocks.prefer`.
- If there's no room, say so and show the crunch: "Week of Nov 9 needs 14 h
  of work; you have 9 free h. Options: start test cases the week before."

## 3. Recalibrate
When the user says how long something actually took ("that took 3 hours"),
append to that type's `log` and recompute `current_min` per the rule at the
top of `estimates.yaml`. Mention the change in your next proposal:
"Reading responses now estimated at 2h (was 2.5h) based on your last 3."
