"""Build the CivicProof Phase 1 / Day 1 notes with the bundled PDF runtime."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Preformatted, Flowable,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output' / 'pdf' / 'CivicProof_Phase1_Roadmap_and_Day1_Notes.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = Path('C:/Windows/Fonts')
for name, file in [('Body', 'calibri.ttf'), ('BodyBold', 'calibrib.ttf'),
                   ('BodyItalic', 'calibrii.ttf'), ('Display', 'georgia.ttf'),
                   ('Mono', 'consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT / file)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic')

INK = colors.HexColor('#17343B')
MUTED = colors.HexColor('#526970')
TEAL = colors.HexColor('#23786F')
PAPER = colors.HexColor('#FCFAF5')
PALE = colors.HexColor('#EAF2EE')
RULE = colors.HexColor('#D8E1DB')
GOLD = colors.HexColor('#B87924')
GOLD_PALE = colors.HexColor('#FBF0DA')
CODE_BG = colors.HexColor('#EEF1F2')
W, H = A4
CW = W - 88

styles = {
    'title': ParagraphStyle('title', fontName='Display', fontSize=25, leading=29,
                            textColor=INK, spaceAfter=11),
    'dek': ParagraphStyle('dek', fontName='Body', fontSize=11.2, leading=15,
                          textColor=MUTED, spaceAfter=13),
    'body': ParagraphStyle('body', fontName='Body', fontSize=11, leading=14.5,
                           textColor=INK, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Body', fontSize=9.5, leading=12.2,
                            textColor=MUTED, spaceAfter=6),
    'label': ParagraphStyle('label', fontName='BodyBold', fontSize=12.8, leading=16,
                            textColor=TEAL, spaceBefore=10, spaceAfter=6),
    'kicker': ParagraphStyle('kicker', fontName='BodyBold', fontSize=9, leading=12,
                             textColor=TEAL, spaceAfter=7),
    'table': ParagraphStyle('table', fontName='Body', fontSize=9.7, leading=12.4,
                            textColor=INK),
    'tableSmall': ParagraphStyle('tableSmall', fontName='Body', fontSize=9.25,
                                 leading=11.5, textColor=INK),
    'th': ParagraphStyle('th', fontName='BodyBold', fontSize=9.6, leading=12.2,
                         textColor=colors.white),
    'code': ParagraphStyle('code', fontName='Mono', fontSize=9, leading=12,
                           textColor=INK, spaceAfter=0),
}

story = []


def p(text, style='body'):
    return Paragraph(text, styles[style])


def add(text, style='body'):
    story.append(p(text, style))


def label(text):
    add(text, 'label')


def bullet(text):
    t = Table([[p('•'), p(text)]], colWidths=[12, CW - 12])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]))
    story.append(t)


def box(title, text, warning=False):
    bg = GOLD_PALE if warning else PALE
    color = GOLD if warning else TEAL
    t = Table([[p(title, 'label')], [p(text)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEBEFORE', (0, 0), (0, -1), 3, color),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 3),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('TOPPADDING', (0, 1), (-1, 1), 1),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
    ]))
    story.extend([t, Spacer(1, 9)])


def code(text, size=9):
    cs = ParagraphStyle('code-local', parent=styles['code'], fontSize=size,
                        leading=size * 1.35)
    lines = text.rstrip().splitlines()
    max_width = max((pdfmetrics.stringWidth(line, 'Mono', size) for line in lines), default=0)
    if max_width > CW - 22:
        raise ValueError(f'Code line too wide ({max_width:.1f}): {max(lines, key=len)}')
    content = Preformatted(text.rstrip(), cs)
    t = Table([[content]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LEFTPADDING', (0, 0), (-1, -1), 11),
        ('RIGHTPADDING', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.extend([t, Spacer(1, 8)])


def table(headers, rows, widths, compact=False):
    style = 'tableSmall' if compact else 'table'
    data = [[p(h, 'th') for h in headers]]
    data += [[p(str(cell), style) for cell in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), INK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6 if not compact else 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6 if not compact else 5),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, RULE),
    ]))
    story.extend([t, Spacer(1, 8)])


def page(kicker, title, dek=None):
    if story:
        story.append(PageBreak())
    add(kicker, 'kicker')
    add(title, 'title')
    if dek:
        add(dek, 'dek')


class AnswerLines(Flowable):
    def __init__(self, count=2):
        super().__init__()
        self.width = CW
        self.height = count * 17
        self.count = count

    def draw(self):
        self.canv.setStrokeColor(RULE)
        self.canv.setLineWidth(0.5)
        for n in range(self.count):
            y = self.height - 10 - n * 17
            self.canv.line(0, y, self.width, y)


# PAGE 1: Purpose and scope.
page('CIVICPROOF / PHASE 1 / STUDY NOTES', 'Evidence before intelligence',
     'Project foundation + Day 1, Lesson 1 | Version 1.0 | 21 October 2026')
add('CivicProof will investigate infrastructure documents using results that can be checked '
    'against the original pages. Phase 1 builds the document and evaluation foundation. '
    '<b>No LLM is introduced in this phase.</b>')
box('The central rule',
    'Every supported extracted field must have verifiable provenance: the correct source '
    'document, page, evidence location and supporting text. Otherwise, mark it unsupported. '
    'Never invent a value to fill a gap.')
label('A concrete example')
add('A tender says: <i>"Supply and lay 1,200 metres of pipeline."</i> The eventual record '
    'should retain 1200, metre, the original wording, the source document identity, page, '
    'bounding box, extraction method and validation state. This is an example, not an '
    'extraction result from a collected tender.')
label('How the pieces connect')
code('PDF -> validate input -> hash and duplicate check\n'
     '    -> extract text + coordinates -> OCR where needed\n'
     '    -> validate records -> check evidence -> store locally\n'
     '    -> compare with reviewed labels -> evaluation report')
table(['Concept group', 'Plain-language purpose'], [
    ('Python engineering', 'Organize, run, inspect, test and maintain the program.'),
    ('Document processing', 'Recover text and locations from digital or scanned pages.'),
    ('Data contracts', 'Define valid records and represent missing information explicitly.'),
    ('Provenance', 'Connect each supported result to its original evidence.'),
    ('Evaluation', 'Compare outputs with reviewed reference answers and count mistakes.'),
], [116, CW-116])
add('<b>Current implementation:</b> a three-file package that prints two startup lines, '
    'plus project documentation. Ingestion, contracts, OCR, storage and scoring are planned.', 'small')
add('<b>Reading map:</b> roadmap (p. 2); architecture and exit gate (p. 3); Lesson 1 (pp. 4-8); '
    'session record and next action (p. 9).', 'small')

# PAGE 2: Full adjustable roadmap.
page('PLAN / FOURTEEN LEARNING CHECKPOINTS', 'A realistic 14-day route',
     'Allow about 1.5-2.5 focused hours per day. Extend a checkpoint when understanding or setup needs time.')
table(['Day', 'Focus', 'Concrete checkpoint'], [
    ('1', 'Modules, packages and imports; then environments and Git basics', 'Run the starter; explain its execution path.'),
    ('2', 'Paths, bytes/text, safe file handling, types, exceptions; first pytest examples', 'Read a local file safely; explain a failing test.'),
    ('3', 'Pydantic, missing values, IDs, dates and schema versions', 'Validate initial project, document and source records.'),
    ('4', 'PDF internals; digital text extraction with PyMuPDF', 'Extract a small multipage digital PDF.'),
    ('5', 'Coordinates, reading order, rotation, spans and table limits', 'Save text with locations; inspect a highlight.'),
    ('6', 'Local Tesseract, OCR routing, uncertain and mixed pages', 'Identify OCR candidates; retain page provenance.'),
    ('7', 'Secure input checks, byte/page limits, SHA-256 and duplicates', 'Reject invalid input; recognize renamed duplicate content.'),
    ('8', 'Timeouts, configuration, logging, failure handling and storage', 'Persist explicit outcomes; diagnose an injected failure.'),
    ('9', 'Observations, candidates, verified claims, inferences and evidence', 'Enforce per-field provenance and source integrity.'),
    ('10', 'Quantities, units, dimensions and conservative normalization', 'Normalize supported units; reject unknown or incompatible cases.'),
    ('11', 'Official tender collection, access/reuse review and dataset splits', 'Document a diverse collection of about 5-10 suitable files.'),
    ('12', 'Annotation guidelines, JSONL, manual review and ambiguity', 'Freeze a reviewed label version; protect held-out examples.'),
    ('13', 'Metric arithmetic, a simple extraction baseline and more tests', 'Produce reproducible scores with explicit denominators.'),
    ('14', 'Integration, regression and failure tests; installation rehearsal', 'Demonstrate the pipeline; audit evidence and limitations.'),
], [32, 235, CW-267], compact=True)
box('Pacing rule', 'A day can contain several small lessons. Advance only after the learner '
    'confirms readiness. Testing starts early; the final days combine and verify the components.')

# PAGE 3: Architecture and acceptance criteria.
page('DESIGN / CURRENT STRUCTURE + PLANNED EXIT GATE', 'Small structure, strict evidence')
code('CivicProof/\n'
     '    .gitignore\n'
     '    README.md\n'
     '    ARCHITECTURE.md\n'
     '    PROGRESS.md\n'
     '    DECISIONS.md\n'
     '    LEARNING_NOTES.md\n'
     '    EVALUATION.md\n'
     '    civicproof/\n'
     '        __init__.py\n'
     '        __main__.py\n'
     '        cli.py', size=8.6)
add('<b>Added later, one responsibility at a time:</b> contracts, ingestion, extraction, '
    'provenance, normalization, storage, evaluation, tests and dataset metadata. '
    'A local command-line pipeline is sufficient; a web backend is unnecessary for Phase 1.', 'small')
label('Acceptance checklist - planned, not completed')
criteria = [
    'Documented installation and execution work on Windows with Python 3.12.',
    'Digital, scanned, mixed, multipage, rotated, empty and table-containing fixtures have tested outcomes.',
    'Hash original bytes with SHA-256; recognize identical content under different filenames.',
    'Handle corrupt, encrypted, unsupported, oversized and timed-out inputs explicitly.',
    'Store versioned, validated records locally; retain originals and explicit missing states.',
    'Every supported extracted field has valid document/page/location/text evidence that actually supports it.',
    'Record official sources, versions, hashes and access/reuse findings for about 5-10 documents.',
    'Version reviewed labels, including positive, missing, ambiguous and OCR-error examples.',
    'Report extraction, normalization, attribution, coverage and unsupported handling reproducibly.',
    'Pass meaningful positive/negative tests; document limitations and reproduce the demonstration.',
]
for n, text in enumerate(criteria, 1):
    add(f'<b>{n:02d}.</b> {text}', 'small')
box('What evidence does and does not establish',
    'A well-shaped citation is not automatically a valid citation. Evidence must support the field. '
    'Proving what a document says does not prove its statement is true in the world. '
    'Never execute instructions found inside documents.')

# PAGE 4: Lesson 1, steps 1-4.
page('DAY 1 / LESSON 1 / STEPS 1-4', 'Modules, packages & imports',
     'Goal: explain how separate Python files become one small, understandable program.')
label('01 / Intuition - a workshop')
add('A function is a tool. A module is a labelled drawer holding related tools. '
    'A package groups related drawers. The repository holds the whole workshop: code, '
    'documentation and version history.')
table(['Term', 'Meaning in this project'], [
    ('Repository', 'The outer CivicProof folder, including its Git history and documents.'),
    ('Module', 'A Python file such as cli.py containing related code.'),
    ('Ordinary package', 'The inner civicproof folder, identified by __init__.py.'),
    ('Working directory', 'The folder from which your terminal command runs.'),
], [115, CW-115])
label('02 / Engineering motivation')
add('Separate coherent responsibilities so you can locate problems, reuse functions and test '
    'behavior without starting the entire application. One file remains reasonable for a '
    'tiny disposable script. Do not split every function into a separate file.')
label('03 / Prerequisites - defining is not calling')
code('def say_hello():\n'
     '    print("Hello")\n'
     '\n'
     'say_hello()')
add('The <b>def</b> statement defines the function. The final line calls it. Only the call '
    'runs its body and prints Hello. An import makes a name available; it does not call '
    'a function merely because the function was imported.')
code('from civicproof.cli import main')
add('Read this as: from the cli module inside civicproof, make the function named main '
    'available here. Importing executes module-level statements; a function body waits for a call.', 'small')
label('04 / Architecture - trace the path')
code('Terminal in the repository root\n'
     '    -> python -m civicproof\n'
     '    -> package initialization + __main__.py\n'
     '    -> import main from cli.py -> main() -> printed output')

# PAGE 5: Implementation.
page('DAY 1 / LESSON 1 / STEP 5', 'Read the three source files',
     'These files exist in the repository. There is no document-processing implementation yet.')
label('civicproof/__init__.py - identify the package')
code((ROOT / 'civicproof' / '__init__.py').read_text(encoding='utf-8'), size=8.5)
add('The triple-quoted text is a <b>module docstring</b>: an explanation for readers and tools. '
    'It prints nothing. Python also supports namespace packages without this file; '
    'that alternative is outside this lesson.', 'small')
label('civicproof/cli.py - define startup behavior')
code((ROOT / 'civicproof' / 'cli.py').read_text(encoding='utf-8'))
add('<b>cli</b> means command-line interface. The function main() takes no arguments. '
    'Calling it displays two lines. It has no explicit return, so Python returns None: '
    'there is no useful result value. The name main is a convention, not a Python keyword.')
label('civicproof/__main__.py - connect command to behavior')
code((ROOT / 'civicproof' / '__main__.py').read_text(encoding='utf-8'), size=8.5)
add('Python uses __main__.py when the package is run with <b>-m</b>. Python supplies '
    '__name__; its value is "__main__" when this module is the entry point. The '
    '<b>entry-point guard</b> calls main() in that situation. Importing this module '
    'does not call main().')
box('Read the distinction carefully',
    '<b>from ... import main</b> makes the function available. <b>main()</b> calls it. '
    'A print() written at the top level of cli.py would run during import; '
    'a print() inside main waits for the function call.')
add('No PDF or user-input handling exists here. We do not need a broad exception handler '
    'around this starter; it could hide useful programming errors.', 'small')

# PAGE 6: Execution and testing.
page('DAY 1 / LESSON 1 / STEPS 6-7', 'Run it, then check behavior')
label('06 / Execution - PowerShell on this laptop')
code("Set-Location -LiteralPath 'C:\\Users\\jains\\OneDrive\\Desktop\\CivicProof'\n"
     'python --version\n'
     'python -m civicproof', size=8.5)
add('<b>Set-Location</b> changes the working directory. Confirm Python 3.12.x first. '
    '<b>-m civicproof</b> asks Python to locate the package by its Python name and '
    'run its __main__.py module.')
label('Expected output')
code('Python 3.12.10\n'
     'CivicProof\n'
     'Phase 1: document evidence and evaluation')
box('Actual environment issue: the launcher',
    'The command py -3.12 selected a stale Microsoft Store executable and failed with '
    '0x80070002 before reaching application code. The python command selected the working '
    'Python 3.12.10 installation. Global launcher settings were not changed.', warning=True)
add('If a future terminal selects the wrong Python, use the verified installed executable. '
    'PowerShell uses <b>&amp;</b> to execute a program at a quoted path:', 'small')
code("& 'C:\\Users\\jains\\AppData\\Local\\Programs\\Python\\Python312\\python.exe' -m civicproof", size=8)
label('07 / Testing - imports should stay quiet')
code('python -c "import civicproof.cli"')
add('<b>-c</b> executes the short quoted Python statement. Expect no output: the prompt '
    'returns without the startup message. This checks that importing the module does '
    'not start the application.')
table(['Check recorded on 21 October 2026', 'Observed result'], [
    ('python --version', 'Python 3.12.10'),
    ('python -m civicproof', 'Expected two startup lines; exit code 0.'),
    ('Import cli and __main__', 'Neither import started the application; exit code 0.'),
    ('python -m compileall -q civicproof', 'No syntax errors reported; exit code 0.'),
], [262, CW-262])
add('These are starter behavior and syntax checks. There is no pytest suite yet, and no '
    'PDF, OCR, provenance or evaluation results have been measured.', 'small')

# PAGE 7: Debugging and exercise.
page('DAY 1 / LESSON 1 / STEPS 8-9', 'Diagnose first. Then practise.')
label('08 / Debugging - identify the earliest failed step')
table(['Symptom', 'Likely cause', 'First investigation'], [
    ('No module named civicproof', 'Python cannot locate the package.', 'Check Get-Location and Get-ChildItem. Does this folder contain civicproof/?'),
    ('Error naming civicproof.__main__', 'The entry-point file is missing or misspelled.', 'Check __main__.py, including both pairs of underscores.'),
    ('IndentationError', 'Code is not indented correctly.', 'Use four spaces under def and if; inspect mixed tabs/spaces.'),
    ('No startup output', 'The function may be defined or imported but never called.', 'Trace whether execution reaches main().'),
    ('Launcher error naming WindowsApps', 'The interpreter failed before project code ran.', 'Check python --version and which executable the terminal selects.'),
], [124, 158, CW-282])
add('If Python cannot launch, editing cli.py cannot repair the missing executable. '
    'First locate the failed layer: terminal command, interpreter, package lookup, import '
    'or function execution.')
code('Get-Location\nGet-ChildItem\nGet-Command python,py')
label('09 / Independent exercise - build one small module')
for text in [
    'Create civicproof/status.py and define a function named phase_message().',
    'Make it return the string "Phase 1: foundations before AI".',
    'Import that function into cli.py and use its returned value for the second printed line.',
    'Keep the first line unchanged. Importing either module should remain quiet.',
]:
    bullet(text)
code('CivicProof\nPhase 1: foundations before AI')
box('Hints before a solution',
    'return gives a value to the caller; print displays a value. Adapt the existing '
    'from ... import ... pattern. Let main() decide what to display. Do not duplicate '
    'all startup code in the new module.')
add('The exercise has not been implemented for you. Try it, run it and keep the first '
    'error message if you get stuck.', 'small')

# PAGE 8: Interview and knowledge worksheet.
page('DAY 1 / LESSON 1 / STEPS 10-11', 'Explain it in your own words',
     'Use this page for active recall. Seeing working code is not the same as understanding it.')
label('10 / Interview understanding')
box('A clear explanation',
    '"I separated the package entry point from startup behavior so other code can import '
    'the function without starting the application. The package can grow around coherent '
    'responsibilities while the initial structure stays easy to follow."')
add('<b>Trade-off:</b> several files introduce navigation and import rules. A tiny disposable '
    'script may be clearer as one file. Here, the separation prepares for reusable '
    'document-processing functions.')
label('11 / Knowledge check - answers pending')
questions = [
    'Which folder is the repository, which is the package, and which files are modules?',
    'Trace python -m civicproof to the printed lines. What does -m do? Why check the Python version first?',
    'Why does importing main not print the message? What changes if print("Starting") is at the top level of cli.py?',
    'Why might the same command fail from another working directory? What would you inspect first?',
    'Why should phase_message() return a string rather than print it?',
]
for n, question in enumerate(questions, 1):
    story.append(KeepTogether([p(f'<b>{n}.</b> {question}'), AnswerLines(2), Spacer(1, 8)]))
add('Write explanations, not memorized definitions. Review your exercise and answers '
    'with the mentor before confirming readiness for the next lesson.', 'small')

# PAGE 9: Session memory.
page('SESSION RECORD / RESUME WITHOUT GUESSING', 'Checkpoint & next action',
     'This document stops after Lesson 1. It does not advance the project to Lesson 2.')
label('Progress / Plans / Problems')
table(['Status', 'Record'], [
    ('Progress', 'Created a runnable three-file package, .gitignore and the six continuity documents. Startup, quiet imports and syntax checks passed.'),
    ('Plans', 'Learner runs the starter, attempts the independent exercise and answers five knowledge questions. Review before moving on.'),
    ('Problems', 'The py -3.12 launcher registration remains stale; documented commands use the working interpreter. Learner understanding is not yet assessed.'),
], [82, CW-82], compact=True)
label('Project memory - what each document is for')
table(['File', 'Purpose'], [
    ('README.md', 'Description, startup instructions and the interpreter fallback.'),
    ('ARCHITECTURE.md', 'Component boundaries, evidence principles and planned acceptance checks.'),
    ('PROGRESS.md', 'Roadmap, actual verification record, pending work and exact next task.'),
    ('DECISIONS.md', 'Design choices and their trade-offs.'),
    ('LEARNING_NOTES.md', 'Concepts introduced, exercise and pending understanding checks.'),
    ('EVALUATION.md', 'Planned dataset, annotation and scoring policy; no measured results yet.'),
], [137, CW-137], compact=True)
add('<b>Remember:</b> .gitignore affects untracked files; it does not protect secrets by itself. '
    'A Git commit records a snapshot and message; none has been created by the assistant. '
    'This repository is under OneDrive: review document storage before collecting real files.', 'small')
label('Suggested checkpoint commit message')
code('chore: initialize CivicProof learning foundation')
box('Your exact next action',
    'Run the starter, attempt the status.py exercise and answer the five questions. '
    'Send your work or the first error you encounter. Only after review and your readiness '
    'confirmation will the next lesson introduce virtual environments and dependencies.')
add('<b>Scope note:</b> the roadmap and acceptance checklist describe future work. No '
    'document pipeline, reviewed tender dataset, scoring report or production-readiness '
    'claim exists yet. This PDF is a study companion to the current project documents.', 'small')


def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, H-7, W, 7, fill=1, stroke=0)
    canvas.setFont('BodyBold', 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(44, H-30, 'CIVICPROOF')
    canvas.setFont('Body', 8)
    canvas.drawRightString(W-44, H-30, 'PHASE 1 / FOUNDATION NOTES')
    canvas.setStrokeColor(RULE)
    canvas.line(44, 39, W-44, 39)
    canvas.setFont('Body', 8)
    canvas.drawString(44, 25, '21 OCT 2026  |  v1.0  |  Lesson 1 only')
    canvas.drawRightString(W-44, 25, f'{doc.page:02d}')
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=44, leftMargin=44,
    topMargin=53, bottomMargin=53, title='CivicProof: Phase 1 Roadmap and Day 1 Study Notes',
    author='CivicProof', subject='Beginner Python project foundations and evidence-first engineering',
    pageCompression=1,
)
doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
print(OUT)
