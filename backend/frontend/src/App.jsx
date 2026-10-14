import { useState } from "react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(null);

  const scanWebsite = async () => {
    if (!url.trim()) {
      setError("Enter a website URL");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setCopied(null);

    try {
      const response = await fetch(
        `${BACKEND_URL}/scan`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      if (!response.ok) {
        const data = await response.json().catch(() => null);

        throw new Error(
          data?.detail || "Scan failed"
        );
      }

      const data = await response.json();

      console.log("WebSentinel result:", data);

      setResult(data);

    } catch (err) {
      setError(
        err.message ||
        "Could not connect to WebSentinel backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const copyFix = async (code, index) => {
    if (!code) {
      return;
    }

    try {
      await navigator.clipboard.writeText(code);

      setCopied(index);

      setTimeout(() => {
        setCopied(null);
      }, 2000);

    } catch (err) {
      console.error(
        "Could not copy code:",
        err
      );
    }
  };

  const ai = result?.ai_analysis;
  const visual = ai?.visual_analysis;

  return (
    <div className="app">

      <header className="header">

        <div>

          <div className="logo">
            WEB<span>SENTINEL</span>
          </div>

          <div className="subtitle">
            AI-powered website quality assurance
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>

      </header>

      <main>

        <section className="hero">

          <h1>
            Find bugs before your users do.
          </h1>

          <p>
            Automatically scan websites for broken links,
            HTTP errors, JavaScript problems, accessibility
            issues and visual UI bugs.
          </p>

          <div className="scan-box">

            <input
              type="text"
              placeholder="https://example.com"
              value={url}
              onChange={(e) =>
                setUrl(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  scanWebsite();
                }
              }}
            />

            <button
              onClick={scanWebsite}
              disabled={loading}
            >
              {loading
                ? "SCANNING..."
                : "SCAN"}
            </button>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {result && (

          <section className="results">

            {/* SCORE */}

            <div className="score-card">

              <div>

                <span className="score-label">
                  WEBSITE HEALTH
                </span>

                <div className="score">
                  {result.score}
                  <small>/100</small>
                </div>

              </div>

              <div className="score-url">
                {result.url}
              </div>

            </div>

            {/* STATS */}

            <div className="stats">

              <div className="stat">
                <span>Pages</span>
                <strong>
                  {result.summary?.pages || 0}
                </strong>
              </div>

              <div className="stat">
                <span>Issues</span>
                <strong>
                  {result.summary?.issues || 0}
                </strong>
              </div>

              <div className="stat">
                <span>Critical</span>
                <strong>
                  {result.summary?.critical || 0}
                </strong>
              </div>

              <div className="stat">
                <span>JS Errors</span>
                <strong>
                  {result.pages?.reduce(
                    (sum, page) =>
                      sum +
                      (page.console_errors || 0),
                    0
                  ) || 0}
                </strong>
              </div>

            </div>

            {/* AI TEXT ANALYSIS */}

            <div className="panel ai-panel">

              <div className="panel-title">
                AI QUALITY ANALYSIS
              </div>

              {!ai && (
                <div className="ai-empty">
                  AI analysis was not returned by the backend.
                </div>
              )}

              {ai && (
                <>

                  <div className="ai-summary">
                    {ai.summary}
                  </div>

                  {ai.recommendations?.length > 0 && (

                    <div className="ai-recommendations">

                      {ai.recommendations.map(
                        (recommendation, index) => (

                          <div
                            className="ai-recommendation"
                            key={index}
                          >

                            <div className="ai-rec-header">

                              <strong>
                                {recommendation.issue}
                              </strong>

                              <span
                                className={
                                  `severity ${
                                    recommendation.severity ||
                                    "medium"
                                  }`
                                }
                              >
                                {recommendation.severity}
                              </span>

                            </div>

                            <div className="ai-section">

                              <span>
                                WHY IT MATTERS
                              </span>

                              <p>
                                {recommendation.why}
                              </p>

                            </div>

                            <div className="ai-section">

                              <span>
                                RECOMMENDED FIX
                              </span>

                              <p>
                                {recommendation.fix}
                              </p>

                            </div>

                            {recommendation.code && (

                              <div className="code-fix">

                                <div className="code-header">

                                  <span>
                                    GENERATED FIX
                                  </span>

                                  <button
                                    onClick={() =>
                                      copyFix(
                                        recommendation.code,
                                        index
                                      )
                                    }
                                  >
                                    {copied === index
                                      ? "COPIED"
                                      : "COPY FIX"}
                                  </button>

                                </div>

                                <pre>
                                  <code>
                                    {recommendation.code}
                                  </code>
                                </pre>

                              </div>

                            )}

                          </div>

                        )
                      )}

                    </div>

                  )}

                  {ai.error && (
                    <div className="ai-error">
                      AI error: {ai.error}
                    </div>
                  )}

                </>
              )}

            </div>

            {/* AI VISION */}

            {ai?.screenshot && (

              <div className="panel vision-panel">

                <div className="panel-title">
                  AI VISUAL QA
                </div>

                <div className="vision-layout">

                  <div className="vision-preview">

                    <div className="vision-label">
                      WEBSITE SCREENSHOT
                    </div>

                    <img
                      src={`${BACKEND_URL}${ai.screenshot}`}
                      alt="Scanned website"
                    />

                  </div>

                  <div className="vision-results">

                    <div className="vision-label">
                      VISION ANALYSIS
                    </div>

                    {visual?.summary && (
                      <div className="vision-summary">
                        {visual.summary}
                      </div>
                    )}

                    {visual?.issues?.length > 0 ? (

                      <div className="vision-issues">

                        {visual.issues.map(
                          (issue, index) => (

                            <div
                              className="vision-issue"
                              key={index}
                            >

                              <div className="vision-issue-header">

                                <strong>
                                  {issue.title}
                                </strong>

                                <span
                                  className={
                                    `severity ${
                                      issue.severity ||
                                      "medium"
                                    }`
                                  }
                                >
                                  {issue.severity}
                                </span>

                              </div>

                              <p>
                                {issue.description}
                              </p>

                              <div className="vision-recommendation">

                                <span>
                                  RECOMMENDATION
                                </span>

                                <p>
                                  {issue.recommendation}
                                </p>

                              </div>

                            </div>

                          )
                        )}

                      </div>

                    ) : (

                      <div className="vision-clean">
                        ✓ No obvious visual problems detected.
                      </div>

                    )}

                    {visual?.error && (

                      <div className="ai-error">
                        Vision AI error: {visual.error}
                      </div>

                    )}

                  </div>

                </div>

              </div>

            )}

            {/* SCANNED PAGES */}

            <div className="panel">

              <div className="panel-title">
                SCANNED PAGES
              </div>

              {result.pages?.map(
                (page, index) => (

                  <div
                    className="page-row"
                    key={index}
                  >

                    <div className="page-status">
                      {page.status}
                    </div>

                    <div className="page-info">

                      <strong>
                        {page.title ||
                          "Untitled page"}
                      </strong>

                      <span>
                        {page.url}
                      </span>

                    </div>

                    <div className="page-links">
                      {page.links} links
                    </div>

                    <div className="success">
                      ✓
                    </div>

                  </div>

                )
              )}

            </div>

            {/* DETECTED ISSUES */}

            {result.errors?.length > 0 && (

              <div className="panel issues">

                <div className="panel-title">
                  DETECTED ISSUES
                </div>

                {result.errors.map(
                  (issue, index) => (

                    <div
                      className="issue"
                      key={index}
                    >

                      <div>

                        <strong>
                          {issue.type}
                        </strong>

                        <span>
                          {issue.message}
                        </span>

                      </div>

                      <div
                        className={
                          `severity ${issue.severity}`
                        }
                      >
                        {issue.severity}
                      </div>

                    </div>

                  )
                )}

              </div>

            )}

          </section>

        )}

      </main>

    </div>
  );
}

export default App;