# From a folder to a handover

Data and Code Management · Thursday, 1 October 2026 · two 45-minute blocks

Today you will diagnose a small project and record a reviewed improvement to its
README. Last week introduced the course; today starts the practical workflow.
R and Python projects use the same habits. **The required Git edits are plain
text: Git and a text editor are enough.** Python is used for the instructor's
runnable demonstration; it is optional for your documentation exercise.

## Before class: get an ordinary project folder

Download and extract the current `student-pack.zip` into a new personal folder,
for example `Documents/dcm-week3`. Use your file manager; work in the extracted
folder, not inside the ZIP. Keep it outside any existing Git repository.
The pack contains `messy-project/` and `live-demo/`, with **no Git history**.
Use the clean `live-demo/` for Git practice; leave the messy specimen alone.
If you already have an older copy, extract to a new location and keep your work.

Complete the course website's VS Code/Git setup, including your commit author
name and email. No Python, GitHub account or network connection is needed for
this local exercise. Do not clone a bundle or set up a remote.

If Git is unavailable, pair with someone whose setup works. Be the reviewer:
read the files, dictate the change, interpret the actual diff and write down the
checks. Finish your own local commit afterwards. Do not spend practical time on
GitHub authentication or an AI account.

## Activity 1: diagnose the messy project (15 minutes)

Open `messy-project/` beside this guide. This is a deliberately broken handover;
**inspect it rather than run it**. The task is to calculate total revenue across
**all four original orders**. The records are synthetic CHF amounts.

1. **4 minutes — inspect.** Identify at least four reproducibility blockers.
   Which files are source, code or generated output? Which roles are uncertain?
   Which path is fragile? What manual step is hidden?
2. **6 minutes — propose.** Sketch a small repaired folder tree and write four
   short README answers: purpose, data, run procedure, expected output. Mark any
   run instruction you have not yet tested as a proposal, not a verified command.
3. **5 minutes — hand over.** Swap with a partner. Can they locate the input and
   entry point? What still prevents a fresh rerun? Leave one question for the author.

Write your plan on paper or in a separate note. No code repair is required.
Deliverable: a diagnosis, a proposed tree, four README answers and one open question.

### Browser/paper fallback: exact specimen contents

`original_orders.csv`:

```csv
order_id,amount_chf
1,10.00
2,15.00
3,12.50
4,12.50
```

`orders.csv`:

```csv
order_id,amount_chf
1,10.00
2,15.00
3,12.50
```

`analysis_final.py`:

```python
# Deliberately fragile handover specimen: inspect rather than run.
import csv

with open('/Users/analyst/Desktop/orders.csv') as source:
    amounts = [float(row['amount_chf']) for row in csv.DictReader(source)]
print(sum(amounts))
```

`summary_final.txt`:

```text
Number of orders: 3
Total revenue (CHF): 37.50
Average order value (CHF): 12.50
```

`report_FINAL.md`:

```markdown
# Orders report — final

We received four orders, with total revenue of CHF 50.00.
Average order value was CHF 12.50.

Numbers copied from the console before sending the folder.
```

`notes.txt`:

```text
Use my cleaned orders.csv. I removed one row in the spreadsheet.
Run analysis_final.py after cleaning. Python is installed on my laptop.
I copied the result into the report. The report is the final version, I think.
```

## Git practice

