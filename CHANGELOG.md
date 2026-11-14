# Changelog

## 1.0.1
- Occasional tip prompt right after a successful conversion summary. A local counter in brain.db counts finished playlist conversions (not scans). The first time is after 3 completed conversions, then at most once every 7 days, and never during first-run setup.
- The only follow-up is "Maybe later" (remind me monthly). Choosing it, or dismissing the prompt, switches the reminder to at most once every 30 days. There is no "don't ask again" and no permanent opt-out. The bot stays free and never moves money.
- Weekly update check is unchanged: still automatic, always on, and not an owner setting.

## 1.0.0
- First public build of Playlist Converter: playlist-conversion, getting-started, personal-memory and hive-mind skills, setup cards, profile, and routines.
- Private memory (brain.db + `mem`) now backs itself up automatically to a private repo in the owner's own GitHub account after every write, checking the repo is private before every push.
- Updates are automatic and always on: a weekly update-check routine installs newer versions from this repo and sends a short "updated to vN" note. Snapshot first, roll back on failure; your memory and choices are kept.
- Hive Mind: optional, default off, send-only (bot code `pc`).
