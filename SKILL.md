---
name: hagobogo-cardnews-en
description: HAGOBOGO Instagram carousel ("card news") maker in English — use when creating evidence-based 1080×1350 Instagram carousel slides (6 by default) for English-speaking audiences on male-factor infertility, sperm health, preconception myth-busting, couple health and relationships, or family planning
---

# HAGOBOGO Card News — English edition (hagobogo-cardnews-en)

Plan and produce informational Instagram carousels for INTIN Inc.'s HAGOBOGO **only on topics backed by accurate sources**, for English-speaking audiences worldwide.
Deliverables: 1080×1350 PNG slides, **6 by default** (add a slide only when essential content overflows because of the large type) + long and short captions + pinned comment + hashtags + reference list + RA review checklist.

**When the skill starts, first ask for "the keyword you want this carousel to be about."** Once you have it, check who the topic will reach and recommend 3 topic options. (Step 1)

**Language**: every deliverable — slide text, `caption.md`, `storyboard.md`, `sources.md`, `image_prompts.md`, alt text, and code comments in the work folder — is in English (US spelling), even when other instructions (for example a global AGENTS.md or CLAUDE.md) say to write documents in another language. Talk with the user in the user's own language.

---

## Running in Codex

This skill runs in Claude Code and in OpenAI Codex. The steps below name Claude Code tools; in Codex use these instead:

| Where this skill says | In Codex |
|---|---|
| AskUserQuestion | `request_user_input`. If it isn't available (e.g., in `codex exec`), ask in chat with numbered options and wait for the answer |
| WebSearch / WebFetch / the web-fetch agent | `web.run` to search and open pages. curl and PubMed E-utilities also work when network access is allowed |
| Read (to look at a PNG) | `view_image` |
| TaskCreate | your planning tool if there is one; otherwise skip it |
| SendUserFile | list the file paths |
| Step 6 "Generate directly with a Codex pane" | skip the Orca pane flow. Generate the images yourself with your image generation tool (`image_gen`), save them as `images/bgN.png`, and resize or crop them to exactly 1080×1350 (object images 1024×1024) with Pillow |

**Sandbox (macOS)**
- `render.py` launches Chromium through Playwright, and the Codex sandbox blocks it (`bootstrap_check_in … Permission denied`). Run `python3 render.py …` outside the sandbox: request escalated permissions for that command and let the user approve it (or the user runs Codex in full-access mode). The same applies to installing Playwright or its Chromium if they're missing
- Fetching pages with curl needs network access. Prefer `web.run`, or request approval for the command
- The Inter font files are bundled in `assets/fonts/`, so fonts need no npm or network
- If `preview.py` reports "0 slides", `render.py` didn't run. Fix that first

---

## 0. Scope

**Covered topics (before pregnancy)**
1. Male factors in infertility
2. Sperm health (lifestyle, environment, nutrition, what test parameters mean)
3. Preconception fact-checks (myths vs evidence, for both women and men)
4. Couple health (health habits partners build together)
5. Relationship care (stress and communication while trying to conceive)
6. Family planning (timing, age, the order of preparation)

**Not covered**: care during pregnancy, birth and postpartum, parenting, policy and social issues, celebrity stories.
Benchmarks showed low engagement for these, and they sit outside the brand. If such a keyword comes in, say it is out of scope and ask whether to proceed.

**Bundling out-of-scope material into an in-scope concept**: when lifestyle material such as travel or seasons comes in, also propose an angle that connects it to an in-scope topic. Once the user picks a concept, proceed with it.
- e.g., "Fall getaways" → "A couple takes a fall trip to plan for a baby together" (family planning + relationship)
- Keep the material itself (destinations, etc.) to about one supporting slide, and fill the core message and evidence with in-scope topics (infertility, testing, lifestyle, etc.)
- Never make unsupported links such as "travel helps you conceive"

**Borderline topics (sex myths, etc.)**: e.g., "Swallowing semen is good for you." It touches sperm health but is closer to a sex myth than to pregnancy preparation, and it can trigger Instagram reach limits or fail internal RA review. When such a keyword comes in, say so, and include a **mixed** option among the topic candidates as the recommendation (keep the myth hook → correct it with the original evidence → close with sperm health, testing, and "together"). If the user picks it, proceed
- Keep sensitive wording (e.g., oral sex) to one supporting line on one slide and the caption, and add the wording level to the RA checklist
- Background scenes must not be sexually suggestive (no bedrooms, nudity, or close-ups of white liquid. For liquid scenes use clear water or colored ink)

---

## 1. Brand standards

