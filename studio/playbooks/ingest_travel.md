# Playbook: Ingest travel documents (tickets, screenshots, confirmations)

## 1. Extract (OCR for screenshots)

For each leg capture: carrier + number, origin airport (IATA), destination
airport, departure date + local time, arrival date + local time, confirmation
code, seat, terminal/gate if shown, passenger name.

- **Read times as local to each airport.** Look up each airport's IANA
  timezone. Arrival can be on a different date than departure.
- If OCR is unclear on any time, date, or code, mark `low_ocr_quality` and
  quote what you read: "I read 'DEP 7:15' — is that AM?"
- Check the passenger name matches the user. If not, ask whose trip it is
  (it might be someone they're picking up).

## 2. Propose events

For a flight, propose a linked set:
1. **Leave for airport** — departure − (airport_arrival_* + home_to_airport_min)
   from preferences. Use international buffer if origin/destination countries differ.
2. **Flight** — departure → arrival, with both local times in the title or
   description: `✈ UA 123 BOS→SFO (dep 7:15a ET / arr 10:45a PT)`.
   Put confirmation code in description (not title).
3. **Post-arrival buffer** — arrival → arrival + post_arrival_buffer_min.
4. Return leg, same pattern.

## 3. Check impact

- **Conflicts:** Does the trip overlap classes, deadlines, meetings, work
  blocks? List each one. For classes, suggest "Email instructor about
  absence" as a task. For deadlines during travel, suggest moving work
  blocks earlier.
- **Timezone shift:** If the user will be in another timezone, note that
  deadlines (e.g., "Monday noon ET") will occur at a different local time.
- **Check-in reminder:** most airlines open check-in 24h before — add a
  reminder task.

## 4. Never
- Check in, change seats, or contact the airline.
- Put the confirmation code or passenger details in an event visible to
  shared calendars.
