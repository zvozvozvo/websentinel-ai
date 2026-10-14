[README.md](https://github.com/user-attachments/files/33449998/README.md)
# WebSentinel

> AI-powered website quality assurance and visual testing platform.

WebSentinel automatically scans websites for technical, JavaScript, accessibility, browser, and visual issues. It combines web crawling, real browser testing, Playwright screenshots, and AI-powered analysis to help developers find problems and generate actionable fixes.

## Features

- Technical website scanning
- Broken link detection
- HTTP error detection
- Missing HTML element detection
- Missing H1 detection
- Missing meta description detection
- Missing canonical URL detection
- JavaScript console error detection
- JavaScript runtime error detection
- Failed network request detection
- Broken image detection
- Website health scoring
- AI-powered issue analysis
- AI-generated code fixes
- Playwright browser testing
- AI-powered visual QA
- Website screenshot analysis

## How It Works

```text
                    Website URL
                         |
                         v
                +------------------+
                |  WebSentinel     |
                |     Scanner      |
                +--------+---------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     Technical QA    Browser QA     Playwright
          |              |              |
          |              |              v
          |              |         Screenshot
          |              |              |
          +--------------+--------------+
                         |
                         v
                 +---------------+
                 |  AI Analysis  |
                 +-------+-------+
                         |
              +----------+----------+
              |          |          |
              v          v          v
          Technical    Generated   Visual
           Analysis      Fixes       QA
              |          |          |
              +----------+----------+
                         |
                         v
                 WebSentinel UI
```

## Technical Scanning

WebSentinel crawls websites and checks for common technical problems.

Detected issues include:

- HTTP errors
- Broken links
- Missing page titles
- Missing H1 headings
- Missing meta descriptions
- Missing canonical URLs
- Connection failures
- Broken resources
- Other HTML and website structure issues

## Browser Testing

WebSentinel uses Playwright and Chromium to test websites in a real browser environment.

It can detect:

- JavaScript console errors
- JavaScript runtime errors
- Failed network requests
- Broken images
- Browser loading problems
- Client-side failures

## AI Analysis

Detected issues can be analyzed by an AI model.

For important issues, WebSentinel generates:

- Issue explanation
- Severity level
- Why the issue matters
- Recommended fix
- Ready-to-use code

Example:

```html
<h1>Descriptive Page Title</h1>
```

Instead of simply reporting that an H1 is missing, WebSentinel provides a practical solution.

## AI Visual QA

WebSentinel captures real website screenshots using Playwright and analyzes them with a vision model.

The visual QA system can detect:

- Low text contrast
- Broken layouts
- Overlapping elements
- Clipped content
- Excessive whitespace
- Inconsistent spacing
- Unreadable text
- Broken visual elements
- Obvious accessibility problems
- Other visible UI issues

Example visual findings:

```text
Visual QA

[MEDIUM] Low text contrast
The grey text has insufficient contrast against
the light background.

Recommendation:
Increase the text contrast to meet WCAG guidelines.

[LOW] Excessive vertical whitespace
Large empty areas make the content feel disconnected.

Recommendation:
Improve the vertical spacing and content positioning.
```

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Requests
- BeautifulSoup
- Playwright

### AI

- Nous Research API
- OpenAI-compatible API
- Text analysis models
- Vision models

## Project Structure

```text
websentinel-ai/
|
+-- backend/
|   |
|   +-- main.py
|   +-- scanner.py
|   +-- browser_scanner.py
|   +-- vision_scanner.py
|   +-- ai_analyzer.py
|   +-- requirements.txt
|   +-- screenshots/
|
+-- frontend/
|   |
|   +-- src/
|   |   +-- App.jsx
|   |   +-- App.css
|   |
|   +-- package.json
|   +-- vite.config.js
|
+-- .gitignore
+-- .env.example
+-- README.md
```

## Installation

### Requirements

- Python 3.10+
- Node.js 18+
- npm
- Git
- Chromium
- Playwright

### Clone the repository

```bash
git clone https://github.com/zvozvozvo/websentinel-ai.git
cd websentinel-ai
```

## Backend Setup

```powershell
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python -m playwright install chromium
```

Create a `.env` file inside the `backend` directory:

```env
NOUS_API_KEY=your_api_key_here
NOUS_TEXT_MODEL=openai/gpt-oss-120b
NOUS_VISION_MODEL=your_vision_model_here
```

Never commit your real API key to the repository.

## Start the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## Scan Workflow

1. Enter a website URL.
2. WebSentinel crawls the website.
3. Technical issues are detected.
4. Playwright opens the website in Chromium.
5. Browser and JavaScript errors are collected.
6. A website screenshot is generated.
7. AI analyzes the detected issues.
8. The vision model analyzes the screenshot.
9. The dashboard displays the complete QA report.
10. AI-generated fixes can be copied directly from the interface.

## Example

```text
WEBSITE HEALTH
84 / 100

Technical Issues
- Missing H1
- Missing meta description
- Missing canonical URL

Browser Issues
- JavaScript runtime error
- Failed network request

Visual Issues
- Low text contrast
- Excessive whitespace
- Inconsistent spacing
```

## Roadmap

### Completed

- [x] Website crawling
- [x] HTTP error detection
- [x] Broken link detection
- [x] Missing H1 detection
- [x] Missing meta description detection
- [x] Missing canonical detection
- [x] JavaScript console error detection
- [x] JavaScript runtime error detection
- [x] Failed network request detection
- [x] Broken image detection
- [x] Website health scoring
- [x] AI issue analysis
- [x] AI-generated fixes
- [x] Playwright screenshots
- [x] AI visual QA

### Planned

- [ ] Responsive visual testing
- [ ] Desktop / tablet / mobile analysis
- [ ] Visual regression testing
- [ ] Screenshot issue highlighting
- [ ] Scan history
- [ ] Website comparison
- [ ] Automated reports
- [ ] PDF reports
- [ ] GitHub Actions integration
- [ ] CI/CD integration
- [ ] Scheduled scans
- [ ] Public API
- [ ] Team dashboards
- [ ] Authentication
- [ ] Cloud deployment

## Security

API keys are stored using environment variables and should never be committed to Git.

Make sure `.env` is included in `.gitignore`.

If an API key is accidentally exposed, revoke it immediately and generate a new one.

## Current Status

WebSentinel is an active experimental project.

The core technical scanning, browser testing, AI analysis, generated fixes, Playwright screenshot capture, and AI visual QA pipeline are currently functional.

Additional responsive testing, reporting, automation, and cloud features are planned.

## License

MIT License

Copyright (c) 2026 zvozvozvo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
