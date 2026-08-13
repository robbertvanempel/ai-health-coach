# Private Workspace Schema

The workspace is the user's durable second brain. It must be separate from the public skill repository.

## Canonical structure

```text
ai-health-coach-data/
├── AGENTS.md
├── onboarding/status.md
├── profile/health-profile.md
├── goals/active-goals.md
├── journal/index.md
├── journal/YYYY-MM-DD - Short Title.md
├── data/checkins.csv
├── data/metrics.csv
├── data/activities.csv
├── data/nutrition.csv
├── data/imports/
├── knowledge/index.md
├── knowledge/inbox/
├── knowledge/library/
├── plans/current-plan.md
├── reviews/
├── templates/
└── audit/log.md
```

## Read/write rules

- Treat `knowledge/inbox/` and `data/imports/` as immutable raw input.
- Put derived summaries in `knowledge/library/` or `reviews/`.
- Keep `profile/health-profile.md` limited to durable, confirmed context.
- Keep `goals/active-goals.md` current; move superseded goals into a dated review rather than silently deleting history.
- Keep `plans/current-plan.md` as the current agreed plan, with start date and review date.
- Append audit events; do not duplicate sensitive content in the audit log.
- Use ISO dates (`YYYY-MM-DD`) and include timezone for timestamps where timing matters.
- Preserve supplied units. Add normalized values only in separate columns.
- Use stable relative links so the workspace remains portable.

## CSV rules

Use UTF-8, comma delimiters, a single header row, ISO timestamps, and one observation per row. Quote free text. Never silently rewrite the source export.

- `checkins.csv`: daily subjective context such as sleep, energy, stress, soreness, pain, and notes.
- `metrics.csv`: weight, circumference, heart rate, blood pressure, steps, wearable estimates, or other scalar observations.
- `activities.csv`: workouts, sports, mobility, walks, and sessions.
- `nutrition.csv`: optional meal or pattern observations. Calorie and macro fields may be blank.

If a device exports richer data, preserve the original under `data/imports/` and create a device-specific normalized file only when useful.

## Journal format

```markdown
# Short Title

- Date: YYYY-MM-DD
- Status: active|closed

## Transcript

### User

Original text

### Coach

Response text

## Reflection

Grounded synthesis with uncertainty.

## Action points

- One small action.
```

Append later turns to the same active entry until the user ends it or changes task.

## Durable memory test

Before updating the profile, ask:

1. Is it explicitly provided or confirmed?
2. Is it likely to matter in future coaching?
3. Is it more durable than a one-day state?
4. Is storage authorized?
5. Can it be stored with less detail?

If any answer is no, leave it in the dated log or do not store it.

## Version-control safety

The starter workspace ignores all data-bearing paths by default. Do not weaken those ignore rules casually. If a user wants synchronization, recommend a private, access-controlled and appropriately encrypted mechanism; never push the workspace to the public skill repository.
