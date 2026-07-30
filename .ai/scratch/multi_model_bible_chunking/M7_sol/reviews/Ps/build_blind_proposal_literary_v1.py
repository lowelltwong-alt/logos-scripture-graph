from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
SOURCE = ROOT / "data/processed/bible/eng-web/usfm/extracted/20-PSAeng-web.usfm"
OUT = Path(__file__).with_name("blind_proposal_literary_v1.json")
SHA_OUT = Path(__file__).with_name("blind_proposal_literary_v1.sha256")


# Each tuple is (first verse, last verse, movement title, literary form).
# A complete numbered psalm remains the exact parent alternative for every row.
SPLITS: dict[int, list[tuple[int, int, str, str]]] = {
    18: [
        (1, 3, "Opening love and refuge confession", "hymnic invocation"),
        (4, 19, "Distress, cry, theophany, and rescue", "lament-to-theophany rescue recital"),
        (20, 30, "Vindication and tested way", "testimonial reflection"),
        (31, 45, "Divine arming and victory", "warrior victory recital"),
        (46, 50, "Nations, deliverance, and closing praise", "international thanksgiving coda"),
    ],
    19: [
        (1, 6, "Heavens proclaim through ordered creation", "creation hymn"),
        (7, 11, "Instruction praised in sixfold parallel", "Torah wisdom hymn"),
        (12, 14, "Hidden faults, guarded speech, and closing prayer", "personal cleansing petition"),
    ],
    22: [
        (1, 11, "Abandonment lament and remembered trust", "individual lament address"),
        (12, 21, "Encircling enemies and urgent rescue plea", "enemy lament and petition"),
        (22, 31, "Assembly praise widening to generations and nations", "thanksgiving vow and public hymn"),
    ],
    24: [
        (1, 2, "Earth and world belong to Yahweh", "creator-kingship proclamation"),
        (3, 6, "Entrance question and answer", "liturgical entrance inquiry"),
        (7, 10, "Gates summoned for the King of glory", "antiphonal gate liturgy"),
    ],
    27: [
        (1, 6, "Confidence, desire, and anticipated praise", "trust song"),
        (7, 12, "Hear, seek, do not forsake, and protect", "direct lament petition"),
        (13, 14, "Confidence and waiting exhortation", "trust coda"),
    ],
    31: [
        (1, 8, "Refuge plea and delivered trust", "lament petition with trust"),
        (9, 18, "Distress, reproach, enemies, and rescue plea", "individual complaint and petition"),
        (19, 24, "Stored goodness and communal exhortation", "thanksgiving and exhortation"),
    ],
    33: [
        (1, 3, "Call for skillful new praise", "hymnic summons"),
        (4, 11, "Word, creation, and enduring counsel", "reasons-for-praise recital"),
        (12, 19, "Chosen people, watching king, and saving eye", "corporate beatitude and kingship reflection"),
        (20, 22, "Waiting, rejoicing, and closing appeal", "communal trust response"),
    ],
    35: [
        (1, 10, "Contend, pursue, rescue, and promised praise", "judicial-war petition"),
        (11, 18, "False witnesses, betrayed care, and assembly thanks", "betrayal lament and vow"),
        (19, 28, "Do not let enemies rejoice; vindicate and praise", "renewed petition and praise close"),
    ],
    37: [
        (1, 6, "Do not fret; trust and commit", "alphabetic wisdom exhortation"),
        (7, 11, "Wait, cease anger, and inherit", "alphabetic patience instruction"),
        (12, 22, "Schemes, reversals, and contrasting ends", "alphabetic wicked-righteous contrast"),
        (23, 31, "Established steps and internalized instruction", "alphabetic righteous-way portrait"),
        (32, 40, "Watchful wicked, observed ends, and salvation", "alphabetic concluding contrast"),
    ],
    40: [
        (1, 10, "Rescue testimony, new song, and proclaimed faithfulness", "thanksgiving testimony"),
        (11, 17, "Renewed troubles and urgent help", "individual lament petition"),
    ],
    41: [
        (1, 12, "Blessing, illness lament, betrayal, and sustaining plea", "beatitude-framed individual lament"),
        (13, 13, "Book-closing blessing", "collection doxology"),
    ],
    42: [
        (1, 5, "Thirst, remembered procession, and first self-address refrain", "lament stanza with refrain"),
        (6, 11, "Deep calls, prayer, taunt, and repeated self-address", "lament stanza with repeated refrain"),
    ],
    44: [
        (1, 8, "Ancestral victory recital and present confidence", "community historical recital"),
        (9, 16, "Present rejection, defeat, and reproach", "community reversal lament"),
        (17, 22, "Fidelity protest under affliction", "community innocence protest"),
        (23, 26, "Awake, arise, and redeem", "urgent communal petition"),
    ],
    45: [
        (1, 1, "Poetic prologue", "scribal-poetic self-introduction"),
        (2, 9, "Royal address, throne, and procession", "royal wedding praise"),
        (10, 15, "Bride address and procession", "wedding instruction and processional"),
        (16, 17, "Descendants and perpetual praise", "dynastic and hymnic coda"),
    ],
    46: [
        (1, 3, "Refuge amid cosmic upheaval", "corporate trust stanza"),
        (4, 7, "River, city, nations, and first presence refrain", "Zion trust stanza with refrain"),
        (8, 11, "Come behold, cease, and repeated presence refrain", "victory invitation and refrain"),
    ],
    49: [
        (1, 4, "All peoples summoned to a wisdom riddle", "wisdom proclamation"),
        (5, 12, "Wealth cannot ransom mortal life", "mortality riddle with refrain"),
        (13, 20, "Two ways, divine reception, and repeated mortality refrain", "wisdom resolution with refrain"),
    ],
    50: [
        (1, 6, "Divine appearance and covenant court summons", "theophanic judgment scene"),
        (7, 15, "Address to the sacrificing people", "divine covenant admonition"),
        (16, 23, "Address to the wicked and closing way", "divine ethical indictment and promise"),
    ],
    51: [
        (1, 9, "Mercy, cleansing, confession, and restored joy plea", "penitential petition"),
        (10, 17, "Renewed heart, sustaining spirit, teaching vow, and true sacrifice", "renewal petition and vow"),
        (18, 19, "Zion good and accepted sacrifices", "communal-cultic coda"),
    ],
    55: [
        (1, 8, "Restless complaint and flight wish", "individual lament opening"),
        (9, 15, "Violent city and intimate betrayal", "city lament and betrayed-friend imprecation"),
        (16, 23, "Repeated prayer, trust, burden, and judgment", "petition-trust conclusion"),
    ],
    57: [
        (1, 5, "Refuge plea rising to exaltation refrain", "lament-petition stanza with refrain"),
        (6, 11, "Reversed trap rising to awakening and repeated refrain", "thanksgiving stanza with refrain"),
    ],
    59: [
        (1, 5, "Deliverance plea and summons to awake", "enemy lament petition"),
        (6, 10, "Evening prowlers and watching confidence", "watch-refrain cycle"),
        (11, 13, "Measured judgment petition", "imprecatory petition"),
        (14, 17, "Repeated evening prowlers and morning praise", "watch-refrain transformed to praise"),
    ],
    62: [
        (1, 4, "Silent rest contrasted with assault", "trust refrain and enemy address"),
        (5, 8, "Repeated rest and communal trust invitation", "trust refrain and exhortation"),
        (9, 12, "Human breath, wealth warning, power, and loyal love", "wisdom conclusion"),
    ],
    65: [
        (1, 4, "Praise, answered prayer, forgiveness, and nearness", "temple thanksgiving"),
        (5, 8, "Saving answer, mountains, seas, and distant awe", "cosmic kingship hymn"),
        (9, 13, "Visited earth, watered fields, and shouting creation", "harvest hymn"),
    ],
    66: [
        (1, 7, "All-earth praise and exodus recital", "universal hymn"),
        (8, 12, "Peoples called to bless through communal testing", "community thanksgiving"),
        (13, 20, "Individual vows, testimony, and answered prayer", "personal thanksgiving and vow"),
    ],
    67: [
        (1, 3, "Blessing plea and peoples' refrain", "priestly-shaped petition and refrain"),
        (4, 5, "Nations rejoice and peoples' refrain", "universal praise center"),
        (6, 7, "Earth yields and blessing reaches its goal", "harvest blessing coda"),
    ],
    68: [
        (1, 6, "Divine arising, enemy scattering, and care for the vulnerable", "processional hymn opening"),
        (7, 10, "Wilderness march and sustaining rain", "historical procession recital"),
        (11, 14, "Victory announcement and scattered kings", "victory oracle-song"),
        (15, 18, "Mountain rivalry and ascent with captives", "mountain-procession hymn"),
        (19, 23, "Daily burden bearing and enemy defeat", "deliverance blessing"),
        (24, 27, "Sanctuary procession and tribal singers", "liturgical procession scene"),
        (28, 31, "Summons for strength and royal tribute", "petition for international homage"),
        (32, 35, "Kingdoms called to praise the rider", "international closing hymn"),
    ],
    69: [
        (1, 6, "Flooded distress and shame plea", "individual lament"),
        (7, 12, "Zeal, reproach, fasting, and public derision", "righteous-sufferer complaint"),
        (13, 18, "Acceptable-time prayer and rescue petition", "direct rescue plea"),
        (19, 28, "Known reproach and judgment appeal", "betrayal lament and imprecation"),
        (29, 36, "Poor petitioner turns to praise and Zion hope", "thanksgiving and communal coda"),
    ],
    71: [
        (1, 8, "Lifelong refuge and praise", "individual trust petition"),
        (9, 16, "Old-age abandonment fear and renewed appeal", "enemy lament and hope"),
        (17, 24, "From youth to old age: teaching and multiplied praise", "lifelong testimony and vow"),
    ],
    72: [
        (1, 7, "Royal justice and flourishing peace", "royal intercession"),
        (8, 11, "Sea-to-sea dominion and royal homage", "royal dominion hymn"),
        (12, 17, "Compassion for the needy and enduring blessing", "royal justice and blessing"),
        (18, 20, "Blessing doxology and collection colophon", "collection doxology and editorial colophon"),
    ],
    73: [
        (1, 12, "Confession and the prosperous wicked", "wisdom problem statement"),
        (13, 17, "Purity crisis until sanctuary discernment", "first-person wisdom crisis and turn"),
        (18, 22, "Slippery end and self-correction", "wisdom resolution"),
        (23, 28, "Continual presence and nearness confession", "trust conclusion"),
    ],
    74: [
        (1, 11, "Rejected flock and ruined sanctuary", "community lament"),
        (12, 17, "Ancient kingship and creation victories remembered", "historical-cosmic recital"),
        (18, 23, "Remember, arise, and defend", "covenant-shaped closing petition"),
    ],
    77: [
        (1, 10, "Night cry, sleepless memory, and six questions", "individual lament crisis"),
        (11, 15, "Deliberate remembrance of ancient wonders", "hymnic recollection"),
        (16, 20, "Waters tremble and unseen path leads the flock", "exodus theophany recital"),
    ],
    78: [
        (1, 8, "Wisdom summons and generational purpose", "historical instruction prologue"),
        (9, 16, "Ephraim failure and exodus wonders", "historical recital opening"),
        (17, 31, "Wilderness testing, provision, and judgment", "rebellion-provision episode"),
        (32, 39, "Persisting sin and recurring compassion", "sin-mercy reflection"),
        (40, 55, "Egyptian signs, exodus, and inheritance", "plague-and-exodus recital"),
        (56, 64, "Rebellion in the land and sanctuary abandonment", "land-rebellion episode"),
        (65, 72, "Divine reversal, Judah choice, and shepherd rule", "historical conclusion"),
    ],
    80: [
        (1, 3, "Shepherd invocation and first restoration refrain", "community petition with refrain"),
        (4, 7, "Tears and reproach with second restoration refrain", "community lament with refrain"),
        (8, 19, "Vine recital, devastation, return plea, and final refrain", "extended vine allegory and refrain"),
    ],
    81: [
        (1, 5, "Festival music and appointed observance", "liturgical summons"),
        (6, 10, "Burden removed and divine command remembered", "deliverance oracle"),
        (11, 16, "Refusal, abandonment, and counterfactual provision", "divine lament and promise"),
    ],
    83: [
        (1, 8, "Enemy tumult and confederacy register", "community threat lament"),
        (9, 12, "Past victories invoked against present chiefs", "historical petition"),
        (13, 18, "Whirlwind pursuit and name-seeking close", "imprecatory petition"),
    ],
    88: [
        (1, 9, "Day-and-night cry from the pit", "individual lament descent"),
        (10, 18, "Questions to the dead and unrelieved abandonment", "death-question lament conclusion"),
    ],
    89: [
        (1, 4, "Loyal-love praise and covenant thesis", "hymnic-covenant prologue"),
        (5, 18, "Heavenly assembly, sea rule, and people's beatitude", "cosmic kingship hymn"),
        (19, 37, "Vision oracle and enduring royal covenant", "extended divine oracle recital"),
        (38, 45, "Anointed king rejected and shamed", "covenant reversal lament"),
        (46, 51, "How long, mortality, and reproach appeal", "urgent communal petition"),
        (52, 52, "Book-closing blessing", "collection doxology"),
    ],
    90: [
        (1, 6, "Enduring dwelling and mortal generations", "divine permanence and human frailty meditation"),
        (7, 12, "Wrath, brief years, and numbered-heart petition", "mortality lament and wisdom plea"),
        (13, 17, "Return, satisfy, reveal, and establish", "communal restoration petition"),
    ],
    91: [
        (1, 8, "Refuge confession and delivered protection", "trust proclamation"),
        (9, 13, "Direct assurance to the refuge-seeker", "protective address"),
        (14, 16, "Divine first-person rescue oracle", "salvation oracle"),
    ],
    92: [
        (1, 4, "Sabbath thanksgiving summons", "thanksgiving opening"),
        (5, 9, "Deep works and passing wicked", "wisdom-hymn contrast"),
        (10, 15, "Exalted horn and flourishing righteous", "testimonial and righteous-tree close"),
    ],
    94: [
        (1, 7, "Vengeance appeal against boastful oppressors", "community lament petition"),
        (8, 11, "Rebuke to the senseless under the Creator's knowledge", "wisdom admonition"),
        (12, 15, "Blessed discipline and returning justice", "wisdom beatitude"),
        (16, 23, "Personal support, consolations, and final retribution", "trust testimony and judgment close"),
    ],
    95: [
        (1, 7, "Come sing, bow, and hear", "processional worship summons"),
        (8, 11, "Do not harden: wilderness warning oracle", "divine admonition"),
    ],
    96: [
        (1, 6, "New song and nations summoned to proclaim", "universal hymn call"),
        (7, 10, "Families ascribe and announce reigning justice", "liturgical homage summons"),
        (11, 13, "Creation rejoices before coming judgment", "cosmic praise conclusion"),
    ],
    99: [
        (1, 3, "Enthroned king and first holiness refrain", "kingship hymn stanza"),
        (4, 5, "Justice-loving strength and second holiness refrain", "justice praise stanza"),
        (6, 9, "Named mediators, answering God, and final holiness refrain", "historical-liturgical stanza"),
    ],
    102: [
        (1, 11, "Afflicted cry and wasting isolation", "individual lament"),
        (12, 22, "Enduring reign, Zion compassion, and nations' worship", "communal restoration hymn"),
        (23, 28, "Shortened strength and unchanging creator", "mortality petition and trust"),
    ],
    103: [
        (1, 5, "Self-summons to bless for personal benefits", "personal thanksgiving"),
        (6, 14, "Justice, revealed ways, compassion, and remembered dust", "communal mercy hymn"),
        (15, 18, "Human grass and enduring loyal love", "mortality-covenant contrast"),
        (19, 22, "Heavenly throne and universal blessing summons", "cosmic doxology"),
    ],
    104: [
        (1, 4, "Majesty clothed in light and heavenly architecture", "creation hymn opening"),
        (5, 9, "Earth founded and waters bounded", "cosmogonic waters movement"),
        (10, 18, "Springs sustain creatures, fields, and trees", "terrestrial provision catalogue"),
        (19, 23, "Moon, sun, night beasts, and human work", "ordered-time movement"),
        (24, 30, "Manifold works, sea creatures, provision, and breath", "creature-providence hymn"),
        (31, 35, "Enduring glory, singer's response, and praise close", "hymnic coda"),
    ],
    105: [
        (1, 6, "Give thanks, seek, remember, and address the descendants", "historical hymn summons"),
        (7, 15, "Covenant, patriarchal wandering, and protected anointed ones", "patriarchal recital"),
        (16, 23, "Famine, Joseph, and Israel entering Egypt", "Joseph episode"),
        (24, 36, "Growth, oppression, Moses, and signs in Egypt", "plague recital"),
        (37, 45, "Exodus, wilderness provision, land gift, and purpose", "exodus-to-inheritance conclusion"),
    ],
    106: [
        (1, 5, "Praise, confession frame, and gathering petition", "hymnic and penitential prologue"),
        (6, 12, "Ancestral sin and rescue at the sea", "exodus rebellion-rescue recital"),
        (13, 23, "Wilderness craving, camp envy, calf, and intercession", "wilderness rebellion cycle"),
        (24, 33, "Rejected land, Baal Peor, Phinehas, and Meribah", "continued rebellion episodes"),
        (34, 46, "Land compromise, repeated oppression, and remembered compassion", "land-era rebellion and mercy recital"),
        (47, 48, "Gathering plea and book-closing blessing", "restoration petition and collection doxology"),
    ],
    107: [
        (1, 3, "Thanksgiving summons and gathered redeemed", "historical thanksgiving prologue"),
        (4, 9, "Wanderers cry and are led to a city", "deliverance refrain cycle"),
        (10, 16, "Prisoners cry and bars are broken", "deliverance refrain cycle"),
        (17, 22, "Sick fools cry and are healed", "deliverance refrain cycle"),
        (23, 32, "Seafarers cry and storm becomes calm", "deliverance refrain cycle"),
        (33, 42, "Landscape and social reversals", "providential reversal hymn"),
        (43, 43, "Wisdom summons to attend to loyal love", "wisdom coda"),
    ],
    108: [
        (1, 5, "Steadfast praise among nations", "hymnic invocation"),
        (6, 13, "Rescue plea, land oracle, and battle trust", "oracle-framed communal petition"),
    ],
    109: [
        (1, 5, "False accusers repay love with hostility", "individual complaint"),
        (6, 20, "Extended accusation and imprecation", "quoted-or-voiced imprecatory unit"),
        (21, 31, "Poor petitioner asks rescue and promises assembly praise", "direct petition and thanksgiving vow"),
    ],
    110: [
        (1, 3, "Throne oracle and willing people", "royal oracle"),
        (4, 7, "Priestly oath and victorious right-hand action", "priestly oracle and battle conclusion"),
    ],
    115: [
        (1, 8, "Name-glory plea and powerless idol satire", "community hymn and idol polemic"),
        (9, 11, "Threefold trust summons", "responsive trust litany"),
        (12, 15, "Remembered blessing for houses and generations", "blessing oracle"),
        (16, 18, "Heavens, earth, dead, and living praise", "cosmic-human praise close"),
    ],
    116: [
        (1, 11, "Loved answer, death cords, rescue, and trusting testimony", "individual thanksgiving"),
        (12, 19, "Return question, cup, vows, servant confession, and temple praise", "thank offering and public vow"),
    ],
    118: [
        (1, 4, "Responsive loyal-love opening", "liturgical thanksgiving refrain"),
        (5, 18, "Distress, encircling nations, reversal, and disciplined survival", "deliverance testimony"),
        (19, 27, "Righteous gates, rejected stone, festal day, and procession", "entrance and festival liturgy"),
        (28, 29, "Personal thanks and repeated loyal-love close", "thanksgiving coda"),
    ],
    119: [
        *[(start, start + 7, f"Alphabetic stanza {letter}", "eight-verse alphabetic Torah meditation")
          for start, letter in zip(
              range(1, 177, 8),
              ["ALEPH", "BETH", "GIMEL", "DALETH", "HE", "VAV", "ZAYIN", "HETH",
               "TETH", "YODH", "KAPH", "LAMEDH", "MEM", "NUN", "SAMEKH", "AYIN",
               "PE", "TZADHE", "QOPH", "RESH", "SIN/SHIN", "TAV"],
          )]
    ],
    132: [
        (1, 10, "Remember David, oath, ark quest, and anointed plea", "Song of Ascents historical-liturgical petition"),
        (11, 18, "Divine oath, Zion choice, provision, and flourishing horn", "answering covenant oracle"),
    ],
    135: [
        (1, 4, "Praise summons to temple servants and chosen community", "liturgical hymn call"),
        (5, 12, "Divine greatness, nature, exodus, kings, and land", "acts-of-power recital"),
        (13, 18, "Enduring name contrasted with idols", "name hymn and idol polemic"),
        (19, 21, "Houses and temple servants called to bless", "responsive blessing close"),
    ],
    136: [
        (1, 3, "Threefold opening thanks", "responsive thanksgiving litany"),
        (4, 9, "Creation wonders with repeated loyal-love response", "creation refrain cycle"),
        (10, 16, "Egypt and wilderness deliverance with repeated response", "exodus refrain cycle"),
        (17, 22, "Kings defeated and land given with repeated response", "conquest refrain cycle"),
        (23, 25, "Low estate remembered and all flesh fed", "communal-providential refrain cycle"),
        (26, 26, "Closing thanks to the God of heaven", "responsive doxology"),
    ],
    137: [
        (1, 4, "By Babylon's rivers: weeping and refused song", "exile lament"),
        (5, 6, "Jerusalem self-oath", "memory oath"),
        (7, 9, "Edom remembrance and Babylon imprecation", "imprecatory close"),
    ],
    139: [
        (1, 6, "Searched and completely known", "knowledge hymn"),
        (7, 12, "No flight from presence", "presence meditation"),
        (13, 18, "Formed in secret and innumerable thoughts", "creation-of-person praise"),
        (19, 22, "Wickedness and contested allegiance", "imprecatory allegiance protest"),
        (23, 24, "Search, test, and lead", "closing self-examination prayer"),
    ],
    144: [
        (1, 4, "Warrior praise and human frailty", "royal-warrior hymn"),
        (5, 8, "Bow heavens and rescue from foreign speech", "theophanic rescue petition"),
        (9, 11, "New song and repeated rescue plea", "praise vow and petition"),
        (12, 15, "Flourishing households, stores, flocks, and beatitude", "community blessing portrait"),
    ],
    145: [
        (1, 7, "Personal and generational acrostic praise", "alphabetic hymn opening"),
        (8, 13, "Gracious character and enduring kingdom", "alphabetic kingship hymn"),
        (14, 20, "Support, provision, nearness, and preservation", "alphabetic providence hymn"),
        (21, 21, "Mouth and all flesh bless the holy name", "universal praise coda"),
    ],
    147: [
        (1, 11, "Praise for rebuilding, healing, cosmic rule, and humble delight", "restoration-creation hymn"),
        (12, 20, "Jerusalem called to praise for security, seasons, word, and statutes", "Zion-word hymn"),
    ],
    148: [
        (1, 6, "Heavens and celestial host summoned to praise", "celestial praise catalogue"),
        (7, 14, "Earth, creatures, rulers, peoples, and faithful summoned", "terrestrial praise catalogue"),
    ],
}


