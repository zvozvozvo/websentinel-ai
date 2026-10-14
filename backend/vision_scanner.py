from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


VIEWPORTS = {
    "desktop": {
        "width": 1440,
        "height": 900,
    },
    "tablet": {
        "width": 1024,
        "height": 768,
    },
    "mobile": {
        "width": 390,
        "height": 844,
    },
}


def capture_responsive_screenshots(url):
    SCREENSHOT_DIR.mkdir(exist_ok=True)

    screenshots = {}

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        try:

            for device, viewport in VIEWPORTS.items():

                page = browser.new_page(
                    viewport=viewport,
                    device_scale_factor=1
                )

                try:
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    page.wait_for_timeout(2000)

                    screenshot_path = (
                        SCREENSHOT_DIR
                        / f"{device}.png"
                    )

                    page.screenshot(
                        path=str(screenshot_path),
                        full_page=True
                    )

                    screenshots[device] = str(
                        screenshot_path
                    )

                    print(
                        f"{device} screenshot captured:"
                        f" {screenshot_path}"
                    )

                finally:
                    page.close()

        finally:
            browser.close()

    return screenshots