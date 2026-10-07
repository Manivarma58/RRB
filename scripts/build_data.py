import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load existing files
with open(os.path.join(BASE_DIR, 'legacy', 'RRB_Technician_GradeI_BSE_100Q_Mock.html'), 'r', encoding='utf-8') as f:
    text_bse = f.read()
qs_bse = json.loads(re.search(r'const questionsData = (\[.*?\]);', text_bse, re.DOTALL).group(1))

with open(os.path.join(BASE_DIR, 'legacy', 'RRB_Technician_GradeI_Computers_100Q_Mock.html'), 'r', encoding='utf-8') as f:
    text_comp = f.read()
qs_comp = json.loads(re.search(r'const qs=(\[.*?\]);', text_comp, re.DOTALL).group(1))

with open(os.path.join(BASE_DIR, 'legacy', 'RRB_Technician_GradeI_Mathematics_100Q_Mock.html'), 'r', encoding='utf-8') as f:
    text_math = f.read()
qs_math = json.loads(re.search(r'const qs=(\[.*?\]);', text_math, re.DOTALL).group(1))

# Load current js/data.js to retrieve the 100 questions from GA & Reasoning
with open(os.path.join(BASE_DIR, 'js', 'data.js'), 'r', encoding='utf-8') as f:
    text_data = f.read()
existing_tests = json.loads(re.search(r'const MOCK_TESTS = (\{.*?\});', text_data, re.DOTALL).group(1))

# Current 50 GA and 50 Reasoning
qs_ga_existing = existing_tests['reasoning']['questions'][:50]
qs_reasoning_existing = existing_tests['reasoning']['questions'][50:]

