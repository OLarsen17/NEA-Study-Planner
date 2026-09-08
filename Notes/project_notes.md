## Study Timer redesign — planning notes (post-basic-implementation)

After testing the first working version of the Study Timer, identified the following issues and improvements needed:

1. Add a genuine Start button — timer currently auto-starts the moment a task is selected, which doesn't match the original GUI design.
2. Add a Pause button, temporarily halting the timer without ending the sitting.
3. Add Reset functionality — split into two options if the user is resuming a previously paused task:
   - "Reset this sitting" — clears only the current session's elapsed time, keeping any previously saved progress from earlier visits intact.
   - "Reset all" — clears all saved progress on the task entirely, including previous sittings.
4. Add a "Continue later" option — ends the current sitting, saves accumulated elapsed time onto the task itself, keeps the task incomplete, and returns to task selection.
5. When resuming a task with saved elapsed time, the timer should start from that saved point rather than zero.
6. Only create a StudySession when the user chooses "Stop and finish" — at this point, the session records the *total* accumulated time (previous saved elapsed time + this sitting), the task is marked complete, and elapsed time resets to zero.
7. Session finished screen should display minutes and seconds, not just whole minutes.
8. Add a manual complete/incomplete toggle checkbox to the Task list screen, available in both the Incomplete and Complete filtered views.
9. Deliberately scoping out automatic study-time estimation (mentioned in original analysis) — decided this is disproportionate in complexity relative to this project's scope and timeframe. Will be documented as a limitation rather than implemented.

Plan: tackle points 1–7 as one connected rebuild of the timer screens, since they interact closely, committing after each individual piece is working and tested. Points 8 and 9 to be handled separately afterwards.


## Features still to build (as of Study Timer completion)

- Confidence rating update on session finish — the "Session finished" screen was designed to include an updated confidence rating (1–5) alongside the Yes/Not yet buttons, but this was missed during implementation. To be fixed now.
- Manual complete/incomplete toggle checkbox on the Task list screen (both filter views) — allows a task to be flipped either way regardless of how it reached its current state, without needing to go through the Study Timer. Next to be built.
- Settings screen — GUI form for theme, font size, high contrast, reminders on/off, and reminder_days. The Settings class already exists in the data layer but has no corresponding screen yet.
- Reminder popup logic (1.1 Check Upcoming Deadlines, 1.2 Send Reminder) — checking each task's deadline against the user's saved reminder_days setting and showing a popup where appropriate. Depends on the Settings screen existing first, since there needs to be a real, user-set reminder_days value to check against.
- Statistics dashboard (6.3) — charts showing study time per subject and task completion.
- Progress report screen (6.4) — written, subject-by-subject feedback generated from stored study and completion data.


## Design decision: subjects remain tied to existing tasks only

Noticed that deleting all tasks in a subject removes that subject from the Add/Edit Task dropdown, since subjects are derived dynamically from the user's current task list rather than being stored independently.

Considered storing subjects as their own persistent list on the User object, so a subject would remain available even with zero current tasks. Decided against this, since it would require building a separate mechanism to remove subjects a user no longer studies, otherwise the list would grow indefinitely with abandoned subjects over time. The added complexity was judged disproportionate to the fairly minor inconvenience of retyping a subject name in the rare case all of its tasks are deleted at once.

Decision: subjects remain derived directly from existing tasks, as originally implemented.


## Ideas and convenience features to consider later

- Statistics comparing actual time studied (from StudySession data) against each task's estimated duration — directly supports the core project aim of helping students recognise when they misjudge task length. Higher priority, belongs naturally in the Statistics module.
- Bind the Enter key to submit on Login and Password screens, so pressing Enter has the same effect as clicking Continue.
- Auto-login toggle in Settings — flagged for further thought before building, since it raises a genuine security/privacy trade-off (bypassing password entry) that may conflict with the system being designed for multiple people sharing one device.
- Statistics showing which tasks saw an improved confidence rating versus which stayed the same or dropped, using the initial_confidence_rating vs confidence_rating fields already built for the Study Timer.

## Statistics screen structure — extending the original design

