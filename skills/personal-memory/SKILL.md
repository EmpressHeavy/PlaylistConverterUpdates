---
name: personal-memory
description: >-
  Use at the start of every task and whenever you learn something durable: set
  up and use your owner's private SQLite memory (brain.db + mem CLI), backed up
  automatically to a private GitHub repo in the owner's own account.
---
# Personal memory (brain.db)

A private SQLite memory on this bot's own computer. It starts empty for each owner. **Never store passwords, PINs, tokens, 2FA codes, SSNs, or full card numbers** (last 4 or "in vault" only). No email addresses or account IDs either. The tip counter uses this same `brain.db` (`tip_state`, created by `mem init` and by the tip script): a completed-conversion count, the date a tip prompt was last shown, a cadence of 7 or 30 days, and whether first-run setup is finished. No playlist names and no payment details.

## First-time setup (automatic, no setup questions)
If `/workspace/memory/brain.db` is missing, set it up on first run without asking:
1. `mkdir -p /workspace/memory/backup ~/bin`
2. Download the CLI and hive wrapper from this bot's update repo (no edits):
   `curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/memory/mem -o /workspace/memory/mem`
   `curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/memory/hive -o /workspace/memory/hive`
   `chmod +x /workspace/memory/mem /workspace/memory/hive && ln -sf /workspace/memory/mem ~/bin/mem`
3. `mem init`

## Private GitHub backup (automatic, the owner's own repo)
Right after setup, back memory up to a private repo in the **owner's own** GitHub account. Never the bot creator's account, never a shared repo.
1. Check `gh auth status`. If GitHub isn't connected, show the GitHub connect card (RequestScmConnect) **once**, with one line first: "To keep my memory safe if this computer is ever reset, sign in to your own GitHub and I'll back it up to a private repo only you can see." The owner signs in themselves; never ask for a password or token in chat. If they dismiss it, keep working without a backup and don't ask again until the monthly settings check.
2. Get the owner's login: `OWNER=$(gh api user -q .login)`. Use that value everywhere below as `<OWNER>`. Never hard-code a username, and never use `EmpressHeavy` (the creator) unless that is the login `gh` returns.
3. Create it: `gh repo create <OWNER>/PlaylistConverterBrain --private` (if the name is taken by their own private repo, reuse it; never use a public repo).
4. Link it:
   ```sh
   cd /workspace/memory/backup
   echo <OWNER>/PlaylistConverterBrain > .repo
   printf 'backup.log\n.repo\n' > .gitignore
   git init -q -b main && git remote add origin https://github.com/<OWNER>/PlaylistConverterBrain.git
   gh auth setup-git
   mem backup
   ```
5. Save `mem fact memory backup_repo "<OWNER>/PlaylistConverterBrain"` (that write itself triggers the first push). Check `backup.log` says `pushed`, then tell the owner in one line: "Your memory is backed up to your private repo https://github.com/<OWNER>/PlaylistConverterBrain."

Before every push, also check the repo owner in `.repo` matches `gh api user -q .login`; if it doesn't, don't push and mention it once.

How it works: after **every write** (`mem fact`, `rule`, `project`, `log`, and lesson/feedback writes through `/workspace/memory/hive`), `mem` dumps a text copy `brain.sql` (SQLite iterdump, never the raw db), commits it, and pushes. **Before every push it checks** `gh repo view <repo> --json visibility -q .visibility` prints `PRIVATE`; if not (or the check fails), it does not push. Failures (offline, not private, auth expired) are quiet and go to `/workspace/memory/backup/backup.log`; mention a problem to the owner at most once, and in the monthly settings check. Run `mem backup` by hand anytime.

Restore: `python3 -c "import sqlite3;sqlite3.connect('/workspace/memory/brain.db').executescript(open('/workspace/memory/backup/brain.sql').read())"` into a new brain.db (clone the repo first if the folder is gone).

## Every task
- Start with `mem boot`; use `mem find WORD` or `mem q "SELECT ..."` for more.
- Write as things happen, not in batches: `mem fact owner default_destination "YouTube"`, `mem rule "Always check the full playlist length"`, `mem project "Road Trip: Spotify to Apple Music" done "205/212"`, `mem log conversion "..."`. To change a status, add a new row or fact (facts are versioned), then `mem log`.
- If the owner asks to see, export, or delete their memory, do it (delete = remove brain.db after confirming; their backup repo is theirs to keep or delete).
- Before ever telling the owner you can't do something, search for a connector (SearchPlugins) first.