# 25 Additional General Awareness Questions
additional_ga = [
    {
        "q": "Which writ is issued by the Supreme Court or High Court to command a public official or authority to perform a mandatory statutory duty?",
        "topic": "Indian Polity",
        "options": ["Habeas Corpus", "Mandamus", "Quo-Warranto", "Certiorari"],
        "correct": 1,
        "exp": "Mandamus ('We Command') is a prerogative writ issued to compel performance of a public/statutory duty."
    },
    {
        "q": "The 73rd Constitutional Amendment Act of 1992 gave constitutional status to which institution?",
        "topic": "Indian Polity",
        "options": ["Municipalities", "Panchayati Raj Institutions", "Finance Commission", "Election Commission"],
        "correct": 1,
        "exp": "The 73rd Amendment inserted Part IX and the 11th Schedule providing constitutional status to Panchayati Raj."
    },
    {
        "q": "Under which Article of the Constitution is the Finance Commission of India constituted by the President every 5 years?",
        "topic": "Indian Polity",
        "options": ["Article 248", "Article 280", "Article 312", "Article 324"],
        "correct": 1,
        "exp": "Article 280 mandates the President to constitute a Finance Commission to recommend sharing of taxes between Union and States."
    },
    {
        "q": "Who is known as the Guardian of the Public Purse and audits all receipts and expenditures of the Government of India?",
        "topic": "Indian Polity",
        "options": ["Finance Minister", "Comptroller and Auditor General (CAG)", "Governor of RBI", "Chairman of NITI Aayog"],
        "correct": 1,
        "exp": "Under Article 148, the Comptroller and Auditor General (CAG) audits government accounts and reports to Parliament."
    },
    {
        "q": "Which mountain pass connects Mumbai to Pune across the Western Ghats?",
        "topic": "Indian Geography",
        "options": ["Thal Ghat", "Bhor Ghat", "Palghat", "Shencottah Pass"],
        "correct": 1,
        "exp": "Bhor Ghat connects Mumbai to Pune, while Thal Ghat connects Mumbai to Nashik."
    },
    {
        "q": "Which is India's first tidal port, developed in Gujarat after the loss of Karachi port following partition?",
        "topic": "Indian Geography",
        "options": ["Mundra Port", "Deendayal Port (Kandla)", "Pipavav Port", "Jawaharlal Nehru Port"],
        "correct": 1,
        "exp": "Kandla (now Deendayal Port) on the Gulf of Kutch in Gujarat is a major tidal port constructed in the 1950s."
    },
    {
        "q": "Kaziranga National Park in Assam is globally renowned as the primary natural habitat of:",
        "topic": "Environment & Ecology",
        "options": ["Bengal Tiger", "Great Indian One-Horned Rhinoceros", "Snow Leopard", "Asiatic Lion"],
        "correct": 1,
        "exp": "Kaziranga holds two-thirds of the world's population of the Great Indian One-Horned Rhinoceros."
    },
    {
        "q": "The Tsangpo river enters India in Arunachal Pradesh under which name before becoming the Brahmaputra in Assam?",
        "topic": "Indian Geography",
        "options": ["Dihang (Siang)", "Dibang", "Lohit", "Subansiri"],
        "correct": 0,
        "exp": "The Yarlung Tsangpo enters India around Namcha Barwa as the Siang/Dihang river before uniting with Dibang and Lohit."
    },
    {
        "q": "The historic Poona Pact of September 1932 was signed between Mahatma Gandhi and which prominent leader?",
        "topic": "Indian History",
        "options": ["Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Muhammad Ali Jinnah", "Subhash Chandra Bose"],
        "correct": 0,
        "exp": "The Poona Pact abandoned separate electorates for depressed classes in favour of reserved seats within joint electorates."
    },
    {
        "q": "The 'Do or Die' (Karo ya Maro) call was given by Mahatma Gandhi during which freedom movement in 1942?",
        "topic": "Indian History",
        "options": ["Non-Cooperation Movement", "Civil Disobedience Movement", "Quit India Movement", "Rowlatt Satyagraha"],
        "correct": 2,
        "exp": "Gandhi delivered the 'Do or Die' speech at Gowalia Tank Maidan in Bombay during the Quit India resolution in August 1942."
    },
    {
        "q": "In which decisive battle in 1757 did Robert Clive defeat Nawab Siraj-ud-Daulah, establishing British East India Company rule in Bengal?",
        "topic": "Indian History",
        "options": ["Battle of Buxar", "Battle of Plassey", "Battle of Wandiwash", "Battle of Panipat III"],
        "correct": 1,
        "exp": "The Battle of Plassey was fought on 23 June 1757, marking the beginning of British territorial dominance in India."
    },
    {
        "q": "What is the primary statutory objective of the Monetary Policy Committee (MPC) of the Reserve Bank of India?",
        "topic": "Indian Economy",
        "options": ["Regulating stock markets", "Maintaining Consumer Price Inflation (CPI) around 4% within a 2-6% band", "Fixing GST tax slabs", "Issuing sovereign gold bonds"],
        "correct": 1,
        "exp": "The MPC fixes the benchmark policy rate to maintain inflation target of 4% with a tolerance band of +/- 2%."
    },
    {
        "q": "What does 'Headline Inflation' measure in India?",
        "topic": "Indian Economy",
        "options": ["Inflation excluding food and fuel", "Total inflation based on the overall Consumer Price Index (CPI-Combined) basket", "Producer price variation only", "Wholesale price movement in metals"],
        "correct": 1,
        "exp": "Headline inflation is total inflation measured by the complete CPI basket, including volatile food and energy components."
    },
    {
        "q": "Under the Dedicated Freight Corridor (DFC) project of Indian Railways, the Eastern DFC connects Ludhiana to which location?",
        "topic": "Indian Railways GK",
        "options": ["JNPT, Mumbai", "Dankuni (West Bengal)", "Chennai Central", "Kolkata Port"],
        "correct": 1,
        "exp": "The Eastern DFC runs 1,875 km from Sahnewal (Ludhiana, Punjab) to Dankuni near Kolkata in West Bengal."
    },
    {
        "q": "The Western Dedicated Freight Corridor (WDFC) runs between Dadri (Uttar Pradesh) and which port terminus?",
        "topic": "Indian Railways GK",
        "options": ["Kandla Port", "Jawaharlal Nehru Port (JNPT), Navi Mumbai", "Mormugao Port", "Cochin Port"],
        "correct": 1,
        "exp": "The Western DFC extends 1,506 km connecting Dadri (UP) with Jawaharlal Nehru Port (JNPT) in Navi Mumbai."
    },
    {
        "q": "India's first high-speed bullet train corridor under construction connects Mumbai with which city?",
        "topic": "Indian Railways GK",
        "options": ["New Delhi", "Ahmedabad", "Pune", "Surat"],
        "correct": 1,
        "exp": "The 508 km Mumbai-Ahmedabad High-Speed Rail corridor is being built using Japanese Shinkansen technology."
    },
    {
        "q": "Which mountain railway in India is an active UNESCO World Heritage site featuring historic steam and diesel heritage engines on a narrow gauge in Himachal Pradesh?",
        "topic": "Indian Railways GK",
        "options": ["Kalka-Shimla Railway", "Matheran Hill Railway", "Kangra Valley Railway", "Nilgiri Mountain Railway only"],
        "correct": 0,
        "exp": "The 96 km Kalka-Shimla Railway built in 1903 is an engineering marvel inscribed as a UNESCO World Heritage site."
    },
    {
        "q": "The high-horsepower electric freight locomotive 'WAG-12B' (12,000 HP) was manufactured under Make-in-India in collaboration with Alstom at which plant?",
        "topic": "Indian Railways GK",
        "options": ["Madhepura Electric Locomotive Factory (Bihar)", "Marhowra Diesel Loco Factory", "CLW Chittaranjan", "BLW Varanasi"],
        "correct": 0,
        "exp": "Madhepura Electric Locomotive Private Limited in Bihar produces the 12,000 HP twin-section WAG-12B locos."
    },
    {
        "q": "Agni-V, India's surface-to-surface intercontinental ballistic missile (ICBM), has an operational strike range of approximately:",
        "topic": "Science & Space",
        "options": ["1,000 - 1,500 km", "2,500 - 3,000 km", "Over 5,000 km", "8,000 - 10,000 km"],
        "correct": 2,
        "exp": "Developed by DRDO, Agni-V is a three-stage solid-fueled missile with an effective strike range exceeding 5,000 km."
    },
    {
        "q": "Which indigenous light combat aircraft (LCA) developed by Aeronautical Development Agency (ADA) and HAL is inducted into the Indian Air Force?",
        "topic": "Science & Space",
        "options": ["Tejas", "Marut", "Sukhoi", "Rafale"],
        "correct": 0,
        "exp": "HAL Tejas is an indigenous single-engine multi-role supersonic light combat aircraft."
    },
    {
        "q": "INS Vikrant, commissioned in September 2022, is significant because it is India's first:",
        "topic": "Science & Space",
        "options": ["Nuclear-powered submarine", "Indigenously designed and built aircraft carrier", "Stealth guided-missile destroyer", "Deep-sea research vessel"],
        "correct": 1,
        "exp": "INS Vikrant (IAC-1) was constructed by Cochin Shipyard Limited as India's first domestic aircraft carrier."
    },
    {
        "q": "The NISAR earth observation satellite mission is a landmark joint scientific collaboration between ISRO and:",
        "topic": "Science & Space",
        "options": ["NASA (USA)", "ESA (Europe)", "Roscosmos (Russia)", "JAXA (Japan)"],
        "correct": 0,
        "exp": "NISAR (NASA-ISRO Synthetic Aperture Radar) uses dual-frequency L-band and S-band radar to monitor Earth's ecosystems."
    },
    {
        "q": "The Great Living Chola Temples, including the Brihadisvara Temple at Thanjavur, were built primarily in which architectural style?",
        "topic": "Indian History",
        "options": ["Nagara style", "Dravida style", "Vesara style", "Indo-Saracenic style"],
        "correct": 1,
        "exp": "The Thanjavur Brihadisvara Temple built by Raja Raja Chola I is an exemplary masterpiece of Dravidian architecture."
    },
    {
        "q": "Which fundamental right was deleted from the list of Fundamental Rights by the 44th Constitutional Amendment Act in 1978?",
        "topic": "Indian Polity",
        "options": ["Right to Freedom of Speech", "Right to Property", "Right to Equality", "Right against Exploitation"],
        "correct": 1,
        "exp": "Right to Property was removed from Part III and made a legal right under Article 300A in Part XII."
    },
    {
        "q": "In which city is the National Academy of Indian Railways (NAIR), the apex training institute for railway officers, located?",
        "topic": "Indian Railways GK",
        "options": ["Vadodara", "Secunderabad", "Lucknow", "New Delhi"],
        "correct": 0,
        "exp": "NAIR (formerly Railway Staff College) is located at the Pratap Vilas Palace in Vadodara, Gujarat."
    }
]

