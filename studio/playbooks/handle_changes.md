# Playbook: Handling changes

Sources change: syllabi are "subject to change", instructors announce new
deadlines, flights get rescheduled.

## Detecting
- `watch: true` sources: re-fetch, normalize (strip whitespace/nav), hash,
  compare to `content_hash`. If different, diff the extracted *items*, not
  the raw text.
- Emails that mention an existing event (same course + similar title, or
  references a date you scheduled).
- User says "that moved" or edits an agent event directly in the calendar
  (detect by comparing calendar state with what you created).

## Responding
1. For each affected `[cal-agent]` event, propose an **update** showing
   old → new and the source of the change.
2. Move linked work blocks too (deadline moved earlier → blocks move earlier;
   later → offer to keep or spread out).
3. Newly filled cells (e.g., a reading got posted) → update the
   placeholder block's title and re-estimate.
4. Conflicting sources (syllabus says Nov 2, Canvas email says Nov 4) →
   **don't pick**. Ask, citing both. Most recent official announcement is
   the suggested default.
5. If the user moved an agent event manually, treat that as a correction:
   log it, don't move it back.
6. Update `content_hash` only after the user approves the changes.
