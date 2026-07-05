let timerState = {
  isRunning: false,
  mode: 'focus', // 'focus' or 'break'
  timeLeft: 25 * 60, // seconds
  targetTime: 0 // timestamp
};

// Default configs
let config = {
  focusDuration: 25,
  breakDuration: 5,
  task: '写代码',
  distractionPatterns: '',
  enabledDefaultDistractions: ['video', 'social', 'shorts'],
  blockMsg: 'Mando, 快回去工作！环境这不是正道！',
  welcomeMsg: 'Mando, 欢迎回来！This is the way.',
  blockerEnabled: true,
  soundEnabled: true,
  lang: 'zh'
};

const DEFAULT_DISTRACTION_GROUPS = {
  video: ['youtube\\.com', 'bilibili\\.com', 'douyin\\.com', 'kuaishou\\.com', 'iqiyi\\.com', 'youku\\.com', 'qq\\.com/x/cover', 'v\\.qq\\.com', 'mgtv\\.com', 'le\\.com', 'sohu\\.com/tv', 'ixigua\\.com', 'hongguoduanju\\.com', 'duanju', 'drama'],
  social: ['weibo\\.com', 'x\\.com', 'twitter\\.com', 'instagram\\.com', 'facebook\\.com', 'threads\\.net'],
  shorts: ['shorts', 'reels'],
  games: ['steampowered\\.com', 'store\\.steamcommunity\\.com', 'epicgames\\.com', 'twitch\\.tv', 'douyu\\.com', 'huya\\.com', 'taptap\\.cn', '4399\\.com'],
  forums: ['tieba\\.baidu\\.com', 'zhihu\\.com/hot', 'reddit\\.com'],
  shopping: ['taobao\\.com', 'jd\\.com', 'pinduoduo\\.com', 'amazon\\.com']
};

// Track distraction state globally
let isDistracted = false;
let activeBlockerTabs = new Set();

// Random emotional event lists
const RANDOM_EVENTS_ZH = [
  { asset: 'cookie1', message: '哇，古古在啃零食！快回来继续工作，一起努力吧～ 🍪' },
  { asset: 'cookie2', message: '古古正在大口享用蓝色饼干，你的代码是它最好的陪伴！ 🍬' },
  { asset: 'meat',    message: '古古在烤肉串串！香味飘来，继续努力，Mando！🍖' },
  { asset: 'eggs',    message: '古古发现了神秘的蛙卵... 它在思考，你也在吗？🐸' },
  { asset: 'peek',    message: '古古正在暗中观察... 瞅瞅你有没有认真工作！👀' },
  { asset: 'fagong',  message: '古古正在发功... 原力充能中！ ✨' },
  { asset: 'zhaoshou', message: '古古在向你热情地招手！原力与你同在，打起精神来～👋' }
];

const RANDOM_EVENTS_EN = [
  { asset: 'cookie1', message: 'Wow, Grogu is snacking! Get back to work and let\'s work hard together~ 🍪' },
  { asset: 'cookie2', message: 'Grogu is enjoying blue cookies. Your code is its best companion! 🍬' },
  { asset: 'meat',    message: 'Grogu is grilling meat skewers! Smells good, keep going, Mando! 🍖' },
  { asset: 'eggs',    message: 'Grogu found mysterious frog eggs... It is thinking, are you? 🐸' },
  { asset: 'peek',    message: 'Grogu is watching you in the dark... Checking if you are working hard! 👀' },
  { asset: 'fagong',  message: 'Grogu is using the Force... Charging up! ✨' },
  { asset: 'zhaoshou', message: 'Grogu is waving at you warmly! May the Force be with you, cheer up~ 👋' }
];

const NOTIFICATIONS = {
  zh: {
    focus_ended: 'Mando, 专注时间结束啦！来喝口热汤休息一下！',
    break_ended: '休息时间结束！原力与你同在，开始工作！'
  },
  en: {
    focus_ended: 'Mando, focus session completed! Time to drink some soup and take a break! 🍲',
    break_ended: 'Break session completed! May the Force be with you, back to work! 🚀'
  }
};
let initPromise = null;

// Initialize settings and sync on startup
chrome.runtime.onStartup.addListener(init);
chrome.runtime.onInstalled.addListener(init);
init();

if (chrome.sidePanel && chrome.sidePanel.setPanelBehavior) {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch((error) => {
    console.log('[SidePanel] Could not set action-click behavior:', error.message);
  });
}