Use **live-demo/**, the ordinary clean folder you extracted. It supplies a
runnable entry point and a useful README. You are improving its handover, not
repairing the broken specimen.

### Required Git practice: one reviewed improvement (15 minutes)

**Start — 4 min.** In VS Code, choose **File → Open Folder** and select
`live-demo/` itself. Open **Terminal → New Terminal**. Your terminal must
be at the project root, where `README.md`, `data/`, `src/` and `.gitignore` live.
Run one command at a time:

```bash
git init
git status
```

Expected: **no commits yet**, with untracked files. Git created a hidden `.git/`
directory for its metadata; leave it alone. Nothing was uploaded. If status
shows an existing history or unrelated files, stop and check which folder you
opened; do not delete previous work. The default branch name may vary; that is fine.

**Record the project as received in a starting/baseline commit before editing.** Read the README, the raw CSV and
the small source files. The CSV has four rows: 10.00, 15.00, 12.50 and 12.50 CHF.
These are safe synthetic data. `.gitignore` excludes generated outputs.
Here `git add .` stages the non-ignored contents of this extracted project;
check the staged files before committing.
Ordinary `git diff` does not show untracked files: first record the supplied
project so Git has a before-version to compare with your README edit.

```bash
git add .
git diff --staged
```

Inspect the listed files and their contents. Press `q` if Git opens a paged view.
When only the intended starter files are staged, record them:

```bash
git commit -m "Record starting project"
git status
```

Expected: one starting/baseline commit and a clean working tree. If Git asks for your
identity, follow the course setup page; your author name/email are not a GitHub
login. Keep the generated `outputs/` and any private files out of the snapshot.

**Edit — 2 min.** In README, replace the arithmetic TODO under **Expected result** with your
own explanation showing count, total and average. Keep the data and code unchanged.
Save the file.

**Review and record — 6 min.** Run:

```bash
git status
git diff
```

Check that only the intended README paragraph changed. Read additions **and**
deletions. Independently calculate 10.00 + 15.00 + 12.50 + 12.50 and compare it with the README
claim; also check 50.00 / 4 = 12.50. Confirm the raw CSV and documented paths agree with that claim.

If you already have Python, also follow the README and run `python3 src/summarize.py`
then `python3 src/check_summary.py` (or your working `python` / `py` launcher).
The analysis creates the output; the checker independently inspects that saved file.
Without Python, complete the file/claim review now and observe the instructor's
rerun; **do not claim that you personally executed the project**.

Then run these commands individually:

```bash
git add README.md
git diff --staged
git commit -m "Clarify expected output in README"
git status
git log --oneline
```

Check the staged diff before committing. If you edit again after staging, review
and stage the revised README again. Commit records the staged version.

**Explain — 3 min.** Show a partner your changed line, the independent check and
the reviewed change in the log. Expected: clean status and two commits: the
starting/baseline commit and the reviewed README change. Commit IDs differ between students; the message and content matter.

## Command card

| Command | Question/action |
| --- | --- |
| `git init` | Start local version control in this project folder; no commit yet. |
| `git status` | Which files are new, modified or staged? |
| `git diff` | Show unstaged changes to tracked files. |
| `git add README.md` | Select the current README content for the next commit. |
| `git diff --staged` | Show the changes selected for the next commit. |
| `git commit -m "Explain the change"` | Record the selected snapshot locally. |
| `git log --oneline` | Inspect recorded history. |

If Git opens a paged view of a long diff/log, press `q` to return to the prompt.
Students do not need to memorize command options.

This exercise has no remote. Your local reviewed commit
is the required deliverable. The instructor will show how that reviewed history can be shared; remote
commands are not required in your activity.

Git ignores the generated `outputs/` directory in this project. Code, README,
checks and this tiny synthetic CSV are versioned. Large or sensitive data need a
documented access strategy. Ignoring a file does not remove a previously committed
version. Keep credentials out of project history.

## From local history to a shared handover

| Command | Purpose |
| --- | --- |
| `git clone` | Copy an existing repository and history into a new local folder. |
| `git remote -v` | See the connected repository URLs; `origin` is the usual remote name. |
| `git push` | Send recorded commits to the configured remote. Saved/staged edits stay local. |
| `git pull` | Fetch and integrate remote changes into the current branch of an existing clone. |

A new local project starts with `git init`; an existing shared project starts
with `git clone`, which already creates the local repository.

GitHub hosts shared history so another person can read the README, inspect a
commit and its diff, then clone and try a fresh run. Coordinate changes before
pulling; start with a clean working tree. Software and ignored data still need
the README's instructions. Branch and pull-request workflows return later.
No GitHub account, remote setup or push is required for today's student task.

## Before next week

Keep your diagnosis and reviewed commits. Be ready to explain the source data,
entry point, expected output and one diff. If you paired because Git was blocked,
complete your own local commit before the next session. On **8 October** we start
code literacy; you do not need to implement this example in both R and Python.

Reference: [Git diff documentation](https://git-scm.com/docs/git-diff).
