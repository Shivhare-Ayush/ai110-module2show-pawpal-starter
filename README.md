# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

Recent scheduler improvements include:

- Sorting tasks by `HH:MM` time so plans are consistently ordered.
- Filtering tasks by completion status and pet name.
- Recurring task rollover: when a `daily` or `weekly` task is completed, a new pending task is auto-created for the next due date (`+1 day` or `+7 days`).
- Lightweight conflict detection that returns warning messages when multiple tasks are scheduled for the same exact time.

## Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

Current tests cover:

- Basic task and pet behavior (completion status and task creation).
- Sorting correctness for out-of-order tasks.
- Recurrence logic for daily task rollover after completion.
- Conflict detection for duplicate scheduled times.
- Edge cases such as a pet owner with no tasks.

Confidence Level: ★★★★☆ (4/5)
