from __future__ import annotations

from .models import Question, q_fill, q_mcq

PLACEMENT: tuple[Question, ...] = (
    q_mcq("“I ___ a student.”", ["is", "am", "are"], 1, "A1: I am."),
    q_mcq("She ___ from Bangladesh.", ["am", "are", "is"], 2, "A1: She is."),
    q_fill("I ___ rice yesterday. (eat/ate)", "ate", "A2: eat → ate."),
    q_mcq("Did you ___ to the market?", ["went", "go", "gone"], 1, "A2: Did + base verb."),
    q_mcq("I have lived here ___ 2019.", ["for", "since", "ago"], 1, "B1: since + starting point."),
    q_fill("If I had more time, I ___ travel. (would)", "would", "B1: second conditional."),
    q_mcq("Bangla ___ in Bangladesh.", ["is spoken", "speaks", "spoken is"], 0, "B2: present passive."),
    q_mcq("He told me that he ___ tired.", ["is", "was", "were"], 1, "B2: reported speech backshift."),
    q_mcq("Never ___ I seen such rain.", ["I have", "have I", "I had"], 1, "C1: negative inversion."),
    q_fill("There was a ___ in exports. (reduction)", "reduction", "C1: nominalisation."),
    q_mcq("IELTS Task 1 Academic usually needs:", ["a story about your family", "an overview of main trends", "only your opinion"], 1, "IELTS: overview is required."),
    q_mcq("TRUE/FALSE/NOT GIVEN: the passage does not mention X.", ["TRUE", "FALSE", "NOT GIVEN"], 2, "IELTS: no information → NOT GIVEN."),
)

PLACEMENT_LEVELS = ("A1", "A1", "A2", "A2", "B1", "B1", "B2", "B2", "C1", "C1", "IELTS", "IELTS")


def place_from_results(correct_flags: list[bool]) -> str:
    """Highest level where the learner got at least half of that level's items right."""
    buckets: dict[str, list[bool]] = {}
    for flag, level in zip(correct_flags, PLACEMENT_LEVELS):
        buckets.setdefault(level, []).append(flag)

    ranked = ("IELTS", "C1", "B2", "B1", "A2", "A1")
    for level in ranked:
        items = buckets.get(level) or []
        if items and (sum(items) / len(items)) >= 0.5:
            # also require some success on the previous rung, except A1
            if level == "A1":
                return "A1"
            idx = ranked.index(level)
            lower = ranked[idx + 1]
            lower_items = buckets.get(lower) or []
            if lower_items and sum(lower_items) == 0:
                return lower
            return level
    return "A1"
