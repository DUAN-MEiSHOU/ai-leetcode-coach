chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type !== "coach:open-side-panel" || !sender.tab?.id) {
    return;
  }

  (async () => {
    try {
      await chrome.sidePanel.open({ tabId: sender.tab.id });
      sendResponse({ ok: true });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error("Failed to open side panel from floating entry:", errorMessage);
      sendResponse({ ok: false, error: errorMessage });
    }
  })();

  return true;
});

console.info("AI LeetCode Coach service worker ready", chrome.runtime.id);

const CONTEXT_MENU_ID = "send-selection-to-ai-leetcode-coach";
const PENDING_SELECTION_KEY = "pendingSelection";

chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .catch((error) => {
      console.error("Failed to configure side panel behavior:", error);
    });

  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: CONTEXT_MENU_ID,
      title: "Send to AI LeetCode Coach",
      contexts: ["selection"]
    });
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId !== CONTEXT_MENU_ID || !info.selectionText) {
    return;
  }

  const selectedText = info.selectionText;
  chrome.storage.local.set({
    [PENDING_SELECTION_KEY]: {
      text: selectedText,
      source: "page_selection",
      receivedAt: new Date().toISOString()
    }
  });

  if (tab?.id) {
    chrome.sidePanel.open({ tabId: tab.id }).catch((error) => {
      console.error("Failed to open side panel for selected text:", error);
    });
  }

  chrome.runtime
    .sendMessage({
      type: "coach:selected-text",
      text: selectedText,
      source: "page_selection"
    })
    .catch(() => {
      // The Side Panel may not be ready yet; storage.local is the durable handoff.
    });
});
