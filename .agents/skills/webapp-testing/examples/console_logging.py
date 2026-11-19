# Modified for Kevoro: localhost only, synthetic fixtures, temporary evidence paths.
from playwright.sync_api import sync_playwright
from urllib.parse import urlsplit

# Example: Capturing console logs during browser automation

url = 'http://localhost:5173'  # Replace with your URL

console_logs = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).scheme in {'http', 'https'} and urlsplit(route.request.url).hostname in {'localhost', '127.0.0.1'} else route.abort())

    # Set up console log capture
    def handle_console_message(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")
        print(f"Console: [{msg.type}] {msg.text}")

    page.on("console", handle_console_message)

    # Navigate to page
    page.goto(url)
    page.locator('body').wait_for()

    # Interact with the page (triggers console logs)
    page.click('text=Dashboard')

    browser.close()

# Save console logs to file
with open('/tmp/kevoro-web-console.log', 'w') as f:
    f.write('\n'.join(console_logs))

print(f"\nCaptured {len(console_logs)} console messages")
print(f"Logs saved to: /tmp/kevoro-web-console.log")