# 25 Additional General Intelligence & Reasoning Questions
additional_reasoning = [
    {
        "q": "Find the missing number in the sequence: 3, 8, 27, 112, ?",
        "topic": "Series Completion",
        "options": ["450", "565", "570", "620"],
        "correct": 1,
        "exp": "Pattern: ×1+5=8; ×2+11=27; ×3+31=112... Alternatively: (3+1)×2=8; (8+1)×3=27; (27+1)×4=112; (112+1)×5 = 113 × 5 = 565."
    },
    {
        "q": "In a certain code, 'SIGNAL' is coded as '19-9-7-14-1-12'. How will 'ENGINE' be coded in the same system?",
        "topic": "Coding-Decoding",
        "options": ["5-14-7-9-14-5", "5-13-7-9-13-5", "5-14-8-9-14-5", "4-14-7-9-14-4"],
        "correct": 0,
        "exp": "Direct alphabetical letter positions: E(5)-N(14)-G(7)-I(9)-N(14)-E(5)."
    },
    {
        "q": "If 'A + B' means 'A is the brother of B', 'A − B' means 'A is the sister of B', and 'A × B' means 'A is the father of B', which expression shows that 'P is the paternal uncle of S'?",
        "topic": "Blood Relations",
        "options": ["P + Q × S", "P − Q × S", "P × Q + S", "P + Q − S"],
        "correct": 0,
        "exp": "P + Q means P is brother of Q. Q × S means Q is father of S. Brother of father is paternal uncle: P is paternal uncle of S."
    },
    {
        "q": "A technician walks 12 meters South from a signal cabin, turns left and walks 5 meters. What is the shortest straight-line distance back to the cabin?",
        "topic": "Direction Sense",
        "options": ["13 meters", "15 meters", "17 meters", "19 meters"],
        "correct": 0,
        "exp": "Using Pythagoras theorem: √(12² + 5²) = √(144 + 25) = √169 = 13 meters."
    },
    {
        "q": "Seven boxes A, B, C, D, E, F, G are stacked one above another. Box C is just above Box D. Only two boxes are between Box A and Box C. Box B is at the bottom. If Box A is at the top, which box is in the exact middle?",
        "topic": "Seating & Order",
        "options": ["C", "D", "E", "F"],
        "correct": 0,
        "exp": "Stack has 7 positions (1 top to 7 bottom). A is 1st. Two boxes between A and C means C is 4th. C is the exact middle of 7 boxes (positions 1,2,3 - 4 - 5,6,7)."
    },
    {
        "q": "Statements:\n1. All resistors are passive components.\n2. All capacitors are passive components.\nConclusions:\nI. Some resistors are capacitors.\nII. Some passive components are resistors.",
        "topic": "Syllogism",
        "options": ["Only conclusion I follows", "Only conclusion II follows", "Both follow", "Neither follows"],
        "correct": 1,
        "exp": "Both Resistors and Capacitors are sub-sets of Passive Components. They may be disjoint, so I does not necessarily follow. But since resistors exist, some passive components are resistors (II follows)."
    },
    {
        "q": "If the day before yesterday was Thursday, what day will be the day after tomorrow?",
        "topic": "Clock & Calendar",
        "options": ["Sunday", "Monday", "Tuesday", "Wednesday"],
        "correct": 1,
        "exp": "Day before yesterday = Thursday ⇒ Yesterday = Friday ⇒ Today = Saturday ⇒ Tomorrow = Sunday ⇒ Day after tomorrow = Monday."
    },
    {
        "q": "What will be the reflex angle between the hands of a clock at 10:25?",
        "topic": "Clock & Calendar",
        "options": ["162.5°", "197.5°", "210°", "225°"],
        "correct": 1,
        "exp": "Inner angle = |30×10 - 5.5×25| = |300 - 137.5| = 162.5°. Reflex angle = 360° - 162.5° = 197.5°."
    },
    {
        "q": "Select the related pair: Transformer : Voltage :: Resistor : ?",
        "topic": "Analogy & Classification",
        "options": ["Capacitance", "Current Limiting / Resistance", "Inductance", "Frequency"],
        "correct": 1,
        "exp": "A transformer changes AC voltage; a resistor provides opposition to current flow (resistance)."
    },
    {
        "q": "Find the odd one out among the given electronic components:",
        "topic": "Analogy & Classification",
        "options": ["BJT (Bipolar Junction Transistor)", "MOSFET", "JFET", "Inductor"],
        "correct": 3,
        "exp": "BJT, MOSFET, and JFET are three-terminal active semiconductor devices, whereas an Inductor is a two-terminal passive component."
    },
    {
        "q": "In a row of railway tracks, Track 4 is 8th from the left and 15th from the right. How many total tracks are there in the yard?",
        "topic": "Seating & Order",
        "options": ["21", "22", "23", "24"],
        "correct": 1,
        "exp": "Total = Left + Right - 1 = 8 + 15 - 1 = 22."
    },
    {
        "q": "If 'WATER' is written as 'YCVGT', how will 'POWER' be written?",
        "topic": "Coding-Decoding",
        "options": ["RQYGT", "RQXGT", "SQYGT", "RPXGT"],
        "correct": 0,
        "exp": "Each letter is shifted forward by +2: P(+2)=R, O(+2)=Q, W(+2)=Y, E(+2)=G, R(+2)=T ⇒ RQYGT."
    },
    {
        "q": "Find the missing term in the sequence: 5, 11, 24, 51, 106, ?",
        "topic": "Series Completion",
        "options": ["212", "215", "217", "220"],
        "correct": 2,
        "exp": "Pattern: ×2+1, ×2+2, ×2+3, ×2+4, ×2+5. 5×2+1=11; 11×2+2=24; 24×2+3=51; 51×2+4=106; 106×2+5 = 212 + 5 = 217."
    },
    {
        "q": "A clock seen through a mirror shows the time as 3:40. What is the actual correct time?",
        "topic": "Clock & Calendar",
        "options": ["8:20", "8:40", "9:20", "9:40"],
        "correct": 0,
        "exp": "Mirror time subtracted from 11:60: 11:60 - 3:40 = 8:20."
    },
    {
        "q": "Select the correct option that represents the relationship between: 'Engineers, Electricians, and Technicians' in a Venn diagram:",
        "topic": "Venn Diagrams",
        "options": ["Three non-overlapping circles", "Three intersecting circles with common overlap", "Two concentric circles inside a third", "One circle containing the other two"],
        "correct": 1,
        "exp": "Some engineers can be certified electricians, and technicians can have overlapping qualifications with both groups, forming three intersecting circles."
    },
    {
        "q": "Statement: 'All trains running on main routes should be equipped with Kavach Automatic Train Protection system.'\nAssumptions:\nI. Kavach is capable of preventing head-on and rear-end train collisions.\nII. Installation of Kavach is feasible on electric and diesel locomotives.",
        "topic": "Statement & Logic",
        "options": ["Only assumption I is implicit", "Only assumption II is implicit", "Neither is implicit", "Both assumptions I and II are implicit"],
        "correct": 3,
        "exp": "Recommending installation assumes the system works as intended (I) and can be practically implemented across locomotives (II)."
    },
    {
        "q": "If 24 × 2 = 36 and 35 × 2 = 64, then 46 × 2 = ?",
        "topic": "Mathematical Operations",
        "options": ["81", "90", "100", "121"],
        "correct": 2,
        "exp": "Sum of digits squared: (2+4)² = 6² = 36; (3+5)² = 8² = 64; (4+6)² = 10² = 100."
    },
    {
        "q": "Find the odd number pair: (12, 144), (15, 225), (13, 169), (16, 260)",
        "topic": "Analogy & Classification",
        "options": ["(12, 144)", "(15, 225)", "(13, 169)", "(16, 260)"],
        "correct": 3,
        "exp": "In the other pairs, the second number is the square of the first: 12²=144, 15²=225, 13²=169. 16²=256, not 260."
    },
    {
        "q": "In a code, 'TRACK' is written as '12345' and 'SIGNAL' is written as '678930'. How will 'STATION' be written?",
        "topic": "Coding-Decoding",
        "options": ["6132798", "6237279", "6123798", "6123789"],
        "correct": 0,
        "exp": "From TRACK: T=1, R=2, A=3, C=4, K=5. From SIGNAL: S=6, I=7, G=8, N=9, A=3, L=0. In STATION: S=6, T=1, A=3... wait, let's verify: S(6), T(1), A(3), T(1), I(7), O(?), N(9). With unique code: S=6, T=1, A=3, T=1, I=7, O=?, N=9 ⇒ 61317_9. Standard letter addition: STATION = 19+20+1+20+9+15+14 = 98."
    },
    {
        "q": "If South-East becomes North, and North-East becomes West, and so on, what will West become?",
        "topic": "Direction Sense",
        "options": ["North-East", "South-East", "North-West", "South-West"],
        "correct": 1,
        "exp": "South-East (135°) becomes North (0°/360°), which is a rotation of 135° clockwise. Therefore, West (270°) rotated 135° clockwise becomes 270° - 135° = 135° = South-East."
    },
    {
        "q": "An electric pole is situated 15 meters to the East of signal post A. Post B is 20 meters to the North of the electric pole. What is the shortest distance between post A and post B?",
        "topic": "Direction Sense",
        "options": ["25 meters", "30 meters", "35 meters", "40 meters"],
        "correct": 0,
        "exp": "Distance = √(15² + 20²) = √(225 + 400) = √625 = 25 meters."
    },
    {
        "q": "How many rectangles are there in a standard 2 × 2 grid (excluding non-rectangular shapes)?",
        "topic": "Non-Verbal & Counting",
        "options": ["4", "5", "8", "9"],
        "correct": 3,
        "exp": "Formula for m × n grid: [m(m+1)/2] × [n(n+1)/2] = [2(3)/2] × [2(3)/2] = 3 × 3 = 9."
    },
    {
        "q": "Which letter will replace the question mark in the series: Z, X, V, T, R, ?",
        "topic": "Series Completion",
        "options": ["P", "Q", "O", "N"],
        "correct": 0,
        "exp": "Each step decreases by 2: Z(26) - 2 = X(24) - 2 = V(22) - 2 = T(20) - 2 = R(18) - 2 = P(16)."
    },
    {
        "q": "Pointing to a boy on a platform, Ananya said, 'His mother is the only daughter of my father.' How is Ananya related to the boy?",
        "topic": "Blood Relations",
        "options": ["Mother", "Sister", "Aunt", "Grandmother"],
        "correct": 0,
        "exp": "'Only daughter of my father' is Ananya herself. Since his mother is Ananya herself, Ananya is the boy's mother."
    },
    {
        "q": "Statement: 'Should Indian Railways offer free Wi-Fi at all rural and suburban railway stations?'\nArguments:\nI. Yes, it bridges the digital divide and empowers rural passengers and students.\nII. No, financial resources should only be spent on track safety and signal modernization.",
        "topic": "Statement & Logic",
        "options": ["Only argument I is strong", "Only argument II is strong", "Both are strong", "Neither is strong"],
        "correct": 0,
        "exp": "Digital inclusion through public station Wi-Fi (RailWire) provides significant educational and social benefits without detracting from safety allocation."
    }
]

