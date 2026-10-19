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

## 1. Overall accuracy
 
Overall accuracy on the held-out set is at least **0.65** on every seed.
 
**Why this target:** With four labels, chance is 25%, and a model that always
guessed my biggest label would score no more than 50% (criterion 4 caps any
label at 50% of my data). 0.65 puts the model at least 15 points above that
guess, while still leaving roughly one post in three wrong, which is about
what I'd expect from a small model.
 
---
 
## 2. Per-label F1
 
Every label has an F1 of at least **0.55** on the held-out set on every seed,
except my thinnest label, which needs at least **0.45**.
 
**Why this target:** Overall accuracy can hide a dead label: a model could
ignore `reaction` entirely and still look fine. 0.55 because the model can find
each label more often than it misses it. My thinnest label will have around 30
examples (the floor in criterion 4), so only about 6 land in the test split,
and one wrong prediction swings its F1 by 0.10 or more. I loosened its target
by 0.10 for that reason instead of pretending the score will be stable.
 
---
 
## 3. The analysis / hot_take boundary
 
On the held-out set, on every seed, at most **25%** of true `hot_take` posts
are predicted as `analysis`, and at most **25%** of true `analysis` posts are
predicted as `hot_take`.
 
**Why this target:** This pair is part of the research question: can the model tell
evidence-based reasoning from unsupported generalization? The likely failure
is a model that learns "contains numbers means analysis", which would potentially mislabel a rant post. Overall accuracy would not show that. I set 25% rather than
something tighter because this is the boundary I find hardest.
 
---
 
## 4. Balance
 
In `labels.csv`, no label makes up more than **50%** of the rows, and no label
has fewer than **30** rows (15% of 200).
 
**Why this target:** The project's rule is 70%, but at 70% a model that always
guesses the biggest label scores 0.70 and my accuracy target in criterion 1
would be meaningless. Capping at 50% keeps that baseline well below my
target. The 30-row floor is what makes criterion 2 measurable: with fewer, my
thinnest label would have about 4 test examples and its F1 would be noise. In
my early reading sample `reaction` was the hardest label to find, so this floor
is the one most likely to need extra sampling.
 
---
 
## 5. Consistency
 
On a blind relabel of **30** randomly chosen rows from `labels.csv`, my new
labels agree with my original labels on at least **80%** of them. The relabel is
done by a classmate using only my written definitions if I can get one, or by
me at least two days later without looking at the original labels.
 
**Why this target:** A model cannot reliably beat the agreement of the people
who labeled the data, so this must sit above the model's 0.65 target in
criterion 1. With four labels and a hot_take / reaction boundary I already
found uncertain, I don't expect near-perfect agreement, so 80% is a real test
without being unreachable. If I fall short, the definitions need fixing before
training, not after.
 
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
