# TB WGS Tool Comparison Scorecard

Use this for MTBseq (legacy), Mykrobe, TBProfiler, and candidate modern pipeline runs.

| Category | Metric | Weight (%) | MTBseq | Mykrobe | TBProfiler | Candidate | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Accuracy | Resistance prediction concordance | 25 |  |  |  |  |  |
| Accuracy | Lineage concordance | 10 |  |  |  |  |  |
| Accuracy | SNP/indel concordance | 15 |  |  |  |  |  |
| Performance | Median wall-clock runtime | 10 |  |  |  |  |  |
| Performance | Peak RAM | 5 |  |  |  |  |  |
| Performance | Disk footprint | 10 |  |  |  |  |  |
| Operability | Install reproducibility (container/workflow) | 8 |  |  |  |  |  |
| Operability | Logging quality (structured + traceable) | 7 |  |  |  |  |  |
| Product fit | Native VCF quality | 4 |  |  |  |  |  |
| Product fit | JSON report readiness | 4 |  |  |  |  |  |
| Product fit | FASTA output support | 2 |  |  |  |  |  |

## Scoring method

1. Normalize each metric to a 0-100 score.
2. Multiply by weight.
3. Sum weighted scores to compare tools.
4. Apply hard gates:
   - resistance concordance must pass threshold
   - lineage concordance must pass threshold

A tool failing hard gates cannot be selected regardless of weighted score.
