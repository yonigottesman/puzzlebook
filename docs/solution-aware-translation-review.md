# Solution-aware translation review

All 313 full solutions reviewed; 58 Hebrew statements revised. These private notes explain semantic corrections and may discuss answers. They are not included in the public catalog or served by the app.

Reviewed every full solution for puzzles 1–105 in tmp/extracted.json against current Hebrew and the original questions. This isolated patch changes 16 puzzle bodies; titles, difficulty levels and skill tags remain unchanged. Restored narratives from the prior translation review remain intact. No answer or solving strategy was added to public wording.

Changed IDs and semantic reasons:
- 2: The teacher explicitly asks whether the two pupils are a pair of identical twins. This makes the Hebrew denial about being a twin pair coherent with the source solution, where they belong to a larger simultaneous sibling set. All names, surname spelling/pronunciation, first-row seating and unison dialogue remain.
- 8: Count rotations relative to the table, not relative to the stationary coin or number of orbits.
- 15: State the standard 365-day independent uniform birthday model used in the solution; exclude Feb.29 for the reader too. No sample-size answer is given.
- 17: Any three of the player's pocketed balls can form the winning sum, rather than requiring the player to win using exactly their first three balls.
- 19: The English volumes are explicitly arranged I, II, III left-to-right. This prevents Hebrew reading/book-order conventions from reversing the intended geometric premise; page locations are not explained.
- 22: Facing straight upward is required. Merely partly upward has a different probability, explicitly distinguished by the solution.
- 24: Preserve Mrs Chance while specifying random sampling of a two-child mother and conditioning on her yes response to the stated question, plus the uniform independent sex/weekday model used by the solution. The solution itself warns that other acquisition mechanisms change the conditional probability.
- 39: State fixed bias, independent tosses and nonzero probability of either face, precisely the requirements noted in the solution. No fair-extraction method is disclosed.
- 40: Raises increase the ongoing weekly/monthly/annual salary rate; the old phrasing could imply a fixed recurring bonus instead.
- 41: Meeting times refer to the first meeting after departure.
- 47: The random responder answers yes/no irrespective of the question, as distinguished by the source solution from randomly deciding whether to tell the truth.
- 58: The pizza and its pieces stay in place between straight cuts, as assumed by the planar-cut solution; rearranging/stacking would change the problem.
- 65: Explicit flat ceiling, the reduction to a two-dimensional disk assumed at the start of the solution.
- 54 and 66: Independent uniform choices are explicit; correlated uniformly marginal choices would produce a different answer.
- 76: Coordinate-plane projections are orthogonal, as required by the geometry in the solution.

All other assigned puzzles were checked and retained. In particular the portrait relation, nested-bag possibility, poisonous-square rule, optional repeat turn, incandescent lamp, sequential hats/late executions, signed ordered sum-of-squares pairs, freely chosen missing card and table-tennis stopping rule all preserve their required logical hinges.


# Solution-based Hebrew review: puzzles 106–210

Read the full extracted solution for every one of the 105 assigned puzzles and compared it against the current full Hebrew statement and original premise. Revised 22 rows for semantic correctness or essential conventions; all other rows retained. Difficulty and skill classifications are unchanged. All restored narrative, dialogue, proper names, examples, and subquestions remain.

No solution, strategy, answer, or hint was added to the public Hebrew statements. In particular, no face-merging clue was added to 200, no convergence conclusion was added to 201, and no parity/matching/representative-sequence construction was added to the relevant puzzles.

The rationales below are PRIVATE review notes and must not be served by the app.

