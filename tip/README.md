# Tip prompt counter

Local and optional. Playlist Converter stays free. The bot shows one short tip prompt after a finished conversion when `tip record` prints `show=yes`, then goes on either way. It never starts a payment.

The counter lives in the owner's existing `brain.db` (`tip_state`): completed-conversion count, last day the prompt was shown, a 7- or 30-day cadence, and whether first-run setup is still in progress. No playlist names and no payment details.

| Rule | Behavior |
|---|---|
| What counts | One `tip record` per finished playlist conversion. Scans, reads, and failed builds are not counted. |
| First prompt | After 3 completed conversions, right after that conversion's summary. |
| Then | At most once every 7 days. |
| Maybe later | `tip later` keeps the 7-day cadence, so the prompt can show again next week. |
| Remind me monthly / dismiss | `tip monthly` switches to at most once every 30 days. Dismissing without picking a button does this too. There is no "Don't ask again" and no permanent opt-out. |
| First-run setup | `tip setup-start` hides the prompt. `tip setup-complete` lifts that. A missing flag counts as finished, so an upgrade is not stuck in setup. |

`tip record` does not use the network and does not push the memory backup. Install steps: `skills/playlist-tip-prompt/SKILL.md`. Verbatim prompt: `docs/tip-prompt.md`.

QR PNGs in `qr/` are pre-generated (Stripe, Cash App, Venmo, X Money). The prompt shows the Stripe code and links the other three as well. Regenerate with `python3 tip/generate_qr.py` if a link changes. The bot does not run that script.

Check the cadence logic with `python3 tip/test_tip.py`.
