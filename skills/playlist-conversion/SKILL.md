---
name: playlist-conversion
description: >-
  Use when someone wants a playlist copied from one music service to another
  (Apple Music, Spotify, YouTube/YouTube Music, others) using the browser.
---
# Convert a playlist (browser method)

Ask one plain-English question at a time, using question cards with buttons where possible. No jargon.

1. **Disclose first.** Before anything else, say: I'm an AI bot, not affiliated with or endorsed by Apple, Google/YouTube, Spotify, or any music service. I only read your playlist's song titles and artists and use your signed-in session in my browser to build what you ask. I never see your password. I ask before signing in, before building, and before saving any data. I won't touch anything else in your account. Any music subscription costs are your own. You can sign out anytime.
2. **Source.** Get the playlist link. If the service isn't clear, ask.
3. **Read the full list.** Read every song (title, artist, length if shown). Always get the FULL track list and confirm the true total against the count the service shows; never stop at the first page (Apple Music's public page initially shows only the first 300 songs, so keep scrolling until everything loads and the count matches). Don't scrape private tokens or private endpoints. Tell the user the total before going on.
4. **Destination.** Ask where it should go. Ask the playlist name (default to the original), private or public, and on a name clash ask: replace, add to it, or make a new one. Remember their usual destination but confirm each time.
5. **Sign in.** Ask before signing in. Open the service's sign-in page and hand the screen to the user so they sign in themselves; never type or ask for their password. Each user signs in to their own account only.
6. **Match.** Match each song by title and artist, preferring the official version and similar length; handle regional or translated titles. Avoid live, remix, or sped-up versions unless the original is one. Retry misses with alternate searches and flag every song still unmatched.
7. **Optional test.** Offer to add 5 songs first so they can check.
8. **Confirm, then build.** Show the matched count and the misses, ask to confirm, then build. On YouTube, a reliable way to add many songs is to open `https://www.youtube.com/watch_videos?video_ids=ID1,ID2,...` (about 50 IDs per URL, no repeats within one URL) in YouTube Music with Autoplay off, then save the queue to the playlist; repeat for each batch, in order. YouTube won't add videos marked "made for kids" ("This action is turned off for content made for kids"); if a batch fails with that, remove those songs, retry the rest, and list them for the user. Respect rate limits; back off and slow down rather than working around them.
9. **Verify.** Compare the source count with the destination count, report both, list anything missing, and offer to retry.
10. **Wrap up.** Give the playlist link and a short summary. Ask whether to keep or delete their song list and results (offer export to their Google Drive). Ask whether to sign out of the service now.
