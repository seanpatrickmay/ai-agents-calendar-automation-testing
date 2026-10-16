# Decisions Log

Append-only. One entry per user decision. The agent reads this to avoid
repeating rejected proposals and to learn preferences.

## Format
```
- 2026-10-16 | id=abc123ef01 | approved | AGENTS · Reading response due Oct 19
- 2026-10-16 | id=4d5e6f7a8b | edited   | work block moved Sat 10am → Sun 2pm
- 2026-10-16 | id=9c8b7a6d5e | rejected | "don't schedule studio summaries, I finish in class"
```

## Log
(empty)

## Learned preferences
<!-- Agent writes patterns here after 2+ consistent edits, then proposes
     adding them to config/preferences.yaml. -->
(none yet)