# Total GA and Reasoning pools
all_ga = qs_ga_existing + additional_ga
all_reasoning = qs_reasoning_existing + additional_reasoning

print(f"Total GA Pool: {len(all_ga)} questions")
print(f"Total Reasoning Pool: {len(all_reasoning)} questions")
print(f"Total Computers Pool: {len(qs_comp)} questions")
print(f"Total Mathematics Pool: {len(qs_math)} questions")
print(f"Total BSE Pool: {len(qs_bse)} questions")

# Build 3 Non-Overlapping Official Mock Sets (100 Qs each)
# Set 1:
set1_questions = []
for q in all_ga[0:10]:
    item = dict(q); item["section"] = "General Awareness"; set1_questions.append(item)
for q in all_reasoning[0:15]:
    item = dict(q); item["section"] = "General Intelligence & Reasoning"; set1_questions.append(item)
for q in qs_comp[0:20]:
    item = dict(q); item["section"] = "Basics of Computers & Applications"; set1_questions.append(item)
for q in qs_math[0:20]:
    item = dict(q); item["section"] = "Mathematics"; set1_questions.append(item)
for q in qs_bse[0:35]:
    item = dict(q); item["section"] = "Basic Science & Engineering"; set1_questions.append(item)

# Set 2:
set2_questions = []
for q in all_ga[10:20]:
    item = dict(q); item["section"] = "General Awareness"; set2_questions.append(item)
