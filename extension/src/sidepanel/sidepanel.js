const input = document.querySelector("#coach-input");
const sendButton = document.querySelector("#send-button");
const output = document.querySelector("#coach-output");

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
    "Backend, DeepSeek, selected-text input, persistence, and review scheduling are intentionally not connected in Phase 1."
  ].join("\n");
}

sendButton.addEventListener("click", () => {
  renderPlaceholder(input.value);
});

input.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    renderPlaceholder(input.value);
  }
});
