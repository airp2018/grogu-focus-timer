// DOM Elements
const timerDisplay = document.getElementById('timer-display');
const timerMode = document.getElementById('timer-mode');
const statusText = document.getElementById('status-text');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const timerCircle = document.querySelector('.timer-circle');

// Config Form Elements
const focusTimeInput = document.getElementById('focus-time-input');
const breakTimeInput = document.getElementById('break-time-input');
const taskInput = document.getElementById('task-input');
const distractionPatternsInput = document.getElementById('distraction-patterns-input');
const defaultBlacklistToggles = document.querySelectorAll('.default-blacklist-toggle');
const blockMsgInput = document.getElementById('block-msg-input');
const blockerToggle = document.getElementById('blocker-toggle');
const soundToggle = document.getElementById('sound-toggle');
const saveSettingsBtn = document.getElementById('save-settings-btn');

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  syncTimerState();
  
  // Register port/listeners
  chrome.runtime.onMessage.addListener(handleBackgroundMessage);
});

// Control Events
startBtn.addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: 'START_TIMER' }, (response) => {
    syncTimerState();
  });
});

pauseBtn.addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: 'PAUSE_TIMER' }, (response) => {
    syncTimerState();
  });
});

resetBtn.addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: 'RESET_TIMER' }, (response) => {
    syncTimerState();
  });
});

saveSettingsBtn.addEventListener('click', () => {
  saveSettings();
});

// Emotional Event Test Buttons
document.querySelectorAll('.btn-event').forEach(btn => {
  btn.addEventListener('click', () => {
    const asset = btn.getAttribute('data-asset');
    // Pulse animation feedback
    btn.classList.add('btn-event-active');
    setTimeout(() => btn.classList.remove('btn-event-active'), 600);
    
    chrome.runtime.sendMessage({ type: 'TRIGGER_RANDOM_EVENT', asset }, () => {
      if (chrome.runtime.lastError) {
        console.warn('[Popup] TRIGGER_RANDOM_EVENT error:', chrome.runtime.lastError.message);
      }
    });
  });
});

// Shortcut Recording Logic
const shortcutButtons = document.querySelectorAll('.btn-shortcut');

function displaySavedShortcuts() {
  chrome.storage.local.get({ summonShortcuts: {} }, (data) => {
    const shortcuts = data.summonShortcuts || {};
    shortcutButtons.forEach(btn => {
      const asset = btn.getAttribute('data-asset');
      const combo = shortcuts[asset];
      if (combo) {
        btn.textContent = combo.displayText;
        btn.style.borderStyle = 'solid';
        btn.style.color = 'var(--color-primary)';
      } else {
        btn.textContent = '点击设置快捷键';
        btn.style.borderStyle = 'dashed';
        btn.style.color = '';
      }
    });
  });
}

// Initial display on load
displaySavedShortcuts();

shortcutButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.classList.contains('listening')) return;
    
    // Clear other active listeners
    shortcutButtons.forEach(b => {
      b.classList.remove('listening');
    });
    displaySavedShortcuts();
    
    btn.classList.add('listening');
    btn.textContent = '按键盘按键...';
    
    const handleRecording = (event) => {
      event.preventDefault();
      event.stopPropagation();
      
      const key = event.key;
      const code = event.code;
      const asset = btn.getAttribute('data-asset');
      
      // Clear shortcut if escape or backspace
      if (key === 'Escape' || key === 'Backspace') {
        chrome.storage.local.get({ summonShortcuts: {} }, (data) => {
          const shortcuts = data.summonShortcuts || {};
          delete shortcuts[asset];
          chrome.storage.local.set({ summonShortcuts: shortcuts }, () => {
            btn.classList.remove('listening');
            displaySavedShortcuts();
            window.removeEventListener('keydown', handleRecording, true);
          });
        });
        return;
      }
      
      // Wait for primary trigger key
      if (['Control', 'Alt', 'Shift', 'Meta'].includes(key)) {
        return;
      }
      
      const ctrl = event.ctrlKey;
      const alt = event.altKey;
      const shift = event.shiftKey;
      
      let keyName = key.toUpperCase();
      if (code.startsWith('Key')) {
        keyName = code.replace('Key', '');
      } else if (code.startsWith('Digit')) {
        keyName = code.replace('Digit', '');
      }
      
      let parts = [];
      if (ctrl) parts.push('Ctrl');
      if (alt) parts.push('Alt');
      if (shift) parts.push('Shift');
      parts.push(keyName);
      
      const displayText = parts.join(' + ');
      
      const combo = {
        ctrl,
        alt,
        shift,
        key: code, // Saved as code (e.g. 'KeyQ', 'Digit1') for layout safety
        displayText
      };
      
      chrome.storage.local.get({ summonShortcuts: {} }, (data) => {
        const shortcuts = data.summonShortcuts || {};
        shortcuts[asset] = combo;
        chrome.storage.local.set({ summonShortcuts: shortcuts }, () => {
          btn.classList.remove('listening');
          displaySavedShortcuts();
          window.removeEventListener('keydown', handleRecording, true);
        });
      });
    };
    
    window.addEventListener('keydown', handleRecording, true);
  });
});

