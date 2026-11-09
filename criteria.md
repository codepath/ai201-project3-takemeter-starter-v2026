# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Every post has a label

<!-- Your criterion. It must name a number. -->
The model correctly categorizes 3 out of every 4 posts (minimum of 75% total accuracy sorting posts).

**Why this target:**
Even if the model labels wrong the objective is to train AI to classify posts. It should be able to learn or choose a label at the very least depending on which of the three labels a post is in with decent accuracy. It is reasonable to say it will miss at least once.


---

## 2. Promo posts are accurate

<!-- Your criterion. -->
Promo posts should be accurately guessed 5 of 5 posts.

**Why this target:**
The promo posts are one of the easiest to diagnose by eye due to them narrating or giving them away but through code it should be a bit more difficult to achieve. We keep the standard at 5/5 to keep expectations high.

---

## 3. Classifying hard posts

<!-- Your criterion. -->
In the case that posts with links are slightly unrelated and hard to classify, at least 4 of 5 random posts where links are provided are classified as follows. Links to threads are labeled `request`. Links to GitHub or live applications are labeled `promo` even if they're asking for advice or reviews.

**Why this target:**
This accounts for edge cases and ensures links and text classify posts easier. It should be easy to check if a string has a ".domain" like ".com".

**REVISED (Unit 6):**
A post with a link to a thread is a request but a link to a GitHub repo or live application is a promo in 4 of 5 posts where links are provided.

**Reason for revising:** Grader said it is unrelated to the subreddit r/WebNovels so I added more context. Instead of removing certain unrelated posts out of training data I try to include them as exceptions in the system. Outside readers should now more clearly understand the criteria is accounting for edge cases

---

## 4. Title default posts

<!-- Your criterion. -->
If the post is title-only and ends with ? or starts with "How to / Looking for", default is request in 5 of 5 posts


**Why this target:**
The title only and question posts are giveaways and should be accurate 100% of the time.


---

## 5. Subset of posts

<!-- Your criterion. -->
Human labeling should match with the model in at least 3 of 5 posts each category. For a set of 20 posts in the set of posts from the file `guesses.csv`.

**Why this target:**
Small test run to test accuracy of model without processing large amount of posts. 3 of 5 allows room for model to make mistakes or incorrectly classify tricky posts.

**REVISION (Unit 6)**
Human labeling should match with the model in at least 3 of 5 posts.

**Why this target:**
Accounts for the AI model and human error since I honestly didn't have time to read all the labels.

**Reason for revising:** Grader indicated it wasn't testable by an outside reader since it doesn't name a set of posts (maybe a subset of 20 though the reader can probably label 20 posts). Therefore, I modified criteria to be more testable to someone who didn't write the criteria.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
