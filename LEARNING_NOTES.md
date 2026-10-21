# CivicProof learning notes

Date: 2026-10-21. Status: Lessons 1-2 prepared; learner understanding not yet assessed. The learner requested progression to Lesson 2; Lesson 1 exercise and answers remain unreviewed.

PDF companion: `output/pdf/CivicProof_Phase1_Roadmap_and_Day1_Notes.pdf` (nine pages, version 1.0). Includes the roadmap, code, Windows commands, debugging table, unsolved exercise and knowledge-check worksheet. Exporting the notes does not change learner mastery or advance to Lesson 2.

## Day 1, Lesson 1: From a script to a small project

### Intuition and motivation

A module is a Python file that groups related code. An ordinary package is a folder of modules with an `__init__.py` file. A repository holds the code, documentation, and version-control history. These are different things. Separating a startup action from reusable functions makes code easier to locate, import, and later test.

### Concepts introduced

- The terminal's working directory is the folder commands start from.
- `python` runs the interpreter selected by the terminal's command lookup. Check `python --version` first. On this laptop it selects Python 3.12.10. The Windows launcher `py -3.12` normally requests a version, but currently selects a stale Store registration and fails before our program starts. An explicit executable path avoids that lookup ambiguity.
- `-m civicproof` asks Python to locate the package and run its `__main__.py` module.
- `def main():` defines a function; `main()` calls it. The name `main` is a convention, not a special Python keyword.
- `from civicproof.cli import main` makes the function available under the local name `main`. Importing a module executes its top-level statements, but defining a function does not execute its body.
- `__init__.py` identifies our ordinary package. Python also has namespace packages without it; those are outside this lesson.
- `__main__.py` is the package entry point used by `-m`.
- `__name__` is assigned by Python. The guard `if __name__ == "__main__":` calls the startup function when this module runs as the entry point, while importing it does not call the function.
- Triple-quoted text at the top of these files is a module docstring: an explanation available to tools and readers.
- `.gitignore` tells Git which untracked paths to ignore. It does not remove files already tracked or protect secrets by itself. A Git commit is a recorded snapshot with a message; simply having a `.git` directory does not mean a commit exists.

### Execution path

```text
PowerShell in the repository root
    -> python -m civicproof (verified Python 3.12)
    -> package initialization and __main__.py
    -> import the function from cli.py
    -> main()
    -> two printed lines
```

### Manual checks

Run the package and compare the exact output with README.md. Importing `civicproof.cli` should produce no startup output. This checks the starter's behavior; it is not an automated PDF test suite. No test files are needed for a two-line startup message.

### Debugging practice

- `No module named civicproof`: inspect `Get-Location` and `Get-ChildItem`; run from the repository root containing `civicproof/`.
- `No module named civicproof.__main__`: inspect whether `__main__.py` exists and is spelled with two underscores on each side.
- `can't open file ...`: distinguish a filesystem path from the dotted module name used with `-m`.
- `IndentationError`: check spaces under `def` and `if`; use four spaces consistently.
- No startup output: check whether the function was called rather than only defined or imported.
- Launcher error 0x80070002 naming a WindowsApps executable: interpreter startup failed before project code ran. Inspect `Get-Command python,py`, check `python --version`, and use the verified interpreter. Rewriting `cli.py` cannot repair a missing launcher target.

### Independent exercise, not implemented by the assistant

Create `civicproof/status.py`. Define `phase_message()` returning `Phase 1: foundations before AI`. Import it into `cli.py` and use its return value for the second printed line. Keep the first line unchanged. Importing either module should remain quiet. Run the package from the repository root.

Hints: `return` gives a value to the caller; `print` displays a value. Follow the existing `from ... import ...` pattern, adapting the module and function names. Do not copy the entire startup code into the new file.

### Interview explanation

The package separates the command entry point from application behavior. This makes future behavior reusable without starting the command during imports. For a tiny program a single file is reasonable; separate modules earn their place by holding a coherent responsibility. Avoid splitting every function into its own file.

### Pending knowledge check

1. Which part of this project is the repository, which is the package, and which files are modules?
2. Trace `python -m civicproof` to the printed lines. What does `-m` do, and why check the Python version first?
3. Why does importing `main` not print the startup message? What would happen if a `print()` call were placed at the top level of `cli.py`?
4. Why can running the same command from a different folder fail? How would you inspect the cause?
5. In the exercise, why should `phase_message()` return a string instead of printing it?

### Progression

The learner explicitly requested the next lesson. Continue with virtual environments and dependency basics below; this does not establish mastery of Lesson 1.

