# MTBseq Modernization Migration Plan (Phase 0/1)

This document defines a safe, incremental recoding path from legacy MTBseq to a modern, observable, JSON-first pipeline.

## Goals

1. Keep scientific reliability while modernizing implementation.
2. Improve runtime and reduce intermediate I/O.
3. Make logging first-class and machine-readable.
4. Standardize outputs around:
   - VCF (canonical variants)
   - JSON (report contract)
   - whole-genome FASTA (consensus)

## Guiding principles

- **No big-bang rewrite**: move in validated phases.
- **Parity before replacement**: compare against legacy MTBseq at every phase.
- **Rollback always available**: every phase is a releasable safe stopping point.

---

## Phase plan with safe stopping points

### Phase 0 — Specification freeze

**Deliverables**
- JSON report schema v0.1.
- Output definitions for VCF and FASTA.
- Baseline acceptance metrics:
  - resistance prediction concordance
  - lineage concordance
  - SNP/indel concordance
  - runtime, RAM, disk footprint

**Safe stopping point A**
- Only specs and benchmarks are added.
- Production still runs legacy MTBseq unchanged.

### Phase 1 — Wrapper + observability around current MTBseq

**Deliverables**
- Thin wrapper command that runs current MTBseq.
- Structured logs (`jsonl`) capturing:
  - run ID, sample IDs, step, start/end timestamps
  - command line and tool versions
  - exit code, wall-clock duration
- Converter from current tabular outputs to JSON report v0.1.

**Safe stopping point B**
- Existing scientific behavior is unchanged.
- You gain robust logging and JSON outputs immediately.

### Phase 2 — Workflow engine migration (same biology)

**Deliverables**
- Re-express current stages in Nextflow/Snakemake.
- Preserve thresholds/default behavior from legacy pipeline.
- Add resume/caching and per-step metadata.

**Safe stopping point C**
- Modern orchestration in place.
- Scientific parity expected with legacy pipeline.

### Phase 3 — Performance modernization

**Deliverables**
- Remove or streamline low-value intermediate artifacts.
- Replace legacy computational hotspots only with parity tests.
- Publish benchmark deltas vs baseline.

**Safe stopping point D**
- Hybrid modern stack with measurable speed/storage gains.

### Phase 4 — Native modern output contract

**Deliverables**
- VCF as canonical variant output.
- JSON report as stable contract for downstream apps.
- Whole-genome FASTA consensus generation standardized.

**Safe stopping point E**
- Target output contract fully available.

### Phase 5 — Legacy decommissioning

**Deliverables**
- Keep `legacy` mode for at least one release cycle.
- Migration notes and output-difference documentation.
- Remove old path after sign-off.

**Safe stopping point F**
- Full migration complete with rollback history.

---

## Initial 2-week execution checklist

1. Define `report.schema.json` (v0.1).
2. Implement wrapper run manifest (`run.json`) and structured logs.
3. Build first output converter to JSON.
4. Run benchmark set on representative samples.
5. Publish pass/fail summary against acceptance metrics.

## Suggested acceptance gates (first release)

- Resistance call concordance: >= 99% vs baseline set.
- Lineage concordance: >= 99% vs baseline set.
- High-confidence SNP concordance: >= 99.5%.
- Runtime improvement: >= 1.5x median, or disk usage reduction >= 30%.

If scientific concordance gates fail, performance gains do not qualify the release.
