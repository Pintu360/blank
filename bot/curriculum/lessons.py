from __future__ import annotations

from .models import Lesson, q_fill, q_mcq

LESSONS: tuple[Lesson, ...] = (
    Lesson(
        id="a1-01",
        level="A1",
        unit=1,
        title="Hello — নমস্কার",
        minutes=8,
        goals=("say hello and goodbye", "use I am / you are", "ask someone's name"),
        teach=(
            "<b>A1 · পাঠ ১ — Hello!</b>\n\n"
            "বাংলাদেশে আমরা প্রায় বলি: <i>Assalamu alaikum</i> বা <i>Hi</i>.\n"
            "ইংরেজিতে:\n"
            "• Hello / Hi — নমস্কার / হাই\n"
            "• Good morning — সুপ্রভাত\n"
            "• Goodbye / Bye — বিদায়\n"
            "• Nice to meet you — আপনার সাথে দেখা হয়ে ভালো লাগল\n\n"
            "<b>I am / You are</b>  (<i>আমি / তুমি</i>)\n"
            "I am Rafi. → I'm Rafi.\n"
            "You are a student. → You're a student.\n"
            "He is from Dhaka. → He's from Dhaka.\n"
            "She is a teacher. → She's a teacher.\n\n"
            "<b>Questions</b>\n"
            "What is your name? — তোমার নাম কী?\n"
            "My name is Nabila.\n"
            "Where are you from? — তুমি কোথা থেকে?\n"
            "I am from Bangladesh."
        ),
        vocab=(
            ("hello", "নমস্কার / হাই", "Hello, I am Karim."),
            ("name", "নাম", "My name is Tania."),
            ("from", "থেকে / বাসিন্দা", "I am from Chattogram."),
            ("student", "শিক্ষার্থী", "I am a student."),
        ),
        questions=(
            q_mcq("Choose the greeting.", ["Goodbye", "Hello", "Thanks"], 1, "Hello = নমস্কার / হাই."),
            q_fill("I ___ from Dhaka. (am/is/are)", "am", "I am. He/She is. You/We/They are."),
            q_mcq("“What is your name?” মানে কী?", ["তুমি কেমন আছ?", "তোমার নাম কী?", "তুমি কোথায়?"], 1, "name = নাম."),
            q_fill("She ___ a teacher.", "is", "She/He/It + is."),
        ),
    ),
    Lesson(
        id="a1-02",
        level="A1",
        unit=2,
        title="Numbers and age — সংখ্যা ও বয়স",
        minutes=8,
        goals=("count 1–20", "say your age", "ask How old are you?"),
        teach=(
            "<b>A1 · পাঠ ২ — Numbers</b>\n\n"
            "1 one, 2 two, 3 three, 4 four, 5 five\n"
            "6 six, 7 seven, 8 eight, 9 nine, 10 ten\n"
            "11 eleven, 12 twelve, 13 thirteen, 14 fourteen, 15 fifteen\n"
            "16 sixteen, 17 seventeen, 18 eighteen, 19 nineteen, 20 twenty\n\n"
            "<b>Age — বয়স</b>\n"
            "I am 18 years old. — আমার বয়স ১৮ বছর।\n"
            "How old are you? — তোমার বয়স কত?\n"
            "He is 10. She is 21.\n\n"
            "<b>This / That</b>\n"
            "This is my book. (কাছের জিনিস)\n"
            "That is a rickshaw. (দূরের জিনিস)"
        ),
        vocab=(
            ("years old", "বছর বয়সী", "I am twenty years old."),
            ("how old", "বয়স কত", "How old are you?"),
            ("book", "বই", "This is my English book."),
            ("ten", "দশ", "I have ten taka."),
        ),
        questions=(
            q_mcq("What number is “fifteen”?", ["5", "15", "50"], 1, "fifteen = 15."),
            q_fill("I am 19 years ___.", "old", "years old = বছর বয়সী."),
            q_mcq("How old are you?", ["তোমার নাম কী?", "তুমি কোথা থেকে?", "তোমার বয়স কত?"], 2, "old = বয়স."),
            q_fill("___ is my bag. (This/These)", "This", "This = একবচন, কাছের জিনিস."),
        ),
    ),
    Lesson(
        id="a1-03",
        level="A1",
        unit=3,
        title="Family — পরিবার",
        minutes=8,
        goals=("name family members", "use my / your", "use have"),
        teach=(
            "<b>A1 · পাঠ ৩ — Family</b>\n\n"
            "mother / mum — মা\n"
            "father / dad — বাবা\n"
            "brother — ভাই    sister — বোন\n"
            "parents — বাবা-মা    children — সন্তান\n"
            "grandmother — দাদী / নানী    grandfather — দাদা / নানা\n\n"
            "<b>my / your</b>\n"
            "This is my sister. That is your brother.\n\n"
            "<b>have</b> (আছে)\n"
            "I have two brothers.\n"
            "She has one sister.\n"
            "We have a small house in Khulna."
        ),
        vocab=(
            ("mother", "মা", "My mother is a nurse."),
            ("father", "বাবা", "My father works in Dhaka."),
            ("sister", "বোন", "I have one sister."),
            ("have", "আছে / রাখা", "I have a bicycle."),
        ),
        questions=(
            q_mcq("“Brother” মানে কী?", ["বোন", "ভাই", "চাচা"], 1, "brother = ভাই, sister = বোন."),
            q_fill("I ___ two sisters. (have/has)", "have", "I/You/We/They have. He/She has."),
            q_fill("This is ___ mother. (my)", "my", "my = আমার."),
            q_mcq("She ___ a brother.", ["have", "has", "is"], 1, "She has."),
        ),
    ),
    Lesson(
        id="a1-04",
        level="A1",
        unit=4,
        title="Food and a/an — খাবার",
        minutes=8,
        goals=("use a / an", "talk about food", "say I like / I don't like"),
        teach=(
            "<b>A1 · পাঠ ৪ — Food</b>\n\n"
            "<b>a / an</b>\n"
            "a banana, a mango, a cup of tea\n"
            "an apple, an egg, an orange  (a, e, i, o, u এর আগে <i>an</i>)\n\n"
            "rice — ভাত    fish — মাছ    bread — রুটি\n"
            "tea — চা     water — পানি    fruit — ফল\n\n"
            "I like rice and fish. — আমার ভাত আর মাছ ভালো লাগে।\n"
            "I don't like coffee.\n"
            "Do you like hilsa? Yes, I do. / No, I don't."
        ),
        vocab=(
            ("rice", "ভাত", "We eat rice every day."),
            ("fish", "মাছ", "Hilsa is a famous fish."),
            ("tea", "চা", "I drink tea in the morning."),
            ("like", "পছন্দ করা", "I like mangoes."),
        ),
        questions=(
            q_fill("I eat ___ egg. (a/an)", "an", "egg vowel sound দিয়ে শুরু — an."),
            q_mcq("Choose the correct sentence.", ["I likes tea.", "I like tea.", "I like teas always."], 1, "I like + noun."),
            q_fill("I don't ___ coffee.", "like", "don't like = পছন্দ করি না."),
            q_mcq("“Water” মানে কী?", ["চা", "পানি", "দুধ"], 1, "water = পানি."),
        ),
    ),
    Lesson(
        id="a1-05",
        level="A1",
        unit=5,
        title="Present simple — প্রতিদিনের কাজ",
        minutes=10,
        goals=("talk about daily habits", "use he/she + -s", "tell the time simply"),
        teach=(
            "<b>A1 · পাঠ ৫ — Every day</b>\n\n"
            "I wake up at 6. — আমি ৬টায় ঘুম থেকে উঠি।\n"
            "I go to school / college / work.\n"
            "I eat lunch at 1 o'clock.\n"
            "I study English in the evening.\n\n"
            "<b>He / She + s</b>\n"
            "I work. → He works. She works.\n"
            "I go. → She goes.\n"
            "I study. → He studies.\n\n"
            "On Friday I visit my grandparents.\n"
            "Bangladesh weekend is often Friday and Saturday."
        ),
        vocab=(
            ("wake up", "ঘুম থেকে ওঠা", "I wake up at six."),
            ("study", "পড়াশোনা করা", "I study English every day."),
            ("go", "যাওয়া", "I go to the market."),
            ("evening", "সন্ধ্যা / সন্ধ্যাবেলা", "I read in the evening."),
        ),
        questions=(
            q_fill("She ___ to college. (go/goes)", "goes", "He/She/It + goes."),
            q_mcq("I ___ up at 6.", ["wakes", "wake", "waking"], 1, "I wake up."),
            q_fill("He ___ English. (study/studies)", "studies", "study → studies."),
            q_mcq("“Every day” মানে কী?", ["গতকাল", "প্রতিদিন", "আগামীকাল"], 1, "every day = প্রতিদিন."),
        ),
    ),
    Lesson(
        id="a2-01",
        level="A2",
        unit=1,
        title="Past simple — গতকাল",
        minutes=10,
        goals=("talk about yesterday", "regular -ed verbs", "use did / didn't"),
        teach=(
            "<b>A2 · পাঠ ১ — Yesterday</b>\n\n"
            "Yesterday I watched a cricket match. — গতকাল আমি ক্রিকেট দেখলাম।\n"
            "I visited my aunt in Rajshahi.\n"
            "We cooked biryani.\n\n"
            "watch → watched    visit → visited    cook → cooked\n"
            "play → played      want → wanted\n\n"
            "<b>Questions / negatives</b>\n"
            "Did you go to the market? Yes, I did. / No, I didn't.\n"
            "I didn't play football yesterday.\n"
            "What did you eat? I ate rice and dal."
        ),
        vocab=(
            ("yesterday", "গতকাল", "Yesterday I stayed home."),
            ("watched", "দেখেছিলাম", "I watched TV."),
            ("did", "করেছিলাম / প্রশ্ন-সাহায্যকারী", "Did you study?"),
            ("cooked", "রান্না করেছিলাম", "My mother cooked fish."),
        ),
        questions=(
            q_fill("I ___ TV yesterday. (watch/watched)", "watched", "past simple: verb + ed."),
            q_mcq("Choose the question.", ["You did go?", "Did you go?", "Do you went?"], 1, "Did + subject + base verb."),
            q_fill("I ___ not play. (did)", "did", "didn't = did not."),
            q_mcq("“Yesterday” মানে কী?", ["আজ", "গতকাল", "কালকে আসি"], 1, "yesterday = গতকাল."),
        ),
    ),
    Lesson(
        id="a2-02",
        level="A2",
        unit=2,
        title="Irregular past — অনিয়মিত past",
        minutes=10,
        goals=("learn high-frequency irregular verbs", "tell a short past story"),
        teach=(
            "<b>A2 · পাঠ ২ — Irregular past</b>\n\n"
            "go → went      eat → ate     see → saw\n"
            "have → had     make → made   come → came\n"
            "take → took    buy → bought  do → did\n"
            "write → wrote  read → read   drink → drank\n\n"
            "Last week I went to Cox's Bazar.\n"
            "I ate seafood and I saw the Bay of Bengal.\n"
            "I bought a shirt in the market.\n"
            "I didn't take many photos. I took only five."
        ),
        vocab=(
            ("went", "গেলাম (go-এর past)", "I went to school."),
            ("ate", "খেলাম", "She ate an apple."),
            ("bought", "কিনলাম", "He bought tea."),
            ("saw", "দেখলাম", "We saw a river."),
        ),
        questions=(
            q_fill("I ___ to Sylhet last year. (go/went)", "went", "go → went."),
            q_mcq("buy-এর past কী?", ["buyed", "bought", "buys"], 1, "buy → bought."),
            q_fill("She ___ a letter. (wrote/written)", "wrote", "write → wrote → written (participle)."),
            q_mcq("I ___ seafood.", ["eated", "ate", "eaten"], 1, "eat → ate."),
        ),
    ),
    Lesson(
        id="a2-03",
        level="A2",
        unit=3,
        title="Countable food — some / any",
        minutes=10,
        goals=("use some / any", "much / many", "shop in English"),
        teach=(
            "<b>A2 · পাঠ ৩ — At the market</b>\n\n"
            "Countable: eggs, mangoes, bananas (গণনা যায়)\n"
            "Uncountable: rice, water, tea, money (গণনা হয় না)\n\n"
            "I would like some tea.\n"
            "We haven't got any sugar.\n"
            "How many bananas? How much rice?\n\n"
            "Shopkeeper: Can I help you?\n"
            "You: I'd like half a kilo of lentils, please.\n"
            "How much is it? — এটার দাম কত?"
        ),
        vocab=(
            ("some", "কিছু", "I'd like some water."),
            ("any", "কোনো (প্রশ্ন/নাবোধক)", "We haven't got any milk."),
            ("many", "অনেক (গণনীয়)", "How many eggs?"),
            ("much", "কতটা (অগণনীয়)", "How much rice?"),
        ),
        questions=(
            q_fill("How ___ mangoes? (much/many)", "many", "mangoes countable → many."),
            q_fill("How ___ water? (much/many)", "much", "water uncountable → much."),
            q_mcq("Negative sentence:", ["I haven't got some tea.", "I haven't got any tea.", "I have any tea."], 1, "negatives use any."),
            q_mcq("“How much is it?” মানে কী?", ["এটা কী?", "এটার দাম কত?", "এটা কার?"], 1, "price question."),
        ),
    ),
    Lesson(
        id="a2-04",
        level="A2",
        unit=4,
        title="Comparatives — তুলনা",
        minutes=10,
        goals=("compare two things", "use more / than", "superlatives"),
        teach=(
            "<b>A2 · পাঠ ৪ — Bigger, cheaper, better</b>\n\n"
            "Dhaka is bigger than Khulna.\n"
            "The bus is cheaper than the plane.\n"
            "Today is hotter than yesterday.\n\n"
            "small → smaller    big → bigger    hot → hotter\n"
            "easy → easier      cheap → cheaper\n"
            "good → better      bad → worse     far → farther/further\n"
            "expensive → more expensive\n\n"
            "The Padma is one of the longest rivers in Bangladesh.\n"
            "This shop is the cheapest."
        ),
        vocab=(
            ("bigger", "আরও বড়", "Dhaka is bigger than Barishal."),
            ("cheaper", "সস্তা", "The local bus is cheaper."),
            ("better", "ভালো", "My English is better now."),
            ("than", "চেয়ে", "Tea is cheaper than coffee."),
        ),
        questions=(
            q_fill("Dhaka is bigger ___ Khulna.", "than", "comparative + than."),
            q_mcq("good-এর comparative?", ["gooder", "better", "more good"], 1, "good → better → best."),
            q_fill("This bag is ___ expensive. (more)", "more", "long adjectives: more + adjective."),
            q_mcq("The cheapest মানে", ["সস্তা", "সবচেয়ে সস্তা", "দামি"], 1, "superlative = সবচেয়ে."),
        ),
    ),
    Lesson(
        id="a2-05",
        level="A2",
        unit=5,
        title="Future — will / going to",
        minutes=10,
        goals=("talk about plans", "make offers with will", "use next / tomorrow"),
        teach=(
            "<b>A2 · পাঠ ৫ — Tomorrow</b>\n\n"
            "<b>going to</b> = পরিকল্পনা\n"
            "I am going to visit my village next Eid.\n"
            "She is going to study tonight.\n\n"
            "<b>will</b> = মুহূর্তের সিদ্ধান্ত / অফার / ভবিষ্যদ্বাণী\n"
            "It's hot. I'll open the window.\n"
            "I'll help you with English.\n"
            "I think it will rain this afternoon.\n\n"
            "tomorrow — আগামীকাল    next week — পরের সপ্তাহ"
        ),
        vocab=(
            ("tomorrow", "আগামীকাল", "I will call you tomorrow."),
            ("going to", "করতে যাচ্ছি", "I'm going to cook dinner."),
            ("will", "করব", "I'll send the message."),
            ("next week", "পরের সপ্তাহ", "The exam is next week."),
        ),
        questions=(
            q_mcq("Plan already made:", ["I'll maybe go.", "I'm going to visit my village.", "I visit yesterday."], 1, "going to = plan."),
            q_fill("I think it ___ rain. (will)", "will", "prediction → will."),
            q_fill("___ help you. (I'll)", "I'll|I will", "offer → will."),
            q_mcq("“Tomorrow” মানে কী?", ["গতকাল", "আজ", "আগামীকাল"], 2, "tomorrow = আগামীকাল."),
        ),
    ),
    Lesson(
        id="b1-01",
        level="B1",
        unit=1,
        title="Present perfect vs past",
        minutes=12,
        goals=("use have/has + past participle", "contrast with past simple", "for / since"),
        teach=(
            "<b>B1 · Lesson 1 — Experience</b>\n\n"
            "I have visited Cox's Bazar. (in my life — time not said)\n"
            "I went to Cox's Bazar in 2022. (finished time)\n\n"
            "Have you ever eaten pitha in winter? Yes, I have. / No, never.\n"
            "She has lived in Dhaka for three years.\n"
            "He has worked here since 2021.\n\n"
            "<b>for</b> = period (for two months)\n"
            "<b>since</b> = starting point (since January)\n\n"
            "already / yet / just / ever / never"
        ),
        vocab=(
            ("ever", "কখনো কি", "Have you ever been to Sylhet?"),
            ("never", "কখনো না", "I have never flown."),
            ("since", "থেকে (সময়ের শুরু)", "since 2020"),
            ("already", "ইতিমধ্যে", "I have already finished."),
        ),
        questions=(
            q_mcq("Life experience, no time:", ["I have seen the Sundarbans.", "I saw it yesterday.", "I seeing it."], 0, "present perfect for experience."),
            q_fill("I have lived here ___ 2021. (for/since)", "since", "since + point in time."),
            q_fill("Have you ___ tried kala bhuna?", "ever", "ever in questions."),
            q_mcq("Finished time marker:", ["already", "yesterday", "ever"], 1, "yesterday → past simple."),
        ),
    ),
    Lesson(
        id="b1-02",
        level="B1",
        unit=2,
        title="Conditionals 1 and 2",
        minutes=12,
        goals=("real future conditions", "unreal present conditions", "if / unless"),
        teach=(
            "<b>B1 · Lesson 2 — If...</b>\n\n"
            "<b>First conditional</b> (real / possible)\n"
            "If I study every day, I will pass the exam.\n"
            "If it rains, we will stay home.\n\n"
            "<b>Second conditional</b> (unreal now)\n"
            "If I had more time, I would read more novels.\n"
            "If I were you, I would practise speaking aloud.\n\n"
            "unless = if not\n"
            "Unless you practise, you won't improve."
        ),
        vocab=(
            ("if", "যদি", "If you try, you will improve."),
            ("unless", "না হলে", "Unless it rains, we will go."),
            ("would", "হত", "I would travel more."),
            ("pass", "পাস করা", "I want to pass IELTS."),
        ),
        questions=(
            q_fill("If I study, I ___ pass. (will)", "will", "first conditional: will + verb."),
            q_mcq("Unreal now:", ["If I am rich, I buy a car.", "If I were rich, I would buy a car.", "If I rich, I bought."], 1, "second: past + would."),
            q_fill("If I ___ you, I would start today. (were)", "were", "If I were you — fixed phrase."),
            q_mcq("unless ≈", ["if not", "because", "although"], 0, "unless = if not."),
        ),
    ),
    Lesson(
        id="b1-03",
        level="B1",
        unit=3,
        title="Modals — advice and rules",
        minutes=10,
        goals=("should / must / have to / can / might", "give advice politely"),
        teach=(
            "<b>B1 · Lesson 3 — Advice</b>\n\n"
            "You should keep a vocab notebook.\n"
            "You shouldn't translate every word.\n"
            "You must write your name on the answer sheet. (rule)\n"
            "I have to wake up early for college. (necessity)\n"
            "You don't have to wear a tie. (not necessary)\n"
            "You mustn't cheat in the exam. (prohibition)\n"
            "It might rain later. (possibility)\n"
            "Can I borrow your pen? (permission)"
        ),
        vocab=(
            ("should", "উচিত", "You should review daily."),
            ("must", "অবশ্যই", "You must stop at red lights."),
            ("might", "হতে পারে", "She might be late."),
            ("borrow", "ধার নেওয়া", "Can I borrow this book?"),
        ),
        questions=(
            q_mcq("Friendly advice:", ["You must to study.", "You should study a little every day.", "You might must study."], 1, "should = advice."),
            q_fill("You ___ cheat. (mustn't)", "mustn't|must not", "prohibition."),
            q_mcq("Not necessary:", ["mustn't", "don't have to", "should"], 1, "don't have to ≠ mustn't."),
            q_fill("It ___ rain. (might)", "might", "possibility."),
        ),
    ),
    Lesson(
        id="b1-04",
        level="B1",
        unit=4,
        title="Opinions and linking",
        minutes=12,
        goals=("give opinions", "agree / disagree", "use because / however / for example"),
        teach=(
            "<b>B1 · Lesson 4 — I think...</b>\n\n"
            "In my opinion, online classes help village students.\n"
            "I believe cricket is more popular than football here.\n"
            "I agree with you. / I don't completely agree.\n\n"
            "<b>Linking</b>\n"
            "because — কারণ\n"
            "so — তাই\n"
            "however — তবে / তবেও\n"
            "for example — উদাহরণস্বরূপ\n"
            "although — যদিও\n\n"
            "Traffic in Dhaka is heavy. However, the metro is improving travel."
        ),
        vocab=(
            ("opinion", "মতামত", "In my opinion, reading helps."),
            ("however", "তবে", "It is hard. However, it is useful."),
            ("although", "যদিও", "Although I was tired, I studied."),
            ("agree", "একমত হওয়া", "I agree with her idea."),
        ),
        questions=(
            q_fill("___ my opinion, English is important.", "In", "In my opinion."),
            q_mcq("Contrast linker:", ["because", "however", "so"], 1, "however = contrast."),
            q_fill("I don't ___ agree.", "completely|fully", "polite disagreement."),
            q_mcq("“Although” মানে", ["কারণ", "যদিও", "তাই"], 1, "although = যদিও."),
        ),
    ),
    Lesson(
        id="b1-05",
        level="B1",
        unit=5,
        title="Relative clauses",
        minutes=12,
        goals=("who / which / that / where", "add information smoothly"),
        teach=(
            "<b>B1 · Lesson 5 — Who / which / that</b>\n\n"
            "The woman who teaches us is from Sylhet.\n"
            "The book that I bought is useful.\n"
            "Cox's Bazar is a town which has a very long beach.\n"
            "The college where I study is near the station.\n\n"
            "who → people\n"
            "which → things\n"
            "that → people or things (defining clauses)\n"
            "where → places\n\n"
            "Avoid: The man which... ✗  → The man who..."
        ),
        vocab=(
            ("who", "যিনি (মানুষ)", "the student who won"),
            ("which", "যা (জিনিস)", "the app which I use"),
            ("that", "যা / যে", "the film that we watched"),
            ("where", "যেখানে", "the village where I grew up"),
        ),
        questions=(
            q_fill("The teacher ___ helped me is kind. (who)", "who", "who + people."),
            q_mcq("Place:", ["the shop who I go", "the shop where I go", "the shop which I go him"], 1, "where + place."),
            q_fill("This is the phone ___ I want.", "that|which", "thing → that/which."),
            q_mcq("Wrong:", ["the girl who sings", "the bus which is late", "the man which called"], 2, "man → who."),
        ),
    ),
    Lesson(
        id="b2-01",
        level="B2",
        unit=1,
        title="Passive voice",
        minutes=12,
        goals=("form be + past participle", "omit the agent", "academic tone"),
        teach=(
            "<b>B2 · Lesson 1 — Passive</b>\n\n"
            "People speak Bangla in Bangladesh.\n"
            "→ Bangla is spoken in Bangladesh.\n\n"
            "The government built the metro.\n"
            "→ The metro was built by the government.\n\n"
            "Present: is/are + V3    Past: was/were + V3\n"
            "Present perfect: has/have been + V3\n"
            "Modal: should be + V3\n\n"
            "Use the passive when the action matters more than the doer, "
            "especially in reports and IELTS Task 1."
        ),
        vocab=(
            ("is spoken", "কথিত হয়", "English is spoken worldwide."),
            ("was built", "নির্মিত হয়েছিল", "The bridge was built in 2022."),
            ("by", "দ্বারা", "written by a journalist"),
            ("report", "প্রতিবেদন", "The report was published yesterday."),
        ),
        questions=(
            q_fill("Rice ___ grown in many districts. (is)", "is", "is + grown."),
            q_mcq("Correct passive:", ["The exam was taken by thousands of students.", "The exam taken thousands.", "Thousands was take the exam."], 0, "was + V3 + by."),
            q_fill("The results have ___ published. (been)", "been", "present perfect passive: have been + V3."),
            q_mcq("Best for Task 1:", ["Someone showed an increase.", "An increase was recorded.", "They did increase."], 1, "passive is more academic."),
        ),
    ),
    Lesson(
        id="b2-02",
        level="B2",
        unit=2,
        title="Reported speech",
        minutes=12,
        goals=("backshift tenses", "report questions", "say / tell / ask"),
        teach=(
            "<b>B2 · Lesson 2 — She said that...</b>\n\n"
            "Direct: “I am tired.”\n"
            "Reported: She said (that) she was tired.\n\n"
            "“I will call you.” → He said he would call me.\n"
            "“I have finished.” → She said she had finished.\n"
            "“Do you like tea?” → He asked if I liked tea.\n"
            "“Where do you live?” → She asked where I lived.\n\n"
            "say something    tell someone something\n"
            "He told me to wait. She said goodbye."
        ),
        vocab=(
            ("said", "বলেছিল", "He said he was late."),
            ("told", "জানাল / বলল (কাউকে)", "She told me the news."),
            ("asked", "জিজ্ঞেস করল", "They asked if I could help."),
            ("whether", "কিনা", "I asked whether the bus had left."),
        ),
        questions=(
            q_mcq("“I am busy.” → She said she ___ busy.", ["is", "was", "were"], 1, "backshift am → was."),
            q_fill("He ___ me to wait. (told)", "told", "tell + person."),
            q_mcq("Yes/No question:", ["He asked where I live?", "He asked if I lived nearby.", "He asked that I live."], 1, "if/whether."),
            q_fill("“I will come.” → She said she ___ come.", "would", "will → would."),
        ),
    ),
    Lesson(
        id="b2-03",
        level="B2",
        unit=3,
        title="Academic collocations",
        minutes=12,
        goals=("learn verb-noun pairs", "avoid informal chat in essays", "build band-6+ lexis"),
        teach=(
            "<b>B2 · Lesson 3 — Natural word pairs</b>\n\n"
            "make a decision  (not *do a decision)\n"
            "take responsibility    pay attention\n"
            "reach a conclusion     play a role\n"
            "raise awareness        conduct research\n"
            "pose a threat          meet a need\n"
            "a significant increase    a wide range of\n\n"
            "Weak: People do pollution and it is very bad.\n"
            "Better: Rapid urban growth contributes to air pollution, "
            "which poses a threat to public health."
        ),
        vocab=(
            ("conduct research", "গবেষণা চালানো", "Scientists conduct research on floods."),
            ("play a role", "ভূমিকা রাখা", "Education plays a key role."),
            ("significant", "উল্লেখযোগ্য", "a significant change"),
            ("pose a threat", "হুমকি সৃষ্টি করা", "Cyclones pose a threat."),
        ),
        questions=(
            q_fill("___ a decision (make/do)", "make", "make a decision."),
            q_mcq("Academic:", ["Kids do lots of pollution.", "Industrial waste contributes to river pollution.", "Rivers are yuck."], 1, "precise collocation."),
            q_fill("Education plays a ___ in development.", "role", "play a role."),
            q_mcq("Best pair:", ["do research", "conduct research", "make research"], 1, "conduct research is the standard collocation."),
        ),
    ),
    Lesson(
        id="b2-04",
        level="B2",
        unit=4,
        title="Cohesion — this / these / such",
        minutes=12,
        goals=("refer back clearly", "avoid repetition", "write tighter paragraphs"),
        teach=(
            "<b>B2 · Lesson 4 — Glue between sentences</b>\n\n"
            "Many graduates move to Dhaka. <b>This</b> trend increases pressure on housing.\n"
            "Fees have risen. <b>As a result</b>, some students take part-time jobs.\n"
            "<b>These</b> jobs can delay graduation.\n\n"
            "Useful: this issue / this pattern / such measures / the former / the latter\n\n"
            "Start of paragraph: topic sentence\n"
            "Middle: reason + example from Bangladesh or globally\n"
            "End: small concluding comment, not a new idea"
        ),
        vocab=(
            ("trend", "ধারা", "This trend is likely to continue."),
            ("as a result", "ফলে", "As a result, traffic increased."),
            ("measure", "পদক্ষেপ", "The government introduced new measures."),
            ("latter", "পরেরটি", "Of buses and trains, the latter is faster."),
        ),
        questions=(
            q_mcq("Best reference:", ["Dhaka grows. Dhaka grows housing problem Dhaka.", "Dhaka is growing rapidly. This puts pressure on housing.", "Growing. Housing."], 1, "this refers to the previous idea."),
            q_fill("Fees rose. ___ a result, students work.", "As", "As a result."),
            q_mcq("Cohesion tool:", ["random new topic", "this / these / such", "only emojis"], 1, "referencing words."),
            q_fill("Of tea and coffee, I prefer the ___. (former)", "former", "the former = the first one mentioned."),
        ),
    ),
    Lesson(
        id="b2-05",
        level="B2",
        unit=5,
        title="Agreeing and hedging",
        minutes=12,
        goals=("soften claims", "use may / tend to / it seems", "sound fair in essays"),
        teach=(
            "<b>B2 · Lesson 5 — Don't overclaim</b>\n\n"
            "Too strong: All Bangladeshi students hate online class.\n"
            "Better: Many students find online classes less motivating.\n\n"
            "Hedging: tend to, may, might, appear to, it is likely that, "
            "a growing number of, in some cases\n\n"
            "I partly agree. While smartphones distract learners, they also "
            "provide access to lectures and dictionaries.\n\n"
            "IELTS loves balanced views + a clear position in the introduction and conclusion."
        ),
        vocab=(
            ("tend to", "সাধারণত করে", "Learners tend to avoid speaking."),
            ("likely", "সম্ভাব্য", "It is likely that demand will grow."),
            ("partly", "আংশিকভাবে", "I partly agree with this view."),
            ("access", "প্রবেশাধিকার", "access to quality education"),
        ),
        questions=(
            q_mcq("Hedged:", ["Everyone is lazy.", "Students tend to delay speaking practice.", "Nobody studies."], 1, "tend to softens the claim."),
            q_fill("It is ___ that floods will increase.", "likely", "it is likely that."),
            q_mcq("Balanced view:", ["I agree 100% always.", "I partly agree: X is true, but Y also matters.", "No opinion."], 1, "clear but nuanced."),
            q_fill("A growing ___ of people use mobile data.", "number", "a growing number of."),
        ),
    ),
    Lesson(
        id="c1-01",
        level="C1",
        unit=1,
        title="Inversion and emphasis",
        minutes=12,
        goals=("negative inversion", "cleft sentences", "add punch to speaking/writing"),
        teach=(
            "<b>C1 · Lesson 1 — Emphasis</b>\n\n"
            "Never have I seen such congestion as in central Dhaka.\n"
            "Not only does the monsoon bring rain, it also replenishes rivers.\n"
            "Rarely do candidates plan their Task 2 before writing.\n\n"
            "It is practice that builds fluency. (cleft)\n"
            "What Bangladesh needs is long-term climate finance.\n\n"
            "Use inversion sparingly — one or two times per essay, not every sentence."
        ),
        vocab=(
            ("not only", "শুধু নয়", "Not only is it cheap, it is reliable."),
            ("rarely", "কদাচিৎ", "Rarely do we consider the cost."),
            ("emphasis", "জোর", "Cleft sentences add emphasis."),
            ("replenish", "পুনরায় পূরণ করা", "Rain replenishes the aquifers."),
        ),
        questions=(
            q_mcq("Correct inversion:", ["Never I have seen...", "Never have I seen...", "Never I saw..."], 1, "Never + auxiliary + subject."),
            q_fill("Not only ___ it rain, it flooded the roads. (did)", "did", "Not only did + subject + verb."),
            q_mcq("Cleft:", ["Practice builds fluency.", "It is practice that builds fluency.", "Fluency practice is."], 1, "It is X that..."),
            q_fill("What the city needs ___ more parks. (is)", "is", "What X needs is Y."),
        ),
    ),
    Lesson(
        id="c1-02",
        level="C1",
        unit=2,
        title="Hedging and stance",
        minutes=12,
        goals=("academic stance verbs", "distance from claims", "Band 7+ caution"),
        teach=(
            "<b>C1 · Lesson 2 — Stance</b>\n\n"
            "The data suggest that rural enrolment has risen.\n"
            "This would appear to support investment in community clinics.\n"
            "It is widely argued that remittances underpin household spending.\n"
            "Critics contend that unplanned urbanisation outweighs the gains.\n\n"
            "Boosters (use carefully): clearly, undoubtedly, essential\n"
            "Hedges: arguably, relatively, to some extent, on balance\n\n"
            "On balance, the benefits of female education outweigh the short-term costs."
        ),
        vocab=(
            ("contend", "যুক্তি দেওয়া", "Critics contend that the policy is unfair."),
            ("underpin", "ভিত্তি হিসেবে কাজ করা", "Remittances underpin the economy."),
            ("on balance", "মোটের উপর", "On balance, I support the plan."),
            ("arguably", "যুক্তিসঙ্গতভাবে", "This is arguably the toughest skill."),
        ),
        questions=(
            q_fill("The figures ___ that demand rose. (suggest)", "suggest", "data/figures + suggest."),
            q_mcq("Cautious academic:", ["This proves everyone is wrong.", "This would appear to support the claim.", "I totally know."], 1, "would appear to = hedge."),
            q_fill("___ balance, the policy works.", "On", "On balance."),
            q_mcq("Stance verb:", ["eat", "contend", "sleep"], 1, "contend = argue."),
        ),
    ),
    Lesson(
        id="c1-03",
        level="C1",
        unit=3,
        title="Nominalisation",
        minutes=12,
        goals=("turn verbs into nouns", "pack more idea per sentence", "Task 1/2 tone"),
        teach=(
            "<b>C1 · Lesson 3 — Nouns from verbs</b>\n\n"
            "People pollute the river. → The pollution of the river...\n"
            "The government invested. → Government investment...\n"
            "Students fail because they don't practise.\n"
            "→ Failure often results from insufficient practice.\n\n"
            "Useful endings: -tion, -ment, -ance, -ity, -al\n"
            "reduce → reduction    develop → development\n"
            "refuse → refusal      available → availability\n\n"
            "Don't nominalise everything or your writing becomes heavy."
        ),
        vocab=(
            ("reduction", "হ্রাস", "a reduction in emissions"),
            ("investment", "বিনিয়োগ", "investment in skills"),
            ("availability", "লভ্যতা", "the availability of clean water"),
            ("insufficient", "অপর্যাপ্ত", "insufficient practice"),
        ),
        questions=(
            q_fill("develop → ___", "development", "verb → noun."),
            q_mcq("Nominalised:", ["They reduced smoke.", "There was a reduction in emissions.", "Smoke go down."], 1, "reduction = noun."),
            q_fill("Fail because no practice → Failure results from ___ practice.", "insufficient|inadequate", "more academic."),
            q_mcq("Best in Task 1:", ["People went up the number.", "There was a sharp increase in enrolment.", "Enrolment did going up."], 1, "there was a + noun."),
        ),
    ),
    Lesson(
        id="c1-04",
        level="C1",
        unit=4,
        title="Precise vocabulary",
        minutes=12,
        goals=("replace vague words", "feel vs believe vs argue", "Band 8 lexis"),
        teach=(
            "<b>C1 · Lesson 4 — Stop saying 'very good'</b>\n\n"
            "good idea → a viable / sound / promising approach\n"
            "bad → detrimental, poor, inadequate\n"
            "big problem → an acute / pressing / structural problem\n"
            "people → residents, commuters, graduates, households\n"
            "get better → improve, recover, rebound\n"
            "a lot of → a substantial / considerable number of\n\n"
            "In Bangladesh, saline intrusion is not merely 'a water problem'; "
            "it is a structural threat to coastal agriculture."
        ),
        vocab=(
            ("viable", "বাস্তবসম্মত", "a viable alternative"),
            ("detrimental", "ক্ষতিকর", "detrimental to health"),
            ("pressing", "জরুরি", "a pressing need"),
            ("substantial", "উল্লেখযোগ্য পরিমাণ", "a substantial increase"),
        ),
        questions=(
            q_mcq("Upgrade “very big problem”:", ["huge bad thing", "a pressing structural problem", "problem big very"], 1, "precise adjective + noun."),
            q_fill("harmful → ___ (detrimental)", "detrimental", "academic synonym."),
            q_mcq("People who travel to work:", ["kids", "commuters", "tourists always"], 1, "commuters."),
            q_fill("a ___ number of applicants (substantial)", "substantial|considerable|significant", "avoid 'a lot of' in essays."),
        ),
    ),
    Lesson(
        id="c1-05",
        level="C1",
        unit=5,
        title="Argument architecture",
        minutes=14,
        goals=("PEEL paragraphs", "rebuttals", "a memorable conclusion"),
        teach=(
            "<b>C1 · Lesson 5 — Build an argument</b>\n\n"
            "<b>PEEL</b>\n"
            "Point — one claim\n"
            "Explain — why it is true\n"
            "Example — Bangladesh or global evidence\n"
            "Link — back to the question\n\n"
            "Rebuttal: It is often claimed that English-medium schooling "
            "guarantees mobility. This overlooks the fact that fluency still "
            "depends on daily use, not the medium of instruction alone.\n\n"
            "Conclusion: restate position + one implication, no new data."
        ),
        vocab=(
            ("rebuttal", "খণ্ডন", "A short rebuttal strengthens the essay."),
            ("implication", "প্রভাব / ইঙ্গিত", "The implication is clear."),
            ("overlook", "উপেক্ষা করা", "This overlooks rural schools."),
            ("mobility", "সামাজিক উন্নতি", "education and social mobility"),
        ),
        questions=(
            q_mcq("PEEL 'E' can be:", ["empty praise", "explain + example", "emoji"], 1, "explain and exemplify."),
            q_fill("This ___ the rural picture. (overlooks)", "overlooks", "overlooks = ignores."),
            q_mcq("Conclusion should:", ["add a brand-new argument", "restate + implication", "copy the intro word for word"], 1, "no new main idea."),
            q_fill("A short ___ answers the other side. (rebuttal)", "rebuttal", "rebuttal = counter-argument."),
        ),
    ),
    Lesson(
        id="ielts-01",
        level="IELTS",
        unit=1,
        title="The test map",
        minutes=12,
        goals=("know the four papers", "understand band scores", "plan 12 weeks"),
        teach=(
            "<b>IELTS · Paper map</b>\n\n"
            "Listening 30 min + 10 min transfer (Academic &amp; General similar)\n"
            "Reading 60 min — 40 questions, three passages (Academic is harder)\n"
            "Writing 60 min — Task 1 (20 min) + Task 2 (40 min)\n"
            "Speaking 11–14 min — 3 parts, recorded\n\n"
            "Bands 0–9. Universities in the UK/Australia often want 6.0–7.5 overall, "
            "sometimes with no band below 6.0.\n\n"
            "For many Bangladeshi candidates, Writing Task 2 and Speaking Part 3 "
            "cap the score. Train those weekly.\n\n"
            "Official-style rule: answer the question, not a memorised essay."
        ),
        vocab=(
            ("band", "স্কোর ব্যান্ড", "Her overall band was 7.0."),
            ("academic", "একাডেমিক মডিউল", "He sat Academic IELTS."),
            ("criterion", "মূল্যায়ন মাপকাঠি", "four writing criteria"),
            ("fluency", "সাবলীলতা", "fluency and coherence"),
        ),
        questions=(
            q_mcq("Writing time split:", ["30+30", "20 Task 1 + 40 Task 2", "10+50"], 1, "Task 2 carries more marks."),
            q_fill("Speaking has ___ parts.", "3|three", "three parts."),
            q_mcq("Reading Academic:", ["one short email", "three long passages", "only graphs"], 1, "three passages."),
            q_mcq("Memorised essays:", ["always Band 9", "risk a penalty if off-topic", "required"], 1, "answer THIS question."),
        ),
    ),
    Lesson(
        id="ielts-02",
        level="IELTS",
        unit=2,
        title="Reading strategy",
        minutes=12,
        goals=("skim vs scan", "TFNG traps", "time discipline"),
        teach=(
            "<b>IELTS · Reading</b>\n\n"
            "Skim for the topic of each paragraph (names, dates, contrast words).\n"
            "Scan for numbers, capitals, and keywords from the question.\n\n"
            "<b>TRUE / FALSE / NOT GIVEN</b>\n"
            "TRUE — same meaning as the text\n"
            "FALSE — text says the opposite\n"
            "NOT GIVEN — the text is silent; do not use world knowledge\n\n"
            "Bangladesh example trap: you know Dhaka is crowded, but if the passage "
            "never says so, the answer is NOT GIVEN.\n\n"
            "Aim: Passage 1 in 15 min, 2 in 20, 3 in 25. Never leave blanks."
        ),
        vocab=(
            ("skim", "দ্রুত সার পড়া", "Skim the headings first."),
            ("scan", "খুঁজে বের করা", "Scan for the year 1971."),
            ("trap", "ফাঁদ", "TFNG is full of traps."),
            ("blank", "খালি উত্তর", "Don't leave a blank."),
        ),
        questions=(
            q_mcq("Passage silent on X:", ["TRUE", "FALSE", "NOT GIVEN"], 2, "no information → NG."),
            q_mcq("Opposite of the text:", ["TRUE", "FALSE", "NOT GIVEN"], 1, "contradiction = FALSE."),
            q_fill("___ for capital letters and numbers. (Scan)", "Scan", "scan = search."),
            q_mcq("Time idea:", ["60 min on passage 3 only", "roughly 15/20/25", "2 hours"], 1, "spread the hour."),
        ),
    ),
    Lesson(
        id="ielts-03",
        level="IELTS",
        unit=3,
        title="Writing Task 1 Academic",
        minutes=14,
        goals=("overview is mandatory", "select key data", "compare, don't list"),
        teach=(
            "<b>IELTS · Task 1</b>\n\n"
            "4 paragraphs: intro (paraphrase) → overview → 2 detail paragraphs.\n"
            "Overview: the big picture, no tiny numbers.\n"
            "Details: 5–8 well-chosen figures, grouped, with comparisons.\n\n"
            "Language: increased sharply, remained stable, overtook, "
            "accounted for, the most pronounced change.\n\n"
            "If a chart showed garment exports vs tea from Bangladesh, "
            "do not write every year. Group: overall rise, a dip, a crossing point."
        ),
        vocab=(
            ("overview", "সার্বিক চিত্র", "An overview is required."),
            ("overtake", "ছাড়িয়ে যাওয়া", "Garments overtook jute."),
            ("stable", "স্থিতিশীল", "The figure remained stable."),
            ("pronounced", "স্পষ্ট / প্রকট", "a pronounced decline"),
        ),
        questions=(
            q_mcq("Missing overview:", ["still Band 9", "caps Task Achievement", "doesn't matter"], 1, "no overview = lower TA."),
            q_fill("Don't list every number; ___ key features. (select)", "select", "select and compare."),
            q_mcq("Good overview:", ["In 2001 it was 12.3 and in 2002 12.4...", "Overall, X rose while Y fell.", "I like this chart."], 1, "trends, not raw lists."),
            q_fill("The most ___ change was in 2019. (pronounced)", "pronounced", "pronounced = striking."),
        ),
    ),
    Lesson(
        id="ielts-04",
        level="IELTS",
        unit=4,
        title="Writing Task 2",
        minutes=14,
        goals=("4-paragraph model", "clear position", "specific examples"),
        teach=(
            "<b>IELTS · Task 2</b>\n\n"
            "Intro: paraphrase + thesis (your position).\n"
            "BP1: strongest reason + example.\n"
            "BP2: second reason or the other side + rebuttal.\n"
            "Conclusion: position in fresh words.\n\n"
            "Question types: opinion, discussion, problem-solution, two-part.\n\n"
            "Weak example: 'In our country education is important.'\n"
            "Better: 'When cyclone warnings are issued in coastal Bangladesh, "
            "Bangla-language mobile alerts reach households faster than English bulletins.'\n\n"
            "Target 270–290 words. Leave 3 minutes to check articles and subject-verb agreement."
        ),
        vocab=(
            ("thesis", "মূল অবস্থান", "State a thesis in the introduction."),
            ("rebuttal", "খণ্ডন", "A rebuttal shows control."),
            ("alert", "সতর্কবার্তা", "cyclone alerts"),
            ("household", "পরিবার / গৃহস্থালি", "rural households"),
        ),
        questions=(
            q_mcq("Intro needs:", ["a joke", "paraphrase + position", "your full life story"], 1, "task + thesis."),
            q_fill("Aim about 2___ words. (70-90)", "70-90|70–90|80", "250 minimum; 270–290 is safe."),
            q_mcq("Better support:", ["Education is good.", "A concrete local or researched example.", "Copy a memorised essay."], 1, "specific beats generic."),
            q_mcq("Discussion essay:", ["ignore the other view", "cover both views + your position if asked", "only stories"], 1, "answer every part."),
        ),
    ),
    Lesson(
        id="ielts-05",
        level="IELTS",
        unit=5,
        title="Speaking Parts 1–3",
        minutes=12,
        goals=("extend answers", "Part 2 timing", "Part 3 abstraction"),
        teach=(
            "<b>IELTS · Speaking</b>\n\n"
            "<b>Part 1</b> (home, study, food, weather): 3–4 sentences, not yes/no.\n"
            "Q: Do you like rain?  A: I do, especially the first monsoon shower in June — "
            "the city feels cooler, though the roads flood quickly.\n\n"
            "<b>Part 2</b> cue card: 1 min plan, 1–2 min talk. Structure: what / when / "
            "who / why it matters. Notes: 8 words, not a script.\n\n"
            "<b>Part 3</b>: compare, speculate, evaluate.\n"
            "'It depends...' + two sides + a small conclusion.\n\n"
            "Pronunciation: stress content words. Don't fake a British accent."
        ),
        vocab=(
            ("cue card", "পার্ট ২ কার্ড", "You get one minute with the cue card."),
            ("speculate", "অনুমান করা", "Part 3 asks you to speculate."),
            ("monsoon", "বর্ষা", "the monsoon season"),
            ("extend", "উত্তর বাড়ানো", "Extend with because + example."),
        ),
        questions=(
            q_mcq("Part 1 yes/no only:", ["Band 9", "too short", "required"], 1, "extend answers."),
            q_fill("Part 2 prep time is ___ minute(s).", "1|one", "one minute."),
            q_mcq("Part 3 skill:", ["only childhood stories", "abstract discussion", "read a memorised speech"], 1, "issues and society."),
            q_mcq("Pronunciation goal:", ["copy a film star perfectly", "clear stress and chunking", "speak as fast as possible"], 1, "clarity over accent theatre."),
        ),
    ),
)


def lessons_for_level(level: str) -> list[Lesson]:
    return [lesson for lesson in LESSONS if lesson.level == level]


def get_lesson(lesson_id: str) -> Lesson | None:
    for lesson in LESSONS:
        if lesson.id == lesson_id:
            return lesson
    return None


def next_lesson(level: str, completed_ids: list[str]) -> Lesson | None:
    for lesson in lessons_for_level(level):
        if lesson.id not in completed_ids:
            return lesson
    return None