## Day 1, Lesson 2: Virtual environments and dependencies

### 1. Intuition

Each project needs its own toolbox. A virtual environment gives CivicProof a project-local place for its Python packages, so installing a tool here does not normally change another project's tools.

### 2. Engineering motivation

Projects may require different versions of the same dependency. A dependency is software a program relies on. Global package installations make those requirements harder to control. Explicitly selecting the interpreter also prevents pip installations from going to one Python while the application runs under another.

### 3. Prerequisites

- The Python interpreter executes Python code. Its actual path can be inspected with `sys.executable` from the standard-library `sys` module.
- The standard library ships with Python; `sys`, `pathlib` and `venv` are examples. Third-party packages, such as the Pydantic we will learn later, are installed separately.
- pip is a package installer. `python -m pip` runs pip through that particular Python interpreter.
- A virtual environment has its own Python executable path and package directory, while using resources from its base Python installation. It is not a copied operating system or an input-security sandbox.
- PowerShell's `.` means the current folder; `.\` begins a relative filesystem path. `-r requirements.txt` tells pip to read requirement lines from that file.
- Activation adjusts command lookup for the current terminal. Directly invoking the environment's interpreter does not require activation.

### 4. Architecture

```text
Verified base Python 3.12
    -> python -m venv .venv (create once per checkout)
    -> .venv/Scripts/python.exe
        -> -m pip ... manages this environment's packages
        -> -m civicproof runs the application

requirements.txt -> intended application dependency list
.gitignore      -> keeps the machine-specific environment out of Git
```

### 5. Implementation

Created `.venv` using the actual installed Python 3.12.10 executable. Added `requirements.txt` with comments only; no third-party package is needed for the starter. `.gitignore` already excludes `.venv/`. The generated environment is not hand-written application code and should be recreated on another machine rather than copied.

Do not introduce package pins for packages that have not been selected or tested. Dependency pins and transitive dependency management will be taught with the first real installation. Bundled artifact-authoring libraries are separate from CivicProof's runtime dependencies.

### 6. Execution

From the repository root, use `.\.venv\Scripts\python.exe` for every interpreter command. Check `--version`, inspect `sys.executable`, compare `sys.prefix` with `sys.base_prefix`, inspect pip, install the currently empty requirements list, run pip's dependency consistency check, and run the application. README.md contains exact PowerShell commands.

The prefix comparison `sys.prefix != sys.base_prefix` should be True. A pip list may initially show only pip. Its version depends on the base interpreter's bundled installation tools. Installing this empty requirements file adds no application package. The `--no-index` option prevents looking for packages in an index; future actual package installations will deliberately use an appropriate source.

Optional activation is `.\.venv\Scripts\Activate.ps1`; `deactivate` restores the current terminal's command lookup. If activation is blocked, use the explicit executable without changing execution policy.

### 7. Testing

Use real interpreter and application behavior checks for this setup. `pip check` validates installed package dependency consistency, not application correctness. The environment identity should be local, global site packages should be excluded, the existing startup should still work, and `git check-ignore` should show that `.venv` is ignored. No pytest suite exists yet and no test file is needed to mirror these setup commands.

### 8. Debugging

- Missing `.venv\Scripts\python.exe`: inspect the working directory and whether creation succeeded.
- Wrong interpreter path: use the explicit environment executable and select that interpreter in the editor.
- Activate.ps1 blocked: use the explicit interpreter; activation is optional.
- Module not found after installing a future dependency: compare the interpreter used for pip with the interpreter running the app.
- No change after installing today's requirements: expected; the file contains comments only.
- Reopening the terminal loses activation: expected; activation belongs to one terminal session.

### 9. Independent exercise

Without installing a package, print the executable path for the base Python and the project environment. Predict whether each has different `sys.prefix` and `sys.base_prefix`, then check. Explain which interpreter should receive CivicProof packages and why `.venv` should not be committed.

Hints: reuse the standard-library `sys` module. The base installation and environment have different executable paths. Compare prefixes inside each interpreter rather than assuming a prompt decoration proves isolation.

### 10. Interview understanding

Explain that each project gets a separate package installation location, commands select the intended interpreter explicitly, and dependencies are recorded for rebuilding. The trade-off is an extra local environment to manage. A venv is not a portable deployment bundle or a security sandbox; interpreter versions and native tools still matter.

### 11. Pending knowledge check

1. Which problem does a virtual environment solve if two projects require different library versions?
2. What is the difference between creating an environment and activating it?
3. Why use the environment's `python.exe -m pip` instead of an unqualified `pip` command?
4. What does a requirements file record, and why is ours currently comments only?
5. What should Git track: `.venv`, `requirements.txt`, both or neither? Explain your reasoning.