chrome.action.onClicked.addListener(async (tab) => {
  try {
    if (chrome.sidePanel && chrome.sidePanel.open) {
      await chrome.sidePanel.open({ tabId: tab.id });
      return;
    }
  } catch (error) {
    console.log('[SidePanel] Falling back to popup window:', error.message);
  }

  chrome.windows.create({
    url: 'popup.html',
    type: 'popup',
    width: 390,
    height: 720
  });
});

if (chrome.commands && chrome.commands.onCommand) {
  chrome.commands.onCommand.addListener((command) => {
    if (command !== 'summon-grogu') return;

    const list = (config.lang === 'en') ? RANDOM_EVENTS_EN : RANDOM_EVENTS_ZH;
    const event = list[Math.floor(Math.random() * list.length)];
    console.log(`[Shortcut] Summoning Grogu via command: ${event.asset}`);
    triggerRandomEvent(event);
  });
}

function init() {
  initPromise = new Promise((resolve) => {
    chrome.storage.local.get({
    focusDuration: 25,
    breakDuration: 5,
    task: '写代码',
    distractionPatterns: '',
    enabledDefaultDistractions: ['video', 'social', 'shorts'],
    blockMsg: 'Mando, 快回去工作！环境这不是正道！',
    welcomeMsg: 'Mando, 欢迎回来！This is the way.',
    blockerEnabled: true,
    soundEnabled: true,
    lang: 'zh',
    timerState: null
  }, (items) => {
    config.focusDuration = items.focusDuration;
    config.breakDuration = items.breakDuration;
    config.task = items.task;
    config.distractionPatterns = items.distractionPatterns;
    config.enabledDefaultDistractions = items.enabledDefaultDistractions;
    config.blockMsg = items.blockMsg;
    config.welcomeMsg = items.welcomeMsg;
    config.blockerEnabled = items.blockerEnabled;
    config.soundEnabled = items.soundEnabled;
    config.lang = items.lang || 'zh';

    isDistracted = false;

    if (items.timerState) {
      timerState = items.timerState;
      if (timerState.isRunning) {
        const now = Date.now();
        if (timerState.targetTime > now) {
          timerState.timeLeft = Math.round((timerState.targetTime - now) / 1000);
          chrome.alarms.create('grogu_alarm', { when: timerState.targetTime });
          
          // Re-establish random event alarm if missing
          chrome.alarms.get('grogu_random_event', (alarm) => {
            if (!alarm && timerState.mode === 'focus') {
              scheduleNextRandomEvent();
            }
          });
        } else {
          timerState.isRunning = false;
          timerState.timeLeft = 0;
        }
      }
    } else {
      timerState.timeLeft = config.focusDuration * 60;
    }
      saveState();
      resolve();
    });
  });
  return initPromise;
}

function saveState() {
  chrome.storage.local.set({ timerState });
}

// Determine tab category: 'neutral' or 'distraction'.
function getTabRelevanceCategory(url, title) {
  const lowercaseUrl = url.toLowerCase();
  const lowercaseTitle = title.toLowerCase();

  // System browser pages cannot be scripted and should never trigger blockers.
  if (
    lowercaseUrl.startsWith('chrome://') ||
    lowercaseUrl.startsWith('chrome-extension://') ||
    lowercaseUrl.startsWith('about:') ||
    lowercaseUrl.startsWith('edge://') ||
    lowercaseUrl.startsWith('file://') ||
    lowercaseUrl === ''
  ) {
    return 'neutral';
  }

  return matchesDistractionPattern(lowercaseUrl) || matchesDistractionPattern(lowercaseTitle)
    ? 'distraction'
    : 'neutral';
}

// Get full list of distraction regex patterns
function getDistractionPatterns() {
  const defaultPatterns = (config.enabledDefaultDistractions || [])
    .flatMap(group => DEFAULT_DISTRACTION_GROUPS[group] || []);
  const customPatterns = (config.distractionPatterns || '')
    .split(/\r?\n|,/)
    .map(pattern => pattern.trim())
    .filter(Boolean);

  return [...defaultPatterns, ...customPatterns];
}

function matchesDistractionPattern(text) {
  return getDistractionPatterns().some(pattern => {
    try {
      return new RegExp(pattern, 'i').test(text);
    } catch (e) {
      console.log(`[Blocker] Ignoring invalid distraction pattern: ${pattern}`);
      return false;
    }
  });
}

