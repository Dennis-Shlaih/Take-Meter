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

TakeMeter sorts posts from r/LocalLLaMA, a public Reddit community about running open-weight language models on local hardware, by how the author supports their central point. The four labels are `analysis`, `announcement`, `hot_take`, and `reaction`. The research question is whether a small fine-tuned model can tell evidence-based technical reasoning from unsupported generalizations and personal reactions, even though all of these posts share the same technical vocabulary. Technical terms, links, and statistics are not enough to decide a label, so the classifier has to pick up on how the evidence is used.

---

## Label Taxonomy
 
**Stretch feature:** `announcement` is a fourth label, added because many r/LocalLLaMA posts relay a release or news item without making a claim of their own, and none of the other three labels fits them.
 
**Scope:** Examples are public r/LocalLLaMA posts (and top-level comments that make sense on their own). I exclude title-only or link-only posts, bodies that are just a pasted model card, and questions or proposals that only ask for input (including help requests). For mixed-purpose posts I use the dominant purpose and explain genuinely ambiguous calls in `note`.
 
### `analysis`
 
**Definition:** The author's own claim is backed by a relevant, checkable detail stated in the post text, paired with a concrete outcome. The detail can be a number tied to a stated setup, an exact prompt or input used in a described test together with its observed result, a model/quant/hardware configuration relevant to a comparison together with a measured or observed result, a calculation, or a linked source whose finding the post states. An adjective such as "best", "solid" or "impressive" is not a concrete outcome. A bare link, screenshot, or demo does not count by itself. A vague personal impression such as "I tried both; X is better," without those details, is `hot_take`.
 
**Example 1:**
> NVIDIA Nemotron-4 340B model finished running prompts from my farel-bench benchmark this morning (it took about 21 hours to process all 450 prompts) and took first place among open-weight models with the score of 78.67 (% of correct answers).
 
**Example 2:**
> if you assume that performance of `ollama run dolphin-mixtral` with `gpt-4-1106-preview`, and you have enough content to run through, then mixtral is ~11x cheaper -- and you get the privacy on top.
 
### `announcement`
 
**Definition:** The post primarily shares a release, news item, result, or technical resource, including the author's own tool, model, project, tutorial, update, or invitation to the author's own group or community, without making a separate evidence-backed claim the post is chiefly defending. If the author adds their own check, comparison, calculation, or critique, use `analysis`.
 
**Example 1:**
> NVIDIA Releases Nemotron Nano 2 AI Models. 6X faster than similarly sized models, while also being more accurate. NVIDIA is also releasing most of the data they used to create it, including the pretraining corpus.
 
**Example 2:**
> I've built a CLI tool that can generate code and scripts with AI using Ollama or LM studio. I've been working on a CLI tool (similar to claude-code) that lets you go from simple questions to more complex tasks. You can install it with: pip install xandai-cli
 
### `hot_take`
 
**Definition:** The author asserts or argues a judgment about the field, a tool, a model, a person, or other people without relevant, checkable support stated in the post text. This includes personal impressions of a tool or model without such details, tests whose only outcome is an adjective, and insults aimed at a tool or person. Anger, profanity, and unsupported or unverifiable figures do not make it `analysis`.
 
**Example 1:**
> 1 million context is the scam, the ai start hallucinating after the 90k. im using the qwen cli and its become trash after 10 percent context window used.
 
**Example 2:**
> Who has noticed that closed models are no longer as popular as they used to be? Openia was wrong about GPT-5, Anthropic is self-destructing, and Google is irrelevant.
 
### `reaction`
 
**Definition:** The post's content is mainly the author's feeling about a specific moment or event, or a personal experience told for its own sake (excitement, amusement, frustration), with no general quality judgment being argued. A judgment such as "X is the dumbest" is `hot_take`, even if it is expressed as a feeling.
 
**Example 1:**
> A Christmas Miracle: Managed to grab 3x RTX 5090 FE at MSRP for my home inference cluster. I am truly grateful to God for so much more than just hardware, but I am also specifically thankful for this opportunity to upgrade my local AI research lab.
 