- **Brand**: HAGOBOGO (INTIN Inc.)
- **Official colors**: `#00B2CF` (cyan), `#003665` (navy)
- **Accent color**: `#FF2A81` (pink). Used for highlighted phrases in tables and body text
- **Logo**: the English HAGOBOGO wordmark, stored in `assets/logo_en.png` and in 'Logo file' at the end of this skill (to replace it, use `scripts/update_logo.py`)
- **Core message**: "I'll go first" (the English form of the brand's Korean core message). Men think and act first in family planning. Infertility is not treated as a woman's problem alone
- **Audience**: English-speaking couples worldwide who are preparing for pregnancy. Card copy is in English (US spelling)
  - **Women are a key audience too.** On Instagram, women do much of the viewing and saving, and they @tag their partners to share
  - Speak to women with "Read this with your partner" and to men with "I'll go first"
  - The default viewpoint within a post is **"together"**. Never put the burden of preparation on women alone
  - Say "partner" and "couple" by default rather than "husband" and "wife"
  - The audience is global. Don't assume one country's health system, insurance, currency, or holidays. When something is country-specific (programs, costs, rules), name the country
- **Tone**
  - Warm, plain, conversational English: second person ("you"), contractions are fine, short sentences, everyday words (roughly a 6th–8th grade reading level)
  - Order: empathize → reassure → correct
  - No fear-mongering, guilt-tripping, blaming men, or blaming women
- **Characters Hago and Bogo**: use them only when the user supplies the image files. Never draw them yourself or generate them with AI
  - The supplied character `assets/character_hc12.png` (transparent PNG) goes **to the left of the Follow button on slide 6 by default**. The character stands and points at the button with an outstretched arm. Its feet float slightly above the bottom border of the follow box, and it overlaps the button by 44px, drawn on top of it. Follow button: cyan background with white text (brand decision), 16px rounded corners, text centered in the button (44px padding on both sides), right edge 24px inside the follow box border. The template reserves room to the left of the button so the character never covers the follow text. Never recolor or stretch it

---

## 2. Workflow

### Step 1: Ask for a keyword → check the keyword → recommend 3 topics (skill start)

**1-1. Ask for a keyword**
- **First ask "What keyword should this carousel be about?"** Ask before researching or making anything
  - Give the 6-topic scope from section 0 in one line and show 3–4 example keywords (e.g., sperm count, timing sex, smoking and sperm, age and fertility)
  - If a keyword was given when the skill was invoked, don't ask again; go straight to 1-2 (keyword check)
  - If no Instagram handle for the Follow button has been given in this conversation, ask for it in the same message. It replaces `{{ACCOUNT}}` on the closing slide. If the user doesn't have it yet, leave the placeholder (render.py will keep warning until it is replaced)

**1-2. Keyword check (who is this topic for?)**
- Posts with huge view counts happen when **people seeing the account for the first time** watch, not existing followers. **The topic sets the size of the audience before the cover design does.** So check the keyword before writing any cover copy (reference: Paddy Galloway's CCN audience model, provided by the brand team)

| Audience | For HAGOBOGO | Check question |
|---|---|---|
| Core | Couples trying to conceive who follow HAGOBOGO. They watch regardless of topic | ① Will existing followers care? |
| Casual | People who don't know the account but care about trying to conceive, sperm health, or couple health. They watch only when the topic fits | ② Would someone generally interested in trying to conceive tap? |
| New | People who know neither the account nor much about trying to conceive. They arrive through Explore, Reels, and friends' shares and tags. They tap only if the topic itself makes them curious | ③ **Would someone seeing HAGOBOGO for the first time be curious?** ← most important |

- When you get the keyword, run a quick search, check the three items below, and show the results as a `Check | Result` table
  1. **Scope**: in scope / borderline / out of scope (section 0). If out of scope, say so and suggest the nearest in-scope topic
  2. **Audience**: Yes · Partly · No for each of questions ①②③, with a one-line reason
  3. **Evidence**: is there a tier 1–2 source? (one source name)
- If ③ is Partly or No, don't drop the keyword; find a **hook that connects it to broad public interest** and widen it (e.g., "how to make YouTube thumbnails" → "5-minute phone-app thumbnail vs pro thumbnail: which gets more clicks?" A topic that only people urgently needing a thumbnail looked for now reaches people without gear and people curious about the result)
  - **Comparison / showdown**: the same task done two ways (e.g., "habits that heat sperm" → laptop on your lap vs on a desk)
  - **Myth flip**: ask about a belief everyone has heard (e.g., "sperm count" → "Is more sperm always better?")
  - **Everyday link**: tie it to objects and habits people use daily (e.g., saunas, tight underwear, a phone in your pants pocket)
  - **Quiz / participation**: let readers guess the answer (e.g., true/false quiz, pick one of three)
- Rules that still apply when widening
  - Stay within the section 0 scope. Don't chase new viewers by going out of scope (pregnancy, parenting, celebrities, etc.)
  - Don't widen with unsupported links, fear, or sensationalism. Cover numbers come only from tier 1–2 sources. Borderline topics follow the mixed format in section 0
  - Even a widened topic fills its core message with evidence-based information. The hook is the way in; don't drift into light lifestyle content

**1-3. Recommend 3 topics**
- Build **3 topic candidates** from the check results and let the user choose with AskUserQuestion (Codex: `request_user_input`). Arrange the three as a ladder that widens one keyword step by step (e.g., a basketball channel's "studio tour → shot-reward challenge → 5 NBA games in 50 hours" drew more people who don't follow basketball the further it went)

| Candidate | Target audience | Example (keyword "sperm count") |
|---|---|---|
| Broad | Core + Casual + New (③ is Yes) | Is more sperm / always better? |
| Interested | Core + Casual (Yes through ②) | 5 habits that / lower sperm count |
| Core | Core (only ① is Yes) | How to read / your semen analysis |

- Attach to each candidate
  - Cover copy draft (title + subtitle)
  - One key piece of evidence (with source name)
  - Check results ①②③ (Yes · Partly · No)
  - One line on how it was widened (for Broad: which hook pulls in first-time viewers)
- **Recommend Broad by default.** Put it as the first option with "(Recommended)". If Broad's tier 1–2 evidence is weak or it conflicts with the Step 5 rules, recommend another candidate and explain why
- If the user already gave a topic and structure, show that topic's check table too and include it as one candidate. Fill the other two slots with the rungs missing from the ladder
- When building candidates, **favor angles with proven engagement** (benchmark: analysis of Mother Insight, a Korean pregnancy-content account. These are Korean-market results; re-check them against your own account's data as it accumulates)
  - Myth vs fact (sex timing, positions, lifestyle myths)
  - Male and couple angles (on the same sauna topic, the husband angle got 69 likes and the pregnant-woman angle got 3)
  - Information that eases anxiety ("It's not your fault")
  - Practical information that changes what people do today
  - Information women want to save and send to their partner (partner tags and shares are also how posts reach first-time viewers)
- Light lifestyle tips, mood posts, and policy news get weak engagement; avoid them
- **If the user provides reference images or other content**, use them only as topic and structure references, and check every number and claim in them against the original paper before choosing a topic
  - Show the results as a `Reference claim | What the original says` correction table together with the keyword check table and the topic question (e.g., "crossing your legs +2.1°C" → the original says "sitting with thighs together"; "sperm recover within 3 months of quitting saunas" → the original says recovery 6 months after stopping)
  - Drop any number whose original you can't find, and record corrections in the sources.md judgment notes
  - Even if a reference image is another Instagram account's content, never cite it as a source (banned source)
- Once the topic is chosen, create a task list (TaskCreate) and proceed in the order below (if TaskCreate isn't available, skip it and just follow the order)

### Step 2: Source research ← most important

**Principles**
- Every fact and number must come **only from original sources you found and opened during this task**. Never use numbers from memory
- Don't put a number on a card unless you opened the original and confirmed the sentence
- Write numbers exactly as in the original (unit, year, population). No rounding, unit conversion, or calculating your own figures
  - The one exception is temperature: write the source's unit first, and you may add the other unit in parentheses for a global audience (°F = °C × 9/5 + 32, one decimal place, e.g., "34.4°C (93.9°F)"). Note the conversion in sources.md. Never convert currencies
- Don't overstate causation. Distinguish "was linked to" from "causes"
- Don't present animal or in vitro studies as findings about people
- Check that guidelines are the latest edition (e.g., the WHO semen analysis manual is the 6th edition from 2021, not the 5th from 2010; the NICE fertility guideline is NG257 (2026-03), which replaced CG156 (2013))
- When evidence conflicts, write "Studies disagree" and show both sides, or propose a different angle
- For claims with no evidence found (e.g., "it's good for you"), don't declare "it doesn't work"; write "There's no evidence for this so far." Record how far you searched (databases, search terms) in the sources.md judgment notes
- For studies often cited as proof of a myth, check the design (survey, correlation, population, route of exposure) in the original abstract, and cite them only to correct the myth (e.g., Gallup 2002, cited as "semen reduces depression," was a survey of female college students on condom use and depression scores, and has nothing to do with swallowing)

**Source tiers**
| Tier | Type | Examples |
|---|---|---|
| Tier 1 (preferred) | International and national clinical guidelines, official bodies | WHO, AUA/ASRM male infertility guideline, ASRM Practice Committee, EAU Sexual and Reproductive Health guidelines, ESHRE, NICE fertility guideline (NG257), ACOG, RCOG, CDC preconception health, NHS, national health agencies (e.g., Health Canada, Australian Department of Health and Aged Care, Korea Disease Control and Prevention Agency), national urology, andrology, and OB-GYN societies |
| Tier 2 | Peer-reviewed systematic reviews and meta-analyses | Cochrane, Human Reproduction Update, Fertility and Sterility, Human Reproduction, Andrology, Lancet and JAMA family journals (indexed in PubMed) |
| Tier 3 (supporting) | Original large cohort studies and RCTs | Always state the study's limitations |
| Banned | — | Blogs, forums (Reddit, etc.), news articles on their own, supplement or vendor sites, Wikipedia, AI summaries, other Instagram or TikTok accounts (including Mother Insight) |

- If you saw something in a news article, find the original paper and cite that
- If an original blocks automated access (e.g., HTTP 403) and you can't confirm the sentence, don't use that number; switch to another tier 1–2 source with the same content. Record the decision in the sources.md judgment notes
- **Non-health supporting information** (destinations, seasons, foliage timing, etc.) uses official sources only, separate from the medical tiers (e.g., national tourism boards, national park services, meteorological agencies). Mark predicted dates as predictions ("expected around…"). Seasons differ by hemisphere; say which one you mean
- **Government programs** (e.g., free or subsidized preconception checkups): confirm the **program year** on the official government page and note it in the sources, name the country, and add "re-check right before posting" to the RA checklist. State in the caption that eligibility and details vary by country and region
- Every key claim needs at least one tier 1–2 source
- Numbers used in the cover hook must come from tier 1–2 sources
- Put **at most 4** sources on the cards. Any extra go only in the caption's reference list

**Method**
1. Search PubMed and official sites with WebSearch (Codex: `web.run`)
2. Open the original (guideline page, paper abstract) with WebFetch and confirm the sentence
   - Without WebFetch: get paper abstracts through PubMed E-utilities. Find PMIDs with `curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<query>&retmode=json"` and fetch the abstract with `curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text"`
   - Fetch guideline and agency pages with `curl -sL -A "Mozilla/5.0" <URL>` and confirm the sentence in the body
   - Agency pages that block curl (e.g., CDC returns HTTP 403): open them with WebFetch, or if there is no WebFetch tool, with the web-fetch agent (Codex: `web.run`), and bring back the original sentence verbatim
   - WHO IRIS documents (e.g., the 6th edition semen analysis manual, handle `10665/343208`): the handle and PDF URLs return only a JavaScript page, so curl can't get the text. Use the DSpace API instead: get the item id with `curl -sL "https://iris.who.int/server/api/pid/find?id=10665/343208"` → find the bitstreams link of the `TEXT` bundle at `https://iris.who.int/server/api/core/items/<id>/bundles` → fetch the `content` link of the `-eng.pdf.txt` file (other language editions have their own suffix) and grep for the sentence
3. Record the fact sheet in `cardnews/<YYYYMMDD>_<topic>/sources.md`

```markdown
| # | Sentence for the card | Original sentence (verbatim, short) | Source (authors, title, organization/journal, year, DOI or URL) | Tier | Slide |
```

### Step 3: Storyboard (6 slides by default)

Write it slide by slide in `cardnews/<YYYYMMDD>_<topic>/storyboard.md`. At the top, record in one line the topic chosen in Step 1 and its check results (candidate type, ①②③, how it was widened), so you can compare against engagement after posting. **The default is 6 slides.** Add a slide only when the overflowing content is clear and essential at the large type size (see "Adding slides" below).

| Slide | Role | Content | Template |
|---|---|---|---|
| 1 | Cover | Hook (question title + subtitle previewing the answer) | `.cover` |
| 2 | Intro | Frame the problem with statistics or the current picture | `.rows` / `.nums` / `.bars` |
| 3 | Body ① | Myth correction + evidence | `.vs` (list-type topics: `.rows` / `.list`) |
| 4 | Body ② | Second key message + evidence | `.bars` / `.list` / `.vs` |
| 5 | Summary | "3 things to remember" + a step the couple can take together | `.list` |
| 6 | Closing | References + disclaimer + follow and partner tag + character | `.refs` + `.disc` + `.follow` |

- One message and one visual per slide
- If it doesn't fit in 6 slides, first tighten the sentences. If the overflow is still clear and essential, add a slide. If it's a side point, cut it or narrow the angle
- **Adding slides**
  - The default is 6. Add a slide only when the overflow at the large type size is clear and essential. Never shrink the type or force out needed content. Conversely, never add filler; cut it
  - Put the extra slide where it fits the flow (between body slides or before the closing), and change every page number to `n/total` (render.py checks this)
  - If long references overflow the closing slide, split it into slide 6 (references + "More references in the caption") and slide 7 (short closing title + disclaimer + follow). Slide 7 can reuse slide 6's photo or get its own `bg7.png`

```html
<!-- Slide 6 references -->
<section class="slide bg" data-bg="images/bg6.png" style="background-image:url(images/bg6.png)">
  <div class="panel">
    <span class="label">References</span>
    <ol class="refs"><li>Author. Title. Journal/Organization. Year</li></ol>
    <p class="src" style="margin-top:auto">More references in the caption</p>
  </div>
  <div class="page">6/7</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>
<!-- Slide 7 closing: title + disclaimer + follow (move .disc and .follow over from template slide 6 unchanged) -->
<section class="slide bg" data-bg="images/bg6.png" style="background-image:url(images/bg6.png)">
  <div class="panel">
    <h3 class="title">Save this and<br>check it together</h3>
    <div class="disc">…</div>
    <div class="follow">…</div>
  </div>
  <div class="page">7/7</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>
```
- **List-type topics** (e.g., "6 habits that heat your sperm"): split slides 3 and 4 into groups by type, 3 items per slide. Slide 3 uses `.rows` (when each item has a number) or `.list` instead of `.vs`, and numbering continues: slide 3 01–03, slide 4 04–06 (e.g., slide 3 "Heat from sitting" `.rows` / slide 4 "Heat from clothes and baths" `.list`)

### Step 4: Copywriting

**General style**
- US spelling, sentence case for titles, labels, and headlines (capitalize only the first word and proper nouns), no ALL CAPS in body copy
- Use numerals for numbers and the `%` sign
- English runs longer than Korean, so the line limits below are in characters (including spaces) per line, measured for Inter at each size

**Cover**
- Title: large (132px), semibold (600), **about 14 characters per line × 2–3 lines (aim for 2)**, a hook ending in a question mark. Break lines yourself with `<br>` at natural phrase boundaries
- Subtitle: regular (400, 62px), **one line of about 28 characters**, previewing the answer or giving a number
- It must read at a glance even small in the feed. If the title reaches 4 lines, cut words (never shrink the type)

| Pattern | Example |
|---|---|
| Myth flip | Is more sperm / always better? |
| Number / study size | What a study of / ○○ men found (exact source number) |
| Male angle | Trying for a baby? / He can go first |
| Couple angle | Who should get / tested first? |
| Showdown | Save it up / or go often? |
| List | 5 checks before / trying for a baby |

**Body slides (2–5)**
- Headline 2 lines max (about 24 characters per line), lead sentence 1–2 lines, about 30 words per slide (the body type is large and has to fit inside the white panel)
- **Keep sentences as short as possible.** One idea per line; cut filler words and modifiers, and pick the shorter of two phrasings that mean the same (e.g., "After 60 minutes of use, scrotal temperature rose by up to this much" → "60 minutes in, / up to this much warmer"). Break lines with `<br>` at meaning units
  - Don't let shortening make something read as causal (e.g., don't shorten a cross-sectional study to "Wearing boxers raises sperm concentration"; write "Men who wore boxers had higher…")
- Three levels of type hierarchy: bold headline or item name → body → gray supporting line. Color highlights on 1–2 keywords only (benchmark: viral.hacker_ cards)
- End each slide with a one-line takeaway (underline or bordered box)
- Put a short source credit at the bottom of the slide (organization, year)
- Explain jargon in plain words first, with the technical term in parentheses (e.g., "how well sperm swim (motility)")
- Wrap highlighted phrases in `<span class="hl">` to show them in pink (`#FF2A81`). The same applies inside tables. Use only 1–2 per slide so they stand out

**Closing slide (6; if it overflows, 6 references / 7 closing)**
- At most 4 references (authors, title, journal/organization, year)
  - If they overflow, cut in this order: ① send individual trials already included in a meta-analysis on the card to the caption reference list only ② if still too long, shorten long titles with an ellipsis (e.g., "Dietary patterns… in male fertility"; the full title goes in the caption list) ③ if still too long, split into slide 6 (references) and slide 7 (closing)
  - If a source credit on a body slide breaks in the middle of a journal name, break it with `<br>` at the journal boundary
- Disclaimer: write **the standard disclaimer "For educational purposes only. For personal health concerns, talk to a doctor."** in bold (break the line with `<br>` after the first sentence; the template splits it into 3 lines so no word sits alone), followed by "Based on guidelines and research, / but not a substitute for medical care." (already in the template). Never change the standard wording
- Follow copy examples: "Baby plans, together", "I'll go first" + supporting line "Tag your partner". Keep the main line to about 20 characters so it stays on one line next to the character
- Replace `{{ACCOUNT}}` on the Follow button with the Instagram handle (without @)

### Step 5: Regulatory and wording check (required)

- **By default, no product mentions in the slide body.** Put one on the closing slide only if the user asks
- **The pinned comment includes a HAGOBOGO suggestion by default.** Put it in a final paragraph separate from the card's key information, and present it only as a way to `observe` sperm. Don't add disclaimers such as "This doesn't replace a clinic test" (brand decision)
- **HAGOBOGO (sperm microscope, "Sperm Microscope")**: use only "observe / observation / look at / see" wording. Never "test, diagnose, measure, analyze," and never their near-synonyms (screen, detect, assess, evaluate, examine, or counting sperm). No wording that reads like a medical device or a treatment effect
- **HAGOBOGO PRO**: only claims within the intended use authorized in the market where the post will be seen. Regulatory status differs by country; if it hasn't been confirmed for the target market, don't mention PRO
- Never write "FDA-cleared/approved," "CE-marked," "clinically proven," or "doctor-recommended" unless RA has confirmed it for that market
- **General prohibitions**
  - Guaranteeing pregnancy, or promising higher chances of pregnancy
  - Wording that implies diagnosis, such as "infertility diagnosis"
  - Recommending specific supplements, foods, or clinics
  - Implying something can replace treatment
  - Comparisons with other companies
  - Fear-mongering, made-up testimonials
  - Unsubstantiated health claims (advertising rules such as the FTC in the US and ASA/CAP in the UK apply)
- Every carousel carries **the standard disclaimer "For educational purposes only. For personal health concerns, talk to a doctor."** (closing-slide disclaimer, long caption, short caption; in captions as the line "Note: For educational purposes only. For personal health concerns, talk to a doctor."). Never reword it or substitute another advice line
- State in the deliverables that **internal RA/QA review is required** before posting

### Step 6: Design and production

**Design principles** (taken from benchmarks, but never copy Mother Insight's design)
- Size 1080×1350 (4:5 portrait), 6 slides by default (add a slide for essential overflow)
- **Every slide gets a background photo** (`images/bg1.png`–`images/bg6.png`). Without a photo it automatically becomes a solid color (navy cover, light cyan body)
- **Backgrounds are only photo, white, or a solid color.** No gradient or blurred backgrounds (exception: the dark shade `.shade` at the bottom of a photo cover)
- **Official colors go on text and some objects** (labels, bars, underlines, borders, buttons)
- Cover: background photo (navy if none) + large title (semibold) in 2–3 lines + one-line subtitle + white arrow + logo
- Body and closing (2–6): a white panel (`.panel`, solid white at 85%, 24px rounded corners) sits **in the middle of the page** (120px inset top and bottom, 60px left and right) and holds the content. The photo shows around the panel. **The logo and page number stay outside the panel**, in the photo strip below it
- Font: **Inter**, bundled in `assets/fonts/` (copy it next to `slides.html` as `fonts/`; the template loads its Latin and Latin Extended subsets; OFL-1.1, license in `assets/fonts/OFL.txt`). render.py reports any font that fails to load
- Weights: **the heaviest is 700 (Bold)**. Never 900 (Black). Cover title 600, body 400, page number 300
- Line heights are tighter than in the Korean edition, because Latin lowercase is only about 0.55em tall and the same value looks looser: cover title 0.95, subtitle 1.15, headline 1.1, lead 1.3, list and body 1.25, takeaway 1.3 (set in the template; don't loosen them). At 0.95 a descender (g, p, y) can touch a tall letter right below it on the next line; if that happens, reword or rebreak the cover title
- Body type sizes (readable instantly on a phone; benchmark: viral.hacker_ body text about 46–64px): label 56px, headline 68px, lead 54px, list 54px (supporting line 44px), row text 48px (item name 52px), box 48px, big-number caption 46px, takeaway 55px, source 33px, references 36px, disclaimer 40px (standard sentence 50px). If it overflows, don't shrink the type; shorten the copy, and add a slide if the content is essential
- The topic title box at the start of the panel (`.label`) is pinned flush to the panel's top-left corner, with only that corner rounded 24px like the panel (in the template). Keep labels to about 25 characters so they stay on one line
- Add `.mid` to the central visual block. It takes an equal share of the leftover space above and below so content doesn't bunch at the top

**Color usage** (based on text legibility)
| Color | Use for | Don't use for |
|---|---|---|
| `#003665` navy | Headlines, emphasized text, big numbers, O marks, labels (white text), takeaway box borders, solid background (cover) | — |
| `#00B2CF` cyan | Bar charts, underlines, reference list rules, Follow button background (white text, brand-decision exception) | Small text on white, white body text on cyan (insufficient contrast; the Follow button is the only exception) |
| `#FF2A81` pink | **Highlighted phrases in tables and body text** (`.hl`, bold). Only 1–2 per slide | Backgrounds, large areas, whole headlines |
| `#1F2A37` dark gray | Body text | — |
| `#E0F6FA` light cyan | Background of "confirmed" cells, body background when there's no photo | Text |

**Logo, page numbers, arrow**
- Logo: **same size and position on every slide** (bottom center, 48px tall, 36px from the bottom). On slides 2–6 it sits in the strip below the panel. The width follows the file (the English wordmark is about 115px wide at 48px tall)
- Page number (`.page`): right side of the same strip on slides 2–6 (aligned to the panel's right edge). White text with no background, weight 300 (Inter Light). It has a strong shadow so it stays readable on bright photos (in the template). Gray on slides without a photo
- Cover arrow (`.next`): the `assets/andrsrxn--arrow-right.svg` icon is inlined in the template. Use it in white (navy only on the white cover `.cover.white`)
- The logo has a white outline, so it works on both dark and white backgrounds. Never recolor or stretch it

**Background and object images**
0. **Ask which images are needed before making any** (brand decision): once the storyboard is set, confirm with AskUserQuestion (Codex: `request_user_input`) before writing prompts or generating. Build a recommended per-slide image plan from the storyboard and show it as the first option
   - **Background photos**: new for each slide, the user's own photos, or several slides sharing one (consecutive slides such as days or steps may share a background)
   - **Object images**: whether you need product, packaged food, or object images (transparent background) placed on the cards, and which slide gets what
   - **Content characters**: whether you need a character to show the content (e.g., a sperm character) and whether there's a reference image (the brand characters Hago and Bogo are never AI-generated)
   - **Cover style**: photoreal or 3D illustration, and whether any text is needed inside the image (signage, etc.)
1. Use photos and brand images supplied by the user. **Create an `images` folder** next to `slides.html` and name them `bg1.png`–`bg6.png` (matching the slide numbers); they load automatically
   - Cover: a dark shade (`.shade`) covers the bottom 60% so the text on the photo stays readable
   - Body: the photo looks like a frame. The 120px strips at the top and bottom (about 9% of the height each) and the 60px sides stay fully visible, and the middle shows faintly behind the white panel
2. If there are no photos, write a photoreal generation prompt for each slide in `image_prompts.md` and deliver it along with the rest (works for both Gemini Nano Banana and ChatGPT)
   - State in the document that generated images go in an **`images` folder** in the work folder as `bg1.png`–`bg6.png`
   - **Choose each scene by analyzing that slide's content.** For each slide, pull out the headline, key message, and the habit or subject it covers, and set a scene with an action, object, or place that shows it at a glance. Don't fill slides with mood shots unrelated to the content (blank walls, windows, curtains)
     - e.g., (habits that heat sperm): "Heat from sitting" → a man in a suit sitting with thighs together and a laptop on his lap / "Hot tubs and saunas" → a steamy bathhouse and sauna room / "Keep it cooler than body temperature" → a man in light underwear stretching his arms overhead / "Check it together" → a couple talking in their kitchen
     - Before the prompts in `image_prompts.md`, write a per-slide **slide content → scene** analysis table (slide, key card content, scene to show, why)
   - English prompts + a one-line scene note. Settings are globally neutral (not tied to one country unless the topic is), with couples and people of diverse ethnicities and backgrounds. Match the season to the posting month and say which hemisphere (default: Northern Hemisphere unless the user's target audience says otherwise)
   - Always specify composition: on the cover, place the subject in the top ~45% and keep the bottom 55% simple (English titles can run 3 lines) / on body slides, spread color and texture evenly across the whole frame (especially the top, bottom, and side edges); the middle shows faintly behind the white panel. If the content needs a person, include one but keep the face out of frame (crop below the chin or shoulders, or show them from behind), and note in the document that people show faintly behind the white panel
   - Append the shared exclusion line: no text, signage, logos, or watermarks; no celebrities or real people; no recognizable faces (backs and hands only); no pregnant women or babies; no medical devices; no heavy retouching or illustration look
   - Aspect ratio line per service: Gemini `Aspect ratio 4:5, vertical.` / ChatGPT `Vertical portrait image, 4:5 aspect ratio (1080×1350).`
   - Advise generating all six in one conversation, adding "same photographic style as the previous image"
   - When covering real places (destinations, etc.), never present AI images as real photos of that place
3. **Generate directly with a Codex pane (optional, when this skill runs in Claude)**: when this skill itself runs in Codex, skip this flow and generate the images with your own image generation tool (see 'Running in Codex'). Otherwise: if a logged-in Codex pane is open in the Orca terminal (`echo $TERM_PROGRAM` is `Orca`), hand over `image_prompts.md` to generate and composite the backgrounds right away. If the conditions aren't met, just deliver the document as in 2
   - Find it: in `orca terminal list`, find the Codex pane (title "Codex …", same project folder), and check with `orca terminal show --terminal <handle>` that it is `writable: true` and waiting for input (`› Ask Codex`). Also check that `image_generation` is `true` in `codex features list`
   - Write the request to a file: absolute path of the work folder / read `image_prompts.md` and create each slide's prompt with the image generation tool / substitute `[shared line]` and `[aspect ratio line]` (ChatGPT version) / save as 1080×1350 PNG to `images/bgN.png` / regenerate only that slide if an excluded element appears / don't modify files outside `images/` or run render.py
   - Send it: `orca terminal send --terminal <handle> --text "$(cat <request file>)" --enter --wait-submit 20 --json` → if the result's `stages` include `turn_started`, it has started
   - Detecting completion: run 'watch_codex.sh' below in the background (`watch_codex.sh <handle> images bg1 bg2 …`). Every 15 seconds it checks both **files saved after the start** and **Codex finishing** (`esc to interrupt` absent twice in a row from `orca terminal read --terminal <handle> --screen`). Don't use a done marker written into the request (e.g., `ALL_BG_DONE`) as the signal, because the request itself reappears on the pane screen. If an approval prompt (Allow, approve) appears, stop and tell the user
   - To redo one slide (e.g., a slide's content changed and the scene no longer fits): first fix that slide's analysis table row and prompt in `image_prompts.md`, back up the existing `bgN.png`, and request only that slide
   - **If the request changes mid-generation**: fix `image_prompts.md` first, then send the change to the same pane (`orca terminal send … --enter --json`; the result's `stages` include `input_accepted`). Codex picks it up and continues. Back up any reference file that would be overwritten (e.g., a character base image) and say in the request not to change it
   - **Object images** (products, packaged food, objects): `images/<name>.png`, 1024×1024, transparent background (pure white #FFFFFF if transparency isn't possible). Use a separate shared line from the backgrounds: single product shot, clean 3D product render, soft studio lighting, simple packaging in HAGOBOGO tones, no text, numbers, logos, brand names, or barcodes
   - **Content characters**: make a base image (`<name>_base.png`) first, then use it as the reference (edit input) to make pose variations with the same look. Each variation changes only expression and pose; hair, face, colors, gloss, and sparkle stay the same. After receiving them, check the look matches with a comparison sheet of the variations side by side on the same background
   - **Reference images**: if a reference image from the user carries a stock-site watermark (Adobe Stock, etc.) or is another account's content, don't pass it as generation input. Describe only its style (ratio, material, color, composition) in words in the prompt, and tell the user you did so
   - After receiving: inspect the backgrounds together for excluded elements (text, logos, faces, etc.; zoom in on small logos such as the back of a phone), confirm no files outside `images/` changed, then run render.py again. Also tell the user how much Codex usage (`5h … left`) changed
4. **Post-generation cover and text fixes** (same whether Codex or another tool made them)
   - **Text inside the image** (signage, etc.): only on slides where the user asks for it, with the exact words in the prompt (e.g., only the word "PHARMACY"). After generating, zoom in to check the text is exact. If it's garbled, regenerate (up to 3 times); if it stays garbled, generate with a blank sign and place the text on the slide instead. Add "no text or brands other than that word" to the RA checklist
   - **If the cover subject covers the title area** (a building or object reaches into the bottom 55% and overlaps the title): regenerate, or shift the image up and fill the empty bottom strip by flipping the strip right above it. Keep the original as e.g. `bg1_original.png`
     ```python
     from PIL import Image, ImageOps
     im = Image.open('images/bg1_original.png').convert('RGB'); S = 150   # pixels to shift up
     out = Image.new('RGB', im.size); out.paste(im.crop((0, S, 1080, 1350)), (0, 0))
     out.paste(ImageOps.flip(out.crop((0, 1350-2*S, 1080, 1350-S))), (0, 1350-S))   # flip the strip just above to fill seamlessly
     out.save('images/bg1.png')
     ```
   - **Fake text marks**: if zoomed inspection finds unreadable marks that look like text (signs, stickers), blur only that area slightly (`ImageFilter.GaussianBlur(3)` on that region). Leave small product patterns that don't read as text at actual size. Record the fixes in `image_prompts.md`
5. For a solid background without photos: navy cover (default) or white cover (change to `.cover.white` and delete `.art`; text and arrow turn navy)
- Never download photos from the web to use. No photos of celebrities or real people
- If AI-generated images are used, tell the user to turn on Instagram's "AI info" label when uploading

**Production procedure**
```bash
# Work folder name = creation date (YYYYMMDD) + "_" + topic (lowercase English, words joined with -). e.g., cardnews/20261031_autumn-trip-plan
mkdir -p cardnews/<YYYYMMDD>_<topic> && cd cardnews/<YYYYMMDD>_<topic>
cp -R <skill folder>/assets/fonts fonts   # Inter font files (bundled, no npm or network). fonts/ must sit next to slides.html
```
1. Copy the skill folder's `assets/logo_en.png` into the work folder (if only this SKILL.md is available, restore it as `logo_en.png` from 'Logo file' below and check the checksum). Also copy `assets/character_hc12.png` from the skill folder into the work folder (slide 6 character; without the file the slide renders without the character). If only this SKILL.md is available (no `assets/fonts/`), run `npm install @fontsource/inter` and copy the ten `node_modules/@fontsource/inter/files/inter-latin-*-normal.woff2` and `inter-latin-ext-*-normal.woff2` files for weights 300–700 into `fonts/`
2. Save the 'Template' below (6 slides) as `slides.html` and fill it in. Slides 2 and 4 can switch to other types to suit the content. Replace `{{ACCOUNT}}` with the Instagram handle. If content overflows, add slides as in "Adding slides"
3. If there are background photos, `mkdir -p images` and place them as `images/bg1.png`–`images/bg6.png` (JPGs work too if renamed this way)
4. Save 'render.py' below and run it (in Codex, outside the sandbox; see 'Running in Codex'): `python3 render.py slides.html slides` → saves straight to `slides/01.png`–`slides/06.png`
5. If it reports overflow, white-panel overflow, or too many lines, shorten the copy and render again; if essential content still overflows, add a slide. If it reports page numbers, change them to `n/total`. If it reports a leftover placeholder, replace it. "Missing background photo" just means that slide came out in a solid color

**Slide types (template classes)**
| Type | Class | Use |
|---|---|---|
| Cover | `.cover.photo` (photo, default) / `.cover` (solid navy) / `.cover.white` (white) | Slide 1 |
| Body frame | `<section class="slide bg">` + `.panel` (central white panel) + `.page` (page number) and `.brand` (logo) outside the panel | Slides 2–6 |
| Number rows | `.rows` (big number on the left + description on the right, units in `<small>`; `<b>` inside the description is the item-name line) | Intro, 3 key figures / per-item numbers for list-type topics |
| Two big numbers | `.nums` (borderless white boxes, numbers 150px, units 81px in `<small>`) / `.nums.one` (one cell) | Compare two amounts or rates / show one key figure large (intro) |
| Bar chart | `.bars` + `--v` | Comparing percentages |
| Comparison table | `.vs` (`.myth` / `.fact`) | "You've heard vs The evidence" |
| O/X and numbered list | `.list` (`li.x` = X, supporting line in `<small>`) / `.list.places` (item names 1.5× larger, names in `<b>`) | Myth roundup, summary slide / places and destinations |
| Centered block | `.mid` (add to the visual block) | Slides 2–5 |
| Closing | `.refs` (references) + `.disc` (disclaimer, white box) + `.follow` (follow: cyan rounded two-line button "handle / Follow" + character `.mascot` standing on top, overlapping the button by 44px) | Slide 6 (if it overflows, slide 6 `.refs` / slide 7 `.title` + `.disc` + `.follow`) |
| One-line takeaway | `.bottom` (underline) / `.box` (border; `<small>` inside is a one-line source) | Slides 2–5 |

### Step 7: Review
- [ ] In Step 1 you showed the keyword check table (scope, ①②③, evidence) and the topic was chosen from 3 candidates. The chosen topic and check results are at the top of storyboard.md
- [ ] 6 slides by default. If more, confirm the added slide is essential and page numbers read `n/total` (render.py report)
- [ ] Body text reads instantly at phone size (half scale), and sentences are short
- [ ] render.py reports "No overflow"
- [ ] Open each PNG with Read (Codex: `view_image`) and check for overlapping or clipped text, awkward line breaks (a single word alone on a line), and typos
- [ ] The cover title reads at a glance in a small preview
- [ ] The logo shows correctly on every slide
- [ ] Backgrounds are photo, white, or solid color only (no gradient backgrounds; only the dark shade at the bottom of a photo cover)
- [ ] Background photos have no text, signage, logos, real people's faces, pregnant women, or babies, and text on photos and on the white panel reads clearly
- [ ] If you wrote `image_prompts.md`, it has the per-slide content → scene analysis table, and each scene shows that slide's content
- [ ] If a slide's content (items, key message) changed, re-check that its analysis row and background still fit; if not, fix the prompt and regenerate only that slide
- [ ] You asked the user which images were needed (backgrounds, objects, characters, cover style) before generating any
- [ ] If a Codex pane made the backgrounds, no files outside `images/` changed and overwritten backgrounds were backed up
- [ ] Object images and characters, if made, have transparent backgrounds and no text, logos, or barcodes on packaging. Character variations were checked with a comparison sheet
- [ ] Text inside images (signage, etc.), if added, was zoomed in and is exact, and the cover subject doesn't cover the title
- [ ] The white panel is centered on the page, and the logo and page number sit in the strip outside it. The cover arrow shows in white
- [ ] Highlighted phrases are pink (`#FF2A81`), at most 1–2 per slide (render.py reports highlights that aren't pink or that became blocks and break lines)
- [ ] `{{ACCOUNT}}` has been replaced with the Instagram handle (render.py reports leftover placeholders)
- [ ] Every number on the cards is in sources.md and matches the original
- [ ] Open source URLs and DOIs with WebFetch (Codex: `web.run`) to confirm they work (without WebFetch, check DOIs via `https://doi.org/api/handles/<DOI>` for responseCode 1 and the linked URL, and web pages for a curl 200 response)
- [ ] Passes the Step 5 regulatory checklist
- [ ] No wording puts the burden on only women or only men
- [ ] `caption.md` has the long caption, short caption, and pinned comment, and `python3 caption_check.py caption.md` reports "Caption format OK"
- [ ] 5 hashtags (#hagobogo + 4 topic tags, all lowercase) are attached at the end of both the long and short captions (2 blank lines above, no separate hashtag section). Topic tags reflect this carousel's topic, with no efficacy-promising or product-name tags
- [ ] The closing-slide disclaimer and both captions carry the standard disclaimer unchanged ("For educational purposes only. For personal health concerns, talk to a doctor."; in captions with "Note: " in front)
- [ ] If the user gave reference images, you showed the correction table and removed numbers whose originals couldn't be confirmed
- [ ] The pinned comment is a short, conversational message with only the key information and the HAGOBOGO suggestion
- [ ] HAGOBOGO is described only as a way to `observe` sperm (no "doesn't replace testing" sentence)

### Step 8: Delivery
1. Deliver the slide PNGs as saved in the `slides/` folder (01.png onward). Don't zip them
2. Make a preview sheet of the slides shrunk and tiled (6 slides: 2 rows of 3; 7–8 slides: 2 rows of 4). Save 'preview.py' below and run `python3 preview.py slides preview_sheet.png`
3. Put the following in a single `caption.md` (section headings exactly as written, because caption_check.py looks for them: `## Long caption`, `## Short caption`, `## Pinned comment`, `## References`, `## RA review checklist`, `## Alt text`)
   - **Long caption**: empathetic question → key evidence and practical info → one disclaimer line → save / tag-your-partner call to action. Keep sentences as short as possible. Don't just list the card contents; connect them in natural, human-sounding conversational English
     - The disclaimer line is the standard line "Note: For educational purposes only. For personal health concerns, talk to a doctor." unchanged. Card-specific caveats such as study size or uncertainty go in body sentences, not on the disclaimer line
   - **Short caption**: about 130 words (hashtag line excluded) keeping only the key message and numbers, or the action and CTA, from the long caption. Drop repeated explanations and references so it can be posted as is. Disclaimer: the standard line "Note: For educational purposes only. For personal health concerns, talk to a doctor." unchanged
   - **Pinned comment**: about 90 words in a `key info + HAGOBOGO suggestion` format. Prefer short conversational sentences over checklist-style notices
     - The key info keeps only the one or two sentences readers need to act on the topic right away: who, which numbers, where to apply, or what to do
     - End by suggesting HAGOBOGO for `observing` sperm. Default sentence: "Curious what your sperm look like while you're trying to conceive? Try observing them at home with HAGOBOGO." (no "doesn't replace testing" sentence)
     - Separate paragraphs so that government-funded or clinic tests and HAGOBOGO never read as the same kind of test, and don't imply any testing, diagnosis, measurement, or analysis function
     - Don't use a sentence linking the key-info paragraph to the product paragraph that implies checking results. Banned examples: "After changing your habits, check the difference with HAGOBOGO", "See how much you've improved with HAGOBOGO"
   - **5 hashtags**: #hagobogo + **4 topic tags that say what this post is about** (brand decision)
     - **Write every hashtag in lowercase**, including the brand tag (e.g., `#spermhealth`, not `#SpermHealth`) (brand decision)
     - Instagram limits posts to 5 hashtags (announced December 2025). Hashtags now tell Instagram what a post is about more than they boost reach, so carry this carousel's topic instead of repeating account-category tags
     - Prefer specific tags that fit the topic over broad ones (#food #health) (e.g., a desk-lunch card → `#desklunch #officelunch #spermhealth #preconceptionnutrition`)
     - No tags that promise effects (#boostspermcount #fertilityboost #getpregnantfast, etc.), and no tags with specific product, brand, or clinic names
     - Use category tags as topic tags only when they match the topic. Reference list: `#ttc #tryingtoconceive #malefertility #spermhealth #preconception #familyplanning #dadtobe #momtobe #fertilityjourney`
     - **Attach them at the end of both the long caption and the short caption.** Don't make a separate hashtag-only section, so copying one section copies the caption and hashtags together
     - Leave 2 blank lines between the last sentence (save / tag-your-partner CTA) and the hashtag line
     - No hashtags in the pinned comment
   - **Reference list** (all of sources.md)
   - **RA review checklist** (Step 5 items, with checkboxes). Also check that the pinned comment's product suggestion is for `observing` only and is separated from government or clinic testing
   - **Alt text**: one line per slide
   - When done, check the format with 'caption_check.py' below: `python3 caption_check.py caption.md` (short caption and pinned comment word counts, 5 lowercase hashtags starting with #hagobogo, 2 blank lines above the hashtags, the standard disclaimer, and the pinned comment's HAGOBOGO paragraph and banned wording)
4. Send all PNGs in the `slides/` folder, the preview sheet, and caption.md with SendUserFile (if SendUserFile isn't available, list the file paths). If you wrote background prompts, send image_prompts.md too (with the Instagram AI label note for AI images)
5. Keep the reply short: one line on what you made, plus what the user should check (places where source judgment was split, wording that needs RA review)

---

## Template (slides.html, 6 slides)

```html
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
/* Font: Inter, bundled in the skill as assets/fonts/ (copy it next to slides.html as fonts/; OFL-1.1). Latin + Latin Extended subsets, so accented letters in author names also render in Inter. No npm or network needed */
@font-face{font-family:I;src:url(fonts/inter-latin-300-normal.woff2);font-weight:300;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:I;src:url(fonts/inter-latin-400-normal.woff2);font-weight:400;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:I;src:url(fonts/inter-latin-500-normal.woff2);font-weight:500;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:I;src:url(fonts/inter-latin-600-normal.woff2);font-weight:600;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:I;src:url(fonts/inter-latin-700-normal.woff2);font-weight:700;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:I;src:url(fonts/inter-latin-ext-300-normal.woff2);font-weight:300;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:I;src:url(fonts/inter-latin-ext-400-normal.woff2);font-weight:400;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:I;src:url(fonts/inter-latin-ext-500-normal.woff2);font-weight:500;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:I;src:url(fonts/inter-latin-ext-600-normal.woff2);font-weight:600;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:I;src:url(fonts/inter-latin-ext-700-normal.woff2);font-weight:700;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
/* HAGOBOGO brand colors: navy #003665, cyan #00B2CF / accent: pink #FF2A81 */
/* Body text is sized to read instantly on a phone (list 54px, sub-line 44px, row text 48px, box 48px, takeaway 55px, source 33px). If text overflows, shorten the copy or add a slide; never shrink the type */
/* Only weights 300-700 are used. The heaviest weight is 700 (Bold) */
/* Line heights are tighter than the Korean edition (Latin lowercase is only ~0.55em tall, so the same value looks looser): display 0.95-1.15, body 1.25-1.3 */
:root{--brand:#003665;--accent:#00B2CF;--point:#FF2A81;--soft:#E0F6FA;--ink:#1F2A37;--paper:#FFFFFF;--muted:#5B6475;--gray:#F1F3F5}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:I,Inter,'Helvetica Neue',Arial,sans-serif;background:#ccc;word-break:normal;overflow-wrap:break-word}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--paper);color:var(--ink);
  padding:110px 90px 120px;display:flex;flex-direction:column;align-items:flex-start}
/* Page number: bottom right, in the photo strip below the white panel (same height as the logo). White text with no background, weight 300, with a strong shadow so it stays readable on bright photos. Gray on slides without a photo */
.page{position:absolute;right:60px;bottom:45px;font-size:30px;line-height:1;font-weight:300;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.65),0 0 14px rgba(0,0,0,.5);z-index:2}
.slide.nophoto .page{color:var(--muted);text-shadow:none}
/* Logo: same size and position on every slide (bottom center, 48px tall, 36px from the bottom) */
.brand{position:absolute;bottom:36px;left:0;right:0;text-align:center;z-index:2}
.brand img{height:48px}

/* ── Cover ── photo cover if images/bg1.png exists, otherwise solid navy. .white is the white cover */
.cover{padding:0;background:var(--brand);color:#fff}
.cover .art{position:absolute;inset:0;background-size:cover;background-position:center}
.cover .shade{display:none}
.cover.photo .shade{display:block;position:absolute;left:0;right:0;bottom:0;height:60%;background:linear-gradient(transparent,rgba(0,0,0,.72))}
.cover.white{background:var(--paper);color:var(--brand)}
.cover .copy{position:absolute;left:72px;right:72px;bottom:220px}
.cover h1{font-size:132px;font-weight:600;line-height:.95;letter-spacing:-3px}
.cover h2{font-size:62px;font-weight:400;line-height:1.15;margin-top:26px;letter-spacing:-1px;opacity:.9}
/* Next-slide arrow: assets/andrsrxn--arrow-right.svg inlined. The stroke follows `color` (white) */
.cover .next{position:absolute;right:72px;bottom:140px;width:84px;height:84px;color:#fff}
.cover .next svg{display:block;width:100%;height:100%}
.cover.white .next{color:var(--brand)}

/* ── Body background photo (slides 2-6) ── a white panel (solid white at 85%) sits in the middle of the page (120px top/bottom, 60px left/right) and the photo shows around it.
   Logo and page number sit in the photo strip below the panel. Without a photo (images/bg2-6.png) the slide falls back to solid light cyan */
.slide.bg{padding:0;background:var(--soft) center/cover no-repeat}
.panel{position:absolute;left:60px;right:60px;top:120px;bottom:120px;border-radius:24px;background:rgba(255,255,255,.85);
  padding:60px;display:flex;flex-direction:column;align-items:flex-start}
/* Middle visual block: splits the leftover vertical space above and below automatically */
.mid{margin-top:auto;margin-bottom:auto;width:100%}

/* Shared body elements */
.label{display:inline-block;background:var(--brand);color:#fff;font-weight:700;font-size:56px;padding:10px 28px;line-height:1.3}
/* The label (topic title box) at the start of the panel is pinned flush to the panel's top-left corner */
.panel>.label:first-child{margin:-60px 0 0 -60px;border-top-left-radius:24px}
.title{color:var(--brand);font-size:68px;font-weight:700;line-height:1.1;letter-spacing:-1px}
.lead{font-size:54px;line-height:1.3;margin-top:32px}
.hl{color:var(--point);font-weight:700}
.bottom{margin-top:auto;font-size:55px;font-weight:700;line-height:1.3;padding-bottom:4px}
/* padding-bottom:4px keeps the 6px underline inside the box at line-height 1.3 (otherwise it pokes about 3px past the line box) */
.bottom span{border-bottom:6px solid var(--accent)}
.box{width:100%;border:3px solid var(--brand);color:var(--brand);background:#fff;padding:28px 36px;font-size:48px;font-weight:700;line-height:1.25}
.panel>.box{margin-top:auto}
.mid .box{margin-top:28px}
/* Source line inside a box (e.g., the organization under a guideline quote) */
.box small{display:block;font-size:34px;font-weight:400;color:var(--muted);margin-top:8px}
.src{font-size:33px;color:var(--muted);margin-top:22px;line-height:1.3}

/* Number rows: big number on the left + description on the right (intro slide) */
.rows{display:flex;flex-direction:column}
.rows>div{display:grid;grid-template-columns:260px 1fr;align-items:center;gap:28px;padding:18px 0;border-bottom:2px solid var(--gray)}
.rows>div:last-child{border-bottom:0}
.rows strong{font-size:92px;font-weight:700;color:var(--brand);letter-spacing:-2px;line-height:1.1}
.rows strong small{font-size:52px;letter-spacing:-1px}
.rows span{font-size:48px;line-height:1.25}
/* Item-name line inside a row description (bold navy): <span><b>01 Item name</b>Description</span> */
.rows span b{display:block;color:var(--brand);font-size:52px;line-height:1.15;margin-bottom:4px}

/* Two big numbers: compare two amounts or rates */
.nums{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;text-align:center}
/* Big-number cell: white box without a border */
.nums>div{background:#fff;padding:36px 12px}
.nums strong{display:block;font-size:150px;font-weight:700;color:var(--brand);letter-spacing:-4px;line-height:1.1}
.nums strong small{font-size:81px;letter-spacing:-2px}
/* Description line: only the cell's direct child span becomes a block (if an inner <span class="hl"> also became a block, the line would break) */
.nums>div>span{display:block;font-size:46px;line-height:1.25;margin-top:12px}
/* One big number: <div class="nums one"> (show one key figure large) */
.nums.one{grid-template-columns:1fr}

/* Comparison table */
.vs{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.vs>div{padding:36px 32px;font-size:48px;line-height:1.3}
.vs .myth{background:var(--gray)}.vs .fact{background:var(--soft)}
.vs b{display:block;font-size:52px;margin-bottom:16px}.vs .fact b{color:var(--brand)}

/* Horizontal bar chart: put a 0-100 value in --v */
.bars{display:flex;flex-direction:column;gap:34px}
.bar{display:grid;grid-template-columns:230px 1fr 140px;align-items:center;gap:20px;font-size:48px}
.bar i{display:block;height:52px;background:var(--soft);position:relative}
.bar i::after{content:"";position:absolute;inset:0;width:calc(var(--v)*1%);background:var(--accent)}
.bar b{text-align:right;font-weight:700;font-size:52px;color:var(--brand)}

/* O/X and numbered list: <small> is the supporting line */
.list{display:flex;flex-direction:column;gap:34px;list-style:none}
.list li{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:start;font-size:54px;line-height:1.25}
.list li em{font-style:normal;font-weight:700;font-size:58px;line-height:1.16;color:var(--brand)}
.list li.x em{color:#C0392B}
.list li b{color:var(--brand)}
/* Larger item names (places, destinations): <ul class="mid list places"> — names at 72px, number centered on the name line */
.list.places li b{font-size:72px;line-height:1.1}
.list.places li em{line-height:79px}
.list li small{display:block;font-size:44px;font-weight:400;color:var(--muted);margin-top:6px;line-height:1.25}

/* Closing slide (6): references + disclaimer + follow */
.refs{width:100%;margin-top:40px;list-style:none;display:flex;flex-direction:column;gap:24px}
.refs li{font-size:36px;line-height:1.25;padding-left:22px;border-left:6px solid var(--accent);color:var(--ink)}
.disc{margin-top:auto;width:100%;background:#fff;padding:34px 38px;font-size:40px;line-height:1.3}
.disc b{display:block;color:var(--brand);font-size:50px;line-height:1.15;margin-bottom:16px}
.follow{position:relative;margin-top:40px;width:100%;border:3px solid var(--brand);background:#fff;padding:26px 32px;display:flex;align-items:center;justify-content:space-between;gap:24px;font-size:40px;font-weight:700;color:var(--brand)}
.follow small{display:block;font-size:32px;font-weight:400;color:var(--muted);margin-top:6px}
/* Follow button: two lines (account handle + Follow). Cyan background + white text (brand decision). The character (character_hc12.png, supplied by the brand team) stands on the left and points at the button */
.follow>span{min-width:0}
/* margin-left reserves room for the character that sticks out to the left of the button, so long follow text wraps instead of hiding behind it */
.follow .cta{position:relative;flex:none;margin-right:-8px;margin-left:70px}
.follow button{position:relative;z-index:1;font:inherit;font-size:34px;font-weight:700;line-height:1.2;background:var(--accent);color:#fff;border:0;border-radius:16px;padding:12px 44px;display:flex;flex-direction:column;align-items:center}
.follow button small{font-size:22px;font-weight:400;color:#fff;margin:0 0 4px}
/* Character: feet float just above the box's bottom border (9px above the line), overlapping the button by 44px and drawn on top of it.
   The button ends 24px inside the follow box border (.cta margin-right:-8px); its text is centered (44px padding on both sides) */
.follow .mascot{position:absolute;z-index:2;right:100%;bottom:-17px;height:180px;margin-right:-44px}
</style></head>
<body>

<!-- Background photos: put bg1.png-bg6.png (numbered like the slides) in an images folder next to slides.html and they load automatically. Missing photos fall back to a solid color -->

<!-- Slide 1 cover: background photo images/bg1.png (solid navy if missing). For a white cover, change to class="slide cover white" and delete .art -->
<section class="slide cover photo"><div class="art" data-bg="images/bg1.png" style="background-image:url(images/bg1.png)"></div><div class="shade"></div>
  <div class="copy"><h1>Is more sperm<br>always better?</h1><h2>What WHO values really mean</h2></div>
  <div class="next" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m13.2 4.93l4.25 4.23c1.34 1.34 2 2 2 2.83s-.66 1.5-2 2.83l-4.24 4.25M4.29 12h14.84"/></svg></div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<!-- Slide 2 intro: number rows (or .nums two big numbers, .bars bar chart) / background photo images/bg2.png -->
<section class="slide bg" data-bg="images/bg2.png" style="background-image:url(images/bg2.png)">
  <div class="panel">
    <h3 class="title">Headline,<br>two lines max</h3>
    <div class="mid rows">
      <div><strong>Val 1</strong><span>One or two lines of description</span></div>
      <div><strong>Val 2</strong><span>One or two lines of description</span></div>
      <div><strong>Val 3</strong><span>One or two lines of description</span></div></div>
    <p class="bottom"><span>One-line takeaway</span></p>
    <p class="src">Source: Organization, Year</p>
  </div>
  <div class="page">2/6</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<!-- Slide 3 body ①: comparison table / background photo images/bg3.png -->
<section class="slide bg" data-bg="images/bg3.png" style="background-image:url(images/bg3.png)">
  <div class="panel">
    <span class="label">1. Label headline</span>
    <p class="lead">Body copy, 1–2 lines. Key words are <span class="hl">highlighted</span>.</p>
    <div class="mid vs"><div class="myth"><b>You've heard</b>The myth</div><div class="fact"><b>The evidence</b>What studies found, with a <span class="hl">key phrase</span></div></div>
    <p class="bottom"><span>One-line takeaway</span></p>
    <p class="src">Source: Organization, Year</p>
  </div>
  <div class="page">3/6</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<!-- Slide 4 body ②: bar chart (values must be the original figures in sources.md) / background photo images/bg4.png -->
<section class="slide bg" data-bg="images/bg4.png" style="background-image:url(images/bg4.png)">
  <div class="panel">
    <span class="label">2. Label headline</span>
    <div class="mid bars">
      <div class="bar"><span>Item A</span><i style="--v:80"></i><b>80%</b></div>
      <div class="bar"><span>Item B</span><i style="--v:45"></i><b>45%</b></div></div>
    <div class="box">Boxed takeaway</div>
    <p class="src">Source: Organization, Year</p>
  </div>
  <div class="page">4/6</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<!-- Slide 5 summary: O/X or numbered list / background photo images/bg5.png -->
<section class="slide bg" data-bg="images/bg5.png" style="background-image:url(images/bg5.png)">
  <div class="panel">
    <span class="label">3 things to remember</span>
    <ul class="mid list">
      <li><em>01</em><span>First takeaway<small>One supporting line</small></span></li>
      <li><em>02</em><span>Second takeaway<small>One supporting line</small></span></li>
      <li><em>03</em><span>A step to take <span class="hl">together</span><small>One supporting line</small></span></li></ul>
    <p class="bottom"><span>One-line takeaway</span></p>
  </div>
  <div class="page">5/6</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<!-- Slide 6 closing: references (max 4) + disclaimer + follow / background photo images/bg6.png
     If the references overflow, split into slide 6 (references) / slide 7 (disclaimer + follow) and change page numbers to n/7 (SKILL.md "Adding slides")
     Replace {{ACCOUNT}} on the Follow button with the Instagram handle for this post (render.py warns if it is left in) -->
<section class="slide bg" data-bg="images/bg6.png" style="background-image:url(images/bg6.png)">
  <div class="panel">
    <span class="label">References</span>
    <ol class="refs"><li>Author. Title. Journal/Organization. Year</li><li>Author. Title. Journal/Organization. Year</li></ol>
    <div class="disc"><b>For educational purposes only.<br>For personal health concerns,<br>talk to a doctor.</b>Based on guidelines and research,<br>but not a substitute for medical care.</div>
    <div class="follow"><span>Baby plans, together<small>Tag your partner</small></span><div class="cta"><img class="mascot" src="character_hc12.png" alt="" onerror="this.remove()"><button><small>{{ACCOUNT}}</small>Follow</button></div></div>
  </div>
  <div class="page">6/6</div><div class="brand"><img src="logo_en.png" alt="HAGOBOGO"></div></section>

<script>
// Background photo check: if a file is missing, turn off photo styling (cover becomes solid navy, body slides solid light cyan).
// render.py waits for window.bgReady before capturing
window.bgReady = Promise.all([...document.querySelectorAll('[data-bg]')].map(el => new Promise(done => {
  const im = new Image();
  im.onload = () => done();
  im.onerror = () => {
    el.style.backgroundImage = 'none'; el.dataset.missing = '1';
    const s = el.closest('.slide'); s.classList.add('nophoto');
    if (s.classList.contains('cover')) s.classList.remove('photo');
    done();
  };
  im.src = el.dataset.bg;
})));
</script>
</body></html>
```

## render.py

Saves each slide as a PNG and reports elements that overflow the slide, content that runs into the white panel's bottom padding, and too many lines on the cover. It also reports slides whose background photo file is missing.

```python
import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
    pg.goto(src.as_uri()); pg.evaluate("document.fonts.ready"); pg.evaluate("window.bgReady || null"); pg.wait_for_timeout(400)
    bad = pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>{const r=s.getBoundingClientRect();return [...s.querySelectorAll('*')].filter(e=>{const q=e.getBoundingClientRect();return q.width&&(q.bottom>r.bottom+1||q.right>r.right+1||e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')}).map(e=>`slide ${i+1}: <${e.tagName.toLowerCase()} class=${e.className}> overflows`)})""")
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>[...s.querySelectorAll('.panel')].filter(p=>{const r=p.getBoundingClientRect();const lim=r.bottom-parseFloat(getComputedStyle(p).paddingBottom);return [...p.querySelectorAll('*')].some(e=>{const q=e.getBoundingClientRect();return q.height&&q.bottom>lim+1})}).map(()=>`slide ${i+1}: content runs into the white panel's bottom padding -> shorten the copy`))""")
    bad += pg.evaluate("""[...document.querySelectorAll('.cover')].flatMap((c,i)=>[...c.querySelectorAll('h1,h2')].filter(e=>{const lh=parseFloat(getComputedStyle(e).lineHeight);const n=Math.round(e.getBoundingClientRect().height/lh);return e.tagName==='H1'?n>3:n>1}).map(e=>`cover: <${e.tagName.toLowerCase()}> has too many lines (title max 3, subtitle max 1) -> shorten the copy`))""")
    n = len(pg.query_selector_all('.slide'))
    if n < 6: bad.append(f'{n} slides (fewer than the default 6)')
    bad += pg.evaluate("""(()=>{const s=[...document.querySelectorAll('.slide')];const n=s.length;return s.flatMap((el,i)=>{const p=el.querySelector('.page');const v=p?p.textContent.trim():'';return p&&v!==`${i+1}/${n}`?[`slide ${i+1}: page number ${v} -> change to ${i+1}/${n}`]:[]})})()""")
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>[...s.querySelectorAll('.hl')].flatMap(e=>{const c=getComputedStyle(e);const t=e.textContent.trim().slice(0,20);const r=[];if(c.color!=='rgb(255, 42, 129)')r.push(`slide ${i+1}: highlight "${t}" is not pink (#FF2A81) -> check whether another rule overrides it`);if(e.tagName==='SPAN'&&c.display==='block')r.push(`slide ${i+1}: highlight "${t}" became a block and breaks the line -> check the span rule of its parent`);return r}))""")
    # Placeholders such as {{ACCOUNT}} (the Instagram handle on the Follow button) must be replaced before rendering
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>(s.innerText.match(/\\{\\{[^}]*\\}\\}/g)||[]).map(m=>`slide ${i+1}: placeholder ${m} is still in the slide -> replace it (e.g., the Instagram handle on the Follow button)`))""")
    # Fonts that failed to load (e.g., the fonts/ folder wasn't copied next to slides.html) would silently fall back to another typeface
    bad += pg.evaluate("""[...new Set([...document.fonts].filter(f=>f.status==='error').map(f=>f.family+' '+f.weight))].map(f=>`font failed to load: ${f} -> copy the skill's assets/fonts/ next to slides.html as fonts/`)""")
    print('\n'.join(bad) or 'No overflow')
    miss = pg.evaluate("[...document.querySelectorAll('[data-missing]')].map(e=>e.dataset.bg)")
    if miss: print('Missing background photo (solid color used instead): ' + ', '.join(miss))
    if n > 6: print(f'{n} slides (default 6 + {n-6} added: confirm the added content is essential and only overflowed because of the large type)')
    for i, s in enumerate(pg.query_selector_all('.slide'), 1):
        s.screenshot(path=str(out / f'{i:02d}.png'))
    b.close()
```

The overflow check catches elements outside the slide, overflow inside the white panel (`.panel`), too many lines in the cover title (max 3) or subtitle (max 1), slide count, and page numbers. It also reports highlights (`.hl`) that another rule turned non-pink or that became blocks and break the line, leftover placeholders such as `{{ACCOUNT}}`, and fonts that failed to load (missing `fonts/` folder). It can't catch elements overlapping each other; check that by opening the PNGs in Step 7.

## preview.py

Shrinks the PNGs in `slides/` and tiles them into one preview sheet (3 columns up to 6 slides, 4 columns from 7). Requires Pillow.

```python
# Preview sheet: shrink slides/*.png and tile them into one image (3 columns up to 6 slides, 4 columns from 7)
import sys, pathlib
from PIL import Image
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'slides'); out = sys.argv[2] if len(sys.argv) > 2 else 'preview_sheet.png'
fs = sorted(src.glob('*.png')); cols = 3 if len(fs) <= 6 else 4; rows = -(-len(fs) // cols)
W, H, g = 360, 450, 24
sheet = Image.new('RGB', (cols*W + (cols+1)*g, rows*H + (rows+1)*g), 'white')
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS)
    sheet.paste(im, (g + (i % cols)*(W+g), g + (i // cols)*(H+g)))
sheet.save(out); print(f'{out} ({len(fs)} slides, {cols} columns)')
```

## caption_check.py

Checks the format of `caption.md`. Word counts are reported only when they fall outside the target range (short caption 95–170 words, pinned comment 60–120 words; tune `SHORT_WORDS` / `PIN_WORDS` at the top if needed). Judgments about content and wording are made separately in Step 5 and the RA checklist.

```python
# caption.md format check: short caption / pinned comment length, hashtags (5, lowercase), standard disclaimer, HAGOBOGO paragraph in the pinned comment
# Usage: python3 caption_check.py caption.md
import re, sys

DISC = 'Note: For educational purposes only. For personal health concerns, talk to a doctor.'
BRAND_TAG = '#hagobogo'      # first hashtag; every hashtag is written in lowercase (brand decision)
SHORT_WORDS = (95, 170)      # short caption: about 130 words (hashtag line excluded)
PIN_WORDS = (60, 120)        # pinned comment: about 90 words
# Words that make HAGOBOGO read like a diagnostic device. Only "observe" wording is allowed in the product paragraph
BANNED = re.compile(r'\b(test(s|ed|ing)?|diagnos\w*|measur\w*|analy[sz]\w*|screening|detect\w*|assess\w*|evaluat\w*|exam(s|ine[sd]?|ining|ination)?|count(s|ed|ing)?)\b', re.I)

t = open(sys.argv[1] if len(sys.argv) > 1 else 'caption.md', encoding='utf-8').read()
bad, info = [], []

def sec(name):
    m = re.search(r'^## ' + name + r'\s*\n(.*?)(?=^---\s*$|^## |\Z)', t, re.S | re.M | re.I)
    return m.group(1).strip('\n') if m else None

def words(body):
    return sum(len(l.split()) for l in body.split('\n') if l.strip() and not l.strip().startswith('#'))

def chars(body):
    return len(''.join(l for l in body.split('\n') if l.strip() and not l.strip().startswith('#')))

def tags_check(name, body):
    lines = body.rstrip().split('\n')
    last = lines[-1].strip()
    if not last.startswith('#'):
        bad.append(f'{name}: the last line is not the hashtag line')
        return
    tags = last.split()
    if len(tags) != 5: bad.append(f'{name}: {len(tags)} hashtags (must be 5)')
    if tags[0].lower() != BRAND_TAG: bad.append(f'{name}: the first hashtag is not {BRAND_TAG}')
    upper = [x for x in tags if x != x.lower()]
    if upper: bad.append(f'{name}: hashtags must be all lowercase: {" ".join(upper)}')
    if len(lines) < 4 or lines[-2].strip() or lines[-3].strip() or not lines[-4].strip():
        bad.append(f'{name}: there must be exactly 2 blank lines between the last sentence and the hashtag line')

for name in ['Long caption', 'Short caption', 'Pinned comment']:
    if sec(name) is None: bad.append(f'missing "## {name}" section')

detail, short, pin = sec('Long caption'), sec('Short caption'), sec('Pinned comment')
for name, body in [('Long caption', detail), ('Short caption', short)]:
    if body is None: continue
    if DISC not in body: bad.append(f'{name}: the standard disclaimer line is missing or altered')
    tags_check(name, body)

if short:
    n = words(short)
    info.append(f'Short caption: {n} words / {chars(short)} characters (hashtag line excluded; target about 130 words)')
    if not SHORT_WORDS[0] <= n <= SHORT_WORDS[1]: bad.append(f'Short caption: {n} words, outside about 130 ({SHORT_WORDS[0]}-{SHORT_WORDS[1]})')

if pin:
    paras = [p for p in re.split(r'\n\s*\n', pin.strip()) if p.strip()]
    n = sum(len(l.split()) for l in pin.split('\n') if l.strip())
    info.append(f'Pinned comment: {n} words / {len("".join(l for l in pin.split(chr(10)) if l.strip()))} characters (target about 90 words)')
    if not PIN_WORDS[0] <= n <= PIN_WORDS[1]: bad.append(f'Pinned comment: {n} words, outside about 90 ({PIN_WORDS[0]}-{PIN_WORDS[1]})')
    if re.search(r'(^|\s)#\w', pin): bad.append('Pinned comment: contains a hashtag')
    last = paras[-1] if paras else ''
    if 'hagobogo' not in last.lower(): bad.append('Pinned comment: the last paragraph does not suggest HAGOBOGO')
    elif not re.search(r'\bobserv', last, re.I): bad.append('Pinned comment: the HAGOBOGO paragraph does not use "observe" wording')
    hit = sorted({m.group(0).lower() for m in BANNED.finditer(last)})
    if hit: bad.append(f'Pinned comment: banned wording in the HAGOBOGO paragraph: {", ".join(hit)}')
    if len(paras) < 2: bad.append('Pinned comment: the key-info paragraph and the HAGOBOGO paragraph are not separated')

print('\n'.join(info))
print('\n'.join(bad) if bad else 'Caption format OK')
```

## watch_codex.sh

Watches a Codex pane's image generation in the background (Step 6 'Generate directly with a Codex pane'). Uses macOS `stat -f`.

```bash
#!/bin/bash
# Watch a Codex pane while it generates images (checks both saved files and whether Codex has finished)
# Usage: watch_codex.sh <terminal handle> <images folder> <file names without .png...>
#   e.g.: watch_codex.sh term_xxxx images bg1 bg2 food_mon sperm_mon
# Text from the request that reappears on screen (e.g., a "done" marker) is never used as a signal
# Exit codes
#   0: all files saved + Codex finished ("esc to interrupt" absent twice in a row)
#   2: approval prompt detected -> tell the user
#   3: Codex stopped before every file was saved
#   1: timed out (MAX_MIN minutes, default 50)
T="$1"; DIR="$2"; shift 2; NAMES="$*"
if [ -z "$T" ] || [ -z "$DIR" ] || [ -z "$NAMES" ]; then echo "Usage: watch_codex.sh <handle> <folder> <file names...>"; exit 9; fi
TOTAL=$(echo $NAMES | wc -w | tr -d ' '); MAX=$(( ${MAX_MIN:-50} * 4 ))
START=$(date +%s); seen=""; idle=0; cnt=0
for i in $(seq 1 $MAX); do
  cnt=0
  for n in $NAMES; do
    f="$DIR/$n.png"
    # Count only files saved (modified) after start -> a regenerated file must be saved again to count
    if [ -f "$f" ] && [ "$(stat -f %m "$f")" -ge "$START" ]; then
      cnt=$((cnt+1))
      if [[ "$seen" != *"[$n]"* ]]; then seen="$seen[$n]"; echo "$(date +%H:%M:%S) $n.png saved ($cnt/$TOTAL)"; fi
    fi
  done
  screen=$(orca terminal read --terminal "$T" --screen 2>/dev/null)
  if echo "$screen" | grep -q -E "Allow|approve|Yes, proceed|Do you want|permission"; then
    echo "$(date +%H:%M:%S) approval prompt detected"; echo "$screen" | grep -v -E '^\s*$' | tail -30; exit 2
  fi
  if echo "$screen" | grep -q "esc to interrupt"; then idle=0; else idle=$((idle+1)); fi
  if [ "$idle" -ge 2 ]; then
    if [ "$cnt" -eq "$TOTAL" ]; then echo "$(date +%H:%M:%S) $TOTAL files saved, Codex finished"; code=0
    else echo "$(date +%H:%M:%S) Codex stopped (saved: $cnt/$TOTAL)"; code=3; fi
    echo "$screen" | grep -v -E '^\s*$' | tail -30; exit $code
  fi
  sleep 15
done
echo "Timed out (${MAX_MIN:-50} min). Saved: $cnt/$TOTAL"; exit 1
```

## Logo file

HAGOBOGO English wordmark (`assets/logo_en.png`, transparent PNG, 282×118, empty margins trimmed). To replace it, run `python3 scripts/update_logo.py <new_logo.png>` in the skill folder; it updates `assets/logo_en.png`, the base64 block below, and the checksum line together.

To restore it, save the base64 text below as `logo.b64` and run:

```bash
python3 -c "import base64,hashlib;d=base64.b64decode(open('logo.b64').read());open('logo_en.png','wb').write(d);print(hashlib.sha256(d).hexdigest()[:16])"
# Expected output: c71dc484d3331ae8
```

If the checksum differs, the logo is corrupted. In that case, ask the user to attach the logo file.

```text
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
TkSuQmCC
```