### Next lesson, gated on learner readiness

Git snapshots, reviewing changes and making the first checkpoint commit. Do not advance until the learner requests progression.

## Git and pull-request explanation requested by the learner

The learner requested a beginner explanation of the PR commands and a reusable workflow. This is authorized Git instruction; understanding has not yet been assessed.

### Core model

Git records project history locally. GitHub hosts a remote repository. GitHub CLI (`gh`) manages GitHub features such as pull requests. Editing, staging, committing, pushing and merging are separate operations.

```text
Working files -> git add -> staged snapshot -> git commit -> local history
    -> git push -> branch on GitHub -> pull request -> review -> merge
```

A branch is a named line of work, not a second physical project folder. `main` is a conventional default-branch name. `origin` is a conventional nickname for a remote URL. `codex/project-foundation` is the chosen branch name. Neither origin nor main is a special Git keyword.

### Commands explained

- `git status`: inspect the current branch and staged/unstaged/untracked changes.
- `git commit --allow-empty -m "chore: initialize repository"`: record an empty baseline. This was one-time setup for the initially empty CivicProof repository, not a routine command for every project or PR. `-m` supplies a message.
- `git switch -c codex/project-foundation`: create a branch from the current commit and switch to it. Without `-c`, switch to an existing branch.
- `git add FILES`: stage the current versions of selected files. Editing again does not automatically update the staged versions. Nothing is uploaded.
- `git diff`: inspect unstaged changes to tracked files. Untracked file content is not shown here.
- `git diff --cached --stat`: summarize staged changes. `--staged` is a synonym for `--cached`; omitting `--stat` shows the actual diff.
- `git commit -m "MESSAGE"`: record the staged snapshot in local history. A commit does not upload changes or run tests by itself.
- `git push -u origin BRANCH`: upload the branch's commits to the remote called origin and establish upstream tracking. Later pushes can usually use `git push`.
- `gh pr create --base main --head BRANCH --title "TITLE" --body "DESCRIPTION"`: create a GitHub proposal to merge the head branch into the base branch. This creates a PR; it does not merge it.

### Reusable workflow for an established repository

Begin the next task only after existing work is committed or otherwise intentionally handled. Inspect `git status`; switch to the actual default branch and update it using `git pull --ff-only`. Create a new feature branch. Edit and test the work. Inspect changes, stage the intended files, inspect the staged diff, commit, push and create the PR. `--ff-only` refuses to combine divergent histories automatically; investigate if it fails. Replace example branch names and file paths with actual project values.

Repository creation or cloning and remote setup happen before this routine workflow. Do not rerun the empty-baseline setup for an existing project. A pull request can receive more commits after it is opened; pushes to its head branch update the PR. Merging remains a separate step.

### Current observed checkpoint

The initial commit `64b694b` exists. The learner is on `codex/project-foundation` and has staged the project files. The project foundation has not yet been committed in the observed checkout. The mentor only inspected Git state and updated these notes; no commit, push, PR creation or merge was performed by the mentor.

Because these notes and PROGRESS.md were updated after the learner staged them, stage their latest versions again before the foundation commit. This demonstrates that the staging area holds a selected snapshot, not a live link to later edits.

### Practice and understanding checks

Read `git status`, `git diff` and `git diff --staged --stat`. Explain what is staged and what is still unstaged before changing Git state. Describe the difference between add/commit/push, identify base and head branches, and explain why a PR does not immediately change main. Read the full staged diff and run appropriate application checks before committing. Answers are pending.

### First PR troubleshooting: pager and authentication

The `(END)` screen is a pager: a viewer for command output. Press `q` while inside it to return to PowerShell. `git --no-pager diff --cached --stat` prints the summary without entering that viewer. A pager display is not a commit result; check actual history to see which commands completed.

Reinspection confirmed that the project files are still staged, the feature branch points to the initial commit, and only main exists on GitHub. The pending foundation commit and feature-branch push must be completed before creating the PR.

HTTP 401 from `gh pr create` indicates GitHub CLI authentication failed. `gh auth status --hostname github.com` identified an invalid stored token. Reauthenticate through the interactive browser flow using `gh auth login --hostname github.com --web`, then check auth status again. Git's successful push and GitHub CLI authentication are separate mechanisms; success with one does not establish the other is configured correctly.

LF/CRLF warnings describe Unix/Windows line-ending conversion. These warnings did not cause the observed PR failure. No line-ending configuration change is required to resolve the pager or invalid credentials.
