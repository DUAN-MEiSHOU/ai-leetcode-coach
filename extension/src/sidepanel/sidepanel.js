const input = document.querySelector("#coach-input");
const sendButton = document.querySelector("#send-button");
const output = document.querySelector("#coach-output");
const pendingSelectionKey = "pendingSelection";

function setInputFromSelection(text) {
  input.value = text;
  output.textContent = "Selected webpage text was sent to the coach input.";
  input.focus();
}

function renderPlaceholder(rawText) {
  const text = rawText.trim();

  if (!text) {
    output.textContent = "Please paste some problem, code, or error text first.";
    input.focus();
    return;
  }

  output.textContent = [
    "Local placeholder response",
    "",
    "The extension shell received your text successfully.",
    "",
    `Characters: ${text.length}`,
    "",
    "Backend, DeepSeek, persistence, and review scheduling are intentionally not connected yet."
  ].join("\n");
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
  renderPlaceholder(input.value);
});

input.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    renderPlaceholder(input.value);
  }
});
