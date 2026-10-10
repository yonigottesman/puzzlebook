# Hebrew book hints: IDs 106–210

Translated all 105 assigned hints from tmp/hints-extracted.json and checked terminology against the restored Hebrew puzzle statements. Output content/hints-middle.tsv has one id|hint_he row per ID; validated complete sequence and exactly two fields per row. Preserved the hint strength, questions, rhetorical tone, and named people. No solution expansion or supplementary strategic clues.

Recommended English fixes:

- **141 Baby Frog:** replace `2n × 2n` with `2^n × 2^n`. This is superscript loss during text extraction; the solution inducts on subdivisions 2^n. Hebrew already uses the corrected plaintext formula.
- **159 Painting the Polyhedron:** replace `triangulate the sphere using the tangent points as vertices` with `triangulate the faces of the polyhedron using the tangent points as vertices`. Verified the erroneous sphere wording is actually printed in the book (PDF page 78), rather than introduced by extraction. The solution uses the tangent point within each polyhedron face to triangulate that face; the corrected Hebrew hint names the polyhedron faces, without any additional argument.
- **184 Wild Guess:** `representive` → `representative`.
- **191 Conversation on a Bus:** `to small` → `too small`.
- **158 Path Through the Cells:** `high-numered colors` → `high-numbered colors`.

Terminology notes:

- **114:** “choice” denotes the Axiom of Choice, rendered explicitly as אקסיומת הבחירה, together with parity.
- **180 and 196:** “holes” denotes the board/grid sites for pegs, not only currently empty sites. Rendered נקודות הסריג to match the Hebrew premise and avoid implying that only unoccupied locations are weighted or colored.
- **208:** translated ace-high straight flush descriptively as a same-suit sequence with ace as highest card; no ranks or decisive-card strategy added.
- **170:** retained the original reference to a friendship graph discussed earlier in the chapter; did not add an explanation beyond the hint.
