const input = document.querySelector("#coach-input");
const modeSelect = document.querySelector("#coach-mode");
const sendButton = document.querySelector("#send-button");
const output = document.querySelector("#coach-output");
const pendingSelectionKey = "pendingSelection";
const backendExplainUrl = "http://127.0.0.1:8000/api/v1/coach/explain";
let currentSource = "manual_paste";

function appendInlineMarkdown(container, text) {
  const pattern = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let cursor = 0;

  for (const match of text.matchAll(pattern)) {
    if (match.index > cursor) {
      container.append(document.createTextNode(text.slice(cursor, match.index)));
    }

    const token = match[0];
    const element = token.startsWith("**") ? document.createElement("strong") : document.createElement("code");
    element.textContent = token.slice(token.startsWith("**") ? 2 : 1, token.startsWith("**") ? -2 : -1);
    container.append(element);
    cursor = match.index + token.length;
  }

  if (cursor < text.length) {
    container.append(document.createTextNode(text.slice(cursor)));
  }
}

function renderMarkdown(markdown, metadata) {
  const fragment = document.createDocumentFragment();
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];

    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.startsWith("```")) {
      const codeLines = [];
      index += 1;
      while (index < lines.length && !lines[index].startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) {
        index += 1;
      }
      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = codeLines.join("\n");
      pre.append(code);
      fragment.append(pre);
      continue;
    }

    const heading = line.match(/^#{1,3}\s+(.+)$/);
    if (heading) {
      const element = document.createElement("h3");
      appendInlineMarkdown(element, heading[1]);
      fragment.append(element);
      index += 1;
      continue;
    }

    const listMatch = line.match(/^(\d+\. |[-*] )(.+)$/);
    if (listMatch) {
      const ordered = /^\d+\. /.test(line);
      const list = document.createElement(ordered ? "ol" : "ul");
      while (index < lines.length) {
        const itemMatch = lines[index].match(ordered ? /^\d+\. (.+)$/ : /^[-*] (.+)$/);
        if (!itemMatch) {
          break;
        }
        const item = document.createElement("li");
        appendInlineMarkdown(item, itemMatch[1]);
        list.append(item);
        index += 1;
      }
      fragment.append(list);
      continue;
    }

    const paragraph = document.createElement("p");
    appendInlineMarkdown(paragraph, line);
    fragment.append(paragraph);
    index += 1;
  }

  const metadataElement = document.createElement("div");
  metadataElement.className = "response-metadata";
  metadataElement.textContent = metadata.join(" | ");
  fragment.append(metadataElement);
  output.replaceChildren(fragment);
}

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
        mode: modeSelect.value,
        source: currentSource,
        content: text
      })
    });

    if (!response.ok) {
      throw new Error(await getResponseError(response));
    }

    const data = await response.json();
    renderMarkdown(data.explanation, [
      `Mode: ${data.mode}`,
      `Provider: ${data.provider}`,
      `Model: ${data.model}`,
      `Prompt: ${data.prompt_version}`
    ]);
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
