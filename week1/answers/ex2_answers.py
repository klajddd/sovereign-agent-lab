"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = "The agent skipped checking The Haymarket Vaults entirely — The Albanach passed on the first check so it moved straight to catering, weather, and flyer generation without being told to stop looking."

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The tool never threw an error — it handled the missing provider internally and handed
back a valid success dict with a placeholder URL, so the agent loop got a clean result
and carried on without knowing anything had gone wrong.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
There was no explicit message to quote here — the agent didn't announce it was
changing course. It read the tool result for The Bow Bar (capacity 80, status full,
meets_all_constraints false) and in the very next step called check_pub_availability
for The Haymarket Vaults. The decision to try a different venue happened entirely
inside the model's reasoning, with no visible output between the two tool calls.
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known Edinburgh venues can accommodate 300 guests with vegan options.
The maximum capacity among the listed venues is 200 (The Guilford Arms), but it
doesn't offer vegan options. The Bow Bar has vegan options but is currently full
and only seats 80. Would you like me to suggest alternatives outside this venue
list or adjust the requirements?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "I don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking: 1. The National Rail website (www.nationalrail.co.uk) 2. Train service apps like Citymapper or Trainline 3. The specific train operator's website (e.g., LNER). Would you like help with anything related to Edinburgh pubs, weather, event planning, or catering estimates instead?"

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this seems fine. The agent knew it had no tool for train schedules, didn't try
to call one anyway, and didn't make up a departure time. It just said it couldn't
help and pointed to the right places to look. For a booking assistant that's the
correct move — the dangerous version would be confidently giving Rod a train time
that turns out to be wrong.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph has three nodes — start, agent, tools — and the agent just
loops back through tools until it decides it's done. All the actual decision-making
happens at runtime inside the model; the diagram doesn't tell you which tools will
be called or in what sequence.

flows.yml works the other way around. Every task is listed explicitly with named
steps in a fixed order. The LLM's job is just to pick which flow to start — once
it does, Rasa runs through the steps in order. You can look at flows.yml and know
exactly what the agent will do. With the LangGraph graph you can't.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most unexpected thing was in Task A — the agent never checked The Haymarket
Vaults at all, even though the brief told it to check both venues. The Albanach
came back available on the first try (capacity 180, vegan yes, status available)
and the agent just moved on to catering, weather, and the flyer. Nobody told it
to stop once it found a match; it worked that out on its own. That felt like a
genuinely interesting moment — it did less than it was told because it understood
what the task was actually trying to achieve, not just the literal instructions.
"""