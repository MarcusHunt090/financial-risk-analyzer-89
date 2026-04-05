'use client';

import { useMemo, useState } from 'react';

type ApiResponse = {
  headline: string;
  cleaned_text: string;
  sentiment: string;
  sentiment_confidence: number;
  topic: string;
  topic_confidence: number;
  risk: string;
  risk_score: number;
  matched_keywords: string[];
  explanation: string;
};

const examples = [
  'Inflation rises unexpectedly as food prices jump',
  'Tech company raises forecast after strong cloud demand',
  'Major bank warns of rising defaults in commercial real estate',
  'Trade tensions ease as exporters see better demand',
  'Home sales rebound after mortgage rates fall'
];

export default function HomePage() {
  const [headline, setHeadline] = useState(examples[0]);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const apiBase = useMemo(() => {
    return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  }, []);

  async function analyze() {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${apiBase}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ headline })
      });
      if (!res.ok) {
        throw new Error(`Request failed with ${res.status}`);
      }
      const data = (await res.json()) as ApiResponse;
      setResult(data);
    } catch (err) {
      setError('Could not analyze the headline. Check that your API service is running and that NEXT_PUBLIC_API_BASE_URL is set correctly.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="hero">
        <div className="title">Financial Headline Risk Analyzer</div>
        <div className="subtitle">
          This version uses a real Python backend with trained sklearn artifacts. Enter a headline to estimate
          sentiment, topic, confidence, and economic risk.
        </div>
      </section>

      <section className="grid grid-2">
        <div className="card grid">
          <div className="label">Headline input</div>
          <textarea value={headline} onChange={(e) => setHeadline(e.target.value)} />
          <div className="row">
            <button onClick={analyze} disabled={loading || !headline.trim()}>
              {loading ? 'Analyzing...' : 'Analyze headline'}
            </button>
          </div>

          <div className="grid examples">
            <div className="label">Try an example</div>
            <div className="row">
              {examples.map((example) => (
                <button key={example} onClick={() => setHeadline(example)} type="button">
                  {example}
                </button>
              ))}
            </div>
          </div>

          {error ? <div className="error small">{error}</div> : null}
        </div>

        <div className="card grid">
          <div className="label">What it returns</div>
          <div className="small">
            The Python API predicts sentiment and topic with trained models, then applies a rule-based risk engine
            using confidence and keyword signals.
          </div>
          <div className="row">
            <div className="pill">Python backend</div>
            <div className="pill">FastAPI</div>
            <div className="pill">scikit-learn</div>
            <div className="pill">Next.js</div>
          </div>
        </div>
      </section>

      {result ? (
        <section className="card grid" style={{ marginTop: 18 }}>
          <div className="label">Analysis result</div>
          <div className="grid grid-2">
            <div className="grid">
              <div className="metric">
                <div className="label">Sentiment</div>
                <div className="value">{result.sentiment}</div>
                <div className="small">Confidence: {(result.sentiment_confidence * 100).toFixed(1)}%</div>
              </div>
              <div className="metric">
                <div className="label">Topic</div>
                <div className="value">{result.topic}</div>
                <div className="small">Confidence: {(result.topic_confidence * 100).toFixed(1)}%</div>
              </div>
              <div className="metric">
                <div className="label">Risk</div>
                <div className="value">{result.risk}</div>
                <div className="small">Risk score: {result.risk_score}</div>
              </div>
            </div>

            <div className="grid">
              <div className="metric">
                <div className="label">Explanation</div>
                <div className="small">{result.explanation}</div>
              </div>
              <div className="metric">
                <div className="label">Matched keywords</div>
                <div className="small">{result.matched_keywords.length ? result.matched_keywords.join(', ') : 'None'}</div>
              </div>
              <div className="metric">
                <div className="label">Cleaned text</div>
                <div className="small">{result.cleaned_text}</div>
              </div>
            </div>
          </div>
        </section>
      ) : null}

      <div className="footer">
        Deploy the frontend and API as separate Vercel services. Set <code>NEXT_PUBLIC_API_BASE_URL</code> on the web service to your Python API URL.
      </div>
    </main>
  );
}
