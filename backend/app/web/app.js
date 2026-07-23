const apiBase = "/api/v1";

const outcomeLabels = {
  solved_independently: "Solved independently",
  solved_with_hints: "Solved with hints",
  viewed_solution: "Viewed solution",
  gave_up: "Gave up",
  reviewed_easily: "Reviewed easily",
  struggled: "Struggled"
};

function setStatus(elementId, text, isError = false) {
  const element = document.getElementById(elementId);
  element.textContent = text;
  element.classList.toggle("error", isError);
}

function emptyState(text) {
  const item = document.createElement("li");
  item.className = "empty-state";
  item.textContent = text;
  return item;
}

function problemLink(title, url) {
  const link = document.createElement("a");
  link.href = url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = title || "Untitled problem";
  return link;
}

async function fetchJson(path, options) {
  const response = await fetch(`${apiBase}${path}`, options);
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || "Request failed. Check that the local backend is running.");
  }
  return response.json();
}

async function loadSummary() {
  const summary = await fetchJson("/dashboard/summary");
  document.getElementById("attempt-count").textContent = summary.total_attempts;
  document.getElementById("due-review-count").textContent = summary.due_review_count;
  const list = document.getElementById("recent-attempts");
  list.replaceChildren();
  if (!summary.recent_attempts.length) { list.append(emptyState("No attempts recorded yet.")); return; }
  for (const attempt of summary.recent_attempts) {
    const item = document.createElement("li");
    const meta = document.createElement("span");
    meta.textContent = `${outcomeLabels[attempt.outcome]} · ${new Date(attempt.attempted_at).toLocaleDateString()}`;
    item.append(problemLink(attempt.title, attempt.url), meta);
    list.append(item);
  }
}

async function loadDueReviews() {
  const reviews = await fetchJson("/reviews/due");
  const list = document.getElementById("due-reviews");
  list.replaceChildren();
  if (!reviews.length) { list.append(emptyState("Nothing due right now.")); return; }
  for (const review of reviews) {
    const item = document.createElement("li");
    const meta = document.createElement("span");
    meta.textContent = `Interval: ${review.interval_days} day${review.interval_days === 1 ? "" : "s"}`;
    item.append(problemLink(review.title, review.url), meta);
    list.append(item);
  }
}

document.getElementById("plan-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const availableMinutes = Number(document.getElementById("available-minutes").value);
  const focus = document.getElementById("plan-focus").value.trim();
  setStatus("plan-status", "Generating plan...");
  try {
    const plan = await fetchJson("/plans", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ available_minutes: availableMinutes, focus: focus || null }) });
    const list = document.getElementById("plan-items");
    list.replaceChildren();
    for (const planItem of plan.items) {
      const item = document.createElement("li");
      const title = document.createElement("strong");
      title.textContent = planItem.item_type === "review" ? (planItem.title || "Review problem") : "Choose a new LeetCode problem";
      item.append(title, document.createTextNode(` · ${planItem.estimated_minutes} minutes`));
      if (planItem.url) { item.append(document.createTextNode(" "), problemLink("Open", planItem.url)); }
      const reason = document.createElement("span");
      reason.textContent = planItem.reason;
      item.append(reason);
      list.append(item);
    }
    setStatus("plan-status", `${plan.allocated_minutes} of ${plan.available_minutes} minutes allocated.`);
  } catch (error) { setStatus("plan-status", error.message, true); }
});

document.getElementById("attempt-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const durationValue = document.getElementById("attempt-duration").value;
  const payload = {
    problem: { platform: "leetcode", url: document.getElementById("problem-url").value.trim(), title: document.getElementById("problem-title").value.trim() || null },
    outcome: document.getElementById("attempt-outcome").value,
    duration_minutes: durationValue === "" ? null : Number(durationValue),
    language: "python",
    notes: document.getElementById("attempt-notes").value.trim() || null
  };
  setStatus("attempt-status", "Saving attempt...");
  try {
    const result = await fetchJson("/attempts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    setStatus("attempt-status", `Saved. Next review: ${new Date(result.next_review_at).toLocaleDateString()}.`);
    event.target.reset();
    await Promise.all([loadSummary(), loadDueReviews()]);
  } catch (error) { setStatus("attempt-status", error.message, true); }
});

document.getElementById("refresh-summary").addEventListener("click", () => loadSummary().catch((error) => setStatus("attempt-status", error.message, true)));
document.getElementById("refresh-reviews").addEventListener("click", () => loadDueReviews().catch((error) => setStatus("plan-status", error.message, true)));
Promise.all([loadSummary(), loadDueReviews()]).catch((error) => setStatus("attempt-status", error.message, true));
