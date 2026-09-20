from __future__ import annotations

from dataclasses import dataclass

from .models import Question, q_fill, q_mcq


@dataclass(frozen=True)
class GrammarRule:
    id: str
    title: str
    title_bn: str
    body: str
    questions: tuple[Question, ...]


BASIC_RULES: tuple[GrammarRule, ...] = (
    GrammarRule(
        id="be",
        title="I am / You are / He is",
        title_bn="আমি / তুমি / সে",
        body=(
            "<b>be</b> — am / is / are\n\n"
            "I <b>am</b> a student.  →  I'm a student.\n"
            "You <b>are</b> kind.  →  You're kind.\n"
            "He / She / It <b>is</b> from Dhaka.\n"
            "We / They <b>are</b> at home.\n\n"
            "Question: <b>Are</b> you ready?  <b>Is</b> she a teacher?\n"
            "Negative: I <b>am not</b> late.  She <b>isn't</b> here.\n\n"
            "✗ I is a student.\n"
            "✓ I am a student."
        ),
        questions=(
            q_fill("I ___ from Bangladesh. (am)", "am", "I am."),
            q_mcq("She ___ my sister.", ["am", "is", "are"], 1, "She is."),
            q_fill("They ___ students. (are)", "are", "They are."),
        ),
    ),
    GrammarRule(
        id="a-an",
        title="a / an",
        title_bn="একটা — a না an?",
        body=(
            "<b>a / an</b> = one (একটা)\n\n"
            "<b>a</b> + consonant sound: a book, a mango, a university (yu-)\n"
            "<b>an</b> + vowel sound: an apple, an egg, an hour (our)\n\n"
            "Look at the <i>sound</i>, not only the letter.\n"
            "an hour ✓   a hour ✗\n"
            "a university ✓  (sound = you)"
        ),
        questions=(
            q_fill("I eat ___ egg. (a/an)", "an", "egg starts with a vowel sound."),
            q_mcq("___ mango", ["an", "a", "the a"], 1, "mango → a."),
            q_fill("She is ___ English teacher. (an)", "an", "English → an."),
        ),
    ),
    GrammarRule(
        id="present",
        title="Present simple",
        title_bn="প্রতিদিনের কাজ",
        body=(
            "Use present simple for habits and facts.\n\n"
            "I / You / We / They  +  verb\n"
            "He / She / It  +  verb<b>s</b>\n\n"
            "I work.  She work<b>s</b>.  He go<b>es</b>.  She stud<b>ies</b>.\n\n"
            "Negative: I <b>don't</b> work.  She <b>doesn't</b> work.\n"
            "Question: <b>Do</b> you work?  <b>Does</b> she work?\n\n"
            "Time words: every day, always, usually, never."
        ),
        questions=(
            q_fill("She ___ to college. (goes)", "goes", "She goes."),
            q_mcq("I ___ up at 6.", ["wakes", "wake", "waking"], 1, "I wake."),
            q_fill("He ___ English. (studies)", "studies", "study → studies."),
        ),
    ),
    GrammarRule(
        id="have",
        title="have / has",
        title_bn="আছে",
        body=(
            "I / You / We / They <b>have</b>\n"
            "He / She / It <b>has</b>\n\n"
            "I have two brothers.\n"
            "She has a bicycle.\n\n"
            "Question: Do you have…?  /  Have you got…?\n"
            "Negative: I don't have a car.  She hasn't got time."
        ),
        questions=(
            q_fill("I ___ two sisters. (have)", "have", "I have."),
            q_mcq("She ___ a brother.", ["have", "has", "is"], 1, "She has."),
            q_fill("We ___ a small house. (have)", "have", "We have."),
        ),
    ),
    GrammarRule(
        id="can",
        title="can / can't",
        title_bn="পারা / না পারা",
        body=(
            "<b>can</b> + verb (no <i>to</i>)\n\n"
            "I can swim.  I can't drive.\n"
            "Can you help me, please?\n"
            "Yes, I can.  Sorry, I can't.\n\n"
            "✓ I can cook.\n"
            "✗ I can to cook.\n\n"
            "Use <b>please</b> to be polite."
        ),
        questions=(
            q_fill("I ___ swim. (can)", "can", "can + verb."),
            q_mcq("Correct:", ["I can to cook.", "I can cook.", "I cooking can."], 1, "no to after can."),
            q_fill("Sorry, I ___. (can't)", "can't|cannot", "can't = cannot."),
        ),
    ),
    GrammarRule(
        id="there",
        title="there is / there are",
        title_bn="আছে (জায়গায়)",
        body=(
            "<b>There is</b> + singular: There is a mosque near my house.\n"
            "<b>There are</b> + plural: There are two shops.\n\n"
            "Question: Is there a station?  Are there any eggs?\n"
            "Negative: There isn't any milk.  There aren't many seats.\n\n"
            "Don't say: Have a book on the table.\n"
            "Say: There is a book on the table."
        ),
        questions=(
            q_fill("There ___ a park. (is)", "is", "singular → is."),
            q_mcq("There ___ two buses.", ["is", "are", "am"], 1, "plural → are."),
            q_fill("___ there a hospital? (Is)", "Is", "Is there…?"),
        ),
    ),
    GrammarRule(
        id="past",
        title="Past simple",
        title_bn="গতকাল — past",
        body=(
            "Regular: verb + <b>ed</b>  →  watched, visited, cooked\n"
            "Irregular: go → <b>went</b>, eat → <b>ate</b>, see → <b>saw</b>, "
            "buy → <b>bought</b>\n\n"
            "Question: <b>Did</b> you go?  (Did + base verb)\n"
            "Negative: I <b>didn't</b> go.\n\n"
            "✗ Did you went?\n"
            "✓ Did you go?"
        ),
        questions=(
            q_fill("I ___ TV yesterday. (watched)", "watched", "watch → watched."),
            q_mcq("Did you ___ to the market?", ["went", "go", "gone"], 1, "Did + base."),
            q_fill("I ___ to Sylhet. (went)", "went", "go → went."),
        ),
    ),
    GrammarRule(
        id="some-any",
        title="some / any / much / many",
        title_bn="কিছু / কোনো / কতটা",
        body=(
            "<b>some</b> — positive: I'd like some tea.\n"
            "<b>any</b> — questions & negatives: Have we got any sugar?  We haven't got any.\n\n"
            "Countable (1, 2, 3…): eggs, mangoes → <b>many</b>\n"
            "Uncountable: rice, water, tea → <b>much</b>\n\n"
            "How many bananas?  How much rice?"
        ),
        questions=(
            q_fill("How ___ mangoes? (many)", "many", "countable."),
            q_fill("How ___ water? (much)", "much", "uncountable."),
            q_mcq("We haven't got ___ milk.", ["some", "any", "a lot mango"], 1, "negative → any."),
        ),
    ),
    GrammarRule(
        id="compare",
        title="Comparatives",
        title_bn="তুলনা — bigger / better",
        body=(
            "small → small<b>er</b>    big → bigg<b>er</b>\n"
            "easy → easi<b>er</b>    expensive → <b>more</b> expensive\n"
            "good → <b>better</b>    bad → <b>worse</b>\n\n"
            "Dhaka is bigger <b>than</b> Khulna.\n"
            "The cheapest shop = superlative (সবচেয়ে).\n\n"
            "✗ more bigger\n"
            "✓ bigger"
        ),
        questions=(
            q_fill("Dhaka is bigger ___ Khulna. (than)", "than", "than."),
            q_mcq("good →", ["gooder", "better", "more good"], 1, "better."),
            q_fill("This bag is ___ expensive. (more)", "more", "long adjective."),
        ),
    ),
    GrammarRule(
        id="future",
        title="will / going to",
        title_bn="ভবিষ্যৎ",
        body=(
            "<b>going to</b> = a plan\n"
            "I am going to visit my village next Eid.\n\n"
            "<b>will</b> = a decision now, an offer, or a prediction\n"
            "I'll open the window.\n"
            "I'll help you.\n"
            "I think it will rain.\n\n"
            "tomorrow, next week, later"
        ),
        questions=(
            q_mcq("Already planned:", ["I'll maybe go.", "I'm going to visit my village.", "I visit yesterday."], 1, "going to = plan."),
            q_fill("I think it ___ rain. (will)", "will", "prediction."),
            q_fill("___ help you. (I'll / I will)", "I'll|I will", "offer."),
        ),
    ),
    GrammarRule(
        id="prepositions",
        title="in / on / at",
        title_bn="সময় ও জায়গার ছোট শব্দ",
        body=(
            "<b>at</b> + clock / home / school: at 6 o'clock, at home, at school\n"
            "<b>on</b> + day / date: on Friday, on 21 March\n"
            "<b>in</b> + month / year / city / morning: in June, in 2024, in Dhaka, in the morning\n\n"
            "in the morning / afternoon / evening\n"
            "at night\n\n"
            "go <b>to</b> the market   (movement)"
        ),
        questions=(
            q_fill("I am ___ home. (at)", "at", "at home."),
            q_mcq("We go ___ the market.", ["in", "to", "on"], 1, "go to."),
            q_fill("I drink tea ___ the morning. (in)", "in", "in the morning."),
        ),
    ),
    GrammarRule(
        id="articles-this",
        title="this / that / these / those",
        title_bn="এটা / ওটা",
        body=(
            "<b>this</b> — one thing near you: This is my book.\n"
            "<b>that</b> — one thing far: That is a rickshaw.\n"
            "<b>these</b> — many near: These are my keys.\n"
            "<b>those</b> — many far: Those are my friends.\n\n"
            "this/that + singular    these/those + plural"
        ),
        questions=(
            q_fill("___ is my bag. (This)", "This", "singular near."),
            q_mcq("___ are my books. (near)", ["That", "These", "This"], 1, "plural near → these."),
            q_fill("___ is a station over there. (That)", "That", "far singular."),
        ),
    ),
)


def get_rule(rule_id: str) -> GrammarRule | None:
    for rule in BASIC_RULES:
        if rule.id == rule_id:
            return rule
    return None
