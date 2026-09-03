# Revision Planner

A desktop revision and study planning application built in Python with Tkinter, created as an OCR A Level Computer Science NEA project.

## About

Revision Planner helps students plan, track and reflect on their revision. It was built to address a common problem: students often misjudge how long a task will actually take, leading to missed deadlines, last-minute cramming, and unnecessary stress.

The system combines task scheduling, a study timer with target-time comparison, confidence-based progress tracking, and time-analysis statistics into a single, accessible tool. It was designed around research and feedback from three real stakeholders with different revision needs — an A Level student, a GCSE student, and someone revising for a single, close-deadline exam.

## Features

- **Task management** — add, edit, delete, sort and filter tasks by subject, deadline or duration
- **Study timer** — track actual time spent on a task against an estimated target
- **Confidence rating** — rate understanding of each topic (1–5) to surface weaker subjects
- **Deadline reminders** — configurable popup warnings ahead of upcoming deadlines
- **Statistics dashboard** — bar and pie charts of study time and task completion, built with matplotlib
- **Progress reports** — written, subject-by-subject feedback generated from stored study data
- **Accessibility settings** — light, dark and high-contrast themes, adjustable font size
- **Multi-user support** — separate logins, tasks, sessions and settings per user

## Screenshots

*(add screenshots here once available)*

## Tech stack

| Component | Technology |
|-----------|------------|
| Language  |Python 3.10+|
|    GUI    |   Tkinter  |
|Data storage|   JSON    |
|   Charts  | matplotlib (`FigureCanvasTkAgg`) |

## Project structure

\`\`\`
revision_planner/
├── main.py              # Entry point
├── auth.py              # Login / account creation
├── tasks.py             # Task management
├── timer.py             # Study timer and session recording
├── statistics.py        # Statistics and progress report calculations
├── settings.py          # User settings and theming
├── data/
│   └── users.json       # Local data storage
└── README.md
\`\`\`

## Getting started

### Requirements

- Python 3.10 or higher
- \`matplotlib\`

\`\`\`bash
pip install matplotlib
\`\`\`

### Running the program

\`\`\`bash
python main.py
\`\`\`

## Data model

Data is structured around four main classes — \`User\`, \`Task\`, \`StudySession\` and \`Settings\` — with a \`Progress\` structure storing calculated weekly statistics.

- Each \`User\` can create many \`Task\`s, but each \`Task\` belongs to one \`User\`
- Each \`Task\` can have many \`StudySession\`s linked to it
- Each \`User\` has exactly one \`Settings\` record

## Status

This project is in active development as part of an OCR A Level Computer Science NEA (Non-Exam Assessment) and is not yet a complete, released application.

## License

Not currently licensed for reuse. All rights reserved while this project is under assessment.