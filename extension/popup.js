// DOM Elements
const timerDisplay = document.getElementById('timer-display');
const timerMode = document.getElementById('timer-mode');
const statusText = document.getElementById('status-text');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const timerCircle = document.querySelector('.timer-circle');
const langBtn = document.getElementById('lang-btn');

// Config Form Elements
const focusTimeInput = document.getElementById('focus-time-input');
const breakTimeInput = document.getElementById('break-time-input');
const taskInput = document.getElementById('task-input');
const distractionPatternsInput = document.getElementById('distraction-patterns-input');
const defaultBlacklistToggles = document.querySelectorAll('.default-blacklist-toggle');
const blockMsgInput = document.getElementById('block-msg-input');
const welcomeMsgInput = document.getElementById('welcome-msg-input');
const blockerToggle = document.getElementById('blocker-toggle');
const soundToggle = document.getElementById('sound-toggle');
const saveSettingsBtn = document.getElementById('save-settings-btn');

// Bilingual Data Dictionary
const I18N_DATA = {
  zh: {
    title: '原力专注 <span>GROGU</span>',
    status_ready: '就绪',
    status_running: '原力运行中',
    status_paused: '已暂停',
    mode_focus: '专注时间',
    mode_break: '休息时间',
    btn_start: '开启原力',
    btn_pause: '暂停',
    btn_reset: '重置',
    config_header: '配置面板',
    focus_duration: '专注时长 (分钟)',
    break_duration: '休息时长 (分钟)',
    task_label: '我当前要做的任务 (当前专注内容)',
    task_placeholder: '例如：写代码、写论文、看书',
    blacklist_label: '默认分心黑名单',
    blacklist_video: '视频/短剧',
    blacklist_social: '社交媒体',
    blacklist_shorts: '短视频关键词',
    blacklist_games: '游戏/直播',
    blacklist_forums: '论坛热点',
    blacklist_shopping: '购物网站',
    custom_blacklist_label: '自定义分心关键词 / 正则 (一行一个)',
    block_msg_label: 'NO 自定义提示语 (当你想偷懒分心时)',
    welcome_msg_label: 'YES 自定义提示语 (当你回到工作页面时)',
    blocker_toggle_label: '启用分心自动劝阻 (YES / NO 联动)',
    sound_toggle_label: '启用声音提醒',
    btn_save: '保存并更新配置',
    btn_saved: '配置已保存',
    summon_header: '召唤古古',
    summon_hint: '点击左侧召唤。全局召唤：Alt+Shift+G；右侧是网页内快捷键（chrome:// 页面不可用）。',
    btn_shortcut_set: '点击设置快捷键',
    btn_shortcut_listening: '按键盘按键...',
    
    // Events
    ev_cookie1: '🍪 吃点马卡龙吧',
    ev_cookie2: '🍬 再吃点马卡龙',
    ev_meat: '🍖 吃点龙肉吧',
    ev_eggs: '🐸 你还好意思吃',
    ev_peek: '👀 偷偷瞅你一眼',
    ev_fagong: '✨ 发功',
    ev_zhaoshou: '👋 招招手'
  },
  en: {
    title: 'Force Focus <span>GROGU</span>',
    status_ready: 'Ready',
    status_running: 'Force Running',
    status_paused: 'Paused',
    mode_focus: 'Focus Time',
    mode_break: 'Break Time',
    btn_start: 'Enable Force',
    btn_pause: 'Pause',
    btn_reset: 'Reset',
    config_header: 'Configuration',
    focus_duration: 'Focus Duration (mins)',
    break_duration: 'Break Duration (mins)',
    task_label: 'My Current Task (Focus Target)',
    task_placeholder: 'e.g. Coding, Writing, Reading',
    blacklist_label: 'Default Blacklist Categories',
    blacklist_video: 'Video / TV Shows',
    blacklist_social: 'Social Media',
    blacklist_shorts: 'Short Video Keywords',
    blacklist_games: 'Gaming / Live Streams',
    blacklist_forums: 'Forums / Hot Topics',
    blacklist_shopping: 'Shopping Sites',
    custom_blacklist_label: 'Custom Distraction Keywords / RegEx (one per line)',
    block_msg_label: 'NO Custom Alert Message (when slacking)',
    welcome_msg_label: 'YES Custom Welcome Message (when returning to work)',
    blocker_toggle_label: 'Enable Auto-Blocker & Warnings (YES/NO)',
    sound_toggle_label: 'Enable Sound Effects',
    btn_save: 'Save Settings',
    btn_saved: 'Settings Saved',
    summon_header: 'Summon Grogu',
    summon_hint: 'Click left button to summon. Global hotkey: Alt+Shift+G. Right button sets in-page hotkey.',
    btn_shortcut_set: 'Set Hotkey',
    btn_shortcut_listening: 'Press any key...',
    
    // Events
    ev_cookie1: '🍪 Snack Macarons',
    ev_cookie2: '🍬 Eat Blue Cookies',
    ev_meat: '🍖 Grill Dragon Meat',
    ev_eggs: '🐸 Eat Frog Eggs?',
    ev_peek: '👀 Peek at you',
    ev_fagong: '✨ Use the Force',
    ev_zhaoshou: '👋 Wave Hello'
  }
};

