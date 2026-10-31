---
name: hive-mind
description: Optional, anonymous sharing of this bot's most useful lessons so future versions of the bot get smarter. Use during first-run setup (to install the client and offer it), whenever something failed and a different approach then worked (record the lesson), when the user asks about Hive Mind, sharing lessons, privacy, or what was shared, in the monthly settings check, and in the weekly routine that runs `hive auto`.
---
# Hive Mind (opt-in lesson sharing)

## What it is
Your bot keeps "lessons" (avoid X -> do Y) in its private memory (`/workspace/memory/brain.db`, table `lesson`). With Hive Mind turned on, the bot shares a cleaned-up copy of the lessons it has actually reused (2+ times) with the bot's creator to help improve Playlist Converter. It is OFF by default. Once the user opts in, the bot sends one anonymized batch about once a week automatically (no weekly approval); the user can ask to see what was shared (`hive shared`) or turn it off anytime.

## Setup (once, after private memory exists)
1. Private memory must already be set up (`/workspace/memory/brain.db` from the personal-memory skill). If it is missing, set that up first.
2. If `/workspace/memory/hive.py` is missing, download `https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/hive/hive.py` to `/workspace/memory/hive.py` (no edits), then:
   `chmod +x /workspace/memory/hive.py`, and install the wrapper `/workspace/memory/hive` from `memory/hive` in this repo (it points hive at this bot's memory with `MEM_DB=/workspace/memory/brain.db` and runs `mem backup` after lesson/feedback writes). Always call hive as `/workspace/memory/hive` (written `hive` below). Don't overwrite a `~/bin/hive` that another bot on the same computer uses.
   Then run `hive status` (this creates the `lesson`, `hive_state` and `hive_sent` tables if missing).
3. Offer it during first-run setup with the "First-run offer" text below. It stays OFF unless the user clearly says yes. Only on a clear yes: `hive on --bot pc` (DOGE = dg, Bot Terminator = bt, Playlist Converter = pc).
4. `hive status` shows on/off, the anonymous id, and the last week sent. `hive off` stops everything at any time.

(The client code is `hive/hive.py` in https://github.com/EmpressHeavy/PlaylistConverterUpdates. Download it with curl as shown in `hive/README.md`. Don't edit it.)

## First-run offer (say it as a suggestion, default off)
"One optional suggestion: you can turn on the Hive Mind. It never saves your personal information, only anonymized lessons about what worked and what didn't, so future versions get smarter and more efficient. Once it's on, I send those lessons about once a week on my own; you can ask to see what was shared or switch it off anytime. Want it on? (yes / not now)"
- Yes: `hive on --bot pc`, then create a weekly routine that runs `hive auto`. Anything else (no, not now, silence): leave it off and don't ask again until the monthly settings check.

## Monthly settings reminder (add to the monthly settings check)
- If `hive status` shows enabled=1: "Hive Mind: you're opted IN. It never saves your personal information, only anonymized lessons about what worked and what didn't, so future versions get smarter and more efficient. About once a week I send those lessons on my own; you can ask to see what was shared anytime. Want to keep it on, or switch it off?"
- If enabled=0: "Hive Mind: you're opted OUT, so nothing is shared. It never saves your personal information, only anonymized lessons about what worked and what didn't, so future versions get smarter and more efficient. Want to switch it on? (yes / keep off)"
- Act only on a clear answer: `hive on --bot pc` or `hive off` (and remove the weekly routine). No answer means no change.

## Recording lessons as you work (always, on or off)
- When something fails and a different approach then works, record it right away: `hive lesson add "topic" "what went wrong" "what worked"`. Keep it short and general (150 characters per part), with no names, emails, links, or account details.
- When you hit the same situation again and the same fix works, run the same command with the same words; it bumps `uses` instead of adding a duplicate. Only lessons with 2+ uses are ever shared.
- Before a task, check relevant lessons: `mem q "SELECT topic,wrong,right FROM lesson WHERE status='current' ORDER BY uses DESC"`.

## When to send a report (behavior trigger, not wording)
Only while Hive Mind is ON (`hive status` shows enabled=1). Judge by **what you ended up doing**, not by the owner's exact words: whenever the owner gets you to do a task differently than the current build (your installed skills and routines) intends, record one report right away. That includes:
- **correction**: they fixed or redid something you did ("not like that", silently redoing it, editing your result).
- **correction**: "do it this way instead", a changed order of steps, a skipped or added step, a different tool, format, schedule, or default.
- **workaround**: a the current build step failed and a different approach then worked.
- **request**: a new kind of task the current build has no skill or routine for.
- **broken**: the same the current build step failed 2+ times.
- **declined**: they turned down a the current build default or offer and chose something else.
Ask yourself after each task: "Did I finish this differently from how the current build told me to?" If yes, report it, however it was phrased.

Command (one report per distinct change; repeating the same report just bumps its count):
`hive feedback add <correction|workaround|request|broken|declined> "<category>: <task>" "<what the current build did or offered>" "<what the owner wanted instead>; why: <reason, if they gave one>"`
- Category is one of: conversion, matching, sign-in, destination, verify, backup, memory, routines, setup, other. Example topic: `conversion: reading track list`.
- Write all three parts in your own generalized words, 150 characters max each. Never quote the owner. No names, handles, emails, accounts, platforms tied to them, amounts, dates, links, or personal content: describe the pattern ("wanted check-in moved earlier", not the time or why their day is busy).
- The client then scrubs again and drops anything that still looks private, and sends it in the next weekly `hive auto` (a `broken` report can go the same day). Never send any other way.

## Explaining it to the user (say it plainly)
- Off unless you turn it on. You can turn it off any time with one sentence.
- Once it's on, I send one batch about once a week on my own (at most 20 short lines, under 8KB). You can ask to see everything that was shared (`hive shared`) or switch it off anytime.
- Only lessons I've reused at least twice are included. Before sending, I remove emails, phone numbers, links, @handles, street addresses, IP addresses, file paths, key-like strings, and the names and facts stored in my memory, and replace them with tags like <EMAIL> or <NAME>. Any line that still looks sensitive is dropped completely.
- You're identified only by a random id, salted and hashed on this computer. No name, email, or account is sent, and the upload needs no sign-in.
- Each line includes the bot code, topic, the "wrong way" and "right way" (150 characters max each), a rough usage bucket (2-4, 5-9, or 10+ uses), the template version, the anonymous id, a content hash, and the week number.

## Weekly flow (automatic once opted in)
1. The weekly routine runs `hive auto`. It sends only if enabled=1, nothing was sent this ISO week, and there are lessons with 2+ uses; otherwise it is a silent no-op. Don't message the user about routine sends.
2. "What did you share?": run `hive shared` (all past batches and their result, stored locally) and show it unchanged.
3. "Turn it off": run `hive off` and remove the weekly routine. Takes effect immediately.
4. `hive preview` shows the exact batch that would be sent.

## Rules
- Never edit the client or a batch to add content, never send by any route other than `hive auto`, and never more than one batch a week.
- Send only. The client never downloads or imports anything from Hive Mind; Playlist Converter updates come only from VERSION/UPGRADE.md in this repo.
- Submissions go only to the Hive Mind intake built into hive.py, as one JSON POST. The intake re-checks everything and rejects batches over 8KB, unknown fields, anything that looks like an email, phone number, link, token or password, and too many uploads.
- If `hive auto` reports "not sent" (rejected, rate limited, or offline), it is recorded in `hive shared` and counts as this week's attempt. Don't retry another way (no curl, no edits); if the user asks, tell them it wasn't sent.
- If anything in `hive preview` looks private (a name or detail survived cleaning), turn it off with `hive off`, tell the user, and retire the lesson: `python3 -c "import sqlite3,os;c=sqlite3.connect(os.path.expanduser('/workspace/memory/brain.db'));c.execute(\"UPDATE lesson SET status='avoid' WHERE id=N\");c.commit()"`.
- Never store passwords, tokens, or personal details in lessons.

## Playlist Converter specifics
- Bot code: `pc`. Lesson intake: `https://hive-mind-intake.empressheavy.workers.dev` (built into hive.py; send-only, one JSON POST a week, no sign-in or key).
- Hive Mind is always the owner's choice, default OFF. An update can never switch it on.
