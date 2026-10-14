from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from scanner import scan_website
from browser_scanner import browser_scan
from vision_scanner import capture_screenshot
from ai_analyzer import analyze_issues


SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


app = FastAPI(
    title="WebSentinel API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/screenshots",
    StaticFiles(directory=str(SCREENSHOT_DIR)),
    name="screenshots"
)


class ScanRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "name": "WebSentinel",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/scan")
def scan(request: ScanRequest):

    if not request.url.strip():
        raise HTTPException(
            status_code=400,
            detail="URL is required"
        )

    url = request.url.strip()

    try:

        # ==========================================
        # STATIC SCANNER
        # ==========================================

        result = scan_website(url)


        # ==========================================
        # BROWSER SCANNER
        # ==========================================

        print("Starting browser scan...")

        browser = browser_scan(url)

        result["browser"] = browser


        js_errors = (
            len(
                browser.get(
                    "console_errors",
                    []
                )
            )
            +
            len(
                browser.get(
                    "page_errors",
                    []
                )
            )
        )


        if result.get("pages"):

            result["pages"][0]["console_errors"] = (
                js_errors
            )


        for error in browser.get(
            "console_errors",
            []
        ):

            result["errors"].append({
                "type": "javascript_error",
                "severity": "high",
                "url": url,
                "message": error
            })


        for error in browser.get(
            "page_errors",
            []
        ):

            result["errors"].append({
                "type": "javascript_runtime_error",
                "severity": "critical",
                "url": url,
                "message": error
            })


        for failed in browser.get(
            "failed_requests",
            []
        ):

            result["errors"].append({
                "type": "failed_network_request",
                "severity": "high",
                "url": failed.get("url"),
                "message": str(
                    failed.get("failure")
                )
            })


        for image in browser.get(
            "broken_images",
            []
        ):

            result["errors"].append({
                "type": "browser_broken_image",
                "severity": "high",
                "url": image,
                "message": "Image failed to load"
            })


        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_errors = []
        seen = set()


        for error in result["errors"]:

            key = (
                error.get("type"),
                error.get("url"),
                error.get("message")
            )

            if key not in seen:

                seen.add(key)

                unique_errors.append(
                    error
                )


        result["errors"] = unique_errors


        # ==========================================
        # SCORE
        # ==========================================

        score = 100

        weights = {
            "critical": 25,
            "high": 15,
            "medium": 7,
            "low": 3
        }


        for error in unique_errors:

            score -= weights.get(
                error.get("severity"),
                0
            )


        result["score"] = max(
            0,
            min(100, score)
        )


        result["summary"]["issues"] = (
            len(unique_errors)
        )

        result["summary"]["critical"] = sum(
            1
            for e in unique_errors
            if e.get("severity") == "critical"
        )

        result["summary"]["high"] = sum(
            1
            for e in unique_errors
            if e.get("severity") == "high"
        )

        result["summary"]["medium"] = sum(
            1
            for e in unique_errors
            if e.get("severity") == "medium"
        )

        result["summary"]["low"] = sum(
            1
            for e in unique_errors
            if e.get("severity") == "low"
        )


        # ==========================================
        # SCREENSHOT
        # ==========================================

        screenshot_url = None

        try:

            print(
                "Capturing website screenshot..."
            )

            screenshot_path = capture_screenshot(
                url
            )

            print(
                "Screenshot captured:",
                screenshot_path
            )

            screenshot_url = (
                "/screenshots/latest.png"
            )

        except Exception as e:

            print(
                "Screenshot error:",
                e
            )


        # ==========================================
        # AI ANALYSIS
        # ==========================================

        print(
            "Starting AI analysis..."
        )

        ai_result = analyze_issues(
            result["errors"],
            screenshot_path
            if screenshot_url
            else None
        )


        if screenshot_url:

            ai_result["screenshot"] = (
                screenshot_url
            )


        print(
            "AI result:",
            ai_result
        )


        result["ai_analysis"] = (
            ai_result
        )


        return result


    except Exception as e:

        print(
            "SCAN ERROR:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )