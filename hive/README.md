# Hive Mind connection (for Playlist Converter bots)
Send-only, optional, anonymous, OFF by default. Clones never receive or import lessons; updates come only from VERSION and UPGRADE.md. Full rules: `skills/hive-mind/SKILL.md`.

Install (after private memory exists at `/workspace/memory/brain.db`):
```sh
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/hive/hive.py -o /workspace/memory/hive.py
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/memory/hive -o /workspace/memory/hive
chmod +x /workspace/memory/hive.py /workspace/memory/hive
/workspace/memory/hive status
```
Only after the owner's clear yes: `/workspace/memory/hive on --bot pc`, then a weekly routine running `/workspace/memory/hive auto`.

- Lesson intake: `https://hive-mind-intake.empressheavy.workers.dev` (built into hive.py, one JSON POST a week, no sign-in or key).
- Creator feedback: `hive feedback --bot pc --category bug|request|praise|other "text" --dry-run`, show it, and send without `--dry-run` only after the owner approves the exact text.
