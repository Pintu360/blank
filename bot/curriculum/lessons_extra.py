from __future__ import annotations

from .models import Lesson, q_fill, q_mcq

EXTRA_LESSONS: tuple[Lesson, ...] = (
    Lesson(
        id="a1-06",
        level="A1",
        unit=6,
        title="Days and time — দিন ও সময়",
        minutes=8,
        goals=("say the days", "tell the time with o'clock", "use today / tomorrow"),
        teach=(
            "<b>A1 · Lesson 6 — Days and time</b>\n\n"
            "Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday\n"
            "শনি  রবি  সোম  মঙ্গল  বুধ  বৃহস্পতি  শুক্র\n\n"
            "What time is it? — কয়টা বাজে?\n"
            "It is 7 o'clock. — ৭টা বাজে।\n"
            "in the morning — সকালে\n"
            "in the afternoon — দুপুরে\n"
            "in the evening — সন্ধ্যায়\n"
            "at night — রাতে\n\n"
            "Today is Friday. Tomorrow is Saturday.\n"
            "I sleep at 11 o'clock at night."
        ),
        vocab=(
            ("today", "আজ", "Today is Friday."),
            ("tomorrow", "আগামীকাল", "See you tomorrow."),
            ("morning", "সকাল", "I drink tea in the morning."),
            ("o'clock", "টা বাজে", "It is six o'clock."),
        ),
        questions=(
            q_mcq("“Tomorrow” মানে কী?", ["গতকাল", "আজ", "আগামীকাল"], 2, "tomorrow = আগামীকাল."),
            q_fill("It is 8 ___. (o'clock)", "o'clock|oclock", "o'clock with a number."),
            q_mcq("I drink tea ___ the morning.", ["on", "in", "at"], 1, "in the morning."),
            q_fill("___ is Friday. (Today)", "Today", "Today = আজ."),
        ),
    ),
    Lesson(
        id="a1-07",
        level="A1",
        unit=7,
        title="Places — কোথায়",
        minutes=8,
        goals=("name places in town", "use in / at / to", "ask Where is…?"),
        teach=(
            "<b>A1 · Lesson 7 — Places</b>\n\n"
            "home — বাড়ি    school — স্কুল    college — কলেজ\n"
            "market — বাজার    hospital — হাসপাতাল    mosque — মসজিদ\n"
            "station — স্টেশন    shop — দোকান    park — পার্ক\n\n"
            "I am at home. — আমি বাড়িতে।\n"
            "She is at school.\n"
            "We go to the market.\n"
            "They live in Dhaka.\n\n"
            "Where is the station? — স্টেশন কোথায়?\n"
            "It is near the park."
        ),
        vocab=(
            ("home", "বাড়ি", "I am at home."),
            ("market", "বাজার", "We go to the market."),
            ("near", "কাছে", "The shop is near my house."),
            ("where", "কোথায়", "Where is the hospital?"),
        ),
        questions=(
            q_fill("I am ___ home. (at)", "at", "at home."),
            q_mcq("We go ___ the market.", ["in", "to", "on"], 1, "go to + place."),
            q_mcq("“Where is the station?” মানে", ["স্টেশন কী?", "স্টেশন কোথায়?", "স্টেশন কার?"], 1, "where = কোথায়."),
            q_fill("They live ___ Dhaka. (in)", "in", "in + city."),
        ),
    ),
    Lesson(
        id="a1-08",
        level="A1",
        unit=8,
        title="Can / can't — পারা / না পারা",
        minutes=8,
        goals=("say what you can do", "ask Can you…?", "use please"),
        teach=(
            "<b>A1 · Lesson 8 — Can</b>\n\n"
            "I can swim. — আমি সাঁতার পারি।\n"
            "I can't drive. — আমি গাড়ি চালাতে পারি না।\n"
            "She can speak Bangla and English.\n"
            "Can you help me, please? — দয়া করে সাহায্য করবেন?\n"
            "Yes, I can. / Sorry, I can't.\n\n"
            "can + verb (no 'to')\n"
            "I can cook.  ✓\n"
            "I can to cook.  ✗"
        ),
        vocab=(
            ("can", "পারা", "I can speak English."),
            ("can't", "না পারা", "I can't drive."),
            ("help", "সাহায্য", "Can you help me?"),
            ("please", "দয়া করে", "Sit down, please."),
        ),
        questions=(
            q_fill("I ___ swim. (can)", "can", "can + verb."),
            q_mcq("Correct:", ["I can to cook.", "I can cook.", "I cooking can."], 1, "no 'to' after can."),
            q_mcq("“Can you help me?” মানে", ["আমি সাহায্য করি", "তুমি কি সাহায্য করতে পারো?", "সাহায্য নেই"], 1, "request."),
            q_fill("Sorry, I ___. (can't)", "can't|cannot", "can't = cannot."),
        ),
    ),
    Lesson(
        id="a2-06",
        level="A2",
        unit=6,
        title="Directions — রাস্তা",
        minutes=10,
        goals=("ask for the way", "left / right / straight", "give simple directions"),
        teach=(
            "<b>A2 · Lesson 6 — How do I get there?</b>\n\n"
            "Excuse me, where is the metro station?\n"
            "Go straight. Turn left. Turn right.\n"
            "It's next to the hospital.\n"
            "It's opposite the park.\n"
            "It's between the shop and the mosque.\n"
            "You can't miss it.\n\n"
            "How long does it take? About ten minutes on foot."
        ),
        vocab=(
            ("straight", "সোজা", "Go straight."),
            ("left", "বাম", "Turn left."),
            ("right", "ডান", "Turn right."),
            ("opposite", "উল্টো দিকে", "It's opposite the bank."),
        ),
        questions=(
            q_mcq("Turn ___ at the lights. (not right)", ["up", "left", "under"], 1, "left / right."),
            q_fill("Go ___. (straight)", "straight", "go straight."),
            q_mcq("“Opposite” মানে", ["পাশে", "উল্টো দিকে", "ভেতরে"], 1, "facing."),
            q_fill("It's next ___ the hospital. (to)", "to", "next to."),
        ),
    ),
    Lesson(
        id="b1-06",
        level="B1",
        unit=6,
        title="Job interview English",
        minutes=12,
        goals=("introduce your background", "talk about strengths", "ask one smart question"),
        teach=(
            "<b>B1 · Lesson 6 — Interview</b>\n\n"
            "Tell me about yourself.\n"
            "I recently finished my HSC / degree. I am looking for a role in …\n"
            "My strength is that I learn quickly.\n"
            "I want to improve my spoken English at work.\n\n"
            "Why should we hire you?\n"
            "I am reliable, and I can start this month.\n\n"
            "Do you have any questions?\n"
            "Yes — what does a normal day look like in this team?"
        ),
        vocab=(
            ("strength", "শক্তি / গুণ", "My strength is teamwork."),
            ("reliable", "নির্ভরযোগ্য", "He is a reliable worker."),
            ("role", "পদ / ভূমিকা", "I want a role in sales."),
            ("background", "পটভূমি", "Tell me about your background."),
        ),
        questions=(
            q_mcq("Best opening:", ["I am very genius.", "I recently finished college and I want to work in sales.", "Give job please."], 1, "clear and modest."),
            q_fill("My ___ is that I learn quickly. (strength)", "strength", "strength = গুণ."),
            q_mcq("A smart question:", ["When is lunch only?", "What does a normal day look like?", "You pay dollar?"], 1, "shows interest."),
            q_fill("I can ___ this month. (start)", "start", "I can start."),
        ),
    ),
)
