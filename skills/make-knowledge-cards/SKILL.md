---
name: make-knowledge-cards
description: Convert a pasted article or a local Markdown/TXT file into 5-8 standalone knowledge cards, each with a title, core knowledge, a plain-language explanation, and an example or self-test question. Use when the user wants study cards, flashcard-style summaries, or revision material from notes, papers, textbook passages, blog posts, or documentation. Does not handle web pages, PDF, Anki export, or a GUI.
argument-hint: <pasted article text or path to a .md/.txt file>
---

# Make Knowledge Cards

## Overview

Turn one plain-text source (pasted article, `.md` file, or `.txt` file) into 5-8 knowledge cards. Each card teaches exactly one idea that the source actually states.

## Workflow

1. **Read the whole source first.** If it is a file, read it completely before extracting anything. Do not skim.
2. **List candidate knowledge points** — terms and definitions, mechanisms, distinctions, constraints, numbers, cause-effect relations, methods and their preconditions, caveats the author flags.
3. **Filter by importance.** Keep a point only if skipping it would leave the reader able to state the source's main conclusion but not understand it. Drop greetings, filler, promotional restatement, and background the reader already has.
4. **Dedupe.** Merge candidates that are the same idea in different words, and adjacent sentences forming one concept cluster (e.g. "mechanism X weakens the effect" + "the effect can partly recover" = one card about mechanism X). Split only when each half would stand on its own as a separate card.
5. **Select 5-8 cards** from what survived, ranked by how much understanding degrades without them.
6. **Write the cards** in the format below.
7. **Verify against the source** (see Self-check) before presenting.

## What is NOT a knowledge point

Do not build cards from:
- **Pure logistics of a one-off event**: dates, times, venues, deadlines, "bring your own badge", sign-up instructions. Announcements, notices, meeting minutes, invitations and similar sources usually contain few or no knowledge points — output 1-3 cards at most, or state that the source has none, rather than converting each sentence into a card.
- **The source's structure** ("the article has three parts", "the author then argues").
- **Opinion without a stated reason**, unless the reason is what the source is teaching.

## Card format

```markdown
### Card N — <short specific title>

**核心知识 / Core knowledge:** <one sentence stating the fact or concept, using the source's own terms where they matter>

**解释 / Explanation:** <2-4 sentences in plain language: why it works or matters, what it depends on, what it is easy to confuse it with>

**例子或自测 / Example or self-test:** <either a concrete example taken from the source, OR a short question the reader can answer — plus its answer>
```

- Field labels stay exactly as written above, even for English sources; the card *content* is written in the source's language.
- Titles must be specific enough to identify the idea out of context: `### Card 3 — 施氮时期决定它作用在穗数还是粒数` beats `### Card 3 — 施氮`. No two cards may share a title.
- Output bare Markdown. Do not wrap the cards in a code fence.
- Example branch only when the source itself narrates a case to illustrate the idea; a number or stage name that *constitutes* the concept is core knowledge, not an example. Otherwise use the question branch, and a source with no examples means every card uses a question.
- Keep cards in the order the source raises their ideas, so the cards double as an outline of the argument.

## Hard rules

- **No fabrication.** Every sentence must be traceable to the source. Do not add outside knowledge, numbers, dates, names, mechanisms, or standard values the source does not state — even well-known ones. If the source is vague, keep the card vague instead of filling the gap.
- **Keep hedges and gaps visible.** If the source says "some studies suggest", "I think", "roughly", or admits it does not explain something, carry that marker into the card and say what the source leaves open. Do not repair a hedged claim into a firm one.
- **One idea per card.** Apply the step 4 test: keep a concept cluster together, and split only when each half would stand on its own as a separate card.
- **No restating another card's fact.** When an explanation must refer to a different card, cross-reference it (`与 Card 1 的负相关相呼应 / echoes Card 1`) instead of repeating its content or numbers. Restating a card's *own* fact inside its example or answer is expected and allowed.
- **Do not pad.** If fewer than 5 cards are supported, output only what is supported and append one line, in the source's language, naming the real count — e.g. `源文本信息量仅支持 3 张卡，未凑数。` / `The source supports only 3 cards; not padding.` Never split one idea into several cards to reach 5. If nothing survives filtering, say so and name what kind of source would work.
- **Marginal cards.** A card that exists only to reach the 5-card floor should be dropped instead, even if that brings the total to 4 — say so in the padding note.
- **Do not silently correct the source.** If a claim looks wrong or contradicts another part, keep it as stated and surface the tension — put it in that card's self-test question or as a closing note.

## Self-check

Before presenting, confirm for every card:
- Can I point at the sentence in the source that supports it?
- Does any other card already state this fact?
- Is the example or answer derived from the source?
- Does the title say which idea this is, and differ from every other title?

## Output

Present the cards in the conversation, preceded by one line naming the source and the card count. Save to a file only when the user asked for a file; write to `knowledge-cards/<source-slug>.md` with content identical to what you presented.

## Input handling

Accept: pasted text in the message; local `.md`, `.txt`, or other plain-text files given by path.

Refuse plainly, in the language the user wrote in, without attempting a workaround, for: URLs and web pages, PDF, images, audio/video, Anki export (`.apkg`), GUI requests. State which of these the request involves and ask for the content as plain text or a Markdown/TXT file — asking the user to re-supply the content is the required response, not a workaround.

If a file path is missing or unreadable, ask for the path instead of generating cards from the filename.
