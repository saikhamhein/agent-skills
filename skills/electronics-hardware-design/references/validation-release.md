# Validation, controlled changes, and release

Use focused checks during exploration; use the complete release sections only for an actual manufacturing/release handoff or when a concrete risk calls for them. A draft may carry explicit unknowns without a formal waiver. Resolve safety-critical unknowns before physical operation; obtain acceptance for consequential prototype deviations before committing the build.

## Use precise claims

Keep these outcomes separate:

- **Design evidence:** calculations, source inspection, ERC/DRC under named settings, model checks, and review.
- **Prototype release:** a defined build permitted within its accepted risks and restrictions.
- **Measured qualification:** recorded hardware results on identified units/revisions and conditions.

None implies the next. “Pass” must identify the check and its scope. Never present characterization targets as measured ratings, typical curves as guaranteed limits, or one fault test as broad immunity/compliance certification.

## Recheck what changed

For a narrow ECO, build an affected-check list and compare against the exact baseline. Use relevant semantic and geometric diffs, not only byte equality or a clean DRC report.

| Change | Minimum affected evidence to consider |
| --- | --- |
| Text/drawing-only correction | Underlying geometry unchanged; correct displayed values; all changed pages and packet content; affected document hashes |
| MPN or supplier substitution | Exact identity, pin/land/body/rating equivalence, sourcing; applicable electrical/thermal/fault/assembly checks; BOM/model parity |
| Placement/routing/fill | Nets, copper, pair/return geometry, electrical budgets, via/pad/body checks, DRC, fills, mechanical/export parity |
| Stackup or fabrication process | Impedance/return path and tolerances, drills/annuli, material/thermal/assembly effects; manufacturing outputs |
| Enclosure/fastener/model change | Transforms, tolerance/interference, conductive hardware, access/sequence, drawings, relevant physical tests |
| Tool/library/exporter change | Regenerated geometry/net/pin parity, units/origins/rotations, report settings, readable/editable native files |

These are review prompts, not permission to skip interacting risks. Explain excluded checks when their relevance is reasonably in doubt; do not create a checklist of every unaffected subsystem for a small edit. Preserve unrelated approved sources and content. For unchanged manufacturing geometry, compare parsed geometry or metadata-normalized output as appropriate; don't erase meaningful metadata merely to make hashes match.

## At release, close applicable design gates with evidence

- Requirements and approved decisions traced to calculations, selected parts, and constraints
- Pin/net assertions and symbol/footprint/package mapping independently checked where risk warrants it
- Fresh ERC/DRC, ignored checks/exclusions reviewed, actual fills and return paths inspected
- BOM/reference/fitted/DNP parity; placement datum/rotation/polarity checked using the actual assembly route or marked unqualified for automatic assembly
- Drill, mask, paste, copper, edge, and model/drawing exports consistent with native sources
- Fit/access/insulation/assembly checks on the exact PCB and enclosure pair
- Full-page and actual-copper visual review, report inventory complete

Record tool versions, inputs and their hashes, date, method, result, and reviewer provenance. “Reviewed report” is different from “reran check.” If a tool is unavailable, use another legitimate check where it can establish the same claim; otherwise mark that claim unverified.

## Plan physical qualification before claiming readiness

Use [the qualification plan](../assets/templates/qualification-plan.csv) for relevant acceptance criteria and raw-result links. Choose tests from the actual design risks, including current-limited bring-up, rail/reset/enable sequencing, no-load/startup/shutdown, all-load inrush, load-step/loop behavior, protection thresholds and recovery, fault energy, hot voltage/temperature, interface enumeration/traffic/control, and mechanical fit/retention/insulation as applicable.

Record specimen revision, exact test setup/probes/loads, measurement planes, environment, instruments, acceptance limits from cited requirements, and observations. Keep fault testing within a safe plan using appropriate dummy loads and protection. Do not use expensive downstream equipment as the first proof of an unverified protection circuit.

Prototype exceptions need explicit acceptance, affected revision/build, residual risk, usage restrictions, and a closure test/condition. Use [the waiver record](../assets/templates/waiver-record.md). Do not infer acceptance, reuse it on another project, or convert “accepted risk” into “verified performance.”

## Freeze and package

1. Freeze the exact design revision and confirm approved changes. Keep the design-source revision distinct from the later packaging/publication commit; generated-file manifests cannot hash themselves recursively.
2. Reopen native files, regenerate derivatives, and capture reproducible tool/version/configuration records. Preserve required local symbols/footprints/models or valid portable references.
3. Include the artifacts required for this release: native electrical/mechanical sources; schematics and copper plots; exact/grouped BOM as useful; valid assembly outputs if applicable; Gerbers/drills and fabrication notes; mechanical exports/drawings; assembly/fastener instructions; final report and approved renders; validation records, open qualification gates, and release notes.
4. Audit the complete final packet and its editable sources, including retained sections. Map requested/approved visuals to intended roles/pages: a product render does not substitute for a populated-PCB view, and a separate image file does not prove embedding. Remove caches and redundant bundles only within scope; preserve history. Do not include private review chatter, credentials, unrelated files, or select a license without instruction.
5. Hash delivered files and record their relationship to the frozen source. The optional helper below checks inventory/integrity only. It does not run CAD, compare semantics, certify manufacturing, prove provenance, or approve waivers.
6. Publish only to the authorized destination. Verify the resulting revision and file availability; give exact current artifact links and clearly state outstanding tests. Do not describe local authoring as installation or publication.

### Optional release inventory helper

Use Python 3.10+ and copy [release-manifest.json](../assets/templates/release-manifest.json) into a release staging directory. Set required roles to the actual handoff scope, then fill in the source revision, artifact paths and SHA-256 values, and justified omissions. The template shows a broad combined electrical/mechanical release, not required paperwork for every task. Each artifact describes material from the declared frozen design revision; external source documents can be referenced in evidence instead of being silently mixed into that claim.

Run from any working directory:

```
python /path/to/skill/scripts/audit_release.py /path/to/release/release-manifest.json
```

All artifact paths are relative to the manifest's directory and must remain inside it. Symlinks are rejected. Required roles must have at least one artifact or an explicit omission reason; omissions are reported, not approved. Missing, duplicate, unexpected, empty, changed, or hash-mismatched artifacts fail. By default every file below the release directory must be inventoried, except the manifest itself. Use `--allow-unlisted` only for a deliberately partial inventory; it still lists the extras and never claims complete coverage.

The design revision must be a full 40- or 64-digit hexadecimal identifier (Git commit or snapshot SHA-256). The helper checks its form, not its existence or its relationship to file content. Verify that provenance separately. Exit code 0 means this inventory check passed; 1 means inventory/integrity errors; 2 means invalid input or invocation.
