# Routines

| # | Name | Schedule (owner's time zone) | When created | Can the owner turn it off? |
|---|---|---|---|---|
| 1 | Weekly Playlist Converter update check | Sunday 10:00 AM (`0 10 * * 0`) | Always, at first run and every upgrade | No (time can be moved). Re-created by the monthly check if missing. |
| 2 | Monthly settings check | 1st of month 10:00 AM (`0 10 1 * *`) | Always, at first run | Yes |
| 3 | Weekly Hive Mind share | Weekly (e.g. Saturday 9:00 AM) | Only after a clear yes to Hive Mind | Yes (`hive off` removes it) |

Prompts: `routine-prompts.md` (1 is in `weekly-update-check.md`).
