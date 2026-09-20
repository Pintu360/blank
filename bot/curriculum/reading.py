from __future__ import annotations

from .models import Reading, q_mcq, q_tfng

READINGS: tuple[Reading, ...] = (
    Reading(
        id="read-a1",
        level="A1",
        title="Rafi's morning",
        text=(
            "My name is Rafi. I am 19. I live in Dhaka with my parents and my sister. "
            "I wake up at six. I drink tea and eat ruti. Then I go to college by bus. "
            "The bus is slow, but it is cheap. In the evening I study English for 20 minutes."
        ),
        questions=(
            q_mcq("How old is Rafi?", ["16", "19", "29"], 1, "I am 19."),
            q_mcq("He goes to college by...", ["rickshaw", "bus", "plane"], 1, "by bus."),
            q_mcq("In the evening he...", ["plays cricket only", "studies English", "sleeps at 5"], 1, "He studies English."),
        ),
    ),
    Reading(
        id="read-a2",
        level="A2",
        title="A trip to Sylhet",
        text=(
            "Last month Nabila went to Sylhet with her family. They travelled by train. "
            "The journey took about seven hours. They visited a tea garden and walked in the rain. "
            "Nabila bought green tea for her teacher. She didn't like the long queue at the station, "
            "but she loved the hills."
        ),
        questions=(
            q_mcq("How did they travel?", ["by plane", "by train", "by boat"], 1, "by train."),
            q_mcq("What did she buy?", ["cakes", "green tea", "tickets for next year"], 1, "green tea."),
            q_mcq("She loved...", ["the queue", "the hills", "the seven-hour wait only"], 1, "she loved the hills."),
        ),
    ),
    Reading(
        id="read-b1",
        level="B1",
        title="Why the metro matters",
        text=(
            "Dhaka's traffic has been a daily struggle for office workers and students. "
            "The MRT Line 6 has not removed congestion, but it has given thousands of people "
            "a more predictable journey. Many riders say they can now plan a 9 a.m. class. "
            "However, tickets are still expensive for some low-income workers, and feeder buses "
            "do not always connect well with stations. Experts argue that one line is only a start."
        ),
        questions=(
            q_mcq("The metro has...", ["ended all traffic", "helped some people plan their day", "closed the schools"], 1, "more predictable journeys."),
            q_tfng("Every worker can easily afford the tickets.", "FALSE", "The text says tickets are expensive for some."),
            q_tfng("Experts think one metro line solves everything.", "FALSE", "They say it is only a start."),
            q_tfng("The passage names the ticket price in taka.", "NOT GIVEN", "No number is given."),
        ),
    ),
    Reading(
        id="read-b2",
        level="B2",
        title="Remittances and households",
        text=(
            "Money sent home by Bangladeshis working abroad is a pillar of many family budgets. "
            "These remittances pay for food, school fees, and sometimes a brick house to replace "
            "a tin shed. Economists note a second effect: villages with many migrants often have "
            "higher wages for local farm labour, because fewer young people remain. "
            "The picture is not entirely positive. Families can become dependent on a single overseas "
            "salary, and skills learned abroad are not always used when workers return. "
            "Policy debates now focus on cheaper transfer fees and training that matches Gulf demand."
        ),
        questions=(
            q_tfng("Remittances are only spent on luxury cars.", "FALSE", "The text lists food, fees, housing."),
            q_tfng("Some villages see higher local farm wages.", "TRUE", "Fewer young people remain → higher wages."),
            q_tfng("Every returning worker uses new skills at home.", "FALSE", "Skills are not always used."),
            q_tfng("The average monthly remittance is $200.", "NOT GIVEN", "No figure is stated."),
        ),
    ),
    Reading(
        id="read-c1",
        level="C1",
        title="Salinity on the coast",
        text=(
            "In south-west Bangladesh, cyclones and a rising sea do not merely flood fields; they leave "
            "salt behind. Farmers who once harvested two rice crops now struggle to grow one, and many "
            "have switched to shrimp. That shift can raise short-term income, yet it often hardens the "
            "soil and squeezes out landless labourers who used to find seasonal rice work. "
            "Researchers argue that the issue is not 'climate versus development' but sequencing: "
            "embankments without drainage can trap saline water, while early-warning systems save lives "
            "without restoring soil. A durable response would combine mangrove belts, freshwater ponds, "
            "and social protection for households during the years when land is too salty to farm."
        ),
        questions=(
            q_mcq("Shrimp farming is presented as...", ["a perfect long-term solution", "a mixed, sometimes harmful adaptation", "illegal everywhere"], 1, "income vs soil and labour."),
            q_tfng("Embankments always solve salinity.", "FALSE", "Without drainage they can trap salt water."),
            q_tfng("The author rejects any role for social protection.", "FALSE", "It is part of a durable response."),
            q_tfng("The passage quotes a 2024 World Bank dollar figure.", "NOT GIVEN", "No dollar figure appears."),
        ),
    ),
    Reading(
        id="read-ielts",
        level="IELTS",
        title="The quiet power of the Sundarbans",
        text=(
            "The Sundarbans mangrove forest, shared by Bangladesh and India, is often described as a "
            "wildlife sanctuary. That label is accurate but incomplete. The dense roots trap sediment "
            "and reduce the height of storm surges that roll in from the Bay of Bengal, which is why "
            "coastal planners treat the forest as infrastructure, not scenery. Satellite studies have "
            "shown patches of thinning, linked to salinity, cyclones, and human pressure. "
            "Restoration projects that plant a single fast-growing species have underperformed compared "
            "with mixed, locally nursery-grown mangroves. Meanwhile, honey collectors and fishers still "
            "depend on the forest, so conservation that simply fences people out tends to fail. "
            "The more successful programmes combine patrols with alternative income, such as tourism "
            "cooperatives that are actually owned by nearby villages rather than distant operators."
        ),
        questions=(
            q_tfng("The forest only matters because of tigers.", "FALSE", "It is also treated as infrastructure."),
            q_tfng("Single-species planting has been the most successful method.", "FALSE", "Mixed local mangroves did better."),
            q_tfng("Excluding local people always protects the forest.", "FALSE", "Fencing people out tends to fail."),
            q_tfng("Village-owned tourism cooperatives are mentioned as a better model.", "TRUE", "Last sentence."),
            q_tfng("The passage states the exact square-kilometre area of the forest.", "NOT GIVEN", "No area figure."),
        ),
    ),
)


def readings_for_level(level: str) -> list[Reading]:
    return [item for item in READINGS if item.level == level]


def get_reading(reading_id: str) -> Reading | None:
    for item in READINGS:
        if item.id == reading_id:
            return item
    return None
