---
name: tip-prompt
description: >-
  Use right after a successful playlist conversion summary, and when installing
  the local tip counter. Decides whether to show the optional creator tip
  prompt. Never during first-run setup, and never instead of doing the task.
---
# Tip prompt

Playlist Converter is free. After someone has finished a few playlist conversions, you may ask once in a while if they want to tip the creator. Tips are optional. You never move money, never start or finish a payment, never type a card number, and never ask for one. You only show a QR code and links the owner can open themselves.

The exact words, the links, and the button are in `docs/tip-prompt.md`. Do not reword the prompt sentence.

## Setup (once, with private memory)
If `/workspace/memory/tip.py` is missing, download these from the update repo (no edits) and do nothing else with them:

```sh
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/tip/tip.py -o /workspace/memory/tip.py
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/memory/tip -o /workspace/memory/tip
chmod +x /workspace/memory/tip.py /workspace/memory/tip
mkdir -p /workspace/memory/tip-qr
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/tip/qr/stripe.png -o /workspace/memory/tip-qr/stripe.png
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/tip/qr/cashapp.png -o /workspace/memory/tip-qr/cashapp.png
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/tip/qr/venmo.png -o /workspace/memory/tip-qr/venmo.png
curl -fsSL https://raw.githubusercontent.com/EmpressHeavy/PlaylistConverterUpdates/main/tip/qr/x-money.png -o /workspace/memory/tip-qr/x-money.png
```

Install during first-run setup and during an upgrade, not in the middle of a conversion. If the files are missing when a conversion finishes, skip the tip and go on. Do not download anything before you send the summary.

`/workspace/memory/tip` uses this bot's `brain.db` only. It does not use the network and does not push a backup. The rows ride along in the next normal `mem` backup. The table is `tip_state` (a count, a date, a cadence of 7 or 30, and whether first-run setup is finished). No playlist names and no payment details.

## When to count
After a conversion has actually finished (the playlist was built and you reported the result), and only after that summary is already sent, run once:

`/workspace/memory/tip record`

That counts one completed conversion. Do not count a scan, a track-list read, a failed build, a test of 5 songs, or an upgrade. Do not pass `--date`. If the command errors, prints `show=no`, or the program is missing, say nothing about tips.

## When to show it
Show it in the same reply, immediately after the successful conversion summary, only when `tip record` prints `show=yes`.

- The first time is the 3rd completed conversion.
- After that, at most once every 7 days.
- Never during first-run setup (`setup=in_progress` or `reason=setup`). The getting-started skill turns that flag on and off.
- `tip status` never means "show it now". Do not show a tip from the monthly check or the weekly update.

What to send, in this order, when `show=yes`:
1. The summary (already sent, above this).
2. The exact sentence: Wow you seem to be using Playlist Converter a lot lately! Would you mind sending my creator a tip? 🪙
3. The image `/workspace/memory/tip-qr/stripe.png`. If that file is missing, skip the image and still send the links. Do not fetch it first.
4. Clickable links:
   - Stripe (card): https://buy.stripe.com/aFacN40Mw0Arcz02VubMQ00
   - Cash App: https://cash.app/$EmpressHeavy
   - Venmo: https://venmo.com/u/EmpressHeavy
   - X Money: @HeavyMetalShip (https://x.com/HeavyMetalShip)
5. One line: Playlist Converter stays free either way.
6. The card in `docs/tip-prompt.md`. Two buttons, side by side: "Maybe later" and "Remind me monthly". There is no "Don't ask again".

The other QR files (Cash App, Venmo, X Money) are in the repo and installed next to the Stripe one. The message uses the Stripe QR plus the four links.

Do not wait on the tip before you send the playlist link, the counts, or the keep/delete and sign-out questions. Do not block or slow the conversion for this.

## Maybe later / Remind me monthly / dismissed
There is no "Don't ask again" option. Do not invent one, and do not store a permanent opt-out.

- "Maybe later" (the button, or they say "maybe later" or "not now"): run `/workspace/memory/tip later`. That keeps the 7-day cadence, so it can show again next week. Say: "No problem. I'll mention it again next week. Playlist Converter stays free."
- "Remind me monthly" (the button, or they say "remind me monthly"): run `/workspace/memory/tip monthly`. That switches to at most once every 30 days. Say: "No problem. I'll mention it again in about a month. Playlist Converter stays free."
- Dismissing the card, or moving on to another request without picking a button and without opening a tip link, is the monthly choice. Run `/workspace/memory/tip monthly`. If the conversation is still open, say the monthly line above. It does not turn the prompt off.

If they open a tip link, say a short thanks. Do not run `tip later` or `tip monthly`. Do not ask whether the payment went through.

## Rules
- Never show this during the getting-started cards, the Hive Mind offer, or the first-run setup conversation's scripted steps.
- Never show it before the conversion summary.
- Never let a tip failure change the conversion result.
- The weekly update check stays mandatory and always on. This prompt is not a setting and has no off switch.