const I18N_MAP = {
  'title-text': 'title',
  'start-btn': 'btn_start',
  'pause-btn': 'btn_pause',
  'reset-btn': 'btn_reset',
  'config-header': 'config_header',
  'focus-time-label': 'focus_duration',
  'break-time-label': 'break_duration',
  'task-label': 'task_label',
  'blacklist-label': 'blacklist_label',
  'lbl-blacklist-video': 'blacklist_video',
  'lbl-blacklist-social': 'blacklist_social',
  'lbl-blacklist-shorts': 'blacklist_shorts',
  'lbl-blacklist-games': 'blacklist_games',
  'lbl-blacklist-forums': 'blacklist_forums',
  'lbl-blacklist-shopping': 'blacklist_shopping',
  'custom-blacklist-label': 'custom_blacklist_label',
  'block-msg-label': 'block_msg_label',
  'welcome-msg-label': 'welcome_msg_label',
  'blocker-toggle-label': 'blocker_toggle_label',
  'sound-toggle-label': 'sound_toggle_label',
  'save-settings-btn': 'btn_save',
  'summon-header': 'summon_header',
  'summon-hint': 'summon_hint',
  
  // Events
  'ev-cookie1': 'ev_cookie1',
  'ev-cookie2': 'ev_cookie2',
  'ev-meat': 'ev_meat',
  'ev-eggs': 'ev_eggs',
  'ev-peek': 'ev_peek',
  'ev-fagong': 'ev_fagong',
  'ev-zhaoshou': 'ev_zhaoshou'
};

let currentLang = 'zh';

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

