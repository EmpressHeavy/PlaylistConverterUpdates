# Setup cards and first-run messages (verbatim)

Welcome message: see `profile/welcome_message.txt`.

Intro line: "I copy your playlists from one music app to another, like Apple Music to YouTube or Spotify to Apple Music."

Disclosure (always, before anything else): the text in step 1 of `skills/playlist-conversion/SKILL.md`.

## Card 1: services
```json
{"question": "Which music services do you use?", "multiSelect": true, "options": ["Apple Music", "Spotify", "YouTube / YouTube Music", "Other"]}
```

## Card 2: default destination
```json
{"question": "Where do you usually want playlists to end up?", "options": ["YouTube / YouTube Music", "Apple Music", "Spotify", "Other"]}
```
Saved as `mem fact owner default_destination "<answer>"`; still confirmed every conversion.

## Card 3: privacy default
```json
{"question": "Do you want new playlists private or public by default?", "options": ["Private", "Public", "Ask me each time"]}
```

## GitHub connect card (only if GitHub isn't connected; shown once)
"I keep a private backup of my memory in a private repo in your own GitHub account, so nothing is lost if my computer is reset. Connect GitHub and I'll set it up. I never see your password." Buttons: Connect GitHub / Not now.

## Hive Mind offer (default off)
Exact text in `skills/hive-mind/SKILL.md` ("First-run offer").

## First conversion prompt
"Paste the link to the first playlist you'd like copied."
