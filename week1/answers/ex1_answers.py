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
All three conditions produced correct answers, but the presentation style influenced which
valid venue was picked. PLAIN (180 tokens) landed on The Haymarket Vaults, while XML (251
tokens) and SANDWICH (289 tokens) both settled on The Albanach. The structure of the prompt
steered the model's choice even though every condition was right — and it came at a cost:
SANDWICH consumed 60% more tokens than PLAIN to reach the same conclusion.
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
The Holyrood Arms (capacity=160, vegan=yes, status=full) is the trickier distractor. It
ticks every box the question explicitly asks about — headcount and vegan options — and only
falls short on availability, a field the question never mentions. The New Town Vault
(capacity=162, vegan=no) is easier to rule out because the contradiction is right there in
the data. Any model that focuses on the stated criteria and glosses over the status field
will confidently land on The Holyrood Arms instead of the right answer.
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
Part C used the small model (Gemma 2B) and all three conditions still came back correct,
but the pattern shifted. Where the large model split — PLAIN picking The Haymarket Vaults,
XML and SANDWICH picking The Albanach — the small model locked onto The Haymarket Vaults
across the board. The weaker model was more susceptible to how the context was laid out,
which suggests that careful prompt structure matters more on smaller models, not less.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when you are working with a less capable model and when
the dataset contains several plausible-looking options. In this run, the large model
(Llama 3.3 70B) split across conditions — PLAIN went with The Haymarket Vaults, while
XML and SANDWICH both landed on The Albanach — yet all three were right. The small model
(Gemma 2B) behaved differently: every condition pointed at The Haymarket Vaults, a
uniform outcome the large model never produced. The structure of the prompt didn't just
drive up token usage, it changed which valid venue the model latched onto — and that pull
was noticeably stronger on the weaker model. In practice this means prompt layout is
something you tune more carefully, not less, as you move toward leaner or cheaper models
in a deployed system.
"""