**Example 2:**
> LLama 3.2 1B and Llama-cli will fit on a 1.4 MB floppy disk. Wild that something that small contains as much information as it does, blows my mind.
 
### Decision rule for the hardest boundary: `analysis` vs. `hot_take`
 
Ask: **could a stranger check the author's claim using only what is in the post, and is there a concrete outcome to check it against?**
 
- Support must be stated in the post text and relevant to the author's claim, and it must come with a concrete outcome: a number, an output, a pass/fail, or an error. The Nemotron post gives a 450-prompt benchmark and a score of 78.67, so it is `analysis`. The Qwen3-Next post says it tested q4_k_m and that it "did the best Tetris in a single HTML file I've ever seen", but "best" is an adjective, with no prompt or score, so it is a `hot_take`.
- Quoting the prompt is not enough on its own. The Qwen 3 14B post gives an exact pygame prompt, but its only outcome is "seems incredibly solid", so it is a `hot_take`. The llama3.1 post gives the model file, the exact prompt, and the answers (Paris, Londen, Paris), so it is `analysis`.
- A vague personal comparison ("I tried both; X is better", "I think I might still prefer Mistral 7b over Llama3 8b") is a `hot_take`. A named model or configuration helps only when it makes the author's stated test or comparison checkable.
- Screenshots, demos, and bare links do not count as evidence by themselves. A link counts when the post states the finding from that source and uses it to support the author's claim: the fblgit post states that HF staff's contamination tool gave a 99% chance of GSM8K contamination, so it is `analysis`.
- Figures that cannot be checked from the post (benchmark numbers with no method, a $/GB range with no named cards) do not make a post `analysis`.
Two secondary boundaries:
 
- **`hot_take` vs. `reaction`:** is the post mainly expressing a feeling about a specific moment or event, or asserting a general judgment? A `reaction` is about the moment or the writer's experience. A general quality judgment or insult about a tool, model, person, or field is a `hot_take`, even when emotional ("SmolVLM2 it's the dumbest shit I ever seen" is a `hot_take`).
- **`analysis` vs. `announcement`:** does the author add something of their own to the source's numbers, such as a check, a comparison, a calculation, or a critique? If yes, `analysis`. If they only pass the numbers along, `announcement`.
- **`announcement` invitations:** inviting people to the author's own group or community counts as sharing their own resource and is an `announcement`, unless another label better fits the post's main purpose.
### The hardest boundary
 
**Which two labels:** `analysis` and `hot_take`.
 
**The decision rule I used every time:**
A post is `analysis` only if the post text itself states a relevant, checkable detail (a number tied to a setup, an exact prompt or input, a configuration, a calculation, or a stated finding from a linked source) together with a concrete outcome. If the support is only a link, a screenshot, a demo, or an adjective like "best" or "solid", it is a `hot_take`, even when the tone is calm and the setup sounds technical.
 

# The Dataset
 
**Where the posts came from:** Public posts (and a few top-level comments that stand on their own) from r/LocalLLaMA, spanning several model generations from early Llama and Mistral to recent releases. Candidates were gathered from the community as a whole rather than from a single thread, and I removed posts outside my scope: title-only or link-only posts, pasted model cards, and questions or help requests that only ask for input. That removed 19 of 169 candidates, leaving 150 labelled rows. A second sampling round then added 58 more posts, chosen to bring the thin labels (`reaction` and `analysis`) up to the 30-row floor and to push `announcement` below my 50% cap. The same scope rules applied, so question-only, title-only, and mixed-purpose posts from that round were left out. The final file has 208 rows.
 
