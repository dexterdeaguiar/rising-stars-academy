from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "forms" / "modern"
LOGO = ROOT / "assets" / "brand" / "rs-logo-transparent.png"

NAVY = colors.HexColor("#153A5B")
BLUE = colors.HexColor("#13A4EC")
GOLD = colors.HexColor("#D8B04C")
INK = colors.HexColor("#263342")
MUTED = colors.HexColor("#65758B")
LINE = colors.HexColor("#D7E1EA")
SOFT = colors.HexColor("#F4F8FB")
PALE_GOLD = colors.HexColor("#FFF8E7")

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 16 * mm
CONTENT_W = PAGE_W - (2 * MARGIN_X)


def make_styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "BrandTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=23,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "DocSubtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=BLUE,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceBefore=9,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "SmallSection",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11.4,
            textColor=INK,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "BodyTight",
            parent=base["Body"],
            fontSize=8,
            leading=10.2,
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            "Tiny",
            parent=base["Body"],
            fontSize=7.2,
            leading=9.2,
            textColor=MUTED,
        )
    )
    base.add(
        ParagraphStyle(
            "RightTiny",
            parent=base["Tiny"],
            alignment=TA_RIGHT,
        )
    )
    base.add(
        ParagraphStyle(
            "CenterSmall",
            parent=base["Body"],
            alignment=TA_CENTER,
            fontSize=8,
            leading=10,
        )
    )
    return base


S = make_styles()


def p(text, style="Body"):
    return Paragraph(text, S[style])


