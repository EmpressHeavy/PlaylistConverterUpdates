#!/usr/bin/env python3
"""Write the tip-prompt QR PNGs into tip/qr/. Run when a link changes; the bot does not.

The PNGs are committed. Playlist Converter shows stripe.png and links the other three.
"""
import os, sys
PROMPT = "Wow you seem to be using Playlist Converter a lot lately! Would you mind sending my creator a tip? \U0001fa99"
BUTTON = "Maybe later"
# (filename, label, url encoded in the QR). X Money's visible handle is not a second URL.
HANDLE = "@HeavyMetalShip"
LINKS = [
    ("stripe.png", "Stripe (card)", "https://buy.stripe.com/aFacN40Mw0Arcz02VubMQ00"),
    ("cashapp.png", "Cash App", "https://cash.app/$EmpressHeavy"),
    ("venmo.png", "Venmo", "https://venmo.com/u/EmpressHeavy"),
    ("x-money.png", "X Money", "https://x.com/HeavyMetalShip"),
]

def main():
    import segno
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qr')
    os.makedirs(out, exist_ok=True)
    for name, _label, url in LINKS:
        segno.make(url, error='m').save(os.path.join(out, name), scale=8, border=4)
        print(name, url)
    return 0

if __name__ == '__main__':
    sys.exit(main())
