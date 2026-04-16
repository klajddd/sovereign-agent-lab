"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit
accepted. I'll send written confirmation to the organiser shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit
I need to check one thing with the organiser before I can confirm. The issue is:
a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call
you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I can only help with confirming tonight's venue booking. For anything else,
please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 0 requiring vegan meals, £200 deposit
accepted. I'll send written confirmation to the organiser shortly.
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM immediately switched to the handle_out_of_scope flow and returned a fixed
response: "I can only help with confirming tonight's venue booking." It then
offered to pick up where we left off. When I said yes, it skipped straight to
asking for the deposit — the vegan_count slot was never collected again. The
booking confirmed with 0 vegan meals, which is incorrect.

What seems to have happened is that when the out-of-scope flow interrupted the
confirm_booking flow, CALM advanced past the vegan_count step rather than
returning to it. The slot stayed empty (defaulting to 0) and the flow continued
to the deposit without flagging the gap. The deflection itself was clean, but
the slot state was silently corrupted in the process — which in a real booking
scenario would mean the kitchen gets no vegan meal order.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph (Exercise 2, Scenario 3) reasoned its way to a clean refusal — it
checked what tools were available, found none relevant to train times, and
wrote a polite decline with suggestions on where to look. It never tried to
call a tool or make anything up. The response felt natural because it came from
the model thinking, not from a template.

CALM handled it differently. It recognised the parking question as out-of-scope
and fired the handle_out_of_scope flow, which returned a fixed canned message.
There was no reasoning involved — just pattern matching to a flow. That's
more predictable, but it came with a side effect: when the conversation resumed,
the vegan_count slot had been dropped and the booking confirmed with 0 vegan
meals. LangGraph has no persistent slot state to corrupt, so this kind of
mid-conversation data loss isn't a risk there. For a high-stakes confirmation
flow, CALM's rigid structure is generally the right call — but this test showed
that interruptions need to be handled more carefully to avoid silent data loss.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Uncommented the four lines in the TASK B block in actions.py. Since it was
around 10am, the real time condition (hour > 16) would never fire, so I
temporarily swapped in `if True:` on the condition line to force the guard to
trigger on every conversation. Restarted the action server, ran a full booking
conversation (160 guests, 50 vegan, £200 deposit), and the agent responded with
"it is past 16:45 — insufficient time to process the confirmation before the 5 PM
deadline" instead of confirming. Reverted to the real condition, left the
`if True:` line as a commented-out reference, and retrained one final time.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
The main thing CALM strips out is the slot parsing boilerplate. Old Rasa required
a FormValidationAction with regex methods to turn "about 160 people" into 160.0,
nlu.yml training examples to classify intents like "I'm calling to confirm", and
rules.yml to map out every dialogue path. CALM replaces all of that with from_llm
slot mappings and flow descriptions written in plain English — the LLM handles
interpretation, and you just describe what each flow is for.

What Python still owns — and should — are the business rules in
ActionValidateBooking. The deposit cap (£300), guest ceiling (170), and vegan
ratio check are straightforward if-statements. They didn't move to the LLM and
shouldn't: if you write "only confirm deposits under £300" in a prompt, the model
might reason around it given the right framing. Python doesn't negotiate.

Something I noticed during the actual conversations that old Rasa wouldn't have
shown: the LLM command parser failed to extract slot values on the first attempt
several times, returning a CannotHandleCommand warning and asking me to rephrase.
Old Rasa's regex was rigid about phrasing, but at least it was deterministic — it
either matched the pattern or it didn't. CALM trades that rigidity for a new kind
of fragility where a perfectly clear response occasionally just doesn't parse.
For a booking call where the manager might be impatient, that's worth being aware of.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
All that overhead — config.yml, domain.yml, flows.yml, endpoints.yml, rasa train,
two terminals, a Pro licence — bought one specific thing: the agent is
constrained to exactly what flows.yml defines. It cannot call a tool that isn't
listed in a flow, it cannot come up with a response it wasn't designed to give,
and it cannot reason its way into creating an unintended commitment. The
Conversation 3 deflection is a good example: CALM returned a fixed message and
offered to resume — it didn't improvise, didn't apologise creatively, didn't
suggest alternatives. Predictable by design.

For a pub booking confirmation, that constraint is the point. LangGraph in
Exercise 2 Scenario 3 reasoned freely about train times from its training
knowledge — that's useful when you want a research agent, but it's a liability
when the agent's words might constitute a legal or financial commitment. The
setup cost buys auditability: you can read flows.yml and know the full set of
things this agent can do. You cannot do the same with a LangGraph loop, where
the paths only emerge at runtime.
"""