**How I labelled them:** The candidates were labelled by combining human oversight with AI assistance, and each row carries a `note` explaining the call. I then reviewed every row against my written definitions for pre-labels. While reviewing, I tightened the `analysis`, `hot_take`, and `reaction` definitions (a checkable detail must be paired with a concrete outcome; adjective-only outcomes, screenshots, demos, and bare links do not count) and re-checked the whole file against the revised wording. That changed 13 labels: 10 `analysis` posts became `hot_take` (e.g. the MiniCPM, Xwin, ChatGPT-4o, and Qwen3-Next posts), 1 `hot_take` became `analysis` (fblgit), 1 `reaction` became `hot_take` (SmolVLM2), and 1 `reaction` became `announcement` (an invitation to the author's own Telegram group). Ambiguous calls are explained in the notes. The 58 second-round posts were labelled under the final definitions, with a `note` on each; hard calls are flagged as such in `note`.
 
**Counts per label:**
 
| Label | Count | Share |
|---|---|---|
| `analysis` | 47 | 22.6% |
| `announcement` | 87 | 41.8% |
| `hot_take` | 44 | 21.2% |
| `reaction` | 30 | 14.4% |
| **Total** | 208 | 100% |
 
**Three hard cases**
 
**1.**
> *The post:* "Qwen3-Next-80B-A3B-Thinking-GGUF has just been released on HuggingFace. Tested q4_k_m. It did the best Tetris in a single HTML file I've ever seen. I tried Devstral recently and the results weren't as accurate."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose `hot_take`, because:* the post names a quant, a task, and a comparison model, which makes it look like a test. But the only outcome is the adjective "best", with no prompt, score, or output a stranger could check. Under my rule, a stated setup needs a concrete outcome to count as `analysis`.
 
**2.**
> *The post:* "fblgit/una-xaberius-34b-v1beta is caught cheating on leaderboard. UNA cybertron juanako is just a lie... HF staff ran contamination detection tool on this model, and it's got a 99% chance of being contaminated on GSM8K."
>
> *Could have been:* `hot_take` or `analysis`
>
> *I chose `analysis`, because:* the tone is an angry accusation ("liar", "nothing but cheating"), which is why it first looked like a `hot_take`. But the post states a specific, checkable finding (HF staff's contamination tool, 99% chance, GSM8K) and uses it as support. The accusation goes further than the finding, which I note in `note`, but the definition asks for a checkable detail, not proof.
 
**3.**
> *The post:* "Kimi K2.5 is No.1 in the Design Arena, beating Gemini 3 Pro and Claude Opus 4.5. It matches my experience. K2.5 can always one-shot a very stunning webpage."
>
> *Could have been:* `announcement` or `hot_take`
>
> *I chose `announcement`, because:* the post's main purpose is relaying a leaderboard result. The closing sentence is an unsupported endorsement, but it is a short add-on rather than a separate claim the post is chiefly defending.

## The Training Run

**Base model:** distilbert-base-uncased

**Settings:** 8 epochs, learning rate 2e-5, batch size 16, maximum sequence length 128, seed 42.

**Anything I changed from the defaults, and why:** I updated the label list to include all four categories in my dataset: analysis, announcement, hot_take, and reaction. I kept the other training settings at their provided defaults to establish a baseline before experimenting with hyperparameters, with the exception of the number of epochs. There was a real risk of underfit, and the model mostly predicting announcement, as per the data and Claude's prediction based on my choices.

Split sizes: To be filled in after running the notebook's train/validation/test split. I will record the number of examples in each split and the per-label counts in the test set. 

---

 
## How I Used AI
 
**Moment 1**
 
- *What I asked for:* After my first pass at the labels, I asked Claude which of five borderline posts (MiniCPM, Deek Seek, LLM Awards, Search is not generation, Mistral 7b vs. Llama3 8b) should change under my written definitions.
- *What came back:* It said to change none of them. It also pointed out that my `chatgpt4o just got worse than gpt4` post was labelled `analysis` while having less to check than MiniCPM, so the two were inconsistent under the same rule.
- *What I changed:* I took the inconsistency point and made it a rule instead of fixing one row. I asked for a full consistency pass, then went further than Claude did: I flagged Qwen3-Next ("did the best Tetris") as another `analysis` post that should be a `hot_take`, which Claude had not caught. Claude later conceded that MiniCPM had to flip too, reversing its first answer.
**Moment 2**
 
- *What I asked for:* A full row-by-row review of my 149 labelled posts for consistency with the definitions, plus suggested tweaks to the definitions themselves.
- *What came back:* Claude proposed adding "a stated detail must appear in the post text" and "paired with a concrete outcome" to the `analysis` definition, and a table of about a dozen row changes. Two of its suggestions were wrong or shaky. It flipped Qwen 3 14B to `analysis` on an "exact prompt" rule that its own later outcome clause contradicted, and it suggested flipping Mistral Nemo to `analysis` based on its belief about what the UGI leaderboard measures, which it said I should verify.
- *What I changed:* I kept Mistral Nemo as `hot_take` rather than relying on an unverified claim. I reverted Qwen 3 14B to `hot_take` once the outcome clause made the rule consistent. I wrote the final definitions into `label_definitions.txt` and this README myself, and I decided each of the final label changes, including removing a help request that did not belong in scope.
**Pre-labelling disclosure:**
 
I used AI to pre-label the candidate posts. For my last few batches candidates came with a draft label and a `note` explaining it as a pre-label, and I started from those. I then reviewed the rows against my written definitions, and I revised the definitions during that review (adding the "stated in the post text" and "concrete outcome" requirements) and re-checked the whole file under the revised wording. That review changed 13 labels (10 `analysis` to `hot_take`, 1 `hot_take` to `analysis`, 1 `reaction` to `hot_take`, 1 `reaction` to `announcement`) and removed 1 out-of-scope row, so the pre-labels were not accepted wholesale. Claude also helped with the mechanics: it assembled `labels.csv` from the candidate posts acquired, computed the label counts.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.406 | 0.594 | +0.188 |
| Macro F1 | 0.212 | 0.457 | +0.245 |
| F1 — `analysis` | 0.250 | 0.667 | +0.417 |
| F1 — `announcement` | 0.600 | 0.733 | +0.133 |
| F1 — `hot_take` | 0.000 | 0.429 | +0.429 |
| F1 — `reaction` | 0.000 | 0.000 | +0.000 |

**What I predicted before I looked:**

Before seeing the trained numbers, I predicted that the trained model would have the most noticeable improvement on `analysis` and `hot_take`, since fine-tuning on labeled examples should help it distinguish evidence-based technical reasoning from unsupported opinions. I also expected some improvement on `announcement`, but I was less certain about `reaction` because it had fewer examples.

**What the gap actually means:**

Fine-tuning improved overall accuracy by **0.188** and macro F1 by **0.245** compared with the baseline. The largest improvement was for `hot_take` (+0.429 F1), followed by `analysis` (+0.417). This suggests that fine-tuning helped the model learn distinctions that the general-purpose baseline struggled with, especially identifying unsupported judgments and evidence-based reasoning. The `announcement` F1 also improved by 0.133.

However, `reaction` F1 remained at 0.000, so fine-tuning did not improve performance across every label. The results suggest that task-specific examples helped, but the model still struggles to recognize reactions. Overall, fine-tuning added measurable value, although the remaining per-label weakness shows that better overall performance does not mean the classifier handles all four categories reliably.

## Run Log — Before
# Everything this notebook needs is already in requirements.txt — you installed
# it when you set the project up. This cell just says what you're running on.

 prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | analysis | anouncement | hot_take | reaction
|---|---|---|---|---|
| analysis | 5 | 1 | 1 | 0
| anouncement | 1 | 11 | 1 | 0
| hot_take | 1 | 3 | 3 | 0
| reaction | 1 | 2 | 2 | 0

**My biggest off-diagonal number, and what it means:**

The largest off-diagonal count was 3 true hot_take posts predicted as announcement. This suggests the model sometimes treated unsupported opinions or judgments as announcements rather than recognizing that the post was primarily expressing an unsupported claim. The same number of reaction posts were also misclassified as announcement (2) and hot_take (2), showing that the model struggled to distinguish reactions from the other categories. Most notably, it predicted zero posts as reaction, missing all 5 true reaction posts.



---

## Verdicts and Diagnoses
device: cpu  (CPU)
torch:  2.14.1+cu130


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

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook
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
