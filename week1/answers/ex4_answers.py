"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues in the known list can accommodate 300 guests with vegan options. The largest available venue with vegan options is The Albanach at 180 capacity, which still falls short of 300."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changing The Albanach's status from 'available' to 'full' in mcp_venue_server.py
caused it to disappear from Query 1's results entirely — search_venues filters
on status == 'available', so it was quietly excluded. The Haymarket Vaults became
the only match returned.

Query 2 (300 guests) was unaffected — it was already returning zero matches and
continued to do so.

Crucially, no client code changed. exercise4_mcp_client.py was not touched.
research_agent.py was not touched. The agent discovered the updated tool state
at runtime through MCP, got a different result back from the server, and
reasoned accordingly — without knowing or caring that the data had changed.
That's the point of the experiment: the tool layer and the agent layer are
genuinely decoupled.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0   # tools defined in venue_tools.py, not in the exercise file
LINES_OF_TOOL_CODE_EX4 = 0   # tools defined in mcp_venue_server.py, discovered dynamically

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
Putting tools in a separate file is just refactoring. MCP buys something
different: any client that speaks the protocol can connect, regardless of
language or framework. In this exercise a LangGraph agent and a Rasa action
both connect to the same server without either knowing the other exists.

When the venue data changes, you update mcp_venue_server.py once. Neither
client needs to be redeployed, restarted, or even aware of the change — they
discover the current tool state dynamically each time they connect. In the
hardcoded Exercise 2 approach, adding a new tool means editing the agent's
import list and restarting the process. With MCP you just add it to the server.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)

WEEK_5_ARCHITECTURE = """
- Planner (autonomous-loop half): a strong reasoning model upstream of the
  ReAct loop that takes Rod's raw WhatsApp message and breaks it into ordered
  subgoals before the Executor sees it, so the loop never has to handle an
  ambiguous task mid-run.

- Executor (autonomous-loop half): the research_agent.py ReAct loop from
  Week 1, extended with real web search and file tools. Carries out the
  subgoals the Planner produces, calls tools, handles failures, and either
  returns a result or routes to the structured agent via the handoff bridge.

- Shared MCP Tool Server (shared layer): the mcp_venue_server.py from Week 1,
  grown to cover every capability both halves need — web search, venue lookups,
  calendar, email. Both the autonomous loop and the Rasa agent discover tools
  from here dynamically, which is what lets the hybrid system stay coherent
  when tools are added or updated.

- Handoff Bridge (shared layer): a bridge.handoff module that lets the
  autonomous loop delegate a human conversation task to the Rasa structured
  agent and receive the outcome back. When the pub manager calls, the loop
  hands off rather than trying to handle it with a ReAct loop, and resumes
  once the structured agent returns a result.

- Structured Agent (Rasa CALM half): the exercise3_rasa/ confirmation agent
  from Week 1, wired to the shared MCP server and extended with a RAG
  knowledge base for questions flows.yml doesn't cover. Handles all
  human-facing interactions where every word could create a legal or financial
  commitment, then hands back to the loop when research is needed.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph belongs on the research problem and Rasa CALM belongs on the
confirmation call. Running both exercises back to back made this feel less like
a design principle and more like something you can just see.

In Exercise 2 Task A, the LangGraph agent got a single brief and figured out the
sequence on its own — checked The Albanach, skipped The Haymarket Vaults once it
had a match, moved to catering costs, checked the weather, generated the flyer.
Nobody told it the order. That's exactly what the research problem needs, because
you can't script the steps in advance when availability, weather, and capacity all
change at runtime.

Swapping the two agents around falls apart quickly. In Exercise 3, when I
interrupted the Rasa agent mid-booking with an out-of-scope question about
parking, it deflected cleanly but then silently dropped the vegan_count slot —
the booking confirmed with 0 vegan meals. A structured agent with no ability to
reason around unexpected inputs would be useless for open-ended research. The
other direction is just as broken: in Exercise 2 Scenario 3, the LangGraph agent
reasoned freely about train times from its own training knowledge even though it
had no relevant tool. That kind of improvisation is what makes it good at
research; it's exactly what you don't want when an agent's words might constitute
a legal commitment or lock Rod into a deposit he hasn't approved.
"""