// Listen for messages from popup or content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_TIMER_STATE' && initPromise) {
    initPromise.then(() => {
      if (timerState.isRunning) {
        const now = Date.now();
        timerState.timeLeft = Math.max(0, Math.round((timerState.targetTime - now) / 1000));
      }
      sendResponse(timerState);
    });
    return true;
  }

  if (message.type === 'GET_TIMER_STATE') {
    if (timerState.isRunning) {
      const now = Date.now();
      timerState.timeLeft = Math.max(0, Math.round((timerState.targetTime - now) / 1000));
    }
    sendResponse(timerState);
  }

  else if (message.type === 'START_TIMER') {
    if (!timerState.isRunning) {
      timerState.isRunning = true;
      timerState.targetTime = Date.now() + timerState.timeLeft * 1000;
      isDistracted = false;
      saveState();
      
      chrome.alarms.create('grogu_alarm', { when: timerState.targetTime });
      scheduleNextRandomEvent();
      console.log(`Timer started. Alarm set for: ${new Date(timerState.targetTime).toLocaleTimeString()}`);
      
      // Evaluate distraction blocker immediately on timer start
      checkActiveTabBlock();
    }
    sendResponse(timerState);
  }

  else if (message.type === 'PAUSE_TIMER') {
    if (timerState.isRunning) {
      timerState.isRunning = false;
      timerState.timeLeft = Math.max(0, Math.round((timerState.targetTime - Date.now()) / 1000));
      saveState();
      
      chrome.alarms.clear('grogu_alarm');
      stopRandomEventScheduler();
      clearAllBlockers();
      console.log('Timer paused.');
    }
    sendResponse(timerState);
  }

  else if (message.type === 'RESET_TIMER') {
    timerState.isRunning = false;
    timerState.mode = 'focus';
    timerState.timeLeft = config.focusDuration * 60;
    isDistracted = false;
    saveState();
    
    chrome.alarms.clear('grogu_alarm');
    stopRandomEventScheduler();
    clearAllBlockers();
    console.log('Timer reset.');
    sendResponse(timerState);
  }

  else if (message.type === 'TRIGGER_RANDOM_EVENT') {
    const eventName = message.asset;
    const list = (config.lang === 'en') ? RANDOM_EVENTS_EN : RANDOM_EVENTS_ZH;
    const event = list.find(e => e.asset === eventName)
      || list[Math.floor(Math.random() * list.length)];
    triggerRandomEvent(event);
    sendResponse({ ok: true });
  }
  else if (message.type === 'PLAY_INTERACTION_AUDIO') {
    playAudio(`assets/${message.sound}`);
    sendResponse({ ok: true });
  }

  else if (message.type === 'SETTINGS_UPDATED') {
    chrome.storage.local.get({
      focusDuration: 25,
      breakDuration: 5,
      task: '写代码',
      distractionPatterns: '',
      enabledDefaultDistractions: ['video', 'social', 'shorts'],
      blockMsg: 'Mando, 快回去工作！环境这不是正道！',
      welcomeMsg: 'Mando, 欢迎回来！This is the way.',
      blockerEnabled: true,
      soundEnabled: true,
      lang: 'zh'
    }, (items) => {
      config.focusDuration = items.focusDuration;
      config.breakDuration = items.breakDuration;
      config.task = items.task;
      config.distractionPatterns = items.distractionPatterns;
      config.enabledDefaultDistractions = items.enabledDefaultDistractions;
      config.blockMsg = items.blockMsg;
      config.welcomeMsg = items.welcomeMsg;
      config.blockerEnabled = items.blockerEnabled;
      config.soundEnabled = items.soundEnabled;
      config.lang = items.lang || 'zh';
      
      if (!timerState.isRunning) {
        timerState.timeLeft = (timerState.mode === 'focus' ? config.focusDuration : config.breakDuration) * 60;
        saveState();
      } else {
        // Re-evaluate current active page distraction state under new settings
        checkActiveTabBlock();
      }
      sendResponse(timerState);
    });
    return true; // Keep message channel open for async response
  }
  return true;
});

// ─── Random Emotional Event Scheduler ───────────────────────────────────────
function scheduleNextRandomEvent() {
  stopRandomEventScheduler();
  if (!timerState.isRunning || timerState.mode !== 'focus') return;

  let delayMinutes;
  if (config.focusDuration <= 2) {
    delayMinutes = 0.25 + Math.random() * 0.4;
  } else if (config.focusDuration <= 10) {
    delayMinutes = 1 + Math.random() * 1;
  } else {
    delayMinutes = 5 + Math.random() * 5;
  }

  console.log(`[RandomEvent] Next event scheduled in ${delayMinutes.toFixed(2)} min(s).`);
  chrome.alarms.create('grogu_random_event', { delayInMinutes: delayMinutes });
}