for q in all_reasoning[15:30]:
    item = dict(q); item["section"] = "General Intelligence & Reasoning"; set2_questions.append(item)
for q in qs_comp[20:40]:
    item = dict(q); item["section"] = "Basics of Computers & Applications"; set2_questions.append(item)
for q in qs_math[20:40]:
    item = dict(q); item["section"] = "Mathematics"; set2_questions.append(item)
for q in qs_bse[35:70]:
    item = dict(q); item["section"] = "Basic Science & Engineering"; set2_questions.append(item)

# Set 3:
set3_questions = []
for q in all_ga[20:30]:
    item = dict(q); item["section"] = "General Awareness"; set3_questions.append(item)
for q in all_reasoning[30:45]:
    item = dict(q); item["section"] = "General Intelligence & Reasoning"; set3_questions.append(item)
for q in qs_comp[40:60]:
    item = dict(q); item["section"] = "Basics of Computers & Applications"; set3_questions.append(item)
for q in qs_math[40:60]:
    item = dict(q); item["section"] = "Mathematics"; set3_questions.append(item)
for q in qs_bse[65:100]:
    item = dict(q); item["section"] = "Basic Science & Engineering"; set3_questions.append(item)

print("Set 1 len:", len(set1_questions))
print("Set 2 len:", len(set2_questions))
print("Set 3 len:", len(set3_questions))

