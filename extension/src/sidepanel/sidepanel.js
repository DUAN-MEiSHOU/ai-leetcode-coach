const input = document.querySelector("#coach-input");
const sendButton = document.querySelector("#send-button");
const output = document.querySelector("#coach-output");
const pendingSelectionKey = "pendingSelection";
const backendExplainUrl = "http://127.0.0.1:8000/api/v1/coach/explain";
let currentSource = "manual_paste";

function setInputFromSelection(text) {
  input.value = text;
  currentSource = "page_selection";
  output.textContent = "Selected webpage text was sent to the coach input.";
  input.focus();
}

function renderBackendUnavailable(rawText, reason) {
  const text = rawText.trim();

  if (!text) {
    output.textContent = "Please paste some problem, code, or error text first.";
    input.focus();
    return;
  }

  output.textContent = [
    "Coach request was not completed",
    "",
    "The local backend or model provider could not be reached.",
    "",
    `Reason: ${reason}`,
    "",
    `Characters: ${text.length}`
  ].join("\n");
}

async function getResponseError(response) {
  try {
    const data = await response.json();
    return data.detail || `Backend returned HTTP ${response.status}`;
  } catch {
    return `Backend returned HTTP ${response.status}`;
  }
}

async function sendToBackend(rawText) {
  const text = rawText.trim();

  if (!text) {
    output.textContent = "Please paste some problem, code, or error text first.";
    input.focus();
    return;
  }

  sendButton.disabled = true;
  output.textContent = "Asking the coach...";

  try {
    const response = await fetch(backendExplainUrl, {
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
      throw new Error(await getResponseError(response));
    }

    const data = await response.json();
    output.textContent = [
      "Coach explanation",
      "",
      data.explanation,
      "",
      `Source: ${data.source}`,
      `Mode: ${data.mode}`,
      `Provider: ${data.provider}`,
      `Model: ${data.model}`
    ].join("\n");
  } catch (error) {
    renderBackendUnavailable(text, error.message);
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
