# Running TakeMeter

Everything about how the starter works.

This pair is different from the last two: **the training runs in a hosted
notebook, not on your machine.** Your laptop does the reading, the labelling,
and the baseline. Colab does the training.

---

## Before your first class

Setup is in **two halves that don't touch each other.** Your device gets a
virtual environment. Colab gets an account and a token. Nothing you install
locally has anything to do with the notebook, and nothing you set up for Colab
affects your machine.

Do both before your first session. The [environment setup page](../pages/ide_setup)
has the per-operating-system commands.

### On your device — the virtual environment

The venv is for **one script**: `baseline.py`, the zero-shot baseline. That's
unit 6, Milestone 1. The notebook never touches it — Colab has its own Python,
and section 1 installs what it needs there.

So why set it up a week before you use it? Because `test.py` is what tells you
your Python is a version the pinned packages don't support, or that you're short
on disk, or that the 1.6 GB baseline model still hasn't downloaded. Each of
those is a twenty-minute problem this week and a dead breakout next week.

**Your disk needs more room — about 9 GB free, up from 6.** The baseline model
is roughly 1.6 GB and PyTorch is not small. `test.py` checks this. Local disk
only — Colab's storage isn't your problem.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**`python test.py` passing is what unit 6 needs.** Unit 5 doesn't use the venv
at all — for that, see the two Colab steps below.

You'll see one `[WARN] Baseline model — not downloaded yet`. That's expected in
unit 5. **Clear it before the unit 6 session** by running the baseline once —
downloading 1.6 GB during class is not how you want to spend the breakout.

### For Colab — an account and a token

Two things, neither of which installs anything. **This is all unit 5 needs.**

**A Google account**, for Colab. No card, no paid tier. You already have one if
you set up an API key in unit 1.

**A GitHub token**, so the notebook can read your repo and commit back to it.
The steps are in the next section — do them now, not during a session.

> ⚠️ **Don't make a venv in Colab.** You'll see `!pip install` in section 1 and
> may be tempted. Colab is already an isolated machine that gets thrown away —
> a venv inside it does nothing except break the link between what you install
> and what the notebook can import.

> **No API key is needed for this pair.** Nothing here calls a hosted model.
> The baseline runs locally and the training runs on Colab's GPU.

---

## The GitHub token — once, before your first session

The notebook clones your repo and pushes its results back, so nothing has to be
uploaded or downloaded by hand. That needs a token. Ten minutes, once.

### 1. Make the token

GitHub → your avatar → **Settings** → **Developer settings** → **Personal
access tokens** → **Fine-grained tokens** → **Generate new token**.

| Field | What to put |
|---|---|
| Token name | `colab-takemeter` |
| Expiration | Custom — the end of term |
| Repository access | **Only select repositories** → your TakeMeter repo |
| Permissions → Repository → **Contents** | **Read and write** |

Contents is the only permission you need. Leave the rest alone.

**Generate token**, then copy it. GitHub shows it once and never again. If you
lose it, delete it and make another — that's routine, not a disaster.

### 2. Put it in Colab, not in the notebook

Open the notebook in Colab (see below), then in the left sidebar click the
**🔑 key icon** → **Add new secret**:

| Field | Value |
|---|---|
| Name | `GH_TOKEN` — exactly this |
| Value | the token you copied |
| Notebook access | **on** |

Secrets belong to your Google account. They aren't stored in the notebook, so
they don't travel to anyone you share it with, and they survive a runtime reset.

> ⚠️ **Never paste the token into a cell.** Cell outputs get saved, and a saved
> token in a public repo is a token strangers can push with. The notebook reads
> it from the secret and never prints it — leave it that way. If you think
> you've exposed one, delete it on GitHub and make a new one.

**The Notebook access toggle is per notebook.** If you ever start from a fresh
copy, switch it on again there.

---

## The notebook

`takemeter.ipynb` runs in **Google Colab**, not on your machine.