While building the Statistics dashboard, decided to split statistics-related content across three distinct screens rather than one dense page, extending the original two-screen plan (Statistics dashboard + Progress report) with a third destination:

- **Statistics dashboard** — the "quick glance" screen from the original mockup: summary numbers (total time, tasks completed, average confidence), a bar chart of time per subject, and a pie chart of task completion.
- **More statistics/graphs** (new) — a dedicated screen for secondary, more detailed visual comparisons that don't belong on the quick-glance dashboard but are still chart-based rather than written: time studied vs. estimated duration per task, and confidence improvement across studied tasks. These were originally noted as convenience ideas rather than part of the initial screen design.
- **Progress report** — unchanged from the original design; stays as the written, subject-by-subject feedback screen, no charts.

Reasoning: keeping the dashboard limited to two charts avoids needing a scroller or cramped layout, matching the original mockup's intent as a quick, glanceable screen. The new "More statistics/graphs" screen gives the deeper visual comparisons a proper home without overloading the dashboard or forcing them awkwardly into the written Progress report.

### Known issues and gaps identified while testing the first version

- Bar chart uses whole-minute floor division (seconds // 60) to convert session time to minutes, which rounds any session under 60 seconds down to 0, making bars for short test sessions invisible. To be fixed using round(seconds / 60, 1) for one-decimal precision.
- Average confidence rating was part of the original Statistics dashboard mockup but was missed when the screen was first built — only total time and completed count were included. To be added.
- Pie chart (task completion split) was part of the original mockup but not yet built — dashboard currently only shows the bar chart. To be added.

Plan: fix all three of the above together as one combined pass, then take a fresh, accurate set of screenshots of the completed dashboard.

## Statistics and Progress report need time-period filtering

While building the Progress report screen, realised the current implementation (and the Statistics dashboard) shows all-time totals only, not filtered by time period. This doesn't match the original design: the Progress report mockup specifically showed "Week of 12 – 18 Feb 2027" in its header, and the 6.1 Calculate study time algorithm was originally designed to support daily, weekly and overall periods as a parameter, none of which is currently implemented.

Plan:
- Add a date-range filter to calculate_statistics(), so it can be called with a specific week (or no filter, for all-time) rather than always summing every session ever recorded.
- Weeks defined as calendar weeks, Monday to Sunday, not rolling 7-day windows.
- Add previous/next week navigation to both the Statistics dashboard and Progress report screens, so the user can look back at any previously studied week.
- Add a monthly view as a dropdown option alongside weekly, letting the user switch between weekly and monthly totals.
- Apply consistently across both screens, so the same selected time period is reflected in both the charts and the written feedback.

This is a genuinely bigger piece of work than previous Statistics additions, since it affects how sessions are filtered before any existing calculation runs, and needs new navigation UI on two screens. To be tackled as its own deliberate, focused piece of work rather than added incrementally on top of the current all-time version.


## Statistics week navigation — issues found during testing

Testing week navigation on the Statistics dashboard revealed several issues:

1. Task completion count, average confidence, and the pie chart are not filtered by the selected week, only total_seconds and subject_totals (session-based) are. This means navigating to a past week with no activity still shows the same completion/confidence figures as the current week, which is misleading. Needs fixing so subject_completion, completed_count, and average_confidence are calculated from week-filtered tasks/sessions, not all-time.

2. The bar chart breaks visually (inverted/negative axis, overlapping "0m 0s" labels) when a selected week has zero recorded study time, since max_height becomes 0 and set_ylim(top=0) produces a nonsensical range. Needs a dedicated "No study data this week" message instead of attempting to draw an empty chart, matching the existing pattern used when a user has no tasks at all.

3. No upper bound on "Next week" navigation, allowing navigation into future weeks that cannot possibly contain data.

4. No lower bound on "Previous week" navigation, allowing navigation before the user's account was even created. Requires storing an account creation date on User, which doesn't currently exist.

5. No way to quickly return to the current week after navigating away, requires manually clicking "Previous/Next week" repeatedly.

Navigation buttons themselves (moving between weeks, updating the displayed date range) work correctly. These are calculation and boundary issues layered on top of otherwise working navigation.
