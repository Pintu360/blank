from __future__ import annotations

from .models import VocabItem

VOCAB: tuple[VocabItem, ...] = (
    VocabItem("a1-hello", "A1", "hello", "নমস্কার / হাই", "Hello, I am Rina."),
    VocabItem("a1-please", "A1", "please", "দয়া করে", "Tea, please."),
    VocabItem("a1-thanks", "A1", "thank you", "ধন্যবাদ", "Thank you for your help."),
    VocabItem("a1-water", "A1", "water", "পানি", "I need water."),
    VocabItem("a1-house", "A1", "house", "বাড়ি", "This is my house."),
    VocabItem("a1-school", "A1", "school", "স্কুল", "The school is near the mosque."),
    VocabItem("a1-today", "A1", "today", "আজ", "Today is Friday."),
    VocabItem("a1-friend", "A1", "friend", "বন্ধু", "He is my friend."),
    VocabItem("a1-help", "A1", "help", "সাহায্য", "Can you help me?"),
    VocabItem("a1-market", "A1", "market", "বাজার", "I go to the market."),
    VocabItem("a1-taka", "A1", "taka", "টাকা", "It is fifty taka."),
    VocabItem("a1-family", "A1", "family", "পরিবার", "My family lives in Bogura."),
    VocabItem("a2-yesterday", "A2", "yesterday", "গতকাল", "Yesterday I was busy."),
    VocabItem("a2-tomorrow", "A2", "tomorrow", "আগামীকাল", "See you tomorrow."),
    VocabItem("a2-weather", "A2", "weather", "আবহাওয়া", "The weather is hot."),
    VocabItem("a2-ticket", "A2", "ticket", "টিকিট", "I bought a train ticket."),
    VocabItem("a2-appointment", "A2", "appointment", "অ্যাপয়েন্টমেন্ট", "I have a doctor's appointment."),
    VocabItem("a2-enough", "A2", "enough", "যথেষ্ট", "There is not enough time."),
    VocabItem("a2-queue", "A2", "queue", "লাইন", "Please wait in the queue."),
    VocabItem("a2-hurry", "A2", "hurry", "তাড়া", "Don't hurry — be careful."),
    VocabItem("a2-invite", "A2", "invite", "নিমন্ত্রণ করা", "They invited us to dinner."),
    VocabItem("a2-village", "A2", "village", "গ্রাম", "My grandparents live in a village."),
    VocabItem("a2-bridge", "A2", "bridge", "সেতু", "We crossed the Padma Bridge."),
    VocabItem("a2-flood", "A2", "flood", "বন্যা", "The flood damaged the road."),
    VocabItem("b1-although", "B1", "although", "যদিও", "Although it rained, we went out."),
    VocabItem("b1-improve", "B1", "improve", "উন্নতি করা", "I want to improve my writing."),
    VocabItem("b1-opportunity", "B1", "opportunity", "সুযোগ", "This job is a good opportunity."),
    VocabItem("b1-pollution", "B1", "pollution", "দূষণ", "Air pollution is a problem in Dhaka."),
    VocabItem("b1-reliable", "B1", "reliable", "নির্ভরযোগ্য", "The metro is more reliable than the bus at peak time."),
    VocabItem("b1-afford", "B1", "afford", "সঙ্গতি থাকা", "Many families cannot afford private tutors."),
    VocabItem("b1-deadline", "B1", "deadline", "শেষ তারিখ", "The deadline is Sunday."),
    VocabItem("b1-confident", "B1", "confident", "আত্মবিশ্বাসী", "She feels more confident now."),
    VocabItem("b1-challenge", "B1", "challenge", "চ্যালেঞ্জ", "Speaking is my biggest challenge."),
    VocabItem("b1-community", "B1", "community", "সম্প্রদায়", "The local community organised a clean-up."),
    VocabItem("b2-significant", "B2", "significant", "উল্লেখযোগ্য", "There was a significant rise in exports."),
    VocabItem("b2-consequence", "B2", "consequence", "পরিণতি", "One consequence is higher rents."),
    VocabItem("b2-infrastructure", "B2", "infrastructure", "অবকাঠামো", "The city needs better infrastructure."),
    VocabItem("b2-urbanisation", "B2", "urbanisation", "নগরায়ণ", "Rapid urbanisation strains services."),
    VocabItem("b2-remittance", "B2", "remittance", "রেমিট্যান্স", "Remittances support many households."),
    VocabItem("b2-sustainable", "B2", "sustainable", "টেকসই", "We need sustainable energy."),
    VocabItem("b2-allocate", "B2", "allocate", "বরাদ্দ করা", "The budget allocates funds to health."),
    VocabItem("b2-decline", "B2", "decline", "হ্রাস", "Jute exports declined over the decade."),
    VocabItem("b2-evidence", "B2", "evidence", "প্রমাণ", "There is little evidence for that claim."),
    VocabItem("b2-perspective", "B2", "perspective", "দৃষ্টিভঙ্গি", "From a student's perspective, fees are high."),
    VocabItem("c1-nuanced", "C1", "nuanced", "সূক্ষ্ম তারতম্যপূর্ণ", "She gave a nuanced answer."),
    VocabItem("c1-exacerbate", "C1", "exacerbate", "আরও খারাপ করা", "Heatwaves exacerbate water shortages."),
    VocabItem("c1-mitigate", "C1", "mitigate", "প্রশমন করা", "Mangroves mitigate storm damage."),
    VocabItem("c1-disparity", "C1", "disparity", "বৈষম্য", "There is a rural-urban disparity in healthcare."),
    VocabItem("c1-resilience", "C1", "resilience", "স্থিতিস্থাপকতা", "Coastal communities show remarkable resilience."),
    VocabItem("c1-unprecedented", "C1", "unprecedented", "অভূতপূর্ব", "an unprecedented flood"),
    VocabItem("c1-compulsory", "C1", "compulsory", "বাধ্যতামূলক", "Primary education is compulsory."),
    VocabItem("c1-plausible", "C1", "plausible", "বিশ্বাসযোগ্য", "That explanation is plausible."),
    VocabItem("c1-constraint", "C1", "constraint", "সীমাবদ্ধতা", "Time is the main constraint."),
    VocabItem("c1-rhetoric", "C1", "rhetoric", "অলংকারপূর্ণ বক্তব্য", "The speech was strong on rhetoric, weak on data."),
    VocabItem("ielts-cohesion", "IELTS", "cohesion", "সংযোগ / ধারাবাহিকতা", "Cohesion is a writing criterion."),
    VocabItem("ielts-coherence", "IELTS", "coherence", "অর্থের শৃঙ্খলা", "Coherence means ideas follow logically."),
    VocabItem("ielts-lexical", "IELTS", "lexical resource", "শব্দভাণ্ডার", "Lexical resource includes collocations."),
    VocabItem("ielts-overview", "IELTS", "overview", "সার্বিক চিত্র", "Task 1 needs a clear overview."),
    VocabItem("ielts-paraphrase", "IELTS", "paraphrase", "অন্যভাবে বলা", "Paraphrase the question in your introduction."),
    VocabItem("ielts-fluency", "IELTS", "fluency", "সাবলীলতা", "Fluency is not the same as speed."),
    VocabItem("ielts-band", "IELTS", "band descriptor", "ব্যান্ড বর্ণনা", "Examiners use band descriptors."),
    VocabItem("ielts-cue", "IELTS", "cue card", "পার্ট ২ কার্ড", "Use the cue card as a map, not a script."),
    VocabItem("ielts-task", "IELTS", "task response", "প্রশ্নের উত্তর দেওয়া", "Task response rewards answering every part."),
    VocabItem("ielts-accuracy", "IELTS", "accuracy", "শুদ্ধতা", "Accuracy of grammar still matters at Band 8."),
)


def vocab_for_level(level: str) -> list[VocabItem]:
    return [item for item in VOCAB if item.level == level]


def get_vocab(word_id: str) -> VocabItem | None:
    for item in VOCAB:
        if item.id == word_id:
            return item
    return None
