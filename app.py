from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Highly Intensive Intent-Based Database for Pragati Smart Desk
CAMPUS_DATA = {
    "courses_only": (
        "🎓 **Pragati Engineering College (Autonomous) Approved Programs:**\n\n"
        "Here is the list of official academic tracks and technical disciplines provided under our campus engineering curriculum matrix:\n\n"
        "• **CSE** — Computer Science & Engineering (Code: `PRAG-CSE`)\n"
        "• **CSE - AI & ML** — Artificial Intelligence & Machine Learning (Code: `PRAG-AIML`)\n"
        "• **CSE - AI** — Artificial Intelligence (Code: `PRAG-AI`)\n"
        "• **CSE - Data Science** — Data Science (Code: `PRAG-DS`)\n"
        "• **CSE - Cyber Security** — Cyber Security (Code: `PRAG-CS`)\n"
        "• **IT** — Information Technology (Code: `PRAG-IT`)\n"
        "• **ECE** — Electronics & Communication Engineering (Code: `PRAG-ECE`)\n"
        "• **EEE** — Electrical & Electronics Engineering (Code: `PRAG-EEE`)\n"
        "• **ME** — Mechanical Engineering (Code: `PRAG-ME`)\n"
        "• **CE** — Civil Engineering (Code: `PRAG-CE`)"
    ),
    "hods_only": (
        "📍 **Pragati Autonomous College Official HODs Directory:**\n\n"
        "Mee dynamic department validation procedures rules handling kosam official Head of Departments contact directory lines list checks:\n\n"
        "• **CSE HOD:** **Dr. D. V. Manjula**\n"
        "• **CSE - AI & ML HOD:** **Dr. A. Radha Krishna**\n"
        "• **CSE - AI HOD:** **Smt. K. Lakshmi Viveka**\n"
        "• **CSE - Data Science HOD:** **Sri. M V Rajesh**\n"
        "• **CSE - Cyber Security HOD:** **Smt. T Ganga Bhavani**\n"
        "• **IT HOD:** **Sri. G Satya Mohan Chowdary**\n"
        "• **ECE HOD:** **Dr. V. Prasanth**\n"
        "• **EEE HOD:** **Sri. K V Durga Prasad**\n"
        "• **Mechanical HOD:** **Dr. G. Avinash**\n"
        "• **Civil HOD:** **Dr. B. Satyanarayana**"
    ),
    "faculty_only": (
        "📋 **Pragati Engineering College Core Faculty Matrix Setup:**\n\n"
        "Department-wise core instructional support cell members list panel configuration profiles:\n\n"
        "• **Computer Science (CSE/IT Blocks):** Dr. M. Radhika, Sri. P. Surya, Smt. S. Lakshmi, Sri. S. Varma, Smt. N. Sridevi, Sri. G. Ravi, Smt. K. Anusha\n"
        "• **AI & Emerging Technologies:** Sri. Ch. Venkata Rao, Smt. G. Swathi, Dr. K. Prasad, Sri. V. Satyanarayana, Smt. T. Devi, Dr. Y. Ramana, Sri. K. Gopi\n"
        "• **Electronics (ECE Wing):** Dr. V. Sailaja, Sri. P. Krishna, Smt. M. Deepthi, Sri. M. Satish\n"
        "• **Electrical Systems (EEE Wing):** Dr. S. N. Singh, Sri. T. Srinivas, Smt. K. Kamala\n"
        "• **Mechanical & Civil Infrastructures:** Dr. P. Kumar, Sri. J. Naidu, Sri. R. Prasad, Smt. V. Gowri, Sri. T. Pawan"
    ),
    "cse_faculty": (
        "💻 **CSE Department Academic Directory:**\n\n"
        "• **Head of Department (HOD):** **Dr. D. V. Manjula**\n"
        "• **Core Faculty Members Panel:** Dr. M. Radhika, Sri. P. Surya, Smt. S. Lakshmi\n"
        "• **Course Code Matrix:** `PRAG-CSE`"
    ),
    "aiml_faculty": (
        "🤖 **CSE (AI & ML) Department Academic Directory:**\n\n"
        "• **Head of Department (HOD):** **Dr. A. Radha Krishna**\n"
        "• **Core Faculty Members Panel:** Sri. Ch. Venkata Rao, Smt. G. Swathi, Dr. K. Prasad\n"
        "• **Course Code Matrix:** `PRAG-AIML`"
    ),
    "ece_faculty": (
        "📡 **ECE Department Academic Directory:**\n\n"
        "• **Head of Department (HOD):** **Dr. V. Prasanth**\n"
        "• **Core Faculty Members Panel:** Dr. V. Sailaja, Sri. P. Krishna, Smt. M. Deepthi\n"
        "• **Course Code Matrix:** `PRAG-ECE`"
    ),
    "hostel_general": (
        "🏢 **Hostel Accommodation & Availability:**\n\n"
        "• At present, **only Boys Hostel facilities** are available inside the college campus premises.\n"
        "• The average hostel fee structure is approximately **₹6,000 per month**.\n"
        "• High-security protocols, clean mess food facilities, and power backups are provided for hostlers."
    ),
    "hostel_girls": (
        "❌ **Girls Hostel Availability Notice:**\n\n"
        "• **No, currently there is NO Girls Hostel facility** available within the campus premises.\n"
        "• Hostels are exclusively functional for **Boys only** at this moment.\n"
        "• For girls traveling from nearby areas, the college provides extensive bus routing arrays."
    ),
    "bus_rajanagaram": (
        "🚌 **Rajanagaram Bus Route Details:**\n\n"
        "• **Annual Transport Fee:** **₹26,000 per year** for the Rajanagaram route.\n"
        "• To check exact timings, boarding points, and seat tracks, please immediately contact **Mr. Ramesh (Transport Incharge)** at **+91 94901 23456**."
    ),
    "bus_kakinada": (
        "🚌 **Kakinada (KKD) Bus Route Details:**\n\n"
        "• **Annual Transport Fee:** **₹25,000 per year** for the Kakinada route complex.\n"
        "• Contact **Mr. Ramesh (Transport Incharge)** at **+91 94901 23456** for boarding timelines."
    ),
    "bus_samalkota": (
        "🚌 **Samalkota Bus Route Details:**\n\n"
        "• **Annual Transport Fee:** **₹19,000 per year** for the Samalkota route framework.\n"
        "• Contact **Mr. Ramesh (Transport Incharge)** at **+91 94901 23456** for pickup charts."
    ),
    "bus_pitapuram": (
        "🚌 **Pitapuram Bus Route Details:**\n\n"
        "• **Annual Transport Fee:** **₹23,000 per year** for the Pitapuram location route.\n"
        "• Contact **Mr. Ramesh (Transport Incharge)** at **+91 94901 23456** for scheduling."
    ),
    "fees_general": (
        "💰 **Official College Fee Component Matrix Details:**\n\n"
        "• **Tuition Fee:** **₹77,800** per Academic Year\n"
        "• **CDC Training Fee:** **₹15,000**\n"
        "• **Uniform Package Fee:** **₹1,300** (*Includes 2 complete pairs of college uniforms*)\n"
        "• **Hostel Accommodation:** Approximately **₹6,000 / month** (*Exclusive Boys Hostel blocks*)"
    ),
    "infrastructure": (
        "🏫 **Pragati Campus Quadrant Infrastructure Split Map:**\n\n"
        "• **Main Block:** Hosts **CSE & IT Departments**, computational research labs, Principal Chambers, Seminar Halls, and the **CDC Cell Room**.\n"
        "• **Block 2:** Dedicated for **ECE, Cyber Security, and Civil Engineering** alongside labs.\n"
        "• **Block 3:** Houses the **EEE and Mechanical Engineering Departments**.\n"
        "• **Block 4:** Flagship block for **AI, AI & ML, and Data Science**.\n"
        "• **Campus Perks:** Full Playgrounds, **NCC support sets**, and a convenient **Xerox/Printing shop** situated right adjacent to the library building complex.\n"
        "• **Canteen Facilities:** Features premium items like customized **juice corners** running full swing during summers."
    ),
    "library": (
        "📚 **Central Reference Library Rules & Timings:**\n\n"
        "• **Normal Days:** Spend a maximum of 1 hour during designated windows to maintain standard seat tracks:\n"
        "  - Mid-day Slot: **12:00 PM to 1:30 PM**\n"
        "  - Evening Slot: **3:00 PM to 4:00 PM**\n"
        "• **Examination Periods:** Open doors! Unlimited reference and study access permitted throughout exams."
    ),
    "cdc": (
        "🚀 **Career Development Centre (CDC) Training Tracks:**\n\n"
        "• **Weekly Training:** Regular sessions specializing in **Aptitude, Soft Skills, and Assessment tests**.\n"
        "• **Coding Profiles Upgrades:** Tests are configured directly on platforms like **HackerRank and LeetCode** to continuously track behavior and growth performance indicators.\n"
        "• **Elite Corporate Alliances:** Ties with global brands like **ServiceNow and Salesforce**. Scores of alumni have completed certified courses, cracked evaluation pipelines, and secured high packages!"
    ),
    "festivals": (
        "🎉 **Flagship Annual Mega-Event Extravaganzas (3-Day Blocks):**\n\n"
        "• **STRIDES:** Technical Fest tracking tech paper presentations and coding sprints.\n"
        "• **PRISM:** Premium Cultural Fest celebrating dynamic fine arts and student performance panels.\n"
        "• **Pongal Samburalu:** Vibrant traditional setup events inside campus grounds right before family Pongal breaks."
    ),
    "summary": (
        "📝 **Comprehensive Campus Blueprint Summary Essay:**\n\n"
        "Pragati Engineering College (Autonomous), situated in Surampalem, stands as an institutional landmark renowned for its high academic standards, strict student code of conduct, and premier infrastructure configurations. The campus spans multiple distinct technological quadrants designed strategically to cluster computing, communication, and mechanical research laboratories. Driven by weekly soft-skills, analytical auditing tools on LeetCode/HackerRank, and prestigious certifications like ServiceNow, Pragati serves as a robust launchpad for corporate readiness, dynamic research, and all-round engineering excellence!"
    ),
    "about_college": "Pragati Engineering College holds a high **NAAC A+ accreditation status** with top placement ties!",
    "location_college": "Located at **3-180, ADB Road, Surampalem, Near Peddapuram, Kakinada District, Andhra Pradesh, 533437**."
}

