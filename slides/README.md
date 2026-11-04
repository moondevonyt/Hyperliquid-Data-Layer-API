# 🌙 Moon Dev's Slide Machine

Turn a day of building into a 7 minute lesson.

I build 4 to 6 hours a day. Most of that work dies the second I close the
laptop. Nobody sees it unless they were live. This folder fixes that. I hand
over the file I just built, and it comes back as a deck that teaches the whole
thing in about 7 minutes. One thousand people watch it. That is a thousand
copies of my day, handed out for free, forever.

My time in. No time out for everybody else.

---

## The subagent does this for me

There is a subagent called **`slide-deck`**. It lives at
`~/.claude/agents/slide-deck.md`, so it works from any repo on this machine.

I just say:

> make slides for `bot_cashcat_liqhunt.py`

or

> slide deck this folder

and it builds the whole thing. I do not have to re-explain the format.

**To change how my decks look or read, edit that one file.** The next deck
picks up the change. That is the point: the format lives in the agent, not in
my head, and not in a chat I will never scroll back to.

Finished decks land in `slides/decks/<name>.html`. The agent publishes it as an
artifact and hands me the link.

---

## The shape of every deck

Two parts. Always.

### Part One: the idea (10 slides)

Ten slides that get somebody caught up to speed with me. No code on these. Each
one is a drawing of what the code does, in the order the bot actually runs.

Rules:

- **One sentence per slide.** Max. Short words, real idea. The picture carries
  the rest.
- **Execution order, not file order.** Cold open first, then read inputs, then
  decide, then act, then the loop that never dies.
- **The numbers 01 to 10 are real.** They are a sequence because the bot IS a
  sequence. I never number things that are not a sequence.
- **Every slide is a different drawing.** No template. Crash lines, tanks,
  candles, state machines, molecules, whatever the section actually looks like.
- **Slide 01 is the thesis.** Open with the most surprising thing the code does.

### Part Two: the code

A divider slide that says PART TWO, then the file walked top to bottom, then a
closer that shows the commands to run it.

Rules:

- **One function per slide.** Split a big one in half only if it will not fit.
- **22 to 32 lines per slide.** Under that and the slide feels empty. Over that
  and the type gets too small to read on a phone.
- **Lines under 76 characters.** Re-wrap long calls. Never let a line run off.
- **Font sizes itself.** Every slide measures its own line count and longest
  line, then picks the biggest type that fits. Lands between 15px and 26px.
- **Highlight the money line.** One or two lines per slide get a green bar and a
  glow. That is the line I talk about.
- **Docstrings and comments stay in.** They are the teaching, not filler.

---

## The look

Dark terminal. Single theme on purpose. No light mode, because this is a
terminal and a terminal only exists lit.

| Thing | Color |
|---|---|
| Ground | `#000000` pure black |
| Panel | `#050807` |
| Neon green (good, alive, ours) | `#00FF6A` |
| Red (liquidation, danger, keywords) | `#FF2E3E` |
| Amber (cumulative, strings, warnings) | `#FFB000` |
| Cyan (rare, one idea only) | `#2BE7FF` |
| Neutral (green biased grey, never pure grey) | `#66786D` |

Type is two faces, no webfonts (they get blocked and fall back silently):

- **Mono** for every number, every code line, every price. `ui-monospace, SF Mono, Menlo`.
- **Condensed** for labels and eyebrows, tracked out wide, all caps.
  `Avenir Next Condensed, Roboto Condensed, Arial Narrow`.

Motion: each slide plays a short build when you land on it, and replays if you
come back. Lines draw, atoms pop in, sweeps wipe left to right, the important
thing ignites last. Everything respects `prefers-reduced-motion`.

Ambient: a faint grid and slow drifting green particles behind everything.
Quiet. It should read as a screen that is on, not as decoration.

**Spend the boldness in one place per slide.** One thing glows. Everything else
stays quiet. If two things glow, neither one does.

---

## The honesty rules

These are not optional. I push this to YouTube with my name on it.

1. **No fake data.** If a chart needs numbers I do not have, either pull the
   real ones or label the slide clearly. The CASHCAT deck says
   `FIGURES ILLUSTRATIVE` on the one slide with made up dollars, and
   `cluster spread is schematic` on the two with a made up distribution.
2. **Real values stay exact.** Anything that IS in the code (83%, 0.0458, the
   $10 minimum, `szDecimals = 0`) shows up exactly as written.
3. **Mark what got cut.** If lines were removed from a function to make it fit,
   the slide header says `· trimmed`. Re-wrapping a long line is fine and does
   not count. Deleting logic does.
4. **Never show a `.env`, a key, or a secret.** Not even a redacted one.

---

## Controls

- Arrow keys, space, PageUp/PageDown
- Home and End
- Number keys 1 to 9 jump to the first ten slides
- Click the left or right half of the slide
- Click any tick in the bottom strip. Green ticks are Part One, amber ticks are
  Part Two.

---

## The files

```
slides/
  README.md              this
  deck-template.html     the engine, empty, ready to fill
  decks/                 finished decks, one html file each
    cashcat-liq-hunter.html
```

`deck-template.html` is a working deck with the content removed. It already
has:

- the whole CSS system, both slide types, all the animations
- the SVG helpers (`E`, `T`, `lab`, `add`, `delay`, `dash`, `rng`, `C`, `DEFS`)
- four starter patterns (`pTanks`, `pFlow`, `pColumns`, `pRing`)
- the Part Two divider, which builds its own table of contents from the code list
- the closer terminal window
- the code renderer: python syntax colors, line numbers, money line highlight,
  auto font sizing, docstring prose mode

Everything below the `▼▼▼ FILL THIS IN ▼▼▼` marker is the part that changes per
bot. Everything above it is the machine.

The starter patterns are there so nobody stares at a blank canvas. **A bespoke
drawing beats a reused one every time.** If a section has a real shape, draw
that shape.

---

## What to avoid

The deck should not look like every other AI made page. Stay away from:

- warm cream backgrounds with a serif headline and a terracotta accent
- one lone acid green pop on near black and nothing else
- purple to blue gradient heroes
- Inter or Space Grotesk as the safe font
- emoji as section markers
- everything centered, everything rounded
- numbered markers on things that are not actually a sequence

---

## The workflow, start to finish

1. I build something. 4 to 6 hours, one file, real money on the line.
2. I hand it over: "make slides for `<file>`".
3. The `slide-deck` agent reads it, finds the sections, and builds both parts.
4. It publishes the artifact and gives me a link.
5. I walk Part One on camera to teach the idea (about 4 minutes).
6. I walk Part Two on camera to show the code (about 3 minutes).
7. It goes up. It teaches forever.

Built with love by Moon Dev 🚀