function stopRandomEventScheduler() {
  chrome.alarms.clear('grogu_random_event');
}

function triggerRandomEvent(event) {
  console.log(`[RandomEvent] Firing event: ${event.asset}`);
  playAudio(`assets/${event.asset}.m4a`);
  injectOverlayToActiveTab(event.asset, event.message, { motion: 'drift' });
}

// Alarm Listener
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'grogu_alarm') {
    timerState.isRunning = false;
    isDistracted = false;
    clearAllBlockers();
    
    if (timerState.mode === 'focus') {
      console.log('Focus completed! Triggering break warning.');
      playAudio('assets/soup.m4a');
      const lang = config.lang || 'zh';
      const msg = lang === 'en' ? NOTIFICATIONS.en.focus_ended : NOTIFICATIONS.zh.focus_ended;
      injectOverlayToActiveTab('soup', msg);
      
      timerState.mode = 'break';
      timerState.timeLeft = config.breakDuration * 60;
    } else {
      console.log('Break completed! Triggering focus warning.');
      playAudio('assets/force.m4a');
      const lang = config.lang || 'zh';
      const msg = lang === 'en' ? NOTIFICATIONS.en.break_ended : NOTIFICATIONS.zh.break_ended;
      injectOverlayToActiveTab('force', msg);
      
      timerState.mode = 'focus';
      timerState.timeLeft = config.focusDuration * 60;
    }
    
    saveState();
    chrome.runtime.sendMessage({ type: 'TIMER_TICK', state: timerState });
  } else if (alarm.name === 'grogu_random_event') {
    if (timerState.isRunning && timerState.mode === 'focus') {
      const list = (config.lang === 'en') ? RANDOM_EVENTS_EN : RANDOM_EVENTS_ZH;
      const event = list[Math.floor(Math.random() * list.length)];
      triggerRandomEvent(event);
      scheduleNextRandomEvent();
    }
  }
});

// Browser tab navigation listeners
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading') {
    activeBlockerTabs.delete(tabId);
    return;
  }
  if (tab.status === 'complete' && (changeInfo.status === 'complete' || changeInfo.url) && tab.url) {
    checkAndApplyTabBlock(tabId, tab.url, tab.title || '');
  }
});

chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab && tab.url) {
      checkAndApplyTabBlock(activeInfo.tabId, tab.url, tab.title || '');
    }
  });
});

// Window Focus Change Listener
chrome.windows.onFocusChanged.addListener((windowId) => {
  if (!config.blockerEnabled || timerState.mode !== 'focus' || !timerState.isRunning) {
    return;
  }
  
  if (windowId === chrome.windows.WINDOW_ID_NONE) {
    return;
  } else {
    chrome.tabs.query({ active: true, windowId: windowId }, (tabs) => {
      if (tabs && tabs[0] && tabs[0].url) {
        const category = getTabRelevanceCategory(tabs[0].url, tabs[0].title || '');
        
        if (category === 'neutral') {
          activeBlockerTabs.delete(tabs[0].id);
          if (isDistracted) {
            console.log(`[Blocker] Switched to non-blocklisted tab ${tabs[0].id}. Triggering YES.`);
            isDistracted = false;
            playAudio('assets/YES.m4a');
            const welcomeMsg = config.welcomeMsg || 'Mando, 欢迎回来！This is the way.';
            sendTabMessage(tabs[0].id, {
              type: 'INJECT_NOTIFICATION',
              asset: 'YES',
              message: welcomeMsg,
              motion: 'peek'
            });
          }
        } else {
          activeBlockerTabs.add(tabs[0].id);
          const assetName = Math.random() > 0.5 ? 'NO' : 'NO2';
          
          sendTabMessage(tabs[0].id, {
            type: 'INJECT_BLOCKER',
            asset: assetName,
            message: config.blockMsg,
            motion: 'alert'
          });

          if (!isDistracted) {
            isDistracted = true;
            playAudio(`assets/${assetName}.m4a`);
          }
        }
      }
    });
  }
});

