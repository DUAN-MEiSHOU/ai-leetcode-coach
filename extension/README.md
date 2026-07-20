# AI LeetCode Coach Extension

This is a local-only Manifest V3 extension prototype.

## What Works

- Chrome/Edge developer-mode loading.
- Toolbar action.
- Browser Side Panel.
- Manual multiline text input.
- Send button.
- Local placeholder output.
- Right-click selected webpage text and send it to the Side Panel.

## Not Included Yet

- Backend connection.
- DeepSeek integration.
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
