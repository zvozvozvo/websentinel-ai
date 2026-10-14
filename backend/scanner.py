import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time


MAX_PAGES = 10
TIMEOUT = 10

HEADERS = {
    "User-Agent": "WebSentinel/1.0"
}


def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/")


def add_error(errors, error_type, severity, url, message):
    errors.append({
        "type": error_type,
        "severity": severity,
        "url": url,
        "message": message
    })


def scan_website(start_url):
    start_url = normalize_url(start_url)

    parsed_start = urlparse(start_url)
    domain = parsed_start.netloc

    queue = deque([start_url])
    visited = set()

    pages = []
    errors = []

    checked_links = set()
    checked_images = set()

    while queue and len(visited) < MAX_PAGES:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            start_time = time.perf_counter()

            response = requests.get(
                current_url,
                timeout=TIMEOUT,
                headers=HEADERS,
                allow_redirects=True
            )

            response_time = round(
                time.perf_counter() - start_time,
                2
            )

            status = response.status_code

            if status >= 400:
                add_error(
                    errors,
                    "http_error",
                    "high",
                    current_url,
                    f"HTTP {status}"
                )
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # =========================
            # BASIC PAGE DATA
            # =========================

            title_tag = soup.find("title")

            title = (
                title_tag.get_text(strip=True)
                if title_tag
                else ""
            )

            h1_tags = soup.find_all("h1")

            description = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            viewport = soup.find(
                "meta",
                attrs={"name": "viewport"}
            )

            html_tag = soup.find("html")

            lang = (
                html_tag.get("lang")
                if html_tag
                else None
            )

            canonical = soup.find(
                "link",
                attrs={"rel": "canonical"}
            )

            robots = soup.find(
                "meta",
                attrs={"name": "robots"}
            )

            links = soup.find_all(
                "a",
                href=True
            )

            images = soup.find_all("img")

            forms = soup.find_all("form")

            buttons = soup.find_all(
                ["button", "input"]
            )

            page_info = {
                "url": current_url,
                "status": status,
                "title": title or "Untitled page",
                "links": len(links),
                "images": len(images),
                "forms": len(forms),
                "buttons": len(buttons),
                "console_errors": 0,
                "response_time": response_time
            }

            pages.append(page_info)

            # =========================
            # TITLE CHECKS
            # =========================

            if not title:
                add_error(
                    errors,
                    "missing_title",
                    "medium",
                    current_url,
                    "Page is missing a <title>"
                )

            elif len(title) < 10:
                add_error(
                    errors,
                    "short_title",
                    "low",
                    current_url,
                    f"Title is too short ({len(title)} characters)"
                )

            elif len(title) > 60:
                add_error(
                    errors,
                    "long_title",
                    "low",
                    current_url,
                    f"Title is too long ({len(title)} characters)"
                )

            # =========================
            # H1 CHECKS
            # =========================

            if not h1_tags:

                add_error(
                    errors,
                    "missing_h1",
                    "medium",
                    current_url,
                    "Page is missing an H1 heading"
                )

            elif len(h1_tags) > 1:

                add_error(
                    errors,
                    "multiple_h1",
                    "low",
                    current_url,
                    f"Page contains {len(h1_tags)} H1 headings"
                )

            # =========================
            # META DESCRIPTION
            # =========================

            if not description:

                add_error(
                    errors,
                    "missing_meta_description",
                    "low",
                    current_url,
                    "Page is missing meta description"
                )

            else:

                description_text = (
                    description.get("content", "").strip()
                )

                if len(description_text) < 50:

                    add_error(
                        errors,
                        "short_meta_description",
                        "low",
                        current_url,
                        "Meta description is too short"
                    )

                elif len(description_text) > 160:

                    add_error(
                        errors,
                        "long_meta_description",
                        "low",
                        current_url,
                        "Meta description is too long"
                    )

            # =========================
            # ACCESSIBILITY
            # =========================

            if not lang:

                add_error(
                    errors,
                    "missing_lang",
                    "medium",
                    current_url,
                    "HTML element is missing a language attribute"
                )

            if not viewport:

                add_error(
                    errors,
                    "missing_viewport",
                    "medium",
                    current_url,
                    "Page is missing responsive viewport meta tag"
                )

            # =========================
            # CANONICAL
            # =========================

            if not canonical:

                add_error(
                    errors,
                    "missing_canonical",
                    "low",
                    current_url,
                    "Page is missing canonical URL"
                )

            # =========================
            # IMAGES
            # =========================

            for image in images:

                src = image.get("src")

                if not src:
                    continue

                image_url = urljoin(
                    current_url,
                    src
                )

                if not image.get("alt"):

                    add_error(
                        errors,
                        "image_missing_alt",
                        "low",
                        current_url,
                        f"Image is missing alt text: {image_url}"
                    )

                if image_url in checked_images:
                    continue

                checked_images.add(image_url)

                try:

                    image_response = requests.get(
                        image_url,
                        timeout=5,
                        headers=HEADERS
                    )

                    if image_response.status_code >= 400:

                        add_error(
                            errors,
                            "broken_image",
                            "high",
                            image_url,
                            f"Image returned HTTP {image_response.status_code}"
                        )

                except requests.RequestException:

                    add_error(
                        errors,
                        "broken_image",
                        "high",
                        image_url,
                        "Could not load image"
                    )

            # =========================
            # BUTTONS
            # =========================

            for button in buttons:

                tag_name = button.name

                if tag_name == "button":

                    text = button.get_text(
                        strip=True
                    )

                else:

                    text = button.get("value", "")

                aria_label = button.get(
                    "aria-label"
                )

                if not text and not aria_label:

                    add_error(
                        errors,
                        "empty_button",
                        "medium",
                        current_url,
                        "Button has no visible text or aria-label"
                    )

            # =========================
            # FORMS
            # =========================

            for form in forms:

                inputs = form.find_all(
                    ["input", "textarea", "select"]
                )

                for field in inputs:

                    field_type = field.get(
                        "type",
                        ""
                    ).lower()

                    if field_type in [
                        "hidden",
                        "submit",
                        "button"
                    ]:
                        continue

                    field_id = field.get("id")

                    if not field_id:
                        add_error(
                            errors,
                            "form_field_without_label",
                            "low",
                            current_url,
                            "Form field has no id and cannot be associated with a label"
                        )
                        continue

                    label = soup.find(
                        "label",
                        attrs={"for": field_id}
                    )

                    if not label:

                        add_error(
                            errors,
                            "form_field_without_label",
                            "low",
                            current_url,
                            f"Form field '{field_id}' has no associated label"
                        )

            # =========================
            # RESPONSE TIME
            # =========================

            if response_time > 3:

                add_error(
                    errors,
                    "slow_page",
                    "medium",
                    current_url,
                    f"Page response time is {response_time}s"
                )

            elif response_time > 1.5:

                add_error(
                    errors,
                    "slow_page",
                    "low",
                    current_url,
                    f"Page response time is {response_time}s"
                )

            # =========================
            # INTERNAL LINKS
            # =========================

            for link in links:

                href = link.get("href")

                if not href:
                    continue

                if href.startswith(
                    ("#", "mailto:", "tel:", "javascript:")
                ):
                    continue

                absolute_url = urljoin(
                    current_url,
                    href
                )

                parsed = urlparse(
                    absolute_url
                )

                if parsed.netloc != domain:
                    continue

                clean_url = (
                    absolute_url
                    .split("#")[0]
                    .rstrip("/")
                )

                if (
                    clean_url not in visited
                    and clean_url not in queue
                    and len(visited) + len(queue) < MAX_PAGES
                ):
                    queue.append(clean_url)

        except requests.RequestException as e:

            add_error(
                errors,
                "connection_error",
                "critical",
                current_url,
                str(e)
            )

        except Exception as e:

            add_error(
                errors,
                "scanner_error",
                "critical",
                current_url,
                str(e)
            )

    # =========================================
    # BROKEN LINKS
    # =========================================

    for page in pages:

        try:

            response = requests.get(
                page["url"],
                timeout=TIMEOUT,
                headers=HEADERS
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for link in soup.find_all(
                "a",
                href=True
            ):

                href = link.get("href")

                if href.startswith(
                    ("#", "mailto:", "tel:", "javascript:")
                ):
                    continue

                target = urljoin(
                    page["url"],
                    href
                )

                target = target.split("#")[0]

                if target in checked_links:
                    continue

                checked_links.add(target)

                try:

                    check = requests.get(
                        target,
                        timeout=5,
                        headers=HEADERS,
                        allow_redirects=True
                    )

                    if check.status_code >= 400:

                        add_error(
                            errors,
                            "broken_link",
                            "high",
                            target,
                            f"Broken link: HTTP {check.status_code}"
                        )

                except requests.RequestException:

                    add_error(
                        errors,
                        "broken_link",
                        "high",
                        target,
                        "Could not reach link"
                    )

        except Exception:
            pass

    # =========================================
    # DUPLICATE ERRORS
    # =========================================

    unique_errors = []
    seen_errors = set()

    for error in errors:

        key = (
            error["type"],
            error["url"],
            error["message"]
        )

        if key not in seen_errors:

            seen_errors.add(key)
            unique_errors.append(error)

    # =========================================
    # HEALTH SCORE
    # =========================================

    score = 100

    severity_weights = {
        "critical": 25,
        "high": 15,
        "medium": 7,
        "low": 3
    }

    for error in unique_errors:

        score -= severity_weights.get(
            error.get("severity"),
            0
        )

    score = max(0, min(100, score))

    # =========================================
    # SUMMARY
    # =========================================

    summary = {
        "pages": len(pages),
        "issues": len(unique_errors),

        "critical": sum(
            1
            for e in unique_errors
            if e.get("severity") == "critical"
        ),

        "high": sum(
            1
            for e in unique_errors
            if e.get("severity") == "high"
        ),

        "medium": sum(
            1
            for e in unique_errors
            if e.get("severity") == "medium"
        ),

        "low": sum(
            1
            for e in unique_errors
            if e.get("severity") == "low"
        ),

        "images": sum(
            page.get("images", 0)
            for page in pages
        ),

        "forms": sum(
            page.get("forms", 0)
            for page in pages
        ),

        "buttons": sum(
            page.get("buttons", 0)
            for page in pages
        )
    }

    return {
        "url": start_url,
        "score": score,
        "pages": pages,
        "errors": unique_errors,
        "summary": summary
    }