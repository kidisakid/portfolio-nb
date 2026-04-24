from django.shortcuts import render


PROFILE = {
    "name": "Neo Genesis Balignasay",
    "tagline": "Computer Science student — Data Science specialization. Full-stack developer turning ideas into working software.",
    "email": "neobalignasay@gmail.com",
    "phone": "0921-711-5827",
    "linkedin": "https://www.linkedin.com/in/neo-balignasay",
    "github": "https://github.com/kidisakid",
    "location": "University of Santo Tomas, Philippines",
}

TECHNICAL_SKILLS = [
    {"name": "Python", "level": "Advanced", "group": "Languages"},
    {"name": "Django", "level": "Proficient", "group": "Backend"},
    {"name": "Streamlit", "level": "Proficient", "group": "Backend"},
    {"name": "JavaScript", "level": "Proficient", "group": "Languages"},
    {"name": "React.js", "level": "Proficient", "group": "Frontend"},
    {"name": "Node.js / Express", "level": "Proficient", "group": "Backend"},
    {"name": "Java", "level": "Proficient", "group": "Languages"},
    {"name": "C#", "level": "Proficient", "group": "Languages"},
    {"name": "PHP", "level": "Familiar", "group": "Languages"},
    {"name": "Kotlin", "level": "Familiar", "group": "Languages"},
    {"name": "SQL", "level": "Advanced", "group": "Data"},
    {"name": "PostgreSQL / MySQL", "level": "Proficient", "group": "Data"},
    {"name": "MongoDB", "level": "Proficient", "group": "Data"},
    {"name": "Firebase", "level": "Familiar", "group": "Data"},
    {"name": "Tableau", "level": "Proficient", "group": "Analytics"},
    {"name": "SAS / R", "level": "Familiar", "group": "Analytics"},
    {"name": "Google Cloud", "level": "Proficient", "group": "Cloud"},
    {"name": "Git / GitHub", "level": "Advanced", "group": "Tools"},
    {"name": "AI & Agentic Workflows", "level": "Proficient", "group": "AI"},
]

SOFT_SKILLS = [
    {"name": "Fast Learner", "blurb": "Picks up new stacks and ships in days, not weeks."},
    {"name": "Project Leadership", "blurb": "Led full-cycle delivery on multiple client-facing projects."},
    {"name": "Research-Driven", "blurb": "Grounds decisions in literature and comparative analysis."},
    {"name": "Client Communication", "blurb": "Demos and deploys directly in clients' working environments."},
    {"name": "Hard Working", "blurb": "Owns the outcome from concept to cloud deployment."},
    {"name": "Systems Thinking", "blurb": "Architects clean module boundaries, not spaghetti."},
]

EXPERIENCE = {
    "role": "Innovations, R&D Intern",
    "company": "Rythmos DB, Inc.",
    "period": "February – April 2026",
    "bullets": [
        "Built a media analytics intelligence web application in Python (Streamlit + MongoDB).",
        "Integrated AI agents and automated documentation flows via Claude skills.",
        "Designed modular pipelines for data cleaning, transformation, and analysis.",
        "Shipped MongoDB-backed authentication with role-based access control and audit logging.",
        "Owned UI adjustments and front-end development across the tool suite.",
    ],
}

PROJECTS = [
    {
        "slug": "rdb",
        "title": "RDB Media Intelligence",
        "role": "R&D Intern — Rythmos DB",
        "stack": ["Python", "Streamlit", "MongoDB", "Pandas", "Claude API"],
        "description": (
            "A full media analytics pipeline — upload CSV/Excel, run cleaning, "
            "translation, topic clustering, and merging steps, then export. "
            "MongoDB-backed auth, role-based access, bcrypt hashing, and "
            "security audit logs."
        ),
        "highlight": "Live demo embedded above ↑",
        "link": None,
    },
    {
        "slug": "mcy",
        "title": "MCY Dental — EDHR",
        "role": "Project Developer · DevOps",
        "stack": ["React", "Node.js", "Express", "MongoDB", "Google Cloud"],
        "description": (
            "Electronic Dental Health Records patient management system, "
            "deployed to Google Cloud for active clinic use. Owned backend "
            "core features and cloud deployment."
        ),
        "highlight": "Live in a working clinic.",
        "link": None,
        "image": "img/mcy_dental.png",
    },
    {
        "slug": "pos",
        "title": "POS System",
        "role": "Full-Stack Developer",
        "stack": ["C#", ".NET", "WinForms", "SQL Server"],
        "description": (
            "A desktop point-of-sale with inventory management, item CRUD, "
            "and transaction handling. Built on Windows Forms with a local "
            "SQL Server database."
        ),
        "highlight": "Desktop-native, offline-capable.",
        "link": None,
    },
    {
        "slug": "quisti",
        "title": "Quisti",
        "role": "Project Head · Lead Developer · Researcher",
        "stack": ["Java", "Android Studio", "SQLite"],
        "description": (
            "A mobile quiz application built from ground-up concept to "
            "full-stack native Android. Research-backed methodology driving "
            "UX decisions."
        ),
        "highlight": "Original concept, shipped end-to-end.",
        "link": None,
    },
    {
        "slug": "malaria",
        "title": "CAE-CNN Malaria Classifier",
        "role": "Lead Researcher · Model Developer",
        "stack": ["Python", "TensorFlow", "Keras", "OpenCV"],
        "description": (
            "Thesis work — robust malaria classification from blood smear "
            "images using Convolutional Autoencoders + CNN ensembles. "
            "Comparative analysis across architectures."
        ),
        "highlight": "Undergraduate thesis.",
        "link": None,
    },
]

EDUCATION = [
    {
        "school": "University of Santo Tomas",
        "period": "2022 – Present",
        "detail": "BS Computer Science, specialization in Data Science.",
    },
    {
        "school": "STI College Sta. Maria",
        "period": "2020 – 2022",
        "detail": "ICT — Mobile App & Web Development. Graduated with High Honors.",
    },
]

CERTIFICATIONS = [
    {
        "name": "PHILNITS IT Passport Certification",
        "date": "October 2025",
    },
]


def index(request):
    return render(
        request,
        "index.html",
        {
            "profile": PROFILE,
            "technical_skills": TECHNICAL_SKILLS,
            "soft_skills": SOFT_SKILLS,
            "experience": EXPERIENCE,
            "projects": PROJECTS,
            "education": EDUCATION,
            "certifications": CERTIFICATIONS,
        },
    )
