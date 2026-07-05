# Grogu Focus Timer

<p align="center">
  <a href="./README.md">简体中文</a> | <strong>English</strong>
</p>

<p align="center">
  <img src="./extension/assets/zhaoshou_cradle.webp" width="260" alt="Grogu Companion - Waving Cradle Animation">
</p>

<p align="center">
  <strong>Grogu drifts across your night sky, with random emojis appearing like shooting stars.</strong>
</p>

<p align="center">
  Cyber Pet + Focus Timer. Accompanying you to stay focused, and gently reminding you to stop looking for excuses to procrastinate.
</p>

A browser-based companion pet extension.

It is not a strict efficiency management software, nor does it try to control you with reports and punishments. It is more like a little buddy drifting across your webpages: when you write, code, or read, it stays with you quietly; when you drift off to distraction, it uses a short "NO" to gently remind you.

> Not control, but companionship.

<p align="center">
  <img src="./extension/assets/grogu_companion_poster.png" width="600" alt="Grogu Focus Timer Poster">
</p>

## Highlights

- **Floating Cradle Companion**: Grogu sits in a little hover cradle, floating gently across your web pages.
- **YES / NO Gentle Reminders**: Gives you encouragement when returning to work pages, and gentle reminders when entering distraction pages.
- **Random Emotional Events**: Snacking, peeking, using the Force, and waving appear randomly to provide emotional value.
- **Audio Feedback**: Emojis are accompanied by short sound effects, which can be disabled in settings.
- **Customizable Distraction Rules**: Supports default website categories, and allows adding custom keywords or regular expressions.
- **In-Page Keyboard Shortcuts**: Set hotkeys for popular emojis to summon Grogu anytime.
- **Chrome Side Panel**: Click the extension icon to open the side panel control UI.

## Ideal For

- Wanting a light companion while coding.
- Seeking a bit of ritual while writing online or organizing materials.
- Wishing for a gentle nudge when browsing news, videos, or shopping sites to check if you are off-track.
- Wanting to make the browser more fun without using strict blocking tools.

## Installation

Currently in local developer version.

1. Open Chrome and navigate to `chrome://extensions/`
2. Turn on "Developer mode" in the top right corner.
3. Click "Load unpacked" in the top left.
4. Select the `extension` folder inside this repository.
5. Click the extension icon in the toolbar to open the side panel.

## Usage

1. Set your current task, e.g., "Coding", "Writing", "Reading".
2. Set focus and break durations.
3. Select default distraction groups or add custom keywords.
4. Click "Enable Force".
5. Let Grogu accompany you on your web pages.

## Project Structure

```text
grogu-focus-timer/
  extension/          Chrome extension source files
    manifest.json     Manifest V3 configuration
    background.js     Timer, distraction detection, random event scheduler
    content.js        Floating avatar injection logic
    content.css       Cradle layout, floating paths, emoji animations
    popup.html        Side panel control panel
    popup.js          Settings, buttons, hotkey triggers
    offscreen.*       Audio playback under Manifest V3
    assets/           WebP animations, audio cues, and icons
```

## Tech Stack

- Chrome Extension Manifest V3
- `chrome.alarms` for background timing and random event scheduling
- `chrome.scripting` for in-page overlay injection
- `chrome.offscreen` for audio playback
- Content Script for capturing in-page shortcuts
- SVG + CSS for drawing hover cradle, LED lighting, and floating animations

## Current Status

This is a personal experimental project focusing on "companionship" and "cuteness". Time management features remain as gentle reminders without complex charts or hard blocking.

## Notice

This project is for personal learning and prototyping only. Character style and asset inspirations come from popular baby alien culture. For official publishing or Web Store release, it is recommended to replace them with original character designs, names, and assets.
