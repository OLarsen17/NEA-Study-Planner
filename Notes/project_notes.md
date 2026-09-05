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