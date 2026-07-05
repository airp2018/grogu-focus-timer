chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'INJECT_NOTIFICATION' || message.type === 'INJECT_BLOCKER') {
    createGroguAssistant(message.asset, message.message, {
      motion: message.motion,
      bubble: message.bubble
    });
    sendResponse({ success: true });
  } else if (message.type === 'CLEAR_BLOCKER') {
    const container = document.querySelector('.grogu-fa-container');
    if (container) {
      container.classList.remove('grogu-fa-show');
      setTimeout(() => {
        const root = document.getElementById('grogu-fa-root');
        if (root && root.contains(container)) {
          root.removeChild(container);
        }
      }, 600);
    }
    sendResponse({ success: true });
  }
  return true;
});

function chooseDefaultMotion(assetName) {
  if (assetName === 'NO' || assetName === 'NO2') return 'alert';
  if (assetName === 'YES') return 'peek';
  if (['cookie1', 'cookie2', 'meat', 'eggs', 'peek', 'fagong', 'zhaoshou'].includes(assetName)) return 'drift';
  return 'dock';
}

function createGroguAssistant(assetName, messageText, options = {}) {
  const motion = options.motion || chooseDefaultMotion(assetName);
  const isRandomEvent = ['cookie1', 'cookie2', 'meat', 'eggs', 'peek', 'fagong', 'zhaoshou'].includes(assetName);
  const showBubble = isRandomEvent ? false : (options.bubble !== false);
  const driftRoutes = {
    cookie1: 'across',
    cookie2: 'up',
    meat: 'up-right',
    eggs: 'down-right',
    peek: 'across',
    fagong: 'up-right',
    zhaoshou: 'across'
  };

  // 1. Check if root container exists, or create it
  let root = document.getElementById('grogu-fa-root');
  if (!root) {
    root = document.createElement('div');
    root.id = 'grogu-fa-root';
    document.body.appendChild(root);
  }

  // 2. Clear any existing assistant widget to avoid duplication
  root.replaceChildren();

  // 3. Build container
  const container = document.createElement('div');
  container.className = 'grogu-fa-container';
  container.classList.add(`grogu-fa-mode-${motion}`);
  if (!showBubble) {
    container.classList.add('grogu-fa-no-bubble');
  }

  if (motion === 'drift') {
    container.classList.add(`grogu-fa-drift-${driftRoutes[assetName] || 'across'}`);
    const driftBottom = 16 + Math.round(Math.random() * 42);
    container.style.setProperty('--grogu-fa-drift-bottom', `${driftBottom}vh`);
  } else if (motion === 'peek') {
    const peekBottom = 12 + Math.round(Math.random() * 44);
    container.style.setProperty('--grogu-fa-peek-bottom', `${peekBottom}vh`);
  }

  let styleClass = 'grogu-fa-yes-style';
  if (assetName === 'NO' || assetName === 'NO2') {
    styleClass = 'grogu-fa-no-style';
  } else if (assetName === 'YES') {
    styleClass = 'grogu-fa-yes-style';
  } else if (['cookie1', 'cookie2', 'meat', 'eggs', 'peek', 'fagong', 'zhaoshou'].includes(assetName)) {
    styleClass = `grogu-fa-${assetName}-style`;
  }
  container.classList.add(styleClass);

  // 4. Build speech bubble
  const speechBubble = document.createElement('div');
  speechBubble.className = 'grogu-fa-speech-bubble';
  speechBubble.textContent = messageText;
  container.appendChild(speechBubble);

  // 5. Build avatar wrapper
  // 5. Build avatar wrapper (the main circular container)
  const avatarWrapper = document.createElement('div');
  avatarWrapper.className = 'grogu-fa-avatar-wrapper';

  // 6. Build avatar image
  const avatar = document.createElement('img');
  avatar.className = 'grogu-fa-avatar';
  avatar.src = chrome.runtime.getURL(`assets/${assetName}.webp`);
  avatar.alt = 'Grogu';
  avatarWrapper.appendChild(avatar);

  // 6.5. Build cradle SVG overlay. Keep the existing circular mask, but make
  // the lower shell read more like Grogu's worn white hover-pram.
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = `
    <svg class="grogu-fa-cradle-svg" viewBox="0 0 130 130">
      <path class="cradle-cavity" d="M 4,67 Q 65,52 126,67 Q 65,82 4,67 Z" />
      <path class="cradle-cavity-shadow" d="M 10,68 Q 65,58 120,68 Q 65,76 10,68 Z" />

      <path class="cradle-base-cup" d="M 0,70 Q 65,102 130,70 A 65,65 0 0,1 0,70 Z" />
      <path class="cradle-lower-shadow" d="M 7,90 Q 65,119 123,90 A 61,61 0 0,1 7,90 Z" />
      <path class="cradle-inner-shadow" d="M 0,70 Q 65,106 130,70 A 65,65 0 0,1 0,70 Z" />

      <path class="cradle-rim-highlight" d="M 0,69 Q 65,101 130,69 Q 65,95 0,69 Z" />
      <path class="cradle-rim-shine" d="M 12,70.5 Q 65,96.5 118,70.5 Q 65,91.5 12,70.5 Z" />
      <path class="cradle-front-lip" d="M 6,76 Q 65,104 124,76" />

      <path class="cradle-side-hinge" d="M 111,79 Q 120,82 123,91" />
      <path class="cradle-scuff" d="M 54,97 l 8,-2 m -4,5 l 10,-3 m 19,6 l 9,-4 m -76,11 l 15,-5 m 30,17 l 17,-5" />
      <path class="cradle-chip" d="M 22,108 l 8,-2 l -2,5 l -7,1 Z" />
      <path class="cradle-chip" d="M 93,87 l 10,-3 l -1,6 l -8,2 Z" />

      <rect class="cradle-dashboard" x="49" y="102" width="32" height="11" rx="3" />
      <circle class="grogu-fa-led led-1" cx="56" cy="107.5" r="2.1" />
      <circle class="grogu-fa-led led-2" cx="65" cy="107.5" r="2.1" />
      <circle class="grogu-fa-led led-3" cx="74" cy="107.5" r="2.1" />
    </svg>
  `;
  const svgEl = tempDiv.firstElementChild;
  avatarWrapper.appendChild(svgEl);

  // 7. Click avatar to trigger Force Particle Effect and voice interaction
  let clickCount = 0;
  const INTERACTIVE_SOUNDS = [
    'interact_shout.mp3',
    'interact_cry.mp3',
    'interact_groan1.mp3',
    'interact_groan2.mp3',
    'interact_laugh1.mp3',
    'interact_laugh2.mp3'
  ];

  avatarWrapper.addEventListener('click', (e) => {
    e.stopPropagation();
    createForceParticles(e.clientX, e.clientY, avatarWrapper, container);

    if (motion === 'drift') {
      clickCount++;
      chrome.storage.local.get({ lang: 'zh' }, (data) => {
        const isEn = data.lang === 'en';
        if (clickCount === 1) {
          // First click: Pop up the Mando dry-rice reminder bubble
          speechBubble.textContent = isEn ? 'No rice left at home, Mando, get to work!' : '家里没米了，Mando  快干活！';
          container.classList.remove('grogu-fa-no-bubble');
          speechBubble.classList.remove('grogu-fa-bubble-click-pop');
          void speechBubble.offsetWidth;
          speechBubble.classList.add('grogu-fa-bubble-click-pop');
        } else {
          // Subsequent clicks: Play random interactive audio and show uniform response subtitle
          const randomSound = INTERACTIVE_SOUNDS[Math.floor(Math.random() * INTERACTIVE_SOUNDS.length)];
          speechBubble.textContent = isEn ? 'May the Force be with us!' : '原力与我们同在！';
          
          speechBubble.classList.remove('grogu-fa-bubble-click-pop');
          void speechBubble.offsetWidth;
          speechBubble.classList.add('grogu-fa-bubble-click-pop');
          
          // Play the custom reaction audio in background
          chrome.runtime.sendMessage({
            type: 'PLAY_INTERACTION_AUDIO',
            sound: randomSound
          }, () => {
            if (chrome.runtime.lastError) {} // Ignore
          });
        }
      });
    }
  });

  container.appendChild(avatarWrapper);

  // 8. Build close button
  const closeBtn = document.createElement('div');
  closeBtn.className = 'grogu-fa-close-btn';
  closeBtn.textContent = '✕';
  closeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    // Slide out animation
    container.classList.remove('grogu-fa-show');
    setTimeout(() => {
      if (root.contains(container)) {
        root.removeChild(container);
      }
    }, 600);
  });
  container.appendChild(closeBtn);

  // Add container to root
  root.appendChild(container);

  // Trigger CSS entry animation (using requestAnimationFrame for smooth transition)
  requestAnimationFrame(() => {
    container.classList.add('grogu-fa-show');
  });

  // Auto-dismiss blockers after 10 seconds, YES after 5 seconds, random events after 6 seconds
  if (assetName === 'NO' || assetName === 'NO2' || assetName === 'YES' || isRandomEvent) {
    const dismissDelay = motion === 'drift' ? 11200 : (assetName === 'YES' ? 6500 : (isRandomEvent ? 7200 : 10000));
    setTimeout(() => {
      if (root.contains(container)) {
        container.classList.remove('grogu-fa-show');
        setTimeout(() => {
          if (root.contains(container)) root.removeChild(container);
        }, 600);
      }
    }, dismissDelay);
  }
}