LAMENTS = {
    3, 4, 5, 6, 7, 11, 12, 13, 17, 26, 28, 38, 39, 43, 52, 54, 56,
    58, 60, 61, 63, 64, 70, 79, 82, 85, 86, 123, 126, 129, 130, 140,
    141, 142, 143,
}
WISDOM = {1, 14, 15, 25, 32, 34, 36, 53, 75, 111, 112, 127, 128, 131}
ROYAL = {2, 20, 21, 101}
THANKSGIVING = {16, 23, 30, 48, 52, 54, 56, 61, 63, 84, 87, 100, 120, 121, 122, 124, 125, 133, 134, 138, 149, 150}


def whole_form(chapter: int) -> str:
    if chapter in LAMENTS:
        return "complete lament, prayer, or trust poem"
    if chapter in WISDOM:
        return "complete wisdom or Torah-shaped poem"
    if chapter in ROYAL:
        return "complete royal or communal petition poem"
    if chapter in THANKSGIVING:
        return "complete hymn, thanksgiving, pilgrimage, or praise poem"
    return "complete psalm poem with integrated address, parallelism, and closure"


def chapter_verse_map(text: str) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    for block in re.split(r"(?=\\c\s+\d+)", text):
        match = re.match(r"\\c\s+(\d+)", block)
        if not match:
            continue
        chapter = int(match.group(1))
        out[chapter] = [int(value) for value in re.findall(r"\\v\s+(\d+)", block)]
    return out


