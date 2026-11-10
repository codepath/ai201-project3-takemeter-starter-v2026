# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->
I chose the r/WebNovels community. Their posts range from things like favorite novels, general advice, discussions, writing, recommendations, resources, looking for novels, and novel ads. Most posts can be boiled down to being either a discussion or question. TakeMeter sorts each post into one of three labels: `promo` (pitches one specific novel), `request` (asks others to name novels) or `discussion` (everything else, mostly opinions).

I am using MPS Apple Silicon - M1.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `request`

**Definition:** A post that asks other people to name novels the poster hasn't named yet, either suggestions to read or help finding a title they forgot.

**Example 1:**
> [DISC] Rec me webnovels where the mc has panic disorder/ depression 
> Hii, I’m kinda new to webnovels but can u recommend me webnovels where the mc has depression/panic disorder/PTSD/mental illness. Its a plus if the mc is an idol or a part of the entertainment industry.here are some webnovels I’ve read:
> - debut or die
> - from thug to idol
> 
> Any recs are much appreciated :)

**Example 2:**
> [DISC] Most Popular Finished Webnovels
> Please suggest the most popular webnovels - ones which everyone agrees are good. I have read Worm,Reverend Insanity,Lord of the Mysteries, Shadow Slave. + Got dropped into ghost story, painter who paints dungeons. I want to read The Most Popular finished Webnovels before reading the underrated ones and ones with mixed opinions. Please help 🙏🙏🫡 PS - no harem plz Edit : Thanks for the replies everyone

### `discussion`

**Definition:** Any post that isn't `promo` or `request`: opinions, questions about novels already named, writing talk, news and resources.

**Example 1:**
> [DISC] No joy in reading since LoTM and Reverend Insanity
> Currently i have read 3 novels: Shadow slave, Reverned Insanity and LoTM. And i just started with my fourth one renegade immortal. But to be honest it just feels like a slop Version of Reverned insanity( I am currently at ch 110 or something like that). Will it get better or did RI and Lotm set the bar to high up. Looking back SS (mostly after tomb of ariel) also feels like a bit of slop compared to these two.

**Example 2:**
>[DISC] This is my decade of experience with Korean, Chinese, Japanese, web and light novels.
> Japanese web/light novels are an escape in the real world, may it be following the culture and integration (reincarnation or Isekai or rebirth, etc), or denial of culture (respectfully or begrudgingly deny other world culture and want to leave by any way possible)

>Korean web/light novels are wish fulfillment in a hyper focus variety (being a hunter, survivor, traveler, adventurer, jobs, or roles). Especially with the new variants at the moment (2025). They focus more on fixation and obsession to a select target.

>Chinese web/light novels focuses more on aggressive take over of story. May it be destroying the foundation of a background story (the martial system, hero system, adventure system, political system, etc) to make their own, finding faults and making their own set of rules and morals and forcefully implement it to the native of the stories. It is basically letting their inner demons out in their stories and finding ways to moralize it. It is worse in fan fics and collective intellectual appropriations of popular media (anime, novels, movies, games, etc) where they hyper impose their standards in a story and forge a narrative around their only select characters.

>Overall, novels are suppose to be interesting. Some have pros and cons and some are trying to redefine and subvert our expectations in their own ways. This is my general take to novels and not me being racist. Have a nice day.

### `promo`

**Definition:** A post whose main purpose is to present one specific novel to readers (a pitch, blurb, synopsis or link), whether the poster wrote it, translated it, or just found it.

*Why not `author`:* I first tried an `author` label, but my second example never says the poster wrote it, and I couldn't tell authors from readers sharing a find. What I can see in the text is whether the post is pitching one novel, so I label that instead.

**Example 1:**
> [IP] The Realm That Called Us [Non-LitRPG Progression Fantasy]
> Hey everyone! I'm Mystery X, and I'd like to share my webnovel, The Realm That Called Us. “You were called because this world needs heroes who can still become human after carrying the weight of gods.” Two strangers. Two completely different personalities. Somehow, they work surprisingly well together...



**Example 2:**
> [IP] Web novel from the website kakuyoumu Reincarnated as the weakest skeleton soldier in an otherworldly dungeon, I aim to become the strongest through evolution.
> Yamada Kaito is a hikikomori abandoned by his family; he makes a living as a professional RPG player. When suddenly he receives a message from a strange man offering him a life in...

### Order of checks

Every post gets exactly one label. Ask these questions in order and stop at the first "yes":

1. Is the post mainly a pitch, blurb, synopsis or link for one specific novel? → `promo`
2. Does it ask others to name novels it hasn't named (suggestions, or "help me find this title")? → `request`
3. Otherwise → `discussion`

