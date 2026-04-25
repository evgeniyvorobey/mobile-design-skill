# Education Mobile Domain Pack

Use this pack for mobile experiences involving learning, courses, practice, homework, tutoring, classroom support, assessment, scheduling, parent/guardian communication, or educational communities.

This pack provides recommendations, not proof of learning efficacy, assessment validity, legal compliance, accessibility conformance, or child-safety readiness.

## When To Use

- Self-paced learning, course, flashcard, language, tutoring, test prep, or skill-practice apps.
- School, classroom, LMS companion, assignment, grading, attendance, or parent/guardian tools.
- Educational social features, peer review, group discussion, or instructor feedback.
- Any flow involving minors, grades, progress, sensitive learning data, or high-stakes assessment.

## Primary User Jobs

- Know what to do next, why it matters, and how long it will take.
- Learn or practice in focused chunks that fit mobile attention and context.
- Recover from mistakes with feedback that supports understanding, not shame.
- Track progress without confusing activity with mastery.
- Manage deadlines, reminders, assignments, submissions, and feedback.
- Control privacy, identity, guardian/instructor visibility, and notifications.

## Trust And Safety Risks

- Claims of learning improvement without evidence.
- Progress visuals that imply mastery from completion alone.
- Dark-pattern streaks, shame copy, or pressure loops that hurt motivation.
- Inaccessible lessons, captions, quizzes, diagrams, or timed tasks.
- Minors' privacy, consent, classroom visibility, and communication boundaries.
- AI/tutoring feedback that fabricates certainty or gives unsupported answers.
- Assessment flows without recovery, accommodations, or clear submission status.

## Common Mobile Surfaces

- Home/next lesson with task, duration, deadline, progress, and resume state.
- Lesson/player with content, transcript/caption, notes, bookmark, and completion.
- Practice/quiz with question, answer input, hints, feedback, retry, and explanation.
- Assignment/submission with files, rubric, due date, draft, upload, and confirmation.
- Progress dashboard with goals, mastered topics, weak areas, and instructor/guardian views.
- Schedule/reminders with class, session, deadline, time zone, and quiet hours.
- Community/help surface with questions, peer replies, moderation, and instructor escalation.

## Hierarchy Guidance

- Lead with the next meaningful learning action, not total feature inventory.
- Show progress as learning state: attempted, practicing, needs review, mastered, submitted.
- Keep lesson and quiz screens focused; avoid competing promotions or unrelated navigation.
- Put feedback immediately after action and connect it to the concept being learned.
- Use plain explanations before advanced terminology, then let users drill deeper.
- Separate learner view from instructor/guardian/admin view.
- Make deadlines and submission state unmistakable: draft, uploading, submitted, late, returned.

## State And Recovery Requirements

- Empty: no courses, no assignments, no progress, no saved lessons, no class.
- Resume: return users to exact lesson, question, draft, or video timestamp where possible.
- Loading/offline: cache safe learning material when intended; clearly mark sync status.
- Error: preserve answers, notes, uploads, and drafts after network failure.
- Submission: prevent duplicate submissions and show receipt, timestamp, and editable/locked status.
- Timed tasks: provide clear timer semantics, warnings, and accommodation path if applicable.
- Feedback: handle correct, incorrect, partially correct, skipped, overdue, resubmitted, and returned states.
- Recovery: retry, review explanation, ask for help, download, re-upload, extend, or contact instructor.

## Accessibility Notes

- Provide captions, transcripts, alt text, and text equivalents for audio, video, diagrams, and charts.
- Do not rely on color alone for correctness, progress, difficulty, or deadline risk.
- Support Dynamic Type/large text without hiding questions, answers, or feedback.
- Avoid strict timers unless pedagogically or policy required; provide accommodations where relevant.
- Make drag-and-drop, matching, drawing, and media tasks usable without pointer precision.
- Design for cognitive load: short chunks, clear instructions, consistent feedback, and reduced distractions.

## Platform Notes

- Use native notification controls for reminders and avoid pressure-heavy streak alerts by default.
- Respect platform privacy controls for camera, microphone, photos, files, and contacts.
- Support orientation, tablet, split-screen, and keyboard where learning content benefits from space.
- On Android, account for predictive back during quizzes, uploads, and draft submissions.
- On iOS, preserve navigation hierarchy so learners can return without losing work.

## Evidence And Compliance Boundaries

- Do not claim learning outcomes without validated educational evidence.
- Do not infer COPPA, FERPA, GDPR, accessibility-law, or school-policy obligations from this pack.
- Do not treat gamification benchmarks as proof of motivation or retention.
- Assessment validity, grading policy, accommodations, and academic integrity need expert review.
- This pack is not compliance proof; child privacy, accessibility, school policy, and assessment claims need qualified review.
- AI-generated tutoring or feedback needs accuracy, disclosure, escalation, and safety controls.

## Design-Quality Traps

- Streaks and badges replacing clear learning feedback.
- Progress bars that measure time spent instead of understanding.
- Mobile lessons that are just compressed desktop PDFs or slides.
- Timed quizzes with inaccessible controls and no recovery.
- Parent/instructor visibility that surprises learners.
- Empty states that sell courses instead of helping users resume or choose a realistic next step.

## Handoff Checks

- Define lesson, progress, mastery, deadline, submission, grading, and feedback states.
- Specify resume behavior, offline cache, draft persistence, and upload failure recovery.
- Include caption/transcript/alt-text requirements for every media type.
- Document notification categories, quiet hours, learner/guardian/instructor visibility, and privacy.
- Map quiz input types, accessibility alternatives, timer behavior, and accommodation hooks.
- Flag education, privacy, safety, legal, accessibility, and AI-review items when applicable.

## Source Anchors

- W3C WCAG 2.2, W3C mobile accessibility, Apple accessibility, Android mobile UI guidance.
- GOV.UK and NHS service guidance are useful references for plain language, forms, errors, and accessibility.
- Use these as grounding references; learning efficacy and student data rules require product-specific review.