def span(chapter: int, start: int, end: int) -> str:
    return f"Ps.{chapter}.{start}-Ps.{chapter}.{end}"


def main() -> None:
    raw = SOURCE.read_text(encoding="utf-8-sig")
    verses = chapter_verse_map(raw)
    assert list(verses) == list(range(1, 151))
    assert sum(len(values) for values in verses.values()) == 2461
    for chapter, values in verses.items():
        assert values == list(range(1, max(values) + 1)), chapter

    proposal: list[dict[str, object]] = []
    outer_audit: list[dict[str, object]] = []
    decision_number = 0
    for chapter in range(1, 151):
        last = verses[chapter][-1]
        units = SPLITS.get(
            chapter,
            [(1, last, f"Psalm {chapter} preserved as a complete poem", whole_form(chapter))],
        )
        observed: list[int] = []
        for unit_index, (start, end, title, form) in enumerate(units):
            decision_number += 1
            observed.extend(range(start, end + 1))
            parent = span(chapter, 1, last)
            exact_alternatives: list[str] = []
            if len(units) > 1:
                exact_alternatives.append(parent)
                if unit_index > 0:
                    exact_alternatives.append(span(chapter, units[unit_index - 1][0], end))
                if unit_index + 1 < len(units):
                    exact_alternatives.append(span(chapter, start, units[unit_index + 1][1]))
            exact_alternatives = list(dict.fromkeys(exact_alternatives))
            if len(units) == 1:
                marker = (
                    f"Ps {chapter}:1 opens the numbered poem and Ps {chapter}:{last} closes it; "
                    "superscription, poetic layout, repeated address, and final cadence were audited, "
                    "with no inner movement decisive enough to displace the whole-poem outer unit"
                )
                confidence = "HIGH" if last <= 12 else "MEDIUM"
                risk = (
                    "low: whole-psalm outer unit is intentional, not a chapter fallback"
                    if last <= 12
                    else "medium: a longer poem was retained whole after movement audit; later specialists may test inner seams"
                )
            else:
                left = f"Ps {chapter}:{start}"
                right = f"Ps {chapter}:{end}"
                previous = "the psalm opening" if start == 1 else f"the seam after Ps {chapter}:{start - 1}"
                following = "the psalm close" if end == last else f"the seam before Ps {chapter}:{end + 1}"
                marker = (
                    f"{previous} opens the '{title}' movement at {left}; {following} closes it at {right}; "
                    f"form changes to or from {form}, while the exact parent {parent} remains preserved"
                )
                confidence = "MEDIUM" if chapter in {42, 46, 57, 59, 62, 67, 80, 99, 107, 118, 119, 136} else "LOW"
                risk = (
                    f"high: internal seam is evidence-only; exact larger alternative {parent} and adjacent-merge "
                    f"alternatives {', '.join(exact_alternatives[1:]) or parent} must remain reviewable"
                )
            proposal.append(
                {
                    "decision_id": f"D{decision_number:03d}",
                    "span": span(chapter, start, end),
                    "title": title,
                    "literary_form": form,
                    "deciding_marker": marker,
                    "exact_alternatives": exact_alternatives,
                    "risk": risk,
                    "confidence": confidence,
                    "non_authorizing_note": (
                        "Literary form, WEB/USFM layout, superscription, refrain, acrostic, and canonical relation "
                        "are evidence only; this row decides no theology, authorship, setting, reading, or source tradition."
                    ),
                }
            )
        assert observed == verses[chapter], chapter
        outer_audit.append(
            {
                "psalm": chapter,
                "parent_span": span(chapter, 1, last),
                "canonical_verse_count": last,
                "treatment": "internally_mapped_with_parent_preserved" if len(units) > 1 else "complete_poem_retained",
                "internal_unit_count": len(units),
                "audit_result": "exact_ordered_coverage_pass",
                "major_evidence": (
                    "stanza/refrain/acrostic/speaker/liturgical or recital movement"
                    if len(units) > 1
                    else "whole-poem coherence outweighed possible line-level or minor movement seams"
                ),
            }
        )

    covered = []
    for row in proposal:
        match = re.fullmatch(r"Ps\.(\d+)\.(\d+)-Ps\.\1\.(\d+)", str(row["span"]))
        assert match
        chapter, start, end = map(int, match.groups())
        covered.extend((chapter, verse) for verse in range(start, end + 1))
    expected = [(chapter, verse) for chapter in range(1, 151) for verse in verses[chapter]]
    assert covered == expected

    artifact = {
        "schema_version": "m7_blind_literary_primary.v1",
        "proposal_id": "M7_sol-Ps-primary-literary-v1-20260723",
        "model_id": "M7_sol",
        "book": "Ps",
        "role": "literary_poetic_form_primary",
        "artifact_status": "candidate_only_non_authorizing",
        "independence_declaration": {
            "blind_primary": True,
            "read_scope": [
                ".ai/scratch/multi_model_bible_chunking/M7_sol/book_strategy/Ps.md",
                ".ai/scratch/multi_model_bible_chunking/M7_sol/review_contract.yaml",
                ".ai/control/chunking_agent_preflight.yaml",
                ".ai/control/contextual_reading_policy.yaml",
                "config/ingest/usfm_marker_coverage.yaml",
                "data/processed/bible/eng-web/usfm/extracted/20-PSAeng-web.usfm",
            ],
            "not_read": [
                "current or fallback M7_sol Psalms chunks",
                "other Psalms primary or sibling outputs",
                "M1-M6 maps",
                "comparison/",
                "T417 layers",
            ],
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_vote": False,
        },
        "non_authorizations": [
            "reviewed_gold",
            "chunk_output_promotion",
            "theology_or_doctrine",
            "canon_or_authorship",
            "superscription_historicity_or_performance_reconstruction",
            "speaker_identity",
            "preferred_translation_or_reading",
            "source_tradition_choice",
            "automatic_intertext_or_graph_truth",
        ],
        "coverage_assertion": {
            "canonical_verses_covered": len(expected),
            "canonical_verses_expected": 2461,
            "ordered": True,
            "every_verse_exactly_once": True,
            "gaps": 0,
            "overlaps": 0,
            "first_verse": "Ps.1.1",
            "last_verse": "Ps.150.6",
            "psalms_audited": 150,
            "proposal_chunk_count": len(proposal),
            "canonical_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        },
        "psalm_outer_unit_audit": outer_audit,
        "proposal": proposal,
        "collection_and_relation_holds": [
            {
                "scope": "Ps.9.1-Ps.10.18",
                "issue": "alphabetic and lexical relation crosses two numbered psalms",
                "decision": "retain Psalms 9 and 10 separately; record the exact paired span as relation evidence only",
            },
            {
                "scope": "Ps.42.1-Ps.43.5",
                "issue": "repeated self-address refrain and continuation pressure cross the numbered-psalm seam",
                "decision": "retain Psalm 42 internal refrain units and Psalm 43 as its own poem; preserve paired span for review",
            },
            {
                "scope": "Ps.120.1-Ps.134.3",
                "issue": "Songs of Ascents form a collection while each poem has its own numbered closure",
                "decision": "retain fifteen whole psalms and record collection relation without merging",
            },
            {
                "scope": "Ps.41.13; Ps.72.18-Ps.72.20; Ps.89.52; Ps.106.47-Ps.106.48",
                "issue": "collection doxologies and colophon functions are distinct but context-dependent",
                "decision": "map the functions explicitly while retaining each whole psalm as exact parent alternative",
            },
        ],
        "oversplit_premortem": [
            "Do not turn parallel bicola, individual imprecations, divine titles, Selah, or every USFM poetry line into chunks.",
            "Do not split short and medium psalms merely because complaint, petition, trust, and praise can be named.",
            "Do not let internal units erase the whole numbered psalm; every split row preserves the exact whole-psalm parent.",
            "Do not merge Psalms 9-10, 42-43, the Songs of Ascents, or Hallel sequences from relation evidence alone.",
            "Do not treat superscriptions, WEB layout, alphabet labels, refrain typography, footnotes, or later canonical reuse as automatic boundary authority.",
            "Do not atomize Psalm 119 below its twenty-two eight-verse alphabetic stanzas.",
            "Do not use collection doxologies to detach theology or authorize a compositional history.",
        ],
        "requested_experts_for_low_confidence_appeals": [
            "Biblical Hebrew poetry, parallelism, discourse, and Masoretic accent specialist",
            "Psalms form, refrain, liturgy, and collection-structure specialist",
            "WEB-to-MT and Hebrew-to-LXX Psalm numbering and versification specialist",
            "Hebrew acrostic and alphabetic-poem specialist",
            "Textual-criticism specialist for obscure or variant-dependent Psalm seams",
            "Qualified ancient Jewish and early-rabbinic reception specialist with explicit chronology labels",
            "Canonical intertext specialist who treats later reuse as evidence rather than seam authority",
        ],
        "final_statement": (
            "This blind literary/poetic map audits all 150 psalms and supplies exact full coverage. "
            "Whole psalms remain governing parent alternatives for every internal movement. Agreement is evidence, "
            "not authority; unresolved seams remain eligible for larger-unit retention, lower confidence, and human "
            "or genuinely independent external-AI review."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, ensure_ascii=False) + "\n"
    OUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    SHA_OUT.write_text(f"{digest}  {OUT.name}\n", encoding="utf-8")
    print(json.dumps({"path": str(OUT), "sha256": digest, "chunks": len(proposal), "verses": len(expected)}))


if __name__ == "__main__":
    main()