### Second boundary: `promo` vs. `discussion`

**Rule:** If most of the post is a blurb, synopsis or link for one novel, it's `promo`, even if it ends with a question like "What do you think?" or "Would you read this?". If the post mentions a novel but mostly gives the poster's opinion of it, it's `discussion`.

**Tags:** Posts start with tags like `[DISC]` and `[IP]`. I removed them from every post in `labels.csv` so the model has to read the post, not the tag.

### The hardest boundary

**Which two labels:** `request` vs. `discussion`

**The decision rule I used every time:**
If a post that isn't `promo` asks other people to name novels it hasn't named, it's `request`. Every other post is `discussion`, including posts phrased as questions about novels the poster already named ("Is X worth reading?", "Will X get better?"), because those ask for opinions, not new titles.

*Boundary example:* "[DISC] is omniscient reader a good starter web novel? … is it well written, is it easy to understand? is it well paced?" It's a question and sounds like asking for advice, but it asks for opinions on a novel already named, so it's `discussion`.
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public text posts from r/WebNovels. I saved Reddit's public JSON listings (New and the next page of New, Hot, Top of the month, Top of the year) from my browser into `data/`. I kept only text posts, dropped image-only posts and duplicates, and removed the leading tags (`[DISC]`, `[IP]`, `[FIN]`…) from every title so the model can't learn the tag instead of the post. Each row's `text` is the post title plus the full body, untrimmed.

**How I labelled them:** I labelled the taxonomy examples myself, and 20 posts cold with no AI (marked `cold` in `note`). Claude pre-labelled the rest using my definitions and order of checks (marked `prelabeled` in `note`). I then reviewed the pre-labels and corrected the ones I disagreed with.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `discussion` | 88 | 38% |
| `promo` | 76 | 33% |
| `request` | 66 | 29% |
| **Total** | 230 | 100% |

**Three hard cases**

**1.**
> *The post:* "Where to find full novel of Slain Dragon Bride for free", asking where to read a novel they already named. About 15 posts in the dataset are like this.
>
> *Could have been:* `request` or `discussion`
>
> *I chose, because:* `discussion`. They're asking for a website, not for people to name novels they haven't named.

**2.**
> *The post:* "Recommending A webnovel I found last night: go read *Zombie Cafe*… it is so GOOD", from a reader, not the author.
>
> *Could have been:* `promo` or `discussion`
>
> *I chose, because:* `promo`. The whole post is a pitch for one novel, and my `promo` label doesn't depend on who wrote it.

**3.**
> *The post:* "Current novel recs: 1. PERFECT RUN 5/5… 2. WORLD'S END… 3. FLORIDA MAN'S GENERAL STORE…", a ranked list of several novels with short reviews.
>
> *Could have been:* `promo`, `request` or `discussion`
>
> *I chose, because:* `discussion`. It pitches several novels rather than one, and it doesn't ask anyone to name novels, so it's an opinion post.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**MPS Apple Silicon

**Settings:** <!-- epochs, learning rate, batch size, seed -->
```
3 labels: promo, request, discussion
Epochs: 3
Learning rate: 2e-05
Batch size: 16
Seed: 42
```

**Anything I changed from the defaults, and why:**<br>
None

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
```
train 160  ·  val 35  ·  test 35
            train  val  test
label                       
promo          52   12    12
request        46   10    10
discussion     62   13    13
```

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Which of my labels I could tighten.
- *What came back:* Claude pointed out that my second `author` example ("Web novel from the website kakuyoumu…") never says the poster wrote it. It could just be a reader sharing a find, so my `author` rule couldn't be applied from the text.
- *What I changed:* I replaced `author` with `promo` (a post pitching one specific novel, whoever wrote it), because that is something I can see in the text.

**Moment 2**

- *What I asked for:* Claude pre-labelled my posts, and I labelled 20 of them cold without seeing its labels.
- *What came back:* We agreed on 15 of 20. Comparing them showed two rows where Claude's labels had shifted by one position ("Any recommendations for a fellow reader…" was marked `discussion`), which was a bug in its pre-labelling, not a judgment call.
- *What I changed:* We fixed the shifted rows. My cold labels replaced Claude's on all 20, and the 5 disagreements are recorded in the `note` column ("cold (Claude pre-label was …)"). It also showed me why the cold check comes first: it's the only way to catch errors in AI labels.

**Pre-labelling disclosure:** Claude pre-labelled about 205 of the 230 posts using my three definitions and my order of checks (promo → request → discussion). Those rows say `prelabeled` in the `note` column. I labelled 20 posts cold myself with no AI (`cold`), and the taxonomy examples are mine (`taxonomy example`). I reviewed the pre-labels and changed the ones I disagreed with.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
