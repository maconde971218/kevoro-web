# Modified for Kevoro: localhost only, synthetic fixtures, temporary evidence paths.
from playwright.sync_api import sync_playwright
from urllib.parse import urlsplit

# Example: serve the static test fixture on localhost before running.
url = 'http://localhost:5173'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).scheme in {'http', 'https'} and urlsplit(route.request.url).hostname in {'localhost', '127.0.0.1'} else route.abort())

    # Navigate to local HTML file
    page.goto(url)

    # Take screenshot
    page.screenshot(path='/tmp/kevoro-web-static_page.png', full_page=True)

    # Interact with elements
    page.click('text=Click Me')
    page.fill('#name', 'John Doe')
    page.fill('#email', 'john@example.com')

    # Submit form
    page.click('button[type="submit"]')

    # Take final screenshot
    page.screenshot(path='/tmp/kevoro-web-after_submit.png', full_page=True)

    browser.close()

print("Static HTML automation completed!")