- **110**: The table may have concave 270° interior corners. Replaced “all corners are right angles” with perpendicular adjacent sides, preserving the separately stated 90° starting corner and allowing the nonconvex geometry of the proof.
- **111**: The solution explicitly includes m=n. Clarified which stack may be chosen when the stack sizes are equal, rather than implying no larger stack exists and hence no legal move.
- **118**: The handshake proof requires Nicholas and Alexandra to be partners. Made explicit the relationship implied by the English “ten other couples”; did not disclose any handshake deduction.
- **124**: The information-value calculation uses the standard balanced 52-card deck. Stated the ordinary deck/color convention rather than leaving “a deck” open to custom sizes or colors.
- **126**: The solution uses a subsequence, not a consecutive block of players. Clarified that the chosen players need not stand next to one another, preserving their original order without adding a selection strategy.
- **137**: The cyclic-preference solution assumes sincere voting with fixed preferences. Added that premise without revealing the cycle or predicting the winner.
- **140**: Replaced the vague “before the boundary” with absence of line endpoints inside the large square, the actual tile-matching condition.
- **151**: The edge ordering relies on distinct road names. “Unique” makes explicit the English “own name” convention without introducing the increasing-walk strategy.
- **154**: As for 140, specifies endpoint continuity across tile boundaries without excluding closed interior curves or adding a construction hint.
- **156**: The solution defines nontriviality on the possible range 0…n, not arbitrary integers. Clarified that the true and false cases must both be feasible counts for this town.
- **159**: The area argument pairs triangles across shared edges. Replaced “surrounded” with the correct edge-adjacency condition, avoiding an unintended condition on mere vertex contact.
- **162**: Domino adjacency is orthogonal; “neighboring” can include diagonal neighbors in other puzzles. Made the sharing-a-side convention explicit.
- **163**: The ant solution counts equiprobable direction assignments. Made the independent, fair choices implicit in the source explicit, without mentioning the balancing criterion.
- **165**: “Side” in Hebrew can inadvertently restrict shapes to polygons. The intended brownie constructions allow curved boundaries, so used a shared boundary segment; did not suggest curved shapes explicitly.
- **166**: Distinct numeric angles can represent the same unoriented line direction (differing by 180°). Specified genuinely distinct directions, which is what the double-cover premise requires.
- **171**: The tournament parity argument assumes one match per unordered pair, the standard single round-robin convention. Made this explicit.
- **175**: The key is the distinction between game-win advantage and series-win advantage. Asked explicitly for the objective already described by the premise, without revealing why the game counts can mislead.
- **182**: The game depends on standard opposite-face numbering and actual quarter-turns onto adjacent faces; a rotation about the vertical axis would not change the upper face. Stated the die and move conventions used by the solution without identifying winning positions.
- **189**: Explicit one-match-per-pair convention matches “round-robin” and the conserved intergroup scoring used by the proof.
- **197**: The minimum-time strategy starts from empty buckets. Explicit initial emptiness prevents the undefined alternative of partly filled starting buckets.
- **206**: The spacetime proof uses constant velocity, including direction. Hebrew “מהירות” alone may mean scalar speed, so clarified no reversals.
- **208**: The poker strategy assumes the ordinary deck and ordinary poker hand order. Stated these conventions without naming decisive cards, royal-flush blocking, or any other strategy.


# Solution-aware Hebrew review: IDs 211–313

All 103 full solution fields in tmp/extracted.json were read and checked against current Hebrew premises. Targeted revisions only; narratives, proper names, examples, levels, and skill codes retained. No solution steps or outcomes inserted into the public puzzle text.

Changed IDs and rationale:

- 215: Specify orthogonal projections. The common-diameter argument presumes perpendicular projection rather than perspective or arbitrary oblique projection.
- 218: State Alice plays first. The solution distinguishes the second player, so named-player convention must be unambiguous.
- 224: Specify equiprobable die faces. Counting ways yields the intended sum distribution only for fair dice.
- 233: Specify an ordinary 52-card deck. The maximal guarantee in the solution depends on 26 red and 26 black cards.
- 234: Specify integer n, as used by the induction and finite-pair argument.
- 240: Make independent draws and knowledge of only one's own number explicit. The bluffing-game equilibrium depends on those conventions.
- 247, 254, 256: Explain best-of-seven as first to four victories, so stopping conditions are clear to Hebrew readers unfamiliar with baseball. In 254 also specify that 'happy' compares the updated championship probability with the probability after game one, exactly the comparison in the solution.
- 253: Replace a square being 'מסומנת' (marked) with 'נבחרה' (selected). A visible mark would let Cressida identify the answer without the coin protocol.
- 269: Specify choosing the available napkin when only one remains, choosing uniformly when both remain, and going without only when neither remains. These are the exact napkin process used in the probability argument.
- 278: Say at most one bit may change. The zero-change option is essential when the broadcast already encodes the intended message.
- 282: State no seconds hand. The book solution explicitly requires it, along with continuous movement and no AM/PM distinction already present.
- 290: Say the slice is flipped upside down, rather than a generic flip; this preserves the physical operation used by the solution without discussing the resulting pattern.
- 295: Specify consecutive tosses, so readers cannot interpret the desired string as a subsequence or separate four-toss blocks.
- 300: State the needle toss is random, preserving the probabilistic premise.
- 306: Specify straight-line distances, as the solution treats house locations as planar points; road distances would change the question.
- 308: Specify simultaneous painting and distances along the fence, rather than straight-line distances. The argument compares the neighboring circular intervals; sequential starts could let a painter pass an unstarted neighbor.
- 310: Replace 'מספר האחדות' with counting occurrences of the digit 1, avoiding a possible reading as the units digit.
- 312: State the near ball is initially at rest, matching the initial y=0 state in the solution and the three-collision baseline.

Intentional ambiguities retained: 261 may have no finite largest submission, 262 leaves the method of choosing a random chord undefined (the puzzle's central issue), 263 does not constrain hole direction, 297 does not require a convex polyhedron, and 307 promises only that eavesdroppers cannot identify the killer with certainty, rather than claiming zero information leakage. Existing key assumptions remain intact in 212 (integers), 223 (finite monotone path segments), 232 (public guesses/results), 238 (unknown light state and no external interference), 260 (second touchdown and fair overtime), 276 (collinearity), 303 (probability-one conclusion), and 311 (independent dispensed amounts).