HELP_DESK_TEXT = (
    "⚠️ **Pragati Campus Help Desk Help Line Incharges:**\n\n"
    "• 🚌 **Transport Routing Issues:** Mr. Ramesh (Transport Incharge) - **+91 94901 23456**\n"
    "• 🎓 **Academic Evaluation & Rules:** Exam Incharge Desk - **+91 94901 77777**\n"
    "• 🚀 **Placements Cell Room:** CDC Support Counter - **+91 94901 88888**\n"
    "• 📞 **General Administration Counter:** Front Desk Registrar Desk - **08852-252233**"
)

OPTION_NAMES_MAP = {
    "courses_only": "List of Engineering Courses",
    "hods_only": "Department HODs Directory",
    "faculty_only": "Core Faculty Profiles",
    "fees_general": "Fee Structure Parameters",
    "infrastructure": "Campus Layout & Infrastructure",
    "library": "Library Access Timings",
    "cdc": "CDC Cell & Career Internships",
    "festivals": "Annual Campus Festivals",
    "summary": "Full Campus Summary Essay"
}

ADVERTISER_POOL = [
    {"pitch": "Check out our amazing **Placements Cell (CDC)** details! Partnerships with **ServiceNow & Salesforce** are massive!", "option": "CDC Cell & Career Internships"},
    {"pitch": "Did you know about **STRIDES and PRISM**? They are our huge annual fests!", "option": "Annual Campus Festivals"},
    {"pitch": "Our campus layout is divided beautifully into **4 specialized department blocks**!", "option": "Campus Layout & Infrastructure"},
    {"pitch": "Shall we review our **Central Library rules or our dynamic summary essay**?", "option": "Library Access Timings"}
]

