# USB DUT hub: bounded worked lessons

## Source and status

These examples were extracted from the USB DUT hub repository at frozen commit [`d496dda93442db02230148e2c6d731601d433488`](https://github.com/saikhamhein/usb-dut-hub/tree/d496dda93442db02230148e2c6d731601d433488). They describe documented decisions and review evidence, not an original reasoning transcript or a guarantee that the hardware is qualified.

The snapshot is R5-LCSC/C5, with 131 fitted parts in 41 catalogue groups. Its current DUT characterization targets are 1 A per port and 2 A combined. Some legacy filenames still say `4x2A`; filenames are not the current requirements. Source access requires permission to the private repository.

Distinguish four scopes when reusing this work:

- **Reusable engineering lessons:** exact identities, operating/fault corners, source-to-output parity, independent assembly checks, and explicit physical gates
- **Sai's preferences:** functional grouping, clear copper-layer review, practical routing geometry, and CAD-linked documentation, listed in [sai-defaults.md](sai-defaults.md)
- **Hub-specific choices:** dimensions, MPNs, stackup, USB geometry, input/protection limits, current targets, fasteners, and assembly method
- **Accepted prototype risks:** unverified behavior or manufacturing tradeoffs accepted for this hub only; acceptance does not validate the behavior

## Selection and sourcing failures worth preventing

- **Suffix and pin-map identity:** the selected APX803S supervisor's SR pinout differs from the SA variant despite the same familiar package family. Qualify the exact orderable part. Generic SOT-23, TO-252, 1206 and crystal footprints also required dimensional correction; inspect actual copper and terminals rather than trusting or rejecting a library name.
- **Complete architecture cost:** the SCT2433 buck choice included an accepted light-load pulse-skipping tradeoff. A planning cost rose after the complete output capacitance/support network was counted. Do not turn a budget-driven choice into a universal cheapest-regulator policy or claim forced-PWM behavior.
- **Inductor equivalence:** a same-land substitute still needed DCR, thermal, normal peak/RMS current, and fault-current analysis. A 3.6 A saturation alternative did not cover the cited 4.25–5.75 A switch-current-limit range. Even the selected part lacked a guaranteed hot saturation minimum, so calculated sensitivity did not close hardware tests.
- **Effective capacitance:** nominal capacitance was insufficient evidence. Exact manufacturer DC-bias data supported one ceramic alternate; tolerance, temperature, and an engineering reserve were applied separately. Typical curves and assumed reserves were not guaranteed limits. A changed hybrid polymer/ceramic network still needed stability/load-step evidence.
- **Protection boundaries:** a static overvoltage threshold estimate did not prove a hard clamp below downstream absolute maximum. Cutoff delay, overshoot and recovery remained physical tests. Regulated-input failed-buck protection did not imply combined surge-plus-failed-buck survival or industrial immunity.
- **Assembly/sourcing identity:** retail stock differed from the PCBA pool; a low-fee catalogue classification did not prove allocation. Budget connector selection drove a changed port target. The native BOM remained authoritative when a visually improved USB-A surrogate model was used.

Evidence: [electrical review](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5/R5_FINAL_ELECTRICAL_REVIEW.txt), [package land audit](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5/R5_STANDARD_PACKAGE_LAND_AUDIT.md), [inductor qualification](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5_LCSC/INDUCTOR_QUALIFICATION.txt), [ceramic qualification](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5_LCSC/OUTPUT_CERAMIC_QUALIFICATION.md), [allocation and fees](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5_ECO/ALLOCATION_AND_FEES.txt). Prices and stock in these records are historical, not refreshed quotes.

## Layout, assembly, and mechanical regression lessons

- Placement approval and electrical gate closure preceded expensive routing. A visually acceptable placement did not resolve regulation/overvoltage margin. The evidence supports this checkpoint order, not a claimed original net-by-net routing algorithm.
- Local support-part moves shortened bypass connections while preserving the USB route geometry. Functional grouping did not mandate squeezing out all residual whitespace.
- Valid connectivity once coexisted with missing outer ground pours. Later, an unanchored higher-priority power island left a void in a lower-priority ground fill. Inspect the actual filled polygons, anchors, priorities and return paths after refill.
- Same-net route/via acceptability did not prove assembly quality. Separate via/pad/body/paste checks were necessary. External thermal vias deviated from the vendor's under-exposed-pad example, so reference-board thermal resistance could not simply be inherited.
- A flush metal insert intersected power and ground beneath soldermask. The enclosure correction used positive plastic insulation and local component relief. The final paired geometry still required physical fit and insulation checks.
- An exporter used footprint anchors as component-centre fields, displacing through-hole assembly previews. ERC/DRC did not catch this. Check the actual placement datum, pin-one/rotation conventions and preview. This snapshot's self-assembly choice did not qualify its retained CPL for automated assembly.
- Reported zero ERC/DRC issues were under inherited settings with ignored checks. Those receipts are scoped evidence, not proof that every possible check passed. Some reviewers examined receipts rather than rerunning tools; preserve that distinction.

Evidence: [routing rules](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/pcb/USB_DUT_Hub_4x2A_Review.kicad_dru), [fill review](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5/R5_FRONT_POWER_FILL_INDEPENDENT_REVIEW.txt), [ECO independent audit](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/R5_ECO/OPTIMIZED_ECO_INDEPENDENT_AUDIT.txt), [current hash audit](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/validation/FINAL_CAD/CURRENT_HASH_AUDIT.txt).

## The impedance exception must not become a design default

Original USB copper geometry targeted a different stackup. A later economical 7628-stackup change retained that copper and was explicitly accepted with unverified impedance. It is a hub-specific prototype waiver, not an impedance pass and not permission to copy the widths into future boards.

For a new design, derive geometry from the selected stackup and interface. Sai's separate preference to omit a paid factory impedance-control service does not waive this engineering step. Reopen signal-integrity checks after a stackup change, or report the unresolved risk and obtain a bounded decision before dependent release.

## What remained to be measured

The snapshot kept explicit gates for current-limited bring-up, simultaneous port enable/inrush, overvoltage cutoff and recovery, loop/load-step/pulse-skipping behavior, hot rail/temperature behavior, USB enumeration/control, and actual assembly/retention/insulation. DNP timing components did not provide port staggering. Characterization targets did not become measured ratings through publication.

Carry forward the method, not unmeasured claims: [prototype acceptance gates](https://github.com/saikhamhein/usb-dut-hub/blob/d496dda93442db02230148e2c6d731601d433488/pcb/PROTOTYPE_ACCEPTANCE_GATES.txt).
