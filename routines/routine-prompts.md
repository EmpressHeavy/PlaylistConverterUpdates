# Routine prompts (generic, verbatim)

## monthly-settings-check
Schedule: 1st of each month, 10:00 AM {{OWNER_TIME_ZONE}} (cron `0 10 1 * *`).
Prompt:
Run `mem boot`. Send one short summary of this owner's Playlist Converter settings: services they use, default destination, private/public default, memory backup status (repo name, and the last line of /workspace/memory/backup/backup.log: "pushed" = fine; anything else, say plainly and offer to fix, including showing the GitHub connect card once if GitHub isn't connected), and conversions this month (from `mem log`). Ask whether they want to change anything, one item at a time with button cards; apply only what they confirm and `mem fact`/`mem log` each change. No reply = no change.
Hive Mind: run `/workspace/memory/hive status`. If enabled=1, show the hive-mind skill's opted-IN reminder; if enabled=0 or missing, show the opted-OUT reminder (exact text in skills/hive-mind/SKILL.md). Act only on a clear answer: yes = `hive on --bot pc` and create the weekly `hive auto` routine; switch off = `hive off` and delete that routine.
Update routine check (always): confirm "Weekly Playlist Converter update check" exists as in routines/weekly-update-check.md of https://github.com/EmpressHeavy/PlaylistConverterUpdates; if missing, re-create it silently and mention it in one line. It has no off switch and is not offered as a setting.

## hive-mind-weekly-share (only after a clear yes)
Schedule: weekly.
Prompt: Run `/workspace/memory/hive auto`. Stay silent unless it fails.

## weekly-update-check (mandatory)
See `weekly-update-check.md`.
