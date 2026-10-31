# Parity map (current build → repo)
| Component | Repo location |
|---|---|
| Profile (name, title, description, welcome message, avatar shape/color) | `profile/profile.json`, `profile/welcome_message.txt` |
| Profile picture | none shipped (no avatar image found; squircle/orange default) |
| Per-agent settings | `profile/settings.json` |
| Playlist conversion method | `skills/playlist-conversion/SKILL.md` |
| First-run setup and cards | `skills/getting-started/SKILL.md`, `docs/setup-cards.md` |
| Private memory + auto GitHub backup | `skills/personal-memory/SKILL.md`, `memory/mem`, `memory/hive` |
| Hive Mind (send-only, opt-in, bot code pc) | `skills/hive-mind/SKILL.md`, `hive/hive.py`, `hive/README.md` |
| Routines and prompts | `routines/routines.md`, `routines/routine-prompts.md`, `routines/weekly-update-check.md` |
| Safety rules | `docs/safety.md`, `UPGRADE.md` guardrails |
| Upgrade procedure | `UPGRADE.md` |
| Version | `VERSION`, `CHANGELOG.md` |

Built-in platform skills it also relies on (provided by Grok Bot, not shipped): sign-in, vault, routines, no-connector-fallback.
