# Skill Interview Protocol

This protocol governs interactive interrogation to gather requirements before scaffolding a new Tier-5 `SKILL.md`.

## Phase 1: Intent Extraction

Parse user input. Identify target domain and primary trigger. Discard unrelated context.

## Phase 2: The 3-Round Skill Grilling

Do not guess requirements. Execute 3 structured rounds of questions (3-4 questions per round). Wait for user answers after each round.

### Round 1: Core Purpose & Identity

1. What exact task does this skill perform?
2. Which Sauron department does this skill belong to (workflow, frontend, backend, database, quality, security, devops, architecture)?
3. Which Fellowship agent owns this skill (Gandalf, Aragorn, Legolas, Gimli, Boromir, Frodo, Samwise, Merry, Pippin)?
4. What is the trigger slash command (for example `/my-skill`)?

### Round 2: Boundaries & Triggers

1. What phrases or user requests MUST trigger this skill?
2. What tasks are strictly OUT OF SCOPE (anti-triggers)?
3. What files or directories does this skill have authority to touch?
4. What files or actions are strictly forbidden?

### Round 3: Quality & Verification

1. What step-by-step workflow steps must the agent follow?
2. What are the stop conditions and hard verification gates?
3. Which specific anti-patterns does this skill prevent (for example AP-1, AP-4, AP-18, AP-26)?
4. Does this skill require auxiliary reference guides in a `references/` subfolder?

## Rules of Engagement

- Stop and wait for user response after every round.
- Number all questions clearly.
- Never write the final `SKILL.md` before completing all 3 rounds.
