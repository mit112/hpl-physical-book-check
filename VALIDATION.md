# Validation scope — 1.3.5

The optional processor and its regression tests are byte-identical to the private 1.3.4 source. Its 54 tests use synthetic and historical public catalog evidence, not current holdings. They exercise status and format interpretation, branch scope, partial coverage, counts, identity/language declarations, timestamps, record/query provenance, deduplication and local persistence.

This release changes public packaging, portable skill loading, listing metadata and documentation. It does not add a live connector, guarded browser adapter, new print-label aliases or new evidence-processing behavior.

The separate retrieval prototype's offline and live checks are not tests of this public plugin. No end-to-end reliability, universal catalog recall, performance improvement or cross-host certification is claimed. Installation and live access depend on the target host; no fresh public 1.3.5 installation or catalog benchmark has been performed.

Unknown material labels and raw statuses may remain unresolved. Reference and special-collection material does not establish lending or transfer eligibility. A closed candidate list alone does not resolve every processor gap. Treat incomplete negatives as Unable to verify and keep unknown totals unknown.

Run `python3 verify.py` for the repository's complete offline gate. No additional live catalog searches are part of this release preparation.