1. Open [colab.research.google.com](https://colab.research.google.com) →
   **File → Open notebook** → the **GitHub** tab → paste your repo URL → pick
   `takemeter.ipynb`.
2. **Runtime → Change runtime type → T4 GPU.**
3. Fill in the four lines at the top of section 1's connect cell — GitHub
   username, repo name, your name, your email — and run section 1.

**Open it from GitHub, not by uploading.** Uploading gives you the notebook and
nothing else. Opening it from your repo is what lets section 1 clone the rest.

> ⚠️ **Set the runtime before running any cell.** Changing it afterwards
> restarts everything and you run section 1 again. This is the single most
> common way to lose twenty minutes in this pair.

### It reads and writes your repo

Section 1 clones your repo into the session. Which means:

- **Nothing to upload.** `labels.csv` and `data/practice_labels.csv` are
  already there.
- **Nothing to download.** Sections 5 and 6 commit `results.json` and
  `results_three_seeds.json` and push them.

The clone is a **snapshot, taken when you ran section 1.** Add rows to
`labels.csv` on your laptop mid-session and the notebook won't see them —
commit and push there, then re-run the connect cell.

> **Two machines now write to one repo.** Before you commit anything on your
> laptop, `git pull`. Skip it and your push is rejected, because Colab got there
> first. This is the one new way to trip yourself up this pair.

> **Your edits to the notebook itself aren't pushed.** `LABELS` and the settings
> live in the Colab session, and git can't see a running notebook. That's fine —
> your taxonomy belongs in your README, which is what gets read.

### What's in it

| Section | When | What it does |
|---|---|---|
| 1. Setup | unit 5 | Installs, and checks you have a GPU |
| 2. Your labels | unit 5 | `LABELS`, the settings, and **the seed** |
| 3. Split | unit 5 | 70/15/15, stratified |
| 4. Train | unit 5 | ~10 minutes |
| 5. Results | unit 5 | Writes `results.json` |
| 6. Three seeds | **unit 6** | Retrains three times in one cell (~30 min) |
| 7. Confusion matrix | **unit 6** | Prints a markdown table to paste |

Sections 6 and 7 are next week. Nothing in unit 5 needs them.

---

## Your data

`labels.csv` in your repo. Three columns:

| Column | What's in it |
|---|---|
| `text` | The whole post. Don't trim it to fit |
| `label` | One of your labels, spelled **exactly** as in `LABELS` |
| `note` | `cold` for the 20 you labelled unaided, and a note on any you pre-labelled |

`labels_template.csv` shows the shape. `data/practice_labels.csv` is the set
used in class — 60 posts from a fictional running forum, already labelled, so
you can run the whole notebook before you have data of your own.

**One file, unsplit.** Don't split it yourself — the notebook does the 70/15/15
split, and splitting twice is how examples leak between training and test.

### The check before training

Section 2's last cell looks for the things that break a run or quietly ruin it:

| It says | What it means |
|---|---|
| `[FIX ME] Labels in your CSV that aren't in LABELS` | A spelling or capital mismatch. `Hot_take` and `hot_take` are different |
| `[FIX ME] 'x' is 78% of your data` | Over the brief's 70% cap. The model will learn to guess it |
| `[look at] N duplicate posts` | They'll land in different splits and inflate your score. That's leakage |
| `[look at] Only 12 examples of 'x'` | Its test split will be tiny, so its F1 will jump between seeds |
| `[look at] 60 rows` | Under the submission floor. Training still runs — fine for the practice data |

---

## The baseline — unit 6

```bash
python baseline.py
python baseline.py --trained results.json
```

This runs a general model over your posts using **only your label
definitions**, with no training. It's the fair opponent your fine-tuned model
has to beat.

**It scores `test_split.csv`** — the held-out posts the notebook saved in unit 5,
the same ones your trained model was measured on. Two numbers from two different
sets of posts aren't a comparison, which is why it reads that file rather than
picking its own sample. If the file isn't there it says so, falls back to a
random sample of `labels.csv`, and tells you to disclose that in your README.

Runs **on your machine**. No account, no key. A few seconds per post, so 30
posts takes a couple of minutes — that slowness is itself part of the finding.

Put your definitions in `label_definitions.txt`, one per line as
`label: definition`, copied from your README. **The definitions are the prompt** —
they're the entire input the model gets.

Without the file it falls back to bare label names, which is a much weaker
prompt. Worth doing on purpose once: run it both ways and the gap between the
two accuracies is what your definitions were worth, measured instead of assumed.
If you report the bare-names run as your baseline, say so in your README.

The second command adds a Trained column and prints the **Baseline vs.
Trained** table ready to paste.

---

## The agreement check — unit 6

Staff labelled 30 posts with your taxonomy. You label the same 30, then compare.

```bash
python agreement.py
```

Three files. The staff set arrives as a pair — the posts, then the labels once
yours are done — and the script joins them on `id`:

| File | Where it comes from |
|---|---|
| `data/staff_posts.csv` | Your TF gives you this: the 30 posts, no labels |
| `data/staff_labels.csv` | Your TF gives you this too. **Don't open it until you've done yours** |
| `my_staff_labels.csv` | You make it: the same posts, labelled by you, with `text` and `label` columns |

Put both staff files in `data/` under those names and the bare command finds
them. Anywhere else, point at them:

```bash
python agreement.py --staff-posts posts.csv --staff-labels labels.csv
```

Posts are matched on their text, so **paste it unchanged**. Retype or trim a
post and it won't match — the script tells you which ones didn't.

It works out the rate and lists every disagreement. **It stops there on
purpose.** The rate is arithmetic; the adjudication is the graded part, and your
README has a block to fill in for each one.

> This is the only instrument you have that can tell a labelling problem from a
> model problem. Milestone 4 asks you to use it as exactly that — a label pair
> you disagreed with staff about, and that your matrix also confuses, is a
> finding about your labels rather than about the model.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python baseline.py` | The zero-shot baseline on your held-out posts — **unit 6** |
| `python agreement.py` | Your labels vs. the staff set — **unit 6** |
| `python baseline.py --help` | All the options |
| Colab: section 1 | Connect to your repo — every session |
| Colab: sections 2–5 | Train once, results pushed — **unit 5** |
| Colab: sections 6–7 | Three seeds and the matrix — **unit 6** |

---

## Which piece goes with which milestone

### Unit 5 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Pick a community and read it | Nothing to run. Read for 20 minutes |
| 2 | Design your labels | README, **Label Taxonomy** |
| 3 | Write your criteria | `criteria.md` — all five are yours this time |
| 4 | Collect and label 200 | `labels.csv` |
| 5 | Run the training | Colab, sections 1–5 |
| 6 | Write it up | README |

### Unit 6 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Run the baseline | `baseline.py` |
| 2 | Retrain three times, read the matrix | Colab, sections 6–7 |
| 3 | Check yourself against the staff labels | `agreement.py` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | Colab, section 6 again |
| 6 | Say what's still broken | README |

---

## Where everything lives

| File | What it does |
|---|---|
| `takemeter.ipynb` | The training notebook. Runs on Colab |
| `baseline.py` | The zero-shot baseline. Runs on your machine |
| `agreement.py` | Your labels against the staff set. **Unit 6** |
| `criteria.md` | Your five criteria. **You write all five** |
| `labels.csv` | Your labelled data. **You create this** |
| `labels_template.csv` | The shape it needs |
| `label_definitions.txt` | Your definitions, for the baseline |
| `data/practice_labels.csv` | The 60-post practice set used in class |
| `data/staff_posts.csv` | The staff set's posts. **Your TF gives you this** |
| `data/staff_labels.csv` | The staff set's labels. **Your TF gives you this** |
| `README.md` | Your submission |
| `results.json` | Written and committed by the notebook |
| `test_split.csv` | Your held-out posts, committed by the notebook. `baseline.py` reads it |
| `results_three_seeds.json` | Written and committed in unit 6 |
| `baseline_results.json` | Written by `baseline.py`. **Commit it** |
| `agreement_results.json` | Written by `agreement.py`. **Commit it** |
| `my_staff_labels.csv` | Your labels on the staff set. **You create this** |

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `NO GPU` in section 1 | Runtime → Change runtime type → T4 GPU, then re-run |
| `CLONE FAILED` | Read the three causes it prints. Usually `REPO` has the whole URL in it instead of just the name |
| `SecretNotFoundError` | The `GH_TOKEN` secret isn't set, or **Notebook access** is off for it. 🔑 in the sidebar |
| `FileNotFoundError: labels.csv` | It isn't committed and pushed yet. Do that on your laptop, then re-run the connect cell |
| The push failed, or nothing pushed | Your token expired, or it's missing **Contents: Read and write**. Make a new one |
| Your files vanished mid-session | The session reset. Re-run section 1 — the clone comes back |
| `git push` rejected **on your laptop** | Colab has pushed since you last pulled. `git pull`, then push |
| `KeyError` during training | A label in your CSV isn't in `LABELS`. Check capitals and spaces |
| Training takes an hour | You're on CPU. See the first row |
| Accuracy swings 15 points between seeds | Your dataset is too small or too lopsided for a stable measure. **That's a diagnosis, not a mistake** — write it down |
| A label's F1 is 0.00 | It probably has almost nothing in the test split. Check the split table |
| `baseline.py` says no `test_split.csv` | Unit 5's results section never finished. Re-run it, or note in your README that your comparison isn't like-for-like |
| `baseline.py` is downloading forever | First run only, ~1.6 GB. Do it before class |
| The baseline is very slow | Expected. A few seconds per post is what no fine-tuning costs at runtime |

The three usual causes when the notebook fails, in order: the runtime isn't set
to GPU, the session reset and the clone is gone, or a label in your CSV doesn't
match `LABELS` exactly.

If none of those fix it, commit your CSV and criteria and write down the error.
**You have a labelled dataset and a filed standard, which is most of the
week's grade.**

---

## A note on committing

At least four commits in unit 5, four more in unit 6. Your commit history is
what shows your criteria existed before your results did.

The `results*.json` files are deliberately **not** in `.gitignore`. They're
evidence the run happened. Colab commits those two for you. Everything else —
`labels.csv`, `criteria.md`, `baseline_results.json`, your README — you commit
from your laptop.

**Pull before you commit locally.** Colab has been pushing to the same repo.

**Do not delete and recreate this repository.** You submit the same URL both
weeks.
