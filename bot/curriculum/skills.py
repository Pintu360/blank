from __future__ import annotations

from .models import Prompt

WRITING: tuple[Prompt, ...] = (
    Prompt(
        id="w-a1",
        level="A1",
        skill="writing",
        title="About me",
        cue="Write 5–7 sentences. Name, city in Bangladesh, family, food you like, and one daily habit.",
        tips=("Use I am / I have / I like.", "Full stops. Capital letters."),
        minutes=10,
    ),
    Prompt(
        id="w-a2",
        level="A2",
        skill="writing",
        title="Yesterday",
        cue="Write a short paragraph (80–100 words) about yesterday. Where did you go? Who did you see? What did you eat?",
        tips=("Use past simple.", "didn't + base verb for negatives."),
        minutes=12,
    ),
    Prompt(
        id="w-b1",
        level="B1",
        skill="writing",
        title="Your town",
        cue="Describe your town or village (120–150 words). Include transport, food, and one problem. Give your opinion.",
        tips=("Use because / however / for example.", "One idea per sentence is fine."),
        minutes=15,
    ),
    Prompt(
        id="w-b2",
        level="B2",
        skill="writing",
        title="Online class",
        cue="Some people say university classes should be fully online. Do you agree or disagree? Write 180–220 words.",
        tips=("Clear position in the introduction.", "One Bangladesh example."),
        minutes=20,
    ),
    Prompt(
        id="w-c1",
        level="C1",
        skill="writing",
        title="Urban pressure",
        cue="As cities grow, housing and transport come under strain. What problems does this cause, and what measures can governments take? Write 250+ words.",
        tips=("PEEL paragraphs.", "Hedge strong claims.", "A short rebuttal."),
        minutes=25,
    ),
    Prompt(
        id="w-ielts-t1",
        level="IELTS",
        skill="writing",
        title="Task 1 — overview practice",
        cue=(
            "The chart below (imagine it) shows garment vs tea export value from Bangladesh, 2005–2020. "
            "Garments rose sharply and stayed dominant; tea was low and fairly stable, with a small dip around 2010. "
            "Summarise the information by selecting and reporting the main features, and make comparisons where relevant. "
            "Write at least 150 words."
        ),
        tips=("Paraphrase the rubric.", "Overview without tiny numbers.", "Group the data."),
        minutes=20,
    ),
    Prompt(
        id="w-ielts-t2",
        level="IELTS",
        skill="writing",
        title="Task 2 — opinion",
        cue=(
            "In many countries, young people are encouraged to study abroad. "
            "Some argue this benefits both the student and the home country; others say it causes a brain drain. "
            "Discuss both views and give your own opinion. Write at least 250 words. "
            "You may use Bangladesh as a context if it helps."
        ),
        tips=("Answer both views + your opinion.", "Specific examples.", "Check articles and S-V agreement."),
        minutes=40,
    ),
)

SPEAKING: tuple[Prompt, ...] = (
    Prompt(
        id="s-a1",
        level="A1",
        skill="speaking",
        title="Introduce yourself",
        cue="Say: your name, city, one family member, one food you like. Speak or type 4–6 sentences.",
        tips=("Slow and clear.", "I am / I like."),
        minutes=3,
    ),
    Prompt(
        id="s-a2",
        level="A2",
        skill="speaking",
        title="Last weekend",
        cue="What did you do last Friday or Saturday? Talk for about 45 seconds.",
        tips=("Past verbs: went, ate, watched, visited."),
        minutes=3,
    ),
    Prompt(
        id="s-b1",
        level="B1",
        skill="speaking",
        title="Food in Bangladesh",
        cue="Describe a meal you enjoy. When do you eat it? Who cooks it? Why is it special?",
        tips=("Because + reason.", "Don't stop at 'I like it'."),
        minutes=4,
    ),
    Prompt(
        id="s-b2",
        level="B2",
        skill="speaking",
        title="A place you would recommend",
        cue="Recommend a place in Bangladesh to a foreign visitor. Include how to get there and one problem they should expect.",
        tips=("would recommend / you should...", "Be honest as well as proud."),
        minutes=5,
    ),
    Prompt(
        id="s-c1",
        level="C1",
        skill="speaking",
        title="Education and class",
        cue="Does English-medium schooling guarantee a better career in Bangladesh? Speak for 1–2 minutes with a balanced view.",
        tips=("It depends...", "Define 'better career'.", "One counter-argument."),
        minutes=6,
    ),
    Prompt(
        id="s-ielts-p2",
        level="IELTS",
        skill="speaking",
        title="Part 2 cue card",
        cue=(
            "Describe a skill you would like to learn.\n"
            "You should say:\n"
            "• what the skill is\n"
            "• how you would learn it\n"
            "• how it would help you\n"
            "and explain why you have not learned it yet.\n"
            "Talk for 1–2 minutes (type if you cannot send voice)."
        ),
        tips=("1 min plan with 8 words.", "Cover every bullet.", "End with a feeling or plan."),
        minutes=3,
    ),
    Prompt(
        id="s-ielts-p3",
        level="IELTS",
        skill="speaking",
        title="Part 3 follow-up",
        cue=(
            "Some people say schools should teach practical skills (farming, coding, first aid) "
            "instead of so much exam theory. To what extent is that true in your country? "
            "What problems might appear if exams were reduced?"
        ),
        tips=("Compare groups (urban/rural).", "Speculate with might / is likely to.", "Finish with a position."),
        minutes=4,
    ),
)


def writing_for_level(level: str) -> list[Prompt]:
    return [p for p in WRITING if p.level == level]


def speaking_for_level(level: str) -> list[Prompt]:
    return [p for p in SPEAKING if p.level == level]


def ielts_tasks() -> list[Prompt]:
    return [p for p in (*WRITING, *SPEAKING) if p.level == "IELTS"]


def get_prompt(prompt_id: str) -> Prompt | None:
    for item in (*WRITING, *SPEAKING):
        if item.id == prompt_id:
            return item
    return None
