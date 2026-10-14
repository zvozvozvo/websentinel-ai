from playwright.sync_api import sync_playwright


def browser_scan(url):
    result = {
        "url": url,
        "console_errors": [],
        "page_errors": [],
        "failed_requests": [],
        "broken_images": [],
        "load_time": 0
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # JavaScript console errors
        def handle_console(message):
            if message.type == "error":
                result["console_errors"].append(
                    message.text
                )

        page.on(
            "console",
            handle_console
        )

        # Runtime JS errors
        def handle_page_error(error):
            result["page_errors"].append(
                str(error)
            )

        page.on(
            "pageerror",
            handle_page_error
        )

        # Failed network requests
        def handle_request_failed(request):
            result["failed_requests"].append({
                "url": request.url,
                "method": request.method,
                "failure": request.failure
            })

        page.on(
            "requestfailed",
            handle_request_failed
        )

        try:

            response = page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            if response:
                result["status"] = response.status

            result["load_time"] = round(
                page.evaluate(
                    "() => performance.now()"
                ) / 1000,
                2
            )

            # Check images
            images = page.locator("img")

            for i in range(images.count()):

                image = images.nth(i)

                try:
                    loaded = image.evaluate(
                        """
                        img => img.complete && img.naturalWidth > 0
                        """
                    )

                    src = image.get_attribute("src")

                    if not loaded:

                        result["broken_images"].append(
                            src or "unknown image"
                        )

                except Exception:
                    pass

        except Exception as error:

            result["page_errors"].append(
                str(error)
            )

        finally:

            browser.close()

    return result