// Load Settings from Local Storage
function loadSettings() {
  chrome.storage.local.get({
    focusDuration: 25,
    breakDuration: 5,
    task: '写代码',
    distractionPatterns: '',
    enabledDefaultDistractions: ['video', 'social', 'shorts'],
    blockMsg: 'Mando, 快回去工作！这不是正道！',
    blockerEnabled: true,
    soundEnabled: true
  }, (items) => {
    focusTimeInput.value = items.focusDuration;
    breakTimeInput.value = items.breakDuration;
    taskInput.value = items.task;
    distractionPatternsInput.value = items.distractionPatterns;
    defaultBlacklistToggles.forEach(toggle => {
      toggle.checked = items.enabledDefaultDistractions.includes(toggle.value);
    });
    blockMsgInput.value = items.blockMsg;
    blockerToggle.checked = items.blockerEnabled;
    soundToggle.checked = items.soundEnabled;
  });
}

// Save Settings to Storage
function saveSettings() {
  const focusVal = parseInt(focusTimeInput.value) || 25;
  const breakVal = parseInt(breakTimeInput.value) || 5;
  const taskVal = taskInput.value.trim();
  const distractionPatternsVal = distractionPatternsInput.value;
  const enabledDefaultDistractionsVal = Array.from(defaultBlacklistToggles)
    .filter(toggle => toggle.checked)
    .map(toggle => toggle.value);
  const blockMsgVal = blockMsgInput.value;
  const blockerVal = blockerToggle.checked;
  const soundVal = soundToggle.checked;

  chrome.storage.local.set({
    focusDuration: focusVal,
    breakDuration: breakVal,
    task: taskVal,
    distractionPatterns: distractionPatternsVal,
    enabledDefaultDistractions: enabledDefaultDistractionsVal,
    blockMsg: blockMsgVal,
    blockerEnabled: blockerVal,
    soundEnabled: soundVal
  }, () => {
    // Notify background script about setting updates and receive the updated state
    chrome.runtime.sendMessage({ type: 'SETTINGS_UPDATED' }, (updatedState) => {
      if (updatedState) {
        updateUI(updatedState);
      } else {
        syncTimerState();
      }
    });
    
    // Brief visual feedback on button
    const origText = saveSettingsBtn.textContent;
    saveSettingsBtn.textContent = '配置已保存';
    saveSettingsBtn.disabled = true;
    setTimeout(() => {
      saveSettingsBtn.textContent = origText;
      saveSettingsBtn.disabled = false;
    }, 1500);
  });
}

// Sync timer state with background script
let timerInterval = null;
function syncTimerState() {
  chrome.runtime.sendMessage({ type: 'GET_TIMER_STATE' }, (state) => {
    if (!state) return;
    updateUI(state);
    
    // Start local interval to count down smoothly in popup
    if (state.isRunning) {
      if (!timerInterval) {
        timerInterval = setInterval(() => {
          const now = Date.now();
          if (state.targetTime > now) {
            const timeLeft = Math.round((state.targetTime - now) / 1000);
            updateUI({ ...state, timeLeft });
          } else {
            clearInterval(timerInterval);
            timerInterval = null;
            syncTimerState();
          }
        }, 1000);
      }
    } else {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
    }
  });
}

// Update DOM elements based on state object
function updateUI(state) {
  // 1. Time display
  const minutes = Math.floor(state.timeLeft / 60);
  const seconds = state.timeLeft % 60;
  timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  
  // 2. Mode label
  if (state.mode === 'focus') {
    timerMode.textContent = '专注时间';
    timerMode.style.color = '#8fbc8f'; // Sage Green
  } else {
    timerMode.textContent = '休息时间';
    timerMode.style.color = '#00ffff'; // Force Cyan
  }

  // 3. Status text and circle glow
  if (state.isRunning) {
    statusText.textContent = '原力运行中';
    statusText.style.color = '#00ffff';
    timerCircle.classList.add('active');
    
    startBtn.disabled = true;
    pauseBtn.disabled = false;
  } else {
    statusText.textContent = '已暂停';
    statusText.style.color = '#94a3b8';
    timerCircle.classList.remove('active');
    
    startBtn.disabled = false;
    pauseBtn.disabled = true;
  }
}

// Handle incoming messages from background worker
function handleBackgroundMessage(message) {
  if (message.type === 'TIMER_TICK') {
    updateUI(message.state);
  }
}
