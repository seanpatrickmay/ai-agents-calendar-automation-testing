# Playbook: Ingest a syllabus or course calendar

Works for PDFs, web pages, and screenshots. Syllabi are messy: the same
deadline might be in a table, a prose paragraph, and a policy page.

## Steps

1. **Extract with locators.** Keep page numbers (PDF), section headings
   (web), or region descriptions (image). You'll cite these.
   - PDF: try text extraction first; if tables come out scrambled or the PDF
     is scanned, OCR the page and say `low_ocr_quality` on affected items.
   - Web: also check linked pages that commonly hold dates (Policies,
     Schedule, Assignments). Add them to `sources.yaml → related`.

2. **Anchor the calendar.**
   - Term start/end, holidays, no-class days.
   - Year: verify that stated day-of-week matches the date. If "Mon Sep 14"
     appears, confirm Sep 14 is a Monday in the candidate year.
   - Class meeting day/time/location. If the course calendar gives the day
     but not the time, check related pages, then the user profile, then ask.

3. **Find recurring obligations in the prose**, not just the tables.
   Look for phrases like "each week", "every Monday", "by noon", "after
   each…". Turn each into a recurring deadline with an RRULE, and *exclude*
   no-class days unless the text says otherwise. Ask if it's ambiguous
   whether a recurring item applies on holiday or presentation weeks.

4. **Find one-off items** (tables, "checkpoints", "due dates"). For each:
   - Explicit date + time → `confirmed`.
   - Date + vague time ("midnight", "before class", "end of day") → `inferred`,
     apply AGENTS.md §8 rules, record the assumption.
   - "TBD", "week of", "scheduled with the instructor", "announced in class"
     → `pending` task. For "scheduled with X", the task is "Contact X to
     schedule", due ~5 business days before the window opens.

5. **Distinguish who it applies to.** "Only the presenter needs to…",
   "one submission per team", "optional", "encouraged but not required".
   - Applies to everyone → propose.
   - Applies conditionally → ask (e.g., "Are you presenting a spotlight?").
   - Optional → list under Ignored with reason, unless profile says otherwise.

6. **Skip the past.** Anything before today → Ignored ("already past").
   Exception: if a past deadline looks like it may not have been done
   (no email confirmation, no user note), flag it once, gently.

7. **Note unfilled cells.** Empty reading cells for future weeks mean
   "not posted yet", not "no reading". Propose the deadline and a
   placeholder work block, flag `pending`, and set `watch: true` so you
   re-check.

8. **Generate work blocks** for each deliverable via `estimate_duration.md`.

9. **Register the source** in `memory/sources.yaml` with a content hash.

## Common traps
- Two courses with the same weekday: check for conflicts between them.
- "Due Monday" in a course that meets Monday: is it before or after class?
- Rubric/grading tables contain percentages that look like dates (10/15).
- A screenshot of a syllabus may be cropped — say what's not visible.
