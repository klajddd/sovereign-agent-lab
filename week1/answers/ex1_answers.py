"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three conditions returned correct answers, but then formatting shifted which valid venue
was selected. 
PLAIN (180 tokens) chose The Haymarket Vaults, while both XML (251 tokens)
and SANDWICH (289 tokens) chose The Albanach. 
Structured formatting affected the model's preference even when all conditions were 
correct. This cost more tokens — SANDWICH used 60% more tokens than PLAIN for the same 
correct result.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
A venue that meets most but not all constraints — for example, one with capacity for
160 but no vegan options — is harder to reject because the model must hold multiple
criteria simultaneously and not anchor on the first plausible match.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran on the small model (Gemma 2B) and all three conditions returned correct answers,
but unlike the large model, XML and SANDWICH both converged on The Haymarket Vaults rather
than The Albanach. This shows that structured formatting has a stronger steering effect on
weaker models — the small model was more sensitive to how context was presented, suggesting
that context engineering matters more, not less, as model capability decreases.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the model is smaller or weaker, and when multiple
valid answers exist that satisfy the constraints. With a large model, all three formats
produced correct results. With the small model, structured formats visibly shifted which
correct venue was selected. The implication for agent engineering is that prompt structure
is not just cosmetic — it actively shapes model behaviour, especially in constrained or
resource-limited deployments.
"""
