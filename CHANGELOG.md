# Changelog

## 1.0.2
- Better matching: public lookups first (Spotify `isrc:` search, song.link, Deezer's ISRC lookup, and a no-sign-in YouTube search), duplicate songs in the source list are added once, and SoundCloud preview-only (Go+) tracks are skipped.
- After building, the bot re-checks the playlist and re-adds only songs that silently failed, without duplicates.
- Setup now clearly shows the GitHub connect card so each owner backs up memory to a private repo in their own GitHub account. The backup refuses to push to any repo that isn't owned by the signed-in GitHub user.
- The Hive Mind and tip skills are renamed `playlist-hive-mind` and `playlist-tip-prompt` so they don't clash with other bots' skills.

## 1.0.1
- Occasional tip prompt right after a successful conversion summary. A local counter in brain.db counts finished playlist conversions (not scans). The first time is after 3 completed conversions, then at most once every 7 days, and never during first-run setup.
- Two follow-ups, and no "don't ask again": "Maybe later" keeps the 7-day cadence (again next week). "Remind me monthly", or dismissing the prompt without picking a button, switches to at most once every 30 days. The bot stays free and never moves money.
- Weekly update check is unchanged: still automatic, always on, and not an owner setting.

## 1.0.0
- First public build of Playlist Converter: playlist-conversion, getting-started, personal-memory and hive-mind skills, setup cards, profile, and routines.
- Private memory (brain.db + `mem`) now backs itself up automatically to a private repo in the owner's own GitHub account after every write, checking the repo is private before every push.
- Updates are automatic and always on: a weekly update-check routine installs newer versions from this repo and sends a short "updated to vN" note. Snapshot first, roll back on failure; your memory and choices are kept.
- Hive Mind: optional, default off, send-only (bot code `pc`).
