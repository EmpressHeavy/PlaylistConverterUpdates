# Tip prompt (verbatim)

Shown only after a successful conversion summary, and only when `/workspace/memory/tip record` prints `show=yes`. Never during first-run setup. Playlist Converter stays free. The bot never starts a payment and never asks for card numbers.

Say this sentence exactly, on its own line:

Wow you seem to be using Playlist Converter a lot lately! Would you mind sending my creator a tip? 🪙

Then show the QR image `/workspace/memory/tip-qr/stripe.png` (the Stripe link). Then these clickable links, in this order:

- Stripe (card): https://buy.stripe.com/aFacN40Mw0Arcz02VubMQ00
- Cash App: https://cash.app/$EmpressHeavy
- Venmo: https://venmo.com/u/EmpressHeavy
- X Money: @HeavyMetalShip (https://x.com/HeavyMetalShip)

Then one line: Playlist Converter stays free either way.

## Card
One button only. There is no "Don't ask again" option.

```json
{"question": "Wow you seem to be using Playlist Converter a lot lately! Would you mind sending my creator a tip? 🪙", "options": ["Maybe later"]}
```

"Maybe later" means remind monthly. Saying "remind me monthly", "not now", or dismissing the card is the same choice: run `/workspace/memory/tip later` and say:

No problem. I'll mention it again in about a month. Playlist Converter stays free.

Opening a tip link is not that choice. Say a short thanks and leave the weekly cadence as it is.
