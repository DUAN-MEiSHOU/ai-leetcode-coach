const input = document.querySelector("#coach-input");
const sendButton = document.querySelector("#send-button");
const output = document.querySelector("#coach-output");
const pendingSelectionKey = "pendingSelection";
const backendEchoUrl = "http://127.0.0.1:8000/api/v1/coach/echo";
let currentSource = "manual_paste";

function setInputFromSelection(text) {
  input.value = text;
  currentSource = "page_selection";
  output.textContent = "Selected webpage text was sent to the coach input.";
  input.focus();
}

function renderLocalFallback(rawText, reason) {
  const text = rawText.trim();

  if (!text) {
    output.textContent = "Please paste some problem, code, or error text first.";
    input.focus();
    return;
  }

  output.textContent = [
    "Local placeholder response",
    "",
    "The extension shell received your text, but the local backend was not reached.",
    "",
    `Reason: ${reason}`,
    "",
    `Characters: ${text.length}`,
    "",
    "Backend, DeepSeek, persistence, and review scheduling are intentionally not connected yet."
  ].join("\n");
}

async function sendToBackend(rawText) {
  const text = rawText.trim();

  if (!text) {
    output.textContent = "Please paste some problem, code, or error text first.";
    input.focus();
    return;
  }

  sendButton.disabled = true;
  output.textContent = "Checking local backend...";

  try {
    const response = await fetch(backendEchoUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mode: "manual",
        source: currentSource,
        content: text
      })
    });

    if (!response.ok) {
      throw new Error(`Backend returned HTTP ${response.status}`);
    }

    const data = await response.json();
    output.textContent = [
      "Backend echo response",
      "",
      data.message,
      "",
      `Source: ${data.source}`,
      `Mode: ${data.mode}`,
      `Characters: ${data.content_length}`,
      "",
      "DeepSeek, persistence, and review scheduling are intentionally not connected yet."
    ].join("\n");
  } catch (error) {
    renderLocalFallback(text, error.message);
  } finally {
    sendButton.disabled = false;
  }
}

chrome.storage.local.get(pendingSelectionKey, (result) => {
  const pendingSelection = result[pendingSelectionKey];

  if (!pendingSelection?.text) {
    return;
  }

  setInputFromSelection(pendingSelection.text);
  chrome.storage.local.remove(pendingSelectionKey);
});

chrome.runtime.onMessage.addListener((message) => {
  if (message?.type !== "coach:selected-text" || !message.text) {
    return;
  }

  setInputFromSelection(message.text);
  chrome.storage.local.remove(pendingSelectionKey);
});

sendButton.addEventListener("click", () => {
  sendToBackend(input.value);
});

input.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    sendToBackend(input.value);
  }
});

input.addEventListener("input", () => {
  currentSource = "manual_paste";
});