// Force Particle Effect
function createForceParticles(x, y, wrapper, container) {
  const particleCount = 15;
  const wrapperRect = wrapper.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();
  
  // Calculate center of avatar wrapper relative to container
  const left = (wrapperRect.left - containerRect.left) + wrapperRect.width / 2;
  const top = (wrapperRect.top - containerRect.top) + wrapperRect.height / 2;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.className = 'grogu-fa-particle';
    
    // Position at center of avatar
    particle.style.left = `${left}px`;
    particle.style.top = `${top}px`;
    
    // Random direction
    const angle = Math.random() * Math.PI * 2;
    const distance = 40 + Math.random() * 60;
    const dx = Math.cos(angle) * distance;
    const dy = Math.sin(angle) * distance;
    
    particle.style.setProperty('--dx', `${dx}px`);
    particle.style.setProperty('--dy', `${dy}px`);
    
    container.appendChild(particle);
    
    // Cleanup particle after animation ends
    setTimeout(() => {
      if (container.contains(particle)) {
        container.removeChild(particle);
      }
    }, 800);
  }
}

// Local memory cache for registered hotkeys (ensures synchronous, instant trigger response)
let cachedShortcuts = {};

chrome.storage.local.get({ summonShortcuts: {} }, (data) => {
  cachedShortcuts = data.summonShortcuts || {};
});

