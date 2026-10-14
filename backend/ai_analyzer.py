import os
import json
import base64

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("NOUS_API_KEY")

TEXT_MODEL = os.getenv(
    "NOUS_TEXT_MODEL",
    "openai/gpt-oss-120b"
)

VISION_MODEL = os.getenv(
    "NOUS_VISION_MODEL",
    "google/gemini-3-flash-preview"
)

client = None

if API_KEY:

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://inference-api.nousresearch.com/v1"
    )


def analyze_issues(issues, screenshot_path=None):

    result = {
        "summary": "",
        "recommendations": [],
        "visual_analysis": None
    }

    if not client:

        result["summary"] = (
            "Nous AI API key is not configured."
        )

        return result

    # ==========================================
    # TEXT ANALYSIS
    # ==========================================

    if issues:

        limited_issues = issues[:30]

        prompt = f"""
You are a senior website QA engineer
and frontend developer.

Analyze these detected website issues.

For every important issue provide:

- issue
- severity
- why
- fix
- code

Return ONLY valid JSON.

Format:

{{
  "summary": "short overall assessment",
  "recommendations": [
    {{
      "issue": "problem name",
      "severity": "critical/high/medium/low",
      "why": "why this matters",
      "fix": "how to fix it",
      "code": "ready to use code or empty string"
    }}
  ]
}}

Do not invent problems.

Detected issues:

{json.dumps(limited_issues, indent=2)}
"""

        try:

            response = client.chat.completions.create(
                model=TEXT_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert website "
                            "QA engineer and frontend developer."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )

            content = response.choices[0].message.content.strip()

            if content.startswith("```"):

                content = (
                    content
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            text_result = json.loads(content)

            result["summary"] = text_result.get(
                "summary",
                ""
            )

            result["recommendations"] = (
                text_result.get(
                    "recommendations",
                    []
                )
            )

        except Exception as e:

            result["summary"] = (
                "AI text analysis failed."
            )

            result["text_error"] = str(e)

    else:

        result["summary"] = (
            "No technical issues detected."
        )

    # ==========================================
    # VISION ANALYSIS
    # ==========================================

    if screenshot_path:

        try:

            with open(
                screenshot_path,
                "rb"
            ) as image_file:

                image_data = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            vision_prompt = """
You are a senior UI/UX and visual QA engineer.

Analyze this screenshot of a website.

Look ONLY for visible problems.

Check for:

- broken or obviously missing visual elements
- overlapping elements
- clipped content
- unreadable text
- poor contrast
- broken layouts
- excessive whitespace
- mobile/responsive problems if visible
- buttons that look broken
- navigation problems
- inconsistent spacing
- obvious accessibility problems
- obvious visual bugs

Do not criticize normal design choices.

Return ONLY valid JSON.

Format:

{
  "summary": "short visual assessment",
  "issues": [
    {
      "title": "short problem name",
      "severity": "critical/high/medium/low",
      "description": "what is visually wrong",
      "recommendation": "how to improve it"
    }
  ]
}

If there are no obvious visual problems,
return an empty issues array.
"""

            response = client.chat.completions.create(

                model=VISION_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert visual "
                            "website QA engineer."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": vision_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": (
                                        "data:image/png;base64,"
                                        + image_data
                                    )
                                }
                            }
                        ]
                    }
                ],

                temperature=0.2
            )

            content = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            if content.startswith("```"):

                content = (
                    content
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            result["visual_analysis"] = json.loads(
                content
            )

        except Exception as e:

            result["visual_analysis"] = {
                "summary": "Visual AI analysis failed.",
                "issues": [],
                "error": str(e)
            }

    return result