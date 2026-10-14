from pathlib import Path

from playwright.sync_api import sync_playwright


SCREENSHOT_DIR = (
    Path(__file__).parent / "screenshots"
)


def capture_screenshot(url):

    SCREENSHOT_DIR.mkdir(
        exist_ok=True
    )

    screenshot_path = (
        SCREENSHOT_DIR / "latest.png"
    )


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900
            },
            device_scale_factor=1
        )


        try:

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )


            page.wait_for_timeout(
                2000
            )


            page.screenshot(
                path=str(
                    screenshot_path
                ),
                full_page=True
            )


            return str(
                screenshot_path
            )


        finally:

            browser.close()