const ENTRY_HOST_ID = "ai-leetcode-coach-floating-entry";

function createFloatingEntry() {
  if (document.getElementById(ENTRY_HOST_ID)) {
    return;
  }

  const host = document.createElement("div");
  host.id = ENTRY_HOST_ID;
  host.setAttribute("aria-hidden", "false");

  const shadow = host.attachShadow({ mode: "open" });
  const style = document.createElement("style");
  style.textContent = `
    :host {
      all: initial;
    }

    button {
      width: 42px;
      height: 42px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      padding: 0;
      background: #276ef1;
      box-shadow: 0 4px 14px rgba(18, 24, 38, 0.24);
      color: #ffffff;
      cursor: pointer;
      font-family: system-ui, sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0;
    }

    button:hover {
      background: #1f5fd1;
    }

    button:focus-visible {
      outline: 3px solid #8ab4ff;
      outline-offset: 3px;
    }
  `;

  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "AI";
  button.setAttribute("aria-label", "Open AI LeetCode Coach");
  button.title = "Open AI LeetCode Coach";
  button.addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "coach:open-side-panel" });
  });

  shadow.append(style, button);
  host.style.cssText = [
    "position: fixed",
    "right: 20px",
    "bottom: 92px",
    "z-index: 2147483647"
  ].join(";");
  document.documentElement.append(host);
}

createFloatingEntry();