def bullet_items(items, style="BodyTight"):
    return ListFlowable(
        [ListItem(p(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        start="circle",
        bulletFontSize=4,
        leftIndent=12,
        bulletIndent=2,
        spaceBefore=2,
        spaceAfter=4,
    )


def checkbox_table(items, cols=2):
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for item in items[i : i + cols]:
            row.append(p("[  ] " + item, "BodyTight"))
        while len(row) < cols:
            row.append("")
        rows.append(row)
    widths = [CONTENT_W / cols] * cols
    table = Table(rows, colWidths=widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def section_box(title, body, bg=SOFT):
    if isinstance(body, list):
        body_flowables = body
    elif hasattr(body, "_content"):
        body_flowables = body._content
    else:
        body_flowables = [body]
    content = [[p(title, "SmallSection")], [body_flowables]]
    table = Table(content, colWidths=[CONTENT_W], splitByRow=0)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def field_table(fields, cols=2, row_h=11 * mm):
    rows = []
    for i in range(0, len(fields), cols):
        row = []
        for label in fields[i : i + cols]:
            row.append(p(f"<font color='{NAVY.hexval()}'><b>{label}</b></font><br/>" + "_" * 42, "BodyTight"))
        while len(row) < cols:
            row.append("")
        rows.append(row)
    table = Table(rows, colWidths=[CONTENT_W / cols] * cols, rowHeights=[row_h] * len(rows), hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    return table


def signature_block(items):
    rows = [[p(label, "BodyTight"), p("________________________________________", "BodyTight")] for label in items]
    table = Table(rows, colWidths=[55 * mm, CONTENT_W - 55 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def doc_header(canvas, doc, title):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = PAGE_H - 12 * mm
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_X, y - 6, PAGE_W - MARGIN_X, y - 6)
    canvas.setFont("Helvetica-Bold", 7.6)
    canvas.setFillColor(NAVY)
    canvas.drawString(MARGIN_X, y, "Rising Stars Academy")
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MARGIN_X, y, f"{title} | Page {doc.page}")
    canvas.restoreState()


def build_doc(filename, title, subtitle, story):
    path = OUT / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP + 6 * mm,
        bottomMargin=MARGIN_BOTTOM,
        title=title,
        author="Rising Stars Academy",
    )
    doc.build(story, onFirstPage=lambda c, d: doc_header(c, d, title), onLaterPages=lambda c, d: doc_header(c, d, title))
    return path


def title_block(title, subtitle):
    img = Image(str(LOGO), width=34 * mm, height=34 * mm)
    img.hAlign = "CENTER"
    return [
        img,
        Spacer(1, 3 * mm),
        p(title, "BrandTitle"),
        p(subtitle, "DocSubtitle"),
        Spacer(1, 2 * mm),
    ]


def banking_box(deposit):
    data = [
        [p("<b>Bank</b>", "BodyTight"), p("Capitec Business Banking", "BodyTight")],
        [p("<b>Account holder</b>", "BodyTight"), p("Sharp Move Trading 70 Pty", "BodyTight")],
        [p("<b>Account no.</b>", "BodyTight"), p("105 062 6966", "BodyTight")],
        [p("<b>Branch code</b>", "BodyTight"), p("450 105", "BodyTight")],
        [p("<b>Reference</b>", "BodyTight"), p("Your child/children's name and surname", "BodyTight")],
    ]
    table = Table(data, colWidths=[38 * mm, CONTENT_W - 38 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
                ("BOX", (0, 0), (-1, -1), 0.5, GOLD),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E8D9A4")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return section_box(
        "Deposit and Banking Details",
        KeepTogether(
            [
                p(f"Non-refundable deposit payable on acceptance/submission: <b>{deposit}</b>.", "BodyTight"),
                Spacer(1, 2 * mm),
                table,
                p("Fees for each month are payable in advance by the 1st of every month.", "Tiny"),
            ]
        ),
        bg=PALE_GOLD,
    )


def primary_high_intro(level, grade_label, report_label):
    docs = [
        ("Child's unabridged birth certificate", "If unavailable, attach the abridged certificate with Home Affairs receipt confirming application for the unabridged certificate."),
        ("Clinic card", "Required for Grade 1 learners; otherwise provide proof of immunisation or a doctor's letter."),
        ("Proof of address", "Municipal account, signed lease, purchase contract or estate agent confirmation valid for at least one year."),
        ("Private residence / tenancy", "Owner's certified proof of address, certified ID document and affidavit confirming tenancy."),
        ("Parents' ID documents", "Both biological parents' ID documents or passports."),
        (report_label, "Latest school report or full academic history where applicable."),
        ("Transfer document", "Required if the learner comes from another school; hand in on or before the first school day."),
    ]
    rows = [[p("<b>Attached</b>", "BodyTight"), p("<b>Required document</b>", "BodyTight"), p("<b>Notes</b>", "BodyTight")]]
    for title, note in docs:
        rows.append([p("[  ]", "CenterSmall"), p(title, "BodyTight"), p(note, "BodyTight")])
    table = Table(rows, colWidths=[22 * mm, 52 * mm, CONTENT_W - 74 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story = title_block("Application for Admission", f"{level} | {grade_label} | 2026")
    story += [
        p("Dear prospective parents/guardians,", "Body"),
        p("It is our pleasure to make this application package for admission to our school available to you.", "Body"),
        section_box(
            "Application Steps",
            KeepTogether(
                [
                    p("<b>Step 1:</b> Complete the application form in full, sign it and attach all required documentation. Submit the application package to the enrolment officer between 08:00 and 14:00, Monday to Friday. Parents must attach proof of online application on submission. Enrolment will only be considered once all necessary documentation has been received.", "BodyTight"),
                    p("<b>Step 2:</b> Visit the school for a guided tour of the campus. Successful parents will be notified via email, telephone or verbal communication and invited to a compulsory meet and greet with the Principal. Unsuccessful applicants will also be notified.", "BodyTight"),
                ]
            ),
        ),
        p("Financial Obligation", "Section"),
        p("Rising Stars Academy is a fee-paying school. School fees are determined by the Board of Trustees each year and are payable on the 1st of every month for the month in advance. New enrolments are requested to pay the non-refundable deposit and first month's school fee upon acceptance of enrolment. Payment is subject to the school fee collection policy.", "Body"),
        p("Parents' evenings take place within the first three to four weeks of the new term, where operational information and parent responsibilities are discussed.", "Body"),
        p("We trust that your child's school career at Rising Stars Academy will be a happy and educationally stimulating one.", "Body"),
        p("Compulsory Documentation", "Section"),
        p("Incomplete applications, or applications submitted without all required documents, may be declined.", "BodyTight"),
        table,
        p("Additional Documentation", "Section"),
        checkbox_table(
            [
                "Non-SA citizens: valid study permit issued by the Department of Home Affairs.",
                "Foster parents: Section 159 documentation as stipulated in the Children's Act 38 of 2005 and letter from registered social worker.",
                "Guardianship: court documents and guardian ID documents.",
                "Completed application form.",
                "General consent form.",
                "Undertaking on admission.",
                "Statutory obligation notice.",
            ],
            cols=1,
        ),
        banking_box("R3 000,00"),
        p("School trading hours: Full day Monday to Friday 06:30 to 18:00. Half day Monday to Friday 06:30 to 14:30.", "Tiny"),
        PageBreak(),
    ]
    return story


def learner_page(level):
    fields = [
        "Surname",
        "Full names",
        "Name by which learner is called",
        "Gender",
        "Date of birth",
        "ID / passport / permit number",
        "Current grade",
        "Home language",
        "Preferred language",
        "Certificate language",
        "Nationality",
        "CEMIS number",
        "Name of previous school",
        "Previous province",
    ]
    story = [
        p("Application Form", "Section"),
        section_box(
            "For Office Use Only",
            field_table(["Admitted", "Date of admission", "CEMIS number", "Profile received", "Requested grade"], cols=5, row_h=10 * mm),
        ),
        p("Section A: Learner Information", "Section"),
        p("Complete sections A, B and C. Failure to complete all sections may result in the application being declined.", "BodyTight"),
        field_table(fields, cols=2),
        p("Disability / Support Needs", "SmallSection"),
        checkbox_table(["Deaf", "Blind", "Hard of hearing", "Partially sighted", "None", "Epilepsy", "Psychiatric support", "Specialised support", "Other: __________________________"], cols=3),
        p("Brothers and Sisters Currently at Rising Stars Academy", "SmallSection"),
        field_table(["Name and surname / grade", "Name and surname / grade", "Name and surname / grade", "Name and surname / grade"], cols=2),
        PageBreak(),
    ]
    return story


def parent_page():
    row_labels = [
        "Title",
        "Relationship to learner",
        "Initials",
        "Full names",
        "Surname",
        "ID / passport number",
        "Residential address",
        "Postal code",
        "Occupation",
        "Employer",
        "Work telephone",
        "Home telephone",
        "Cellphone",
        "Work email",
        "Home email",
        "Marital status",
    ]
    rows = [[p("", "BodyTight"), p("<b>Father / Guardian</b>", "BodyTight"), p("<b>Mother / Guardian</b>", "BodyTight")]]
    for label in row_labels:
        rows.append([p(f"<b>{label}</b>", "BodyTight"), p("_" * 34, "BodyTight"), p("_" * 34, "BodyTight")])
    table = Table(rows, colWidths=[42 * mm, (CONTENT_W - 42 * mm) / 2, (CONTENT_W - 42 * mm) / 2], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return [
        p("Section B: Parent, Adoptive Parent or Guardian Information", "Section"),
        p("The school liaises with the biological parent, step-parent, guardian or sponsor with whom the child resides. This parent is considered the main parent and will receive correspondence. As the Principal acts in loco parentis during school hours, partner details are also required where applicable.", "BodyTight"),
        table,
        Spacer(1, 3 * mm),
        signature_block(["Signature: Parent / Guardian", "Signature: Parent / Guardian", "Date"]),
        PageBreak(),
    ]


def medical_page():
    return [
        p("Section C: Medical Information", "Section"),
        p("Compulsory for parent/guardian to complete.", "BodyTight"),
        field_table(["Allergies", "Medication required", "Operations learner has had", "Doctor / clinic name", "Doctor / clinic telephone number", "Blood group", "Medical aid name", "Medical aid number"], cols=2),
        p("Illnesses the Learner Has Had", "SmallSection"),
        checkbox_table(["Measles", "German measles", "Whooping cough", "Chicken-pox", "Mumps", "Other: ____________________"], cols=3),
        p("Immunisations", "SmallSection"),
        checkbox_table(["Tuberculosis (B.C.G.)", "Diphtheria", "Whooping cough", "Tetanus", "Measles", "Poliomyelitis"], cols=3),
        p("All learners should be immunised against the above illnesses before school attendance. Immunisation against poliomyelitis and Tuberculosis (B.C.G.) is legally compulsory. Written evidence is required when a learner is admitted to a Western Cape Education Department school for the first time.", "BodyTight"),
        p("Emergency Contact", "SmallSection"),
        field_table(["Full name", "Contact number", "Relationship to learner"], cols=3),
        p("Persons Authorised to Collect the Learner", "SmallSection"),
        field_table(["Surname / name / contact / relationship", "Surname / name / contact / relationship", "Surname / name / contact / relationship", "Surname / name / contact / relationship"], cols=2),
        section_box("Declaration", p("I, the undersigned, understand that the school reserves the right to verify all information supplied via this application. In the event of fraudulent documents, the school reserves the right to lay criminal charges of fraud against any parties to this application.", "BodyTight")),
        signature_block(["Signature", "Name", "Date"]),
        PageBreak(),
    ]


UNDERTAKING_ITEMS = [
    "Support the school as partner in the educational process and co-operate with the school, teacher and Principal for the duration of the learner's association with Rising Stars Academy and its Board of Trustees.",
    "Comply with, accept and acknowledge the school's code of conduct and school rules, admission policy, academic and homework policy, and attendance policy.",
    "Reimburse the school for any damage to school property caused by the learner.",
    "Understand that while reasonable effort is made to prevent loss or damage to clothing and equipment, the school cannot be held liable in such event.",
    "Give written notice of any intention to remove the learner from the school, return school books/equipment and ensure the school fee account is settled in full before leaving.",
    "Ensure the learner is punctual at the beginning of each day and collected on time at the end of the school day.",
    "Accept that the school may verify information supplied and may lay criminal charges in the event of fraudulent documents.",
    "Accept responsibility for immunising the learner against contagious diseases and producing proof if required.",
    "Inform the educator of the learner's absence from school and produce a doctor's certificate when required.",
    "Accept that Rising Stars Academy and its Board of Trustees may amend the Code of Conduct, School Rules, Discipline Policy, Homework Policy and Admission Policy.",
    "Understand that the Principal or authorised agent may act in loco parentis when specific authority cannot reasonably be sought or obtained in time.",
    "Inform the school in writing of any change of address, email address or cell phone number.",
    "Confirm that all forms have been completed accurately and that all information supplied is true.",
    "Accept responsibility for the school fee monthly account and ensure payment by the first (1st) of every month, for the month in advance.",
    "Agree that non-payment may result in further action by the school, including suspension of services or expulsion depending on the situation.",
    "Accept that this agreement, acknowledgement and commitment remains valid from signature until the learner officially leaves the school.",
]


def undertaking_page():
    return [
        p("Undertaking on Admission", "Section"),
        p("I/We, the parent(s) or legal guardian(s) of __________________________________________ Grade ______ hereby confirm and undertake that he/she and I/we:", "Body"),
        bullet_items(UNDERTAKING_ITEMS),
        p("I, legal parent/guardian __________________________________________, hereby undertake, understand, comply with and fully agree to the above-mentioned understandings, acceptances and policies as set out by the Board of Trustees of Rising Stars Academy and the South African Schools Act.", "BodyTight"),
        signature_block(["Signature: Parent / Guardian", "Date"]),
        PageBreak(),
    ]


def consent_page():
    return [
        p("General Consent Form", "Section"),
        p("It is widely recognised that attendance at school or any school activity, including participation in excursions, games, sporting or other activities at or through the school, and the use of transport arranged by the school, may entail risks for a learner. Such risks are part and parcel of life and education.", "BodyTight"),
        p("Acknowledging the foregoing, I, __________________________________________, parent and/or legal guardian of __________________________________________, hereby consent to my son/daughter participating in activities arranged, organised or offered by the school, and where relevant, being transported to and from activities by transport made available by the school.", "BodyTight"),
        p("I further agree that such participation or use shall be at the risk of the learner and parent/guardian. Insofar as every reasonable and practicable precaution is taken for safety and welfare, I hold blameless Rising Stars Academy and associated persons/organisations should loss, damage, illness or injury occur, unless caused by negligence, wilfulness or deliberate act of the school or its employees.", "BodyTight"),
        p("I appoint school staff accompanying or supervising an activity to act in loco parentis should the need arise and to take reasonable steps if the learner becomes ill, injured or requires medical attention.", "BodyTight"),
        p("Relevant Medical Information", "SmallSection"),
        p("Does your son/daughter have any medical condition or allergy of which teachers need to be aware?", "BodyTight"),
        checkbox_table(["Yes", "No"], cols=2),
        field_table(["Details", "Medical aid society", "Medical aid number", "Principal member", "Medical practitioner contact", "Emergency contact telephone numbers"], cols=2),
        signature_block(["Signature: Parent / Guardian", "Signature: Witness", "Date"]),
        PageBreak(),
    ]


STATUTORY = [
    ("Definitions", [
        '"the Act" means the South African Schools Act 84 of 1996 and all regulations promulgated under it.',
        '"the parent" means the parent or guardian of a learner, the person legally entitled to custody of a learner, or the person who undertakes the obligations of a parent towards the learner\'s education at school.',
        '"School fees" means school fees contemplated in Section 39 and includes monetary contributions in relation to attendance or participation in any school programme.',
        '"the Capital sum" means the school fees in full per annum with any further costs or damages, including attorney/client fees and collection costs that may occur.',
        '"BOT" means a meeting of the School Board of Trustees in terms of the Act.',
    ]),
    ("Annual School Fees", [
        "The annual school fee will be a compulsory sum for 2026 determined by the Board of Trustees and may escalate for every consecutive year.",
        "School fees are payable on the first (1st) of every month for the month in advance.",
        "Biological parents are jointly liable for payment of school fees irrespective of marital status.",
    ]),
    ("Notices and Contact Details", [
        "The parent chooses a domicilium citandi et executandi for all notices and must update the school in writing when details change.",
        "Any notice or process delivered by hand is deemed received on the date of delivery; registered post is deemed received seven (7) days after posting.",
        "A notice actually received by the parent constitutes proper delivery even if not delivered in terms of the above.",
    ]),
    ("Non-payment and Recovery", [
        "In the event of non-payment and on demand under the Act, the parent acknowledges being indebted to the school for the capital sum.",
        "The school may enforce payment of fees.",
        "The parent consents to confidential information being processed for administration, collection, tracing, research, updating and related school operations.",
        "The school may obtain from and disclose to a third party, including a credit bureau, relevant credit record, payment history and related information for affordability enquiry and record updates.",
        "If the parent fails to update required details, the school may instruct a tracing agent and the parent will be liable for tracing fees.",
        "Disputes on statements of account must be raised with the financial office in writing.",
        "This commitment does not fall under the National Credit Act. The school follows the legal framework applicable to statutory school fee debt.",
    ]),
    ("General Terms", [
        "A reference to any gender includes the other genders; singular includes plural and vice versa; a natural person includes a juristic person and vice versa.",
        "I/We undertake to give one term's written notice of any intention to remove my/our child from the school and to return any books or equipment belonging to the school.",
        "In the event of fraudulent documents, the school reserves the right to lay a criminal charge of fraud against any parties to this application.",
        "This commitment remains valid from signature until the pupil officially leaves the school.",
        "No alteration, variation, amendment or cancellation shall be of force unless reduced to writing and signed by or on behalf of the parent and creditor.",
        "If any provision is unenforceable, void or voidable, it is severable and the remaining provisions remain in full force and effect.",
    ]),
]


def statutory_pages():
    story = [
        p("Statutory Obligation Notice", "Section"),
        p("Kindly note that all parents/guardians must complete this form in full and in print.", "BodyTight"),
        checkbox_table(["Father", "Mother", "Guardian"], cols=3),
        field_table(["Parent/guardian full name", "Learner full name", "Grade applied for"], cols=3),
    ]
    for heading, items in STATUTORY[:3]:
        story += [p(heading, "SmallSection"), bullet_items(items)]
    story += [
        p("Domicilium / Contact Details", "SmallSection"),
        field_table(["Full name and surname", "Physical address", "Email address", "Contact number"], cols=2),
        PageBreak(),
    ]
    story += [p("Statutory Obligation Notice Continued", "Section")]
    for heading, items in STATUTORY[3:]:
        story += [p(heading, "SmallSection"), bullet_items(items)]
    story += [
        p("Declaration", "SmallSection"),
        p("I/We hereby declare that I/we are the only known parent(s) to the learner.", "BodyTight"),
        field_table(["Signed at", "Day", "Month", "Year 20__"], cols=4, row_h=10 * mm),
        signature_block(["Father: print name and surname", "Father: signature in full", "Father: ID number", "Relationship to learner", "Mother: print name and surname", "Mother: signature in full", "Mother: ID number", "Relationship to learner", "Witness: print name and surname", "Witness: signature", "Witness: contact telephone number"]),
    ]
    return story


def build_primary_high(level, filename, grade_label, report_label):
    story = []
    story += primary_high_intro(level, grade_label, report_label)
    story += learner_page(level)
    story += parent_page()
    story += medical_page()
    story += undertaking_page()
    story += consent_page()
    story += statutory_pages()
    return build_doc(filename, f"{level} Application Form", f"{grade_label} | 2026", story)


def build_ecd():
    story = title_block("ECD Enrolment Application", "Early Childhood Development | 2026")
    story += [
        p("Sharp Move Trading 70 Pty (Ltd) | Reg No: 2004/024982/07", "CenterSmall"),
        p("6 Circle Road, Table View, 7441 | admin@risingstarsacademy.co.za | 021 822 5400", "CenterSmall"),
        p("Social Development: 15/5/13/2/2 T9662 | WCED: 13/14/4 H52289", "CenterSmall"),
        Spacer(1, 2 * mm),
        p("Dear Parents,", "Body"),
        p("We would like to welcome you and your child/children to our school. Below is a breakdown of the rules and regulations to ensure a peaceful and safe environment for all to enjoy.", "Body"),
        section_box(
            "Hours and Collection",
            KeepTogether(
                [
                    p("<b>Full day:</b> 06:30 to 18:00<br/><b>Half day:</b> 06:30 to 14:30", "BodyTight"),
                    p("Please be punctual in collecting your child. Any child collected after 18:00 will be charged R50.00 per 15 minutes or any part thereof.", "BodyTight"),
                    p("Please inform the Principal or teacher if your child is to be collected by anyone other than a parent, otherwise we will not allow your child to leave the Academy.", "BodyTight"),
                ]
            ),
        ),
        p("Health, Meals and Belongings", "Section"),
        p("All medication must be given to your child's teacher, who will record the dosage in the medical record file. If your child is not feeling well, please mention this to their teacher so your child can be monitored. If your child has a contagious disease, please notify us.", "BodyTight"),
        p("Breakfast, morning snack and lunch are provided. Please pack only a healthy afternoon snack and do not allow your child to bring sweets, chips or toys to the Academy. Breakfast is served between 08:00 and 08:30 and is served up to and including the Grade R class.", "BodyTight"),
        p("Please Supply Clearly Marked Items", "SmallSection"),
        bullet_items(["Sun hat and sun block.", "Mattress cover (120cm x 60cm).", "A change of clothing in case of little accidents."]),
        p("Children Must Stay Home If They Show Any of the Following", "SmallSection"),
        bullet_items([
            "Contagious illness such as chicken pox, measles or mumps.",
            "Vomiting two or more times.",
            "Two or abnormally loose stools.",
            "Contagious conjunctivitis or pus draining from the eye.",
            "Bacterial infection such as streptococcal pharyngitis or impetigo.",
            "Untreated hair lice, ringworm or scabies.",
            "An undiagnosed rash or a rash attributable to contagious illness.",
            "Not able to participate in Academy activities with reasonable comfort.",
            "Requires more care than staff can provide without compromising the health and safety of other children.",
        ]),
        p("It is the responsibility of each parent to ensure alternative arrangements are available if they cannot collect an ill child.", "BodyTight"),
        p("Application Requirements", "Section"),
        checkbox_table(["Application fee", "Certified copy of learner's birth certificate", "Certified copies of parents' identity documents", "Immunisation records"], cols=1),
        PageBreak(),
        p("Enrolment Application", "Section"),
        field_table(["Date", "Child's surname", "Child's first names", "Date of birth", "Residential address", "Postal address", "Position in family"], cols=1, row_h=10 * mm),
        p("Parent / Guardian Details", "Section"),
        field_table(["Mother's name", "Mother's address", "Mother's home number", "Mother's work number", "Mother's cell number", "Mother's email", "Mother's employer name/address", "Father's name", "Father's address", "Father's home number", "Father's work number", "Father's cell number", "Father's email", "Father's employer name/address"], cols=2),
        PageBreak(),
        p("Emergency, Medical and Pick-up Permission", "Section"),
        field_table(["Alternative contact person and relationship", "Home number", "Work number", "Cell number", "Child's doctor name", "Doctor telephone number", "Medical aid number"], cols=2),
        p("Medical Information: Allergies and/or Important Information", "SmallSection"),
        field_table(["Details", "Additional comments / information"], cols=1, row_h=16 * mm),
        p("Pick-up Permission Form", "SmallSection"),
        p("I hereby give permission for my child ________________________________________ to leave Rising Stars Academy with the following persons named below.", "BodyTight"),
        field_table(["Name / relationship / ID no.", "Name / relationship / ID no.", "Name / relationship / ID no."], cols=1, row_h=11 * mm),
        signature_block(["Signature of parent", "Date"]),
        PageBreak(),
        p("Consent and Indemnity", "Section"),
        p("I, __________________________________________, residing at __________________________________________, the parent/legal guardian, give consent for my child to take part in educational tours and excursions while attending Rising Stars Academy.", "BodyTight"),
        p("I fully understand and accept that while every effort is made by Rising Stars Academy to transport my child/children safely, all tours and excursions shall be undertaken at my child's own risk. I undertake on behalf of myself, my executors, my spouse and child to indemnify the Principal and staff against claims that may arise in connection with loss or damage to property or injury to my child, in the knowledge that the Principal and staff will take all reasonable precautions for the safety and welfare of my child.", "BodyTight"),
        signature_block(["Signature of parent/legal guardian"]),
        p("I have read, understood and will abide by the rules and regulations of Rising Stars Academy.", "BodyTight"),
        signature_block(["Signature", "Date"]),
        banking_box("R1 000,00"),
        PageBreak(),
        p("Contract of Enrolment", "Section"),
        p("I/we am/are the legal guardian(s) of the learner whose details appear on the application form. I/we have read and understood the policies of the school as published by the school.", "BodyTight"),
        p("Policies of the School", "SmallSection"),
        bullet_items([
            "I/we agree to abide by these policies, including the Debtors Policy, Terms and Conditions of the School, and the School's cautionary and grievance procedures as adopted from time to time.",
            "I/we undertake to abide by and comply with all rules and regulations of the school and acknowledge that it is incumbent upon me/us to become familiar with them.",
            "I/we acknowledge responsibility for my/our child after the published finishing times of any school activity, event or function.",
            "I/we will ensure that the learner abides by all applicable policies.",
            "The school reserves the right to give a shorter period of notice of termination should the Head determine it appropriate.",
        ]),
        p("Disclaimer and Withdrawal", "SmallSection"),
        bullet_items([
            "The school does not take responsibility for theft, loss, damage or destruction of any property brought onto school premises.",
            "I/we undertake to give one month's written notice to the Head for withdrawal. If such notice is not given, a full month's fees shall be paid in lieu of notice.",
            "One full month's fees are payable in the event of withdrawal between acceptance of a place and the beginning month.",
            "If the school elects for adequate reason to terminate enrolment, it may do so on one month's notice.",
        ]),
        PageBreak(),
        p("Payment of Fees and Acknowledgement of Debt", "Section"),
        bullet_items([
            "Fees for each month are payable in advance by the 1st of every month.",
            "With the exception of annual and termly payments in advance, fees are payable via cash, debit card or internet.",
            "If payment is not made within the prescribed period, a surcharge may be levied, the whole balance may become due and payable, and the Head may prevent attendance until fees are paid.",
            "Should fees remain unpaid, the Head may fill the learner's place without prejudice to the claim for fees in lieu of notice.",
            "I/we assume absolute responsibility for payment of fees and acknowledge that facilities exist for monthly payments.",
            "I/we agree in terms of Section 45 of the Magistrate's Court Act No. 32 of 1944 that the school may institute legal proceedings for recovery of monies owing.",
            "In the event of legal action to recover fees, I/we shall be liable for costs incurred by the school as between attorney and client.",
            "I/we confirm that all particulars furnished are full, true and accurate and undertake to advise the school in writing of any changes.",
        ]),
        p("I/we accept the offer of a place for: __________________________________________", "BodyTight"),
        signature_block(["Signature of first parent/guardian", "Signature of second parent/guardian", "Date"]),
    ]
    return build_doc("ECD-Enrolment-Form-2026-Redesigned.pdf", "ECD Enrolment Application", "Early Childhood Development | 2026", story)


def build_fees():
    story = title_block("2026 Fee Structure", "Pre-Primary | Primary School | High School")
    pre = [
        ("Registration fee", "R 1 000,00"),
        ("Bunny Class: 3 months - 18 months", "R 3 020,00"),
        ("Teddy Tiny Tots: 18 months - 2 years", "R 3 020,00"),
        ("Teddy Class: 2 years - 3 years", "R 3 020,00"),
        ("Hippo Class: 3 years - 4 years", "R 3 020,00"),
        ("Tiger Class: 4 years - 5 years", "R 3 300,00"),
        ("Grade RR", "R 4 525,00"),
    ]
    primary = [
        ("Registration fee", "R 3 000,00"),
        ("Grade 1 - Grade 7 half day fee *", "R 6 150,00"),
        ("Grade 1 - Grade 7 full day fee *", "R 6 440,00"),
    ]
    high = [
        ("Registration fee", "R 3 000,00"),
        ("Grade 8 - Grade 12", "R 6 440,00"),
    ]

    def fee_table(title, rows):
        data = [[p(f"<b>{title}</b>", "BodyTight"), p("<b>Monthly fee</b>", "BodyTight")]]
        data += [[p(a, "BodyTight"), p(b, "BodyTight")] for a, b in rows]
        table = Table(data, colWidths=[CONTENT_W - 38 * mm, 38 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table

    story += [
        p("All fees are payable in advance by the 1st of every month. Registration fees are payable on acceptance/submission as applicable.", "Body"),
        fee_table("Pre-Primary Tuition Fees", pre),
        Spacer(1, 4 * mm),
        fee_table("Primary School Tuition Fees", primary),
        Spacer(1, 4 * mm),
        fee_table("High School Tuition Fees", high),
        Spacer(1, 5 * mm),
        section_box(
            "Primary School Timing Notes",
            KeepTogether(
                [
                    p("* Half day for Primary School ends at 14:30 and does not include aftercare services.", "BodyTight"),
                    p("* Full day for Primary School ends at 18:00 and includes aftercare services.", "BodyTight"),
                ]
            ),
        ),
    ]
    return build_doc("Rising-Stars-Academy-Fees-2026-Redesigned.pdf", "2026 Fee Structure", "Pre-Primary | Primary | High School", story)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    generated = [
        build_primary_high("Primary School", "Primary-School-Enrolment-Form-2026-Redesigned.pdf", "Grade 1 - Grade 7", "Latest school report / Grade 1 June report where applicable"),
        build_primary_high("High School", "High-School-Enrolment-Form-2026-Redesigned.pdf", "Grade 8 - Grade 12", "Latest school report / full academic history where applicable"),
        build_ecd(),
        build_fees(),
    ]
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
