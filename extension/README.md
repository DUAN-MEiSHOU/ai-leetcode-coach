# AI LeetCode Coach Extension

This is a local-only Manifest V3 extension prototype.

## What Works

- Chrome/Edge developer-mode loading.
- Toolbar action.
- Browser Side Panel.
- Manual multiline text input.
- Visible coaching-mode selector.
- Auto-detect or Python language selection.
- Optional line number for selected-line explanations.
- Send button.
- Right-click selected webpage text and send it to the Side Panel.
- Local FastAPI request to a DeepSeek-backed explanation endpoint.

## Not Included Yet

- Database persistence.
- Page scraping.
- LeetCode editor access.

## Load In Chrome Or Edge

1. Open `chrome://extensions` or `edge://extensions`.
2. Enable developer mode.
3. Choose **Load unpacked**.
4. Select this `extension` directory.
5. Click the AI LeetCode Coach toolbar icon.
6. Paste text into the Side Panel and click **Send**.

## Send Selected Text

1. Select text on a webpage.
2. Right-click the selection.
3. Choose **Send to AI LeetCode Coach**.
4. Confirm the Side Panel opens and the selected text appears in the input area.

This feature only receives text selected by the user. It does not read or scrape the full page.

## Get A Coach Explanation

Start the backend first:

```bash
cd ../backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then return to the Side Panel and click **Send**. The output should begin with:

```text
Explanation
```

The backend must have a local DeepSeek configuration as described in
`../backend/README.md`. Sending text passes that text to the local backend, which
then sends it to DeepSeek for the explanation. The extension never receives the
API key and does not persist the submitted text.

If the backend is unavailable or the provider rejects the request, the Side
Panel shows the returned error without falling back to a fabricated explanation.

For **Explain selected line**, paste the surrounding Python code, choose
**Python**, and enter the line number. The backend parses the submitted text
without executing it, then provides the selected line and nearby context to the
coach.
