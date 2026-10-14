# WebSentinel

AI-powered website QA and testing platform.

WebSentinel automatically scans websites for technical, JavaScript, accessibility, and visual issues. It combines traditional web crawling, browser-based testing, Playwright screenshots, and AI-powered analysis to detect problems and generate actionable fixes.

## Features

- Website crawling and technical analysis
- Broken link detection
- HTTP error detection
- Missing HTML elements detection
- JavaScript console error detection
- Browser runtime error detection
- Failed network request detection
- Broken image detection
- AI-powered issue analysis
- AI-generated fixes
- AI visual QA
- Website screenshots with Playwright
- Visual accessibility analysis

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- BeautifulSoup
- Requests
- Playwright

### AI
- Nous Research API
- OpenAI-compatible API
- Vision model for visual QA

## Architecture

```text
Website URL
     │
     ▼
WebSentinel Scanner
     │
     ├── Technical Scanner
     │
     ├── Browser Scanner
     │
     └── Playwright
           │
           ▼
       Screenshot
           │
           ▼
       AI Analysis
           │
           ├── Technical QA
           ├── Generated Fixes
           └── Visual QA
                    │
                    ▼
              Web Dashboard
