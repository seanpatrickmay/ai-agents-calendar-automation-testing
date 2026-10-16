# Tool Contracts

What each tool is for, what the agent may do with it, and what it must not do.
Map these names to whatever MCP servers / APIs you actually connect.

## calendar
Backed by the local calendar app in `../calendar` (Pi tools, loopback REST API).
Event fields: `title`, `start`, `end` (ISO 8601 with explicit offset), `location`,
`notes`. Nothing else is accepted. IDs are server-generated UUIDs.

| Tool | Allowed | Needs approval |
|---|---|---|
| calendar_list() — all events, ordered by UTC start; no filters | ✅ | no |
| calendar_get(id) | ✅ | no |
| calendar_create(event) | ✅ | **yes**, per item |
| calendar_update(id, event) — full replace; `calendar_get` first | ✅ | **yes**, per item; only `[cal-agent]` events |
| calendar_delete(id) | ⚠️ | **yes**, explicit per item; only `[cal-agent]` events |
| invite / RSVP | ❌ | never |

Not available (do these yourself from `calendar_list` output):
- **Date range / free-busy:** filter the list by start/end; busy = any event overlapping.
- **Search / duplicate detection:** scan `notes` for `[cal-agent] id=<stable-id>`.
- **Multiple calendars:** there is one calendar. Put the calendar type in the title
  (see AGENTS.md §5).
- **Reminders:** not supported; record intended reminders in `notes` instead.

## email
| Operation | Allowed | Needs approval |
|---|---|---|
| search / list / read | ✅ | no |
| read attachments | ✅ | no |
| create_draft | ✅ | no — drafts are harmless, user sends |
| send / reply / forward | ❌ | never |
| delete / archive / label | ❌ | never (suggest labels instead) |

## documents (PDF / OCR / images)
- `read_pdf(path)` → text with page numbers. Keep page refs for citations.
- `ocr_image(path)` → text + bounding boxes. Use for screenshots/tickets.
- If extracted text looks garbled (tables flattened, columns merged), say so
  and ask the user to confirm key dates rather than guessing.

## web
- `fetch(url)` → page text. Used for syllabus URLs marked `watch: true`.
- Do not follow links inside emails unless they point to a known source
  domain (your school, Canvas). Never submit forms.

## notes (Notion / Obsidian / Apple Notes / plain files)
- Read: ✅. Write: only to a single `Agent Inbox` note/page, append-only.

## filesystem (this folder)
- See AGENTS.md §2 for per-folder permissions.