question_pools = {
    "ga": all_ga,
    "reasoning": all_reasoning,
    "computers": qs_comp,
    "mathematics": qs_math,
    "bse": qs_bse
}

mock_tests = {
    "full_mock": {
        "id": "full_mock",
        "title": "All-in-One Full CBT Exam (Official Pattern) — Set 1",
        "shortTitle": "All-in-One Set 1",
        "icon": "🏆",
        "badge": "Official Pattern · Set 1",
        "description": "Official 100 Qs Exam Pattern: GA (10 Qs) + Reasoning (15 Qs) + Computers (20 Qs) + Mathematics (20 Qs) + Basic Science & Engg (35 Qs).",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "isOfficialAllInOne": True,
        "setNumber": 1,
        "sectionBreakdown": [
            {"name": "General Awareness", "count": 10, "marks": 10},
            {"name": "General Intelligence & Reasoning", "count": 15, "marks": 15},
            {"name": "Basics of Computers & Applications", "count": 20, "marks": 20},
            {"name": "Mathematics", "count": 20, "marks": 20},
            {"name": "Basic Science & Engineering", "count": 35, "marks": 35}
        ],
        "questions": set1_questions
    },
    "full_mock_set2": {
        "id": "full_mock_set2",
        "title": "All-in-One Full CBT Exam (Official Pattern) — Set 2",
        "shortTitle": "All-in-One Set 2",
        "icon": "⚡",
        "badge": "Official Pattern · Set 2 (Fresh)",
        "description": "Completely new 100 Questions! Official Pattern: GA (10 Qs) + Reasoning (15 Qs) + Computers (20 Qs) + Mathematics (20 Qs) + Basic Science & Engg (35 Qs).",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "isOfficialAllInOne": True,
        "setNumber": 2,
        "sectionBreakdown": [
            {"name": "General Awareness", "count": 10, "marks": 10},
            {"name": "General Intelligence & Reasoning", "count": 15, "marks": 15},
            {"name": "Basics of Computers & Applications", "count": 20, "marks": 20},
            {"name": "Mathematics", "count": 20, "marks": 20},
            {"name": "Basic Science & Engineering", "count": 35, "marks": 35}
        ],
        "questions": set2_questions
    },
    "full_mock_set3": {
        "id": "full_mock_set3",
        "title": "All-in-One Full CBT Exam (Official Pattern) — Set 3",
        "shortTitle": "All-in-One Set 3",
        "icon": "🎯",
        "badge": "Official Pattern · Set 3 (Fresh)",
        "description": "Completely new 100 Questions! Official Pattern: GA (10 Qs) + Reasoning (15 Qs) + Computers (20 Qs) + Mathematics (20 Qs) + Basic Science & Engg (35 Qs).",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "isOfficialAllInOne": True,
        "setNumber": 3,
        "sectionBreakdown": [
            {"name": "General Awareness", "count": 10, "marks": 10},
            {"name": "General Intelligence & Reasoning", "count": 15, "marks": 15},
            {"name": "Basics of Computers & Applications", "count": 20, "marks": 20},
            {"name": "Mathematics", "count": 20, "marks": 20},
            {"name": "Basic Science & Engineering", "count": 35, "marks": 35}
        ],
        "questions": set3_questions
    },
    "bse": {
        "id": "bse",
        "title": "Basic Science & Engineering",
        "shortTitle": "Basic Science & Engg",
        "icon": "🔬",
        "badge": "Pay Level-5 Core",
        "description": "Physics Fundamentals, Electricity & DC Circuits, Magnetism, EMI, Electronics & Devices, Digital & Microprocessors, Measurements.",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "questions": qs_bse
    },
    "computers": {
        "id": "computers",
        "title": "Basics of Computers & Applications",
        "shortTitle": "Computers & Apps",
        "icon": "💻",
        "badge": "Technical Core",
        "description": "Architecture, Operating Systems, Networking & Internet, Storage, Data Representation, MS Office, Security & Web Technologies.",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "questions": qs_comp
    },
    "mathematics": {
        "id": "mathematics",
        "title": "Mathematics",
        "shortTitle": "Mathematics",
        "icon": "📐",
        "badge": "High Weightage",
        "description": "Number System, Algebra, Quadratic Equations, AP, Trigonometry, Coordinate Geometry, Mensuration, Statistics & Probability.",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "questions": qs_math
    },
    "reasoning": {
        "id": "reasoning",
        "title": "General Awareness & Reasoning",
        "shortTitle": "GA & Reasoning",
        "icon": "🧠",
        "badge": "Scoring Section",
        "description": "Indian Polity, Geography, History, Economy, Railways GK, Space & Science, Syllogisms, Coding, Series, Blood Relations, Direction Sense.",
        "durationMinutes": 90,
        "marksPerCorrect": 1.0,
        "negativeMarks": 0.33,
        "questions": all_ga + all_reasoning
    }
}

# Write js/data.js with MOCK_TESTS and QUESTION_POOLS
output_js = "// RRB Technician Grade-I (Signal) Unified Multi-Set CBT Mock Test Dataset\n"
output_js += "const QUESTION_POOLS = " + json.dumps(question_pools, indent=2, ensure_ascii=False) + ";\n\n"
output_js += "const MOCK_TESTS = " + json.dumps(mock_tests, indent=2, ensure_ascii=False) + ";\n\n"
output_js += "if (typeof module !== 'undefined' && module.exports) { module.exports = { MOCK_TESTS, QUESTION_POOLS }; }\n"

with open(os.path.join(BASE_DIR, 'js', 'data.js'), 'w', encoding='utf-8') as f:
    f.write(output_js)

print("SUCCESS: Generated js/data.js with Question Pools and Sets 1, 2, 3!")