function checkAndApplyTabBlock(tabId, url, title) {
  if (!config.blockerEnabled || timerState.mode !== 'focus' || !timerState.isRunning) {
    return;
  }

  try {
    const category = getTabRelevanceCategory(url, title);
    
    if (category === 'neutral') {
      activeBlockerTabs.delete(tabId);
      
      if (isDistracted) {
        console.log(`[Blocker] Switched to non-blocklisted tab ${tabId} (${url}). Triggering YES.`);
        isDistracted = false;
        playAudio('assets/YES.m4a');
        const welcomeMsg = config.welcomeMsg || 'Mando, 欢迎回来！This is the way.';
        sendTabMessage(tabId, {
          type: 'INJECT_NOTIFICATION',
          asset: 'YES',
          message: welcomeMsg,
          motion: 'peek'
        });
      }
    } else {
      console.log(`[Blocker] Tab ${tabId} matches distraction pattern (${url}). Triggering NO.`);
      activeBlockerTabs.add(tabId);
      const assetName = Math.random() > 0.5 ? 'NO' : 'NO2';
      const warningMsg = config.blockMsg;
      
      sendTabMessage(tabId, {
        type: 'INJECT_BLOCKER',
        asset: assetName,
        message: warningMsg,
        motion: 'alert'
      });

      if (!isDistracted) {
        isDistracted = true;
        playAudio(`assets/${assetName}.m4a`);
      }
    }
  } catch (e) {
    // Ignore
  }
}

// Resilient tab message sender
function sendTabMessage(tabId, msg) {
  chrome.tabs.get(tabId, (tab) => {
    if (chrome.runtime.lastError || !tab || !tab.url) return;
    
    const url = tab.url.toLowerCase();
    if (
      url.startsWith('chrome://') ||
      url.startsWith('edge://') ||
      url.startsWith('about:') ||
      url.startsWith('chrome-extension://')
    ) {
      return;
    }

    chrome.tabs.sendMessage(tabId, msg, (response) => {
      if (chrome.runtime.lastError) {
        chrome.scripting.executeScript({
          target: { tabId: tabId },
          files: ['content.js']
        }).then(() => {
          chrome.scripting.insertCSS({
            target: { tabId: tabId },
            files: ['content.css']
          }).then(() => {
            chrome.tabs.sendMessage(tabId, msg, () => {
              if (chrome.runtime.lastError) {} // Ignore
            });
          });
        }).catch((e) => {
          console.log('[Scripting] Suppressed script injection error:', e.message);
        });
      }
    });
  });
}

// Inject overlay to active tab helper
function injectOverlayToActiveTab(asset, msg, options = {}) {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    if (tabs && tabs[0]) {
      sendTabMessage(tabs[0].id, {
        type: 'INJECT_NOTIFICATION',
        asset: asset,
        message: msg,
        motion: options.motion,
        bubble: options.bubble
      });
    }
  });
}

function clearAllBlockers() {
  for (const tabId of activeBlockerTabs) {
    chrome.tabs.sendMessage(tabId, { type: 'CLEAR_BLOCKER' }, () => {
      if (chrome.runtime.lastError) {}
    });
  }
  activeBlockerTabs.clear();
}

// Audio player using Chrome Offscreen Document
async function playAudio(soundFile) {
  if (!config.soundEnabled) {
    console.log('[Audio] Muted by user setting.');
    return;
  }

  const absoluteUrl = chrome.runtime.getURL(soundFile);
  
  let contexts = await chrome.runtime.getContexts({
    contextTypes: ['OFFSCREEN_DOCUMENT']
  });
  
  if (contexts.length === 0) {
    try {
      await chrome.offscreen.createDocument({
        url: 'offscreen.html',
        reasons: ['AUDIO_PLAYBACK'],
        justification: 'Play sound notifications'
      });
      await new Promise(resolve => setTimeout(resolve, 100));
    } catch (e) {
      console.log('[Audio] Suppressed duplicate offscreen document creation:', e.message);
    }
  }
  
  chrome.runtime.sendMessage({
    type: 'PLAY_AUDIO',
    file: absoluteUrl
  }, (response) => {
    if (chrome.runtime.lastError) {
      const errMsg = chrome.runtime.lastError.message;
      if (errMsg.includes("Could not establish connection") || errMsg.includes("Receiving end does not exist")) {
        setTimeout(() => {
          chrome.runtime.sendMessage({
            type: 'PLAY_AUDIO',
            file: absoluteUrl
          }, () => {
            if (chrome.runtime.lastError) {
              console.error('[Audio] Playback failed after retry:', chrome.runtime.lastError.message);
            }
          });
        }, 150);
      }
    }
  });
}
