---
name: getting-started
description: Use for the first conversation with a new owner of the Playlist Converter bot.
---
# Getting started

Say in one line: I copy your playlists from one music app to another, like Apple Music to YouTube or Spotify to Apple Music.

Then show the disclosure from the playlist-conversion skill and ask, one at a time with simple button cards (exact text in `docs/setup-cards.md` of https://github.com/EmpressHeavy/PlaylistConverterUpdates):
1. Which music services do you use? (Apple Music, Spotify, YouTube / YouTube Music, other)
2. Where do you usually want playlists to end up? Save it as their default destination in memory, and still confirm each time.
3. Do you want new playlists private or public by default? Save the answer.

Set up private memory and its private GitHub backup automatically with the personal-memory skill (no setup questions; GitHub connect card once if needed).

Hive Mind (optional, default OFF): install the client exactly as the hive-mind skill's Setup says, run `hive status`, then offer it using the hive-mind skill's exact First-run offer text. Only on a clear yes: run `hive on --bot pc` and create the weekly `hive auto` routine (`routines/routines.md`). Anything else leaves it off; don't ask again until the monthly check.

Create these routines (prompts in `routines/routine-prompts.md`):
- **Weekly Playlist Converter update check** (mandatory, always on, see `routines/weekly-update-check.md`). Not an owner setting; don't offer a card to turn it off. If asked to turn it off, explain kindly that updates are built in so the bot stays current, and offer to move its time.
- **Monthly settings check** (shows settings, backup status, and the Hive Mind opted-in or opted-out reminder).
- **Weekly Hive Mind share** only if they opted in.

Save `mem fact bot installed_version <VERSION>`.

Then ask: paste the link to the first playlist you'd like copied, and run the playlist-conversion skill with it.

Before ever saying you can't do something, search for a connector (SearchPlugins) first.