// Update cache in real-time if settings change
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.summonShortcuts) {
    cachedShortcuts = changes.summonShortcuts.newValue || {};
  }
});

// Global keyboard shortcuts listener to summon Grogu
document.addEventListener('keydown', (e) => {
  if (!document.activeElement) return;
  // Skip if user is focusing an input, textarea or editable element
  if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName) || document.activeElement.isContentEditable) {
    return;
  }
  
  // Skip if a NO distraction blocker is active on screen to prevent bypassing/conflicts
  if (document.querySelector('.grogu-fa-container.grogu-fa-mode-alert')) {
    return;
  }
  
  for (const [asset, combo] of Object.entries(cachedShortcuts)) {
    if (!combo) continue;
    
    const ctrlMatch = !!combo.ctrl === e.ctrlKey;
    const altMatch = !!combo.alt === e.altKey;
    const shiftMatch = !!combo.shift === e.shiftKey;
    const keyMatch = e.code === combo.key;
    
    if (ctrlMatch && altMatch && shiftMatch && keyMatch) {
      e.preventDefault();
      e.stopPropagation();
      
      // Trigger summon event via background page
      chrome.runtime.sendMessage({
        type: 'TRIGGER_RANDOM_EVENT',
        asset: asset
      }, () => {
        if (chrome.runtime.lastError) {} // Ignore
      });
      break;
    }
  }
}, true); // Use capture phase to intercept early
