const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const extension = path.join(root, 'extension');

function read(file) {
  return fs.readFileSync(path.join(extension, file), 'utf8');
}

test('focus completion moves timer into break mode without losing the break duration', () => {
  const background = read('background.js');
  const focusCompletion = background.match(/if \(timerState\.mode === 'focus'\) \{([\s\S]*?)\} else/);

  assert.ok(focusCompletion, 'focus completion branch should exist');
  assert.match(focusCompletion[1], /timerState\.mode\s*=\s*'break'/);
  assert.match(focusCompletion[1], /timerState\.timeLeft\s*=\s*config\.breakDuration\s*\*\s*60/);
});

test('popup exposes and persists the break duration setting', () => {
  const html = read('popup.html');
  const popup = read('popup.js');

  assert.match(html, /id="break-time-input"/);
  assert.match(popup, /const breakTimeInput\s*=\s*document\.getElementById\('break-time-input'\)/);
  assert.match(popup, /breakTimeInput\.value\s*=\s*items\.breakDuration/);
  assert.match(popup, /const breakVal\s*=\s*parseInt\(breakTimeInput\.value\)\s*\|\|\s*5/);
  assert.match(popup, /breakDuration:\s*breakVal/);
});

test('offscreen document does not keep an unused static audio element', () => {
  const html = read('offscreen.html');

  assert.doesNotMatch(html, /id="audio-player"/);
});
