chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'PLAY_AUDIO') {
    playAudio(message.file);
    sendResponse({ success: true });
  }
  return false;
});

let activeAudio = null;

function playAudio(source) {
  try {
    // Forcefully release the previous audio player and its decoder resource
    if (activeAudio) {
      activeAudio.pause();
      activeAudio.removeAttribute('src');
      activeAudio.load(); // Force browser to release system media decoder
      activeAudio = null;
    }
    
    activeAudio = new Audio(source);
    activeAudio.volume = 1.0;
    activeAudio.play().catch((error) => {
      console.error(`Error playing sound: ${error}`);
    });
    
    // Release resources immediately when playback ends
    activeAudio.addEventListener('ended', () => {
      if (activeAudio) {
        activeAudio.removeAttribute('src');
        activeAudio.load();
        activeAudio = null;
      }
    });
  } catch (e) {
    console.error(`Failed to initialize Audio: ${e}`);
  }
}
