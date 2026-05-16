# Codex Weekly Automation Prompt

Create this week's research brief for the `ai-research-briefs` repository.

## Scope

Find the 10-20 most important papers, journals, and technical articles published or last updated in the previous 7 days across:

- Computer Science
- AI/ML
- Recommender Systems
- LLMs
- AI Agents
- adjacent areas relevant to AI engineering and product systems

## Source Priorities

Prioritize credible sources such as:

- arXiv
- ACM Digital Library
- IEEE
- ACL Anthology
- OpenReview
- NeurIPS, ICLR, ICML, AISTATS, CVPR proceedings when newly relevant
- Google Research
- DeepMind
- OpenAI
- Anthropic
- Meta AI
- Microsoft Research
- Apple ML Research
- Amazon Science
- Hugging Face
- Papers with Code
- reputable technical research blogs

## Selection Rules

- Prefer strong novelty, technical quality, practical relevance, or likely research impact.
- Avoid duplicates and near-duplicates.
- Exclude weak, thin, or promotional content.
- If fewer than 10 strong items exist, publish fewer rather than dilute quality.

## Required Output

1. Create or update the digest at `docs/YYYY/MM/YYYY-MM-DD.md` for today's date.
2. Group entries by semantic theme.
3. Add:
   - executive summary
   - key trends of the week
   - strongest papers to read first
   - caveats about freshness, peer review status, or weak evidence
4. For each item include:
   - title
   - published date or last updated date
   - authors
   - institutions or affiliations when available
   - source link
   - topic tags
   - estimated reading time
   - relevance rating out of 5
   - quality rating out of 5
   - concise summary
   - problem investigated
   - context
   - possible solutions explored
   - key results
   - conclusion
   - my take
5. Run:
   - `python3 scripts/generate_index.py`
   - `python3 scripts/rss.py`
6. Commit and push only if meaningful new content was produced.

## Style

- minimalist
- technical/editorial
- concise
- easy to scan
- professional
- no marketing tone
- avoid complex wording and long paragraphs