langBtn.addEventListener('click', () => {
  const nextLang = currentLang === 'zh' ? 'en' : 'zh';
  changeLanguage(nextLang);
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
        btn.textContent = I18N_DATA[currentLang].btn_shortcut_set;
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
    btn.textContent = I18N_DATA[currentLang].btn_shortcut_listening;
    
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

// Apply dynamic translations
function applyLanguage(lang) {
  currentLang = lang;
  const data = I18N_DATA[lang];
  
  // Apply text mapping
  for (const [id, key] of Object.entries(I18N_MAP)) {
    const el = document.getElementById(id);
    if (el) {
      if (id === 'title-text') {
        el.innerHTML = data[key];
      } else {
        el.textContent = data[key];
      }
    }
  }
  
  // Apply inputs placeholder
  taskInput.placeholder = data.task_placeholder;
  distractionPatternsInput.placeholder = lang === 'en' ? 'e.g. youtube.com\nbilibili.com' : '例如：youtube.com\nbilibili.com';
  
  // Language button text toggler
  langBtn.textContent = lang === 'zh' ? 'EN' : '中';
  
  // Refresh shortcuts button texts
  displaySavedShortcuts();
  
  // Update state text
  syncTimerState();
}

// Change language globally
function changeLanguage(newLang) {
  currentLang = newLang;
  
  // Auto translate defaults to respect language choices
  if (newLang === 'en') {
    if (taskInput.value.trim() === '写代码') taskInput.value = 'Coding';
    
    // Auto-translate NO blockMsg variants
    const currentBlockVal = blockMsgInput.value.trim();
    if (currentBlockVal === 'Mando, 快回去工作！环境这不是正道！' || 
        currentBlockVal === 'Mando, 快回去工作！这不是正道！' ||
        currentBlockVal === 'Mando, 回去工作，这不是正道' ||
        currentBlockVal === 'Mando, 回去工作，这不是正道.') {
      blockMsgInput.value = 'Mando, get back to work! This is not the way!';
    }
    
    // Auto-translate YES welcomeMsg variants
    const currentWelcomeVal = welcomeMsgInput.value.trim();
    if (currentWelcomeVal === 'Mando, 欢迎回来！This is the way.' ||
        currentWelcomeVal === 'Mando, 欢迎回来，This is the way.' ||
        currentWelcomeVal === 'Mando, 欢迎回来，This is the way') {
      welcomeMsgInput.value = 'Mando, welcome back! This is the way.';
    }
  } else {
    if (taskInput.value.trim() === 'Coding') taskInput.value = '写代码';
    
    // Auto-translate back to Chinese
    if (blockMsgInput.value.trim() === 'Mando, get back to work! This is not the way!') {
      blockMsgInput.value = 'Mando, 回去工作，这不是正道.';
    }
    if (welcomeMsgInput.value.trim() === 'Mando, welcome back! This is the way.') {
      welcomeMsgInput.value = 'Mando, 欢迎回来，This is the way.';
    }
  }
  
  chrome.storage.local.set({ lang: newLang }, () => {
    // Notify background to update settings
    chrome.runtime.sendMessage({ type: 'SETTINGS_UPDATED' });
    applyLanguage(newLang);
  });
}

// Load Settings from Local Storage
function loadSettings() {
  chrome.storage.local.get({
    focusDuration: 25,
    breakDuration: 5,
    task: '写代码',
    distractionPatterns: '',
    enabledDefaultDistractions: ['video', 'social', 'shorts'],
    blockMsg: 'Mando, 回去工作，这不是正道.',
    welcomeMsg: 'Mando, 欢迎回来，This is the way.',
    blockerEnabled: true,
    soundEnabled: true,
    lang: 'zh'
  }, (items) => {
    currentLang = items.lang;
    applyLanguage(currentLang); // Apply translations first
    
    focusTimeInput.value = items.focusDuration;
    breakTimeInput.value = items.breakDuration;
    taskInput.value = items.task;
    distractionPatternsInput.value = items.distractionPatterns;
    defaultBlacklistToggles.forEach(toggle => {
      toggle.checked = items.enabledDefaultDistractions.includes(toggle.value);
    });
    blockMsgInput.value = items.blockMsg;
    welcomeMsgInput.value = items.welcomeMsg;
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
  const welcomeMsgVal = welcomeMsgInput.value;
  const blockerVal = blockerToggle.checked;
  const soundVal = soundToggle.checked;

  chrome.storage.local.set({
    focusDuration: focusVal,
    breakDuration: breakVal,
    task: taskVal,
    distractionPatterns: distractionPatternsVal,
    enabledDefaultDistractions: enabledDefaultDistractionsVal,
    blockMsg: blockMsgVal,
    welcomeMsg: welcomeMsgVal,
    blockerEnabled: blockerVal,
    soundEnabled: soundVal,
    lang: currentLang
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
    saveSettingsBtn.textContent = I18N_DATA[currentLang].btn_saved;
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
    timerMode.textContent = I18N_DATA[currentLang].mode_focus;
    timerMode.style.color = '#8fbc8f'; // Sage Green
  } else {
    timerMode.textContent = I18N_DATA[currentLang].mode_break;
    timerMode.style.color = '#00ffff'; // Force Cyan
  }

  // 3. Status text and circle glow
  if (state.isRunning) {
    statusText.textContent = I18N_DATA[currentLang].status_running;
    statusText.style.color = '#00ffff';
    timerCircle.classList.add('active');
    
    startBtn.disabled = true;
    pauseBtn.disabled = false;
  } else {
    const isReady = state.timeLeft === (state.mode === 'focus' ? parseInt(focusTimeInput.value) || 25 : parseInt(breakTimeInput.value) || 5) * 60;
    statusText.textContent = isReady ? I18N_DATA[currentLang].status_ready : I18N_DATA[currentLang].status_paused;
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
