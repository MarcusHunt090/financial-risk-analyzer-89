# Financial Headline Risk Analyzer

**A full-stack NLP prototype for exploring financial headlines through sentiment, topic classification, and an explainable risk score.**

[Deployment link](https://financial-risk-analyzer-89-meh4.vercel.app)

The application combines a **Next.js / TypeScript** interface with a **Python / FastAPI / scikit-learn** backend. Enter a headline to inspect predicted sentiment, topic, model confidence, matched keywords, and a low/medium/high risk label.

## Start here

The application lives in [`financial-headline-risk-analyzer-v2/`](financial-headline-risk-analyzer-v2/).

1. [Set up the API and frontend](financial-headline-risk-analyzer-v2/README.md#run-locally).
2. [Try the API example](financial-headline-risk-analyzer-v2/README.md#api-example).
3. [Understand the scoring rules and limits](financial-headline-risk-analyzer-v2/README.md#interpreting-the-output).

The score summarizes headline language using classification and rules. This project is separate from my work on macroeconomic time-series early-warning models.

## Related work

- [FinSentiment](https://github.com/MarcusHunt090/nlp-finance): article and text sentiment analysis, model comparisons, and explainability.
- [Related copy of this application](https://github.com/MarcusHunt090/financial-risk-analyzer): the two repositories currently contain the same application source.

Built by [Marcus Hunt](https://github.com/MarcusHunt090), a student developer interested in AI, economics, and technology for community impact.