MEDIA_ELEMENTS = {
    "courses_only": '<iframe class="bot-embed-video" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
    "transport": '<iframe class="bot-embed-video" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
    "summary": '<iframe class="bot-embed-video" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
    "cdc": '<a href="https://in.linkedin.com/school/pragati-engineering-college/" target="_blank" class="bot-linkedin-badge"><i class="fa-brands fa-linkedin"></i> Explore Pragati Official LinkedIn Drive Feed</a>'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_flow', methods=['POST'])
def get_bot_flow():
    data = request.json
    action = data.get("action")
    user_msg = data.get("message", "").lower().strip()
    
    if action == "init_languages":
        return jsonify({
            "type": "languages",
            "text": "Welcome to Pragati Engineering College Help Desk! 🏫 Please select your tracking route layout below:",
            "options": ["English Menu Options", "Telugu / Tel-English Interactive Tracks"]
        })
        
    elif action == "select_lang":
        return jsonify({
            "type": "menu",
            "welcome": "Hello! I am your smart campus assistant. Ask me anything about Pragati Engineering College!",
            "options": ["Hostel Accommodation", "List of Engineering Courses", "Department HODs Directory", "Core Faculty Profiles"] + list(OPTION_NAMES_MAP.values())[3:] + ["🔗 View College FAQs Portal"]
        })
        
    elif action == "select_option":
        option = data.get("option")
        
        if "FAQs" in option:
            return jsonify({
                "type": "direct_answer",
                "text": "🔗 FAQ Portal: For quick references visit: [https://pragati.ac.in/faqs](https://pragati.ac.in/faqs)",
                "options": ["Full Campus Summary Essay"]
            })
            
        if option == "Hostel Accommodation":
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["hostel_general"], "options": ["Fee Structure Parameters"]})
            
        reverse_map = {v: k for k, v in OPTION_NAMES_MAP.items()}
        target_key = reverse_map.get(option, "summary")
        adv_choice = random.choice(ADVERTISER_POOL)
        
        return jsonify({
            "type": "direct_answer",
            "text": f"{CAMPUS_DATA[target_key]}\n\n---\n💬 **More Insights For You:**\n{adv_choice['pitch']}",
            "options": [option, adv_choice["option"]],
            "media": MEDIA_ELEMENTS.get(target_key, "")
        })

    elif action == "text_query":
        adv_choice = random.choice(ADVERTISER_POOL)
        
        

        # 🏢 1. Hostel Context Matrix
        if "girl" in user_msg and ("hostel" in user_msg or "room" in user_msg or "stay" in user_msg):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["hostel_girls"], "options": ["Transport Rules & Bus Fee"]})
        elif "boy" in user_msg and ("hostel" in user_msg or "room" in user_msg or "stay" in user_msg):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["hostel_general"], "options": ["Fee Structure Parameters"]})
        elif "hostel" in user_msg or "hostels" in user_msg or "accommodation" in user_msg:
            return jsonify({"type": "direct_answer", "text": f"Here are the core hostel specs for our campus:\n\n{CAMPUS_DATA['hostel_general']}", "options": ["Fee Structure Parameters"]})

        # 💻 2. Department Faculties & HOD Blocks
        elif "cse" in user_msg and ("faculty" in user_msg or "teacher" in user_msg or "hod" in user_msg or "prof" in user_msg):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["cse_faculty"], "options": ["CDC Cell & Career Internships"], "media": MEDIA_ELEMENTS["courses_only"]})
        elif ("aiml" in user_msg or "ai" in user_msg) and ("faculty" in user_msg or "teacher" in user_msg or "hod" in user_msg):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["aiml_faculty"], "options": ["CDC Cell & Career Internships"]})
        elif "ece" in user_msg and ("faculty" in user_msg or "teacher" in user_msg or "hod" in user_msg):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["ece_faculty"], "options": ["CDC Cell & Career Internships"]})
        elif "faculty" in user_msg or "faculties" in user_msg or "staff" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["faculty_only"], "options": ["Core Faculty Profiles", "Department HODs Directory"]})
        elif "hod" in user_msg or "heads" in user_msg or "head of" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["hods_only"], "options": ["Department HODs Directory", "List of Engineering Courses"]})

        # 🚌 3. Transport Bus Routes System
        elif "rajanagaram" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["bus_rajanagaram"], "options": ["Transport Rules & Bus Fee"], "media": MEDIA_ELEMENTS["transport"]})
        elif "kakinada" in user_msg or "kkd" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["bus_kakinada"], "options": ["Transport Rules & Bus Fee"], "media": MEDIA_ELEMENTS["transport"]})
        elif "samalkota" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["bus_samalkota"], "options": ["Transport Rules & Bus Fee"], "media": MEDIA_ELEMENTS["transport"]})
        elif "pitapuram" in user_msg:
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["bus_pitapuram"], "options": ["Transport Rules & Bus Fee"], "media": MEDIA_ELEMENTS["transport"]})
        elif "bus" in user_msg or "transport" in user_msg or "route" in user_msg:
            return jsonify({"type": "direct_answer", "text": f"Here is our standard transit profile overview:\n\n{CAMPUS_DATA['bus_rajanagaram']}", "options": ["Transport Rules & Bus Fee"], "media": MEDIA_ELEMENTS["transport"]})

        # 📝 4. General Info Queries
        elif any(x in user_msg for x in ["how is the", "about pragati", "review", "summary", "essay"]):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["summary"], "options": [adv_choice["option"]], "media": MEDIA_ELEMENTS["summary"]})
        elif any(x in user_msg for x in ["fee", "tution", "cost", "money"]):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["fees_general"], "options": ["Fee Structure Parameters"]})
        elif any(x in user_msg for x in ["where is", "location", "address", "surampalem"]):
            return jsonify({"type": "direct_answer", "text": CAMPUS_DATA["location_college"], "options": ["Transport Rules & Bus Fee"]})
        elif any(x in user_msg for x in ["contact", "number", "phone", "help", "incharge"]):
            return jsonify({"type": "direct_answer", "text": HELP_DESK_TEXT, "options": ["Full Campus Summary Essay"]})

        # Base Catch-all General Mapping Scanner
        mapping_nodes = {
            "courses_only": ["course", "branch", "branches", "program"],
            "infrastructure": ["canteen", "block", "playground", "ncc", "xerox", "labs", "campus"],
            "library": ["library", "book", "read"],
            "cdc": ["placement", "cdc", "internship", "hackerrank", "leetcode", "interview", "servicenow", "salesforce"],
            "festivals": ["fest", "strides", "prism", "event", "pongal"]
        }
        
        matched_key = None
        for key, tokens in mapping_nodes.items():
            if any(token in user_msg for token in tokens):
                matched_key = key
                break
                
        if matched_key:
            return jsonify({
                "type": "direct_answer",
                "text": CAMPUS_DATA[matched_key],
                "options": [OPTION_NAMES_MAP[matched_key], adv_choice["option"]],
                "media": MEDIA_ELEMENTS.get(matched_key, "")
            })
        else:
            return jsonify({
                "type": "direct_answer",
                "text": f"I couldn't quite match that sentence. Here are the contact points:\n\n{HELP_DESK_TEXT}",
                "options": ["Full Campus Summary Essay"]
            })

@app.route('/faqs')
def faqs_page():
    return render_template('faqs.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)