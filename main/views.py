from django.shortcuts import render


PROFILE = {
    "name": "Neo Genesis Balignasay",
    "tagline": (
        "BS Computer Science — Data Science specialization at UST. "
        "I build data pipelines, train models, and ship AI-augmented tools."
    ),
    "email": "neobalignasay@gmail.com",
    "phone": "0921-711-5827",
    "linkedin": "https://www.linkedin.com/in/neo-balignasay",
    "github": "https://github.com/kidisakid",
    "location": "University of Santo Tomas, Philippines",
}

# Three pillars shown in the hero "focus areas" strip.
FOCUS_AREAS = [
    {
        "tag": "01",
        "name": "Data Engineering",
        "blurb": "ETL, cleaning, transformation, and pipeline design — Python, Pandas, SQL.",
    },
    {
        "tag": "02",
        "name": "ML & Deep Learning",
        "blurb": "Model training and comparison — scikit-learn, TensorFlow, Keras, OpenCV.",
    },
    {
        "tag": "03",
        "name": "AI & Agentic Systems",
        "blurb": "LLM integration, tool use, and automated workflows with Claude.",
    },
]

# Grouped so the Hero can render a categorised matrix instead of a flat chip list.
SKILL_GROUPS = [
    {
        "name": "Data & ML",
        "tag": "/ data-ml",
        "items": [
            "Python", "Pandas", "NumPy", "scikit-learn",
            "TensorFlow", "Keras", "OpenCV",
            "Jupyter", "Matplotlib", "Seaborn",
        ],
    },
    {
        "name": "AI & LLMs",
        "tag": "/ ai",
        "items": [
            "Claude API", "Agentic Workflows", "Tool Use",
            "RAG Patterns", "Prompt Engineering", "AI Automation",
        ],
    },
    {
        "name": "Analytics",
        "tag": "/ analytics",
        "items": ["Tableau", "SAS", "R", "Statistical Analysis"],
    },
    {
        "name": "Databases",
        "tag": "/ data-stores",
        "items": [
            "SQL", "PostgreSQL", "MySQL",
            "MongoDB", "Firebase", "Microsoft Access",
        ],
    },
    {
        "name": "Engineering",
        "tag": "/ eng",
        "items": [
            "Django", "Streamlit", "Node.js / Express",
            "React.js", "Java", "C#", "Kotlin",
            "Git / GitHub", "Google Cloud",
        ],
    },
]

SOFT_SKILLS = [
    {"name": "Research-Driven",       "blurb": "Literature-first; models chosen from comparative analysis, not vibes."},
    {"name": "Pragmatic Rigor",       "blurb": "Ships useful baselines fast, then iterates with measurement."},
    {"name": "Cross-Discipline Fluency", "blurb": "Translates stakeholder asks into data problems and back to insight."},
    {"name": "Systems Thinking",      "blurb": "Clean module boundaries from ingest → feature → model → UI."},
    {"name": "Client Communication",  "blurb": "Demos and deploys directly in clients' working environments."},
    {"name": "Fast Learner",          "blurb": "New frameworks and domains absorbed in days, not weeks."},
]

EXPERIENCE = {
    "role": "Innovations, R&D Intern",
    "company": "Rythmos DB, Inc.",
    "period": "February – April 2026",
    "bullets": [
        "Built a media analytics intelligence web application in Python — ingest, clean, translate, and cluster news data at scale.",
        "Integrated Claude agents and tool-use workflows to automate documentation, data tagging, and analyst support.",
        "Designed modular data pipelines (cleaning → enrichment → clustering → merge) reusable across datasets.",
        "Implemented TF-IDF + KMeans topic clustering and language detection-driven translation for multi-source feeds.",
        "Shipped MongoDB-backed authentication with role-based access, bcrypt hashing, and a security audit trail.",
    ],
}

PROJECTS = [
    {
        "slug": "rdb",
        "title": "RDB Media Intelligence",
        "role": "R&D Intern — Rythmos DB",
        "stack": ["Python", "Pandas", "scikit-learn", "Streamlit", "Claude API", "MongoDB"],
        "description": (
            "Media analytics pipeline: ingest CSV/Excel, clean, translate, "
            "cluster topics with TF-IDF + KMeans, and merge sources — with "
            "Claude agents handling documentation and tagging. Production "
            "build uses MongoDB-backed auth with audit logs."
        ),
        "highlight": "Live demo embedded above ↑",
        "link": None,
    },
    {
        "slug": "malaria",
        "title": "CAE-CNN Malaria Classifier",
        "role": "Lead Researcher · Model Developer",
        "stack": ["Python", "TensorFlow", "Keras", "OpenCV", "NumPy"],
        "description": (
            "Undergraduate thesis — robust malaria classification from "
            "blood-smear images using Convolutional Autoencoders + CNN "
            "ensembles. Comparative study across architectures, with "
            "denoising preprocessing improving recall on noisy field data."
        ),
        "highlight": "Thesis · Deep Learning.",
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
            "core features, data model, and cloud deployment."
        ),
        "highlight": "Live in a working clinic.",
        "link": None,
        "image": "img/mcy_dental.png",
    },
    {
        "slug": "quisti",
        "title": "Quisti",
        "role": "Project Head · Lead Developer · Researcher",
        "stack": ["Java", "Android Studio", "SQLite"],
        "description": (
            "A mobile quiz application built from ground-up concept to "
            "full-stack native Android. Research-backed methodology "
            "driving item generation and UX decisions."
        ),
        "highlight": "Original concept, shipped end-to-end.",
        "link": None,
    },
    {
        "slug": "pos",
        "title": "POS System",
        "role": "Full-Stack Developer",
        "stack": ["C#", ".NET", "WinForms", "SQL Server"],
        "description": (
            "Desktop point-of-sale with inventory management, item CRUD, "
            "and transaction handling. Built on Windows Forms with a local "
            "SQL Server database."
        ),
        "highlight": "Desktop-native, offline-capable.",
        "link": None,
    },
]

EDUCATION = [
    {
        "school": "University of Santo Tomas",
        "period": "2022 – Present",
        "detail": "BS Computer Science — Data Science specialization.",
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
    total_technical = sum(len(g["items"]) for g in SKILL_GROUPS)
    return render(
        request,
        "index.html",
        {
            "profile": PROFILE,
            "focus_areas": FOCUS_AREAS,
            "skill_groups": SKILL_GROUPS,
            "total_technical": total_technical,
            "soft_skills": SOFT_SKILLS,
            "experience": EXPERIENCE,
            "projects": PROJECTS,
            "education": EDUCATION,
            "certifications": CERTIFICATIONS,
        },
    )
