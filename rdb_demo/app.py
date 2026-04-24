"""
RDB App — Portfolio Demo Build
──────────────────────────────
A slim, stateless showcase of the Rythmos DB intern tool's UI.
Strips out: MongoDB auth, secrets, bcrypt, logo, heavy deps.
Keeps: sidebar navigation, step selection, file upload, preview,
download — the exact flow a reviewer would walk through.
"""

import io
from datetime import datetime

import pandas as pd
import streamlit as st


# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="RDB App · Demo",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Portfolio demo build. No credentials, no database."},
)


STEP_GROUPS = {
    "Cleaning":     {"color": "#6366f1", "bg": "#eef2ff"},
    "Filter":       {"color": "#ec4899", "bg": "#fdf2f8"},
    "Enrichment":   {"color": "#f59e0b", "bg": "#fffbeb"},
    "Analysis":     {"color": "#0ea5e9", "bg": "#f0f9ff"},
    "Merge":        {"color": "#8b5cf6", "bg": "#f5f3ff"},
}

STEP_REGISTRY = [
    {"id": "normalize",    "group": "Cleaning",   "label": "Normalize headers"},
    {"id": "duplicates",   "group": "Cleaning",   "label": "Remove duplicates"},
    {"id": "country",      "group": "Cleaning",   "label": "Standardize country"},
    {"id": "filter_value", "group": "Filter",     "label": "Filter by column value"},
    {"id": "date",         "group": "Enrichment", "label": "Add date metadata"},
    {"id": "translate",    "group": "Enrichment", "label": "Translate columns"},
    {"id": "topic",        "group": "Analysis",   "label": "Topic clustering"},
]


# ── Lightweight implementations for the demo ───────────────────────

def _normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().title() for c in df.columns]
    return df


def _remove_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
    return df.drop_duplicates(subset=subset) if subset else df.drop_duplicates()


def _add_date_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if "date" in str(col).lower():
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                df["Year"] = parsed.dt.year
                df["Month"] = parsed.dt.month
                df["Day"] = parsed.dt.day
                df["Quarter"] = parsed.dt.quarter
                return df
            except Exception:
                continue
    return df


STUBBED_OPS = {
    "translate": "Translation runs against Google Translate in production. Disabled in demo.",
    "topic":     "Topic clustering uses sklearn TF-IDF + KMeans in production. Disabled in demo.",
    "country":   "country-converter integration disabled in demo.",
    "filter_value": "Filter step UI shown; apply manually after download.",
}


# ── Styles ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* hide the default streamlit header/menu + footer when embedded */
  #MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }
  .stAppDeployButton { display: none !important; }

  /* palette aligned with the portfolio */
  :root {
    --bg:       #14170d;
    --surface:  #1c2013;
    --elev:     #232716;
    --ink:      #f3ecd4;
    --ink-soft: #cdc4a6;
    --accent:   #d4b73d;
    --olive:    #6d7a3a;
    --line:     rgba(243,236,212,0.12);
  }

  body, .stApp { background: var(--bg) !important; color: var(--ink); }
  .main .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
  }

  /* sidebar */
  section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--line);
  }
  section[data-testid="stSidebar"] .stButton > button {
    justify-content: flex-start !important;
    border: 1px solid var(--line) !important;
    background: transparent !important;
    color: var(--ink-soft) !important;
    font-weight: 500;
    text-align: left;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--ink) !important;
    background: rgba(212,183,61,0.06) !important;
  }
  section[data-testid="stSidebar"] .stButton > button[kind="primary"],
  section[data-testid="stSidebar"] .stButton > button:focus {
    background: var(--accent) !important;
    color: #14170d !important;
    border-color: var(--accent) !important;
  }

  /* headings */
  h1, h2, h3, h4 { color: var(--ink) !important; font-weight: 700; }
  h1 { letter-spacing: -0.02em; }

  /* demo banner */
  .demo-banner {
    background: linear-gradient(90deg, rgba(212,183,61,0.12), rgba(212,183,61,0.02));
    border: 1px solid rgba(212,183,61,0.25);
    border-left: 3px solid var(--accent);
    color: var(--ink);
    padding: 0.7rem 1rem;
    border-radius: 8px;
    font-size: 0.88rem;
    margin-bottom: 1.3rem;
  }
  .demo-banner code {
    background: rgba(212,183,61,0.1);
    color: var(--accent);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
  }

  /* cards + chips */
  .rdb-card {
    background: var(--elev);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
  }
  .pipeline-strip {
    background: var(--elev);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin: 1rem 0 1.5rem;
  }
  .pipeline-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--ink-soft);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-right: 0.5rem;
  }
  .pipeline-chip {
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
  }
  .pipeline-arrow { color: var(--ink-soft); }

  .section-divider {
    display: flex; align-items: center; gap: 0.8rem;
    margin: 1.4rem 0 0.8rem;
  }
  .section-divider-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .section-divider-line {
    flex: 1;
    height: 1px;
    background: var(--line);
  }

  /* stTabs, inputs */
  .stSelectbox, .stMultiSelect, .stTextInput, .stTextArea {
    color: var(--ink) !important;
  }

  /* data frames */
  [data-testid="stDataFrame"] {
    background: var(--elev);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 0.4rem;
  }
</style>
""", unsafe_allow_html=True)


# ── Sample data (offered if user has none) ─────────────────────────
SAMPLE_CSV = b"""Date,Headline,Source,Country,Sentiment
2025-12-01,Central bank holds rates steady,Reuters,PH,positive
2025-12-02,Tech sector sees record investment,Bloomberg,SG,positive
2025-12-03,Oil prices dip on weak demand,Reuters,US,negative
2025-12-03,Oil prices dip on weak demand,Reuters,US,negative
2025-12-04,AI adoption accelerates in SEA,Nikkei,MY,positive
2025-12-05,Currency weakens against dollar,Bloomberg,PH,negative
"""


def load_sample():
    st.session_state["uploaded_df"] = pd.read_csv(io.BytesIO(SAMPLE_CSV))
    st.session_state["uploaded_name"] = "sample_media.csv"


# ── Pipeline tool ──────────────────────────────────────────────────
def tool_data_pipeline():
    st.markdown(
        '<div class="demo-banner">'
        '<strong>Demo build.</strong> Interactive UI with a subset of operations enabled '
        '(<code>normalize headers</code>, <code>remove duplicates</code>, <code>add date metadata</code>). '
        'Heavier ops like translation + topic clustering are stubbed.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.title("Data Pipeline")
    st.caption("Upload a CSV or Excel file, select steps, and run the pipeline.")

    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx", "xls"],
            key="pl_upload",
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("Use sample data", use_container_width=True):
            load_sample()
            st.rerun()

    if uploaded is not None:
        try:
            suffix = uploaded.name.lower().rsplit(".", 1)[-1]
            if suffix in ("xlsx", "xls"):
                df = pd.read_excel(uploaded)
            else:
                df = pd.read_csv(uploaded)
            st.session_state["uploaded_df"] = df
            st.session_state["uploaded_name"] = uploaded.name
        except Exception as e:
            st.error(f"Failed to load file: {e}")

    df = st.session_state.get("uploaded_df")
    name = st.session_state.get("uploaded_name", "—")
    if df is None:
        st.info("Upload a file or load sample data to begin.")
        return

    st.markdown(
        '<div class="section-divider">'
        '<span class="section-divider-label">Input</span>'
        '<span class="section-divider-line"></span></div>',
        unsafe_allow_html=True,
    )
    st.write(f"**File:** `{name}` · **{len(df):,} rows** × **{len(df.columns)} cols**")
    st.dataframe(df.head(10), use_container_width=True, height=230)

    st.markdown(
        '<div class="section-divider">'
        '<span class="section-divider-label">Steps</span>'
        '<span class="section-divider-line"></span></div>',
        unsafe_allow_html=True,
    )

    labels = [s["label"] for s in STEP_REGISTRY]
    selected = st.multiselect(
        "Select pipeline steps",
        options=labels,
        default=["Normalize headers", "Remove duplicates"],
        key="pl_selected",
    )

    if selected:
        chips_html = []
        for i, label in enumerate(selected):
            step = next((s for s in STEP_REGISTRY if s["label"] == label), None)
            if step:
                cfg = STEP_GROUPS[step["group"]]
                chips_html.append(
                    f'<span class="pipeline-chip" style="background:{cfg["bg"]};color:{cfg["color"]};'
                    f'border:1px solid {cfg["color"]}55">{label}</span>'
                )
                if i < len(selected) - 1:
                    chips_html.append('<span class="pipeline-arrow">→</span>')

        st.markdown(
            '<div class="pipeline-strip">'
            '<span class="pipeline-label">Pipeline:</span>'
            + "".join(chips_html) +
            '</div>',
            unsafe_allow_html=True,
        )

    if st.button("▶ Run pipeline", type="primary", use_container_width=True):
        if not selected:
            st.warning("Select at least one step.")
            return

        result = df.copy()
        log = []
        progress = st.progress(0.0, text="Running…")

        for i, label in enumerate(selected):
            step = next((s for s in STEP_REGISTRY if s["label"] == label), None)
            if not step:
                continue

            try:
                if step["id"] == "normalize":
                    result = _normalize_headers(result)
                    log.append(f"✓ Normalized {len(result.columns)} column headers.")
                elif step["id"] == "duplicates":
                    before = len(result)
                    result = _remove_duplicates(result)
                    log.append(f"✓ Removed {before - len(result)} duplicate rows.")
                elif step["id"] == "date":
                    before_cols = set(result.columns)
                    result = _add_date_metadata(result)
                    added = sorted(set(result.columns) - before_cols)
                    log.append(f"✓ Added date metadata: {', '.join(added) or '(no date col found)'}")
                elif step["id"] in STUBBED_OPS:
                    log.append(f"⚠ {label}: {STUBBED_OPS[step['id']]}")
            except Exception as e:
                log.append(f"✗ {label}: {e}")

            progress.progress((i + 1) / len(selected), text=f"Step {i+1}/{len(selected)}: {label}")

        progress.empty()
        st.success(f"Pipeline complete — {len(result):,} rows × {len(result.columns)} cols.")

        with st.expander("Log", expanded=True):
            for line in log:
                st.write(line)

        st.markdown(
            '<div class="section-divider">'
            '<span class="section-divider-label">Result preview</span>'
            '<span class="section-divider-line"></span></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(result.head(20), use_container_width=True, height=320)

        st.markdown(
            '<div class="section-divider">'
            '<span class="section-divider-label">Download</span>'
            '<span class="section-divider-line"></span></div>',
            unsafe_allow_html=True,
        )

        fmt = st.radio("Format", ["CSV", "Excel"], horizontal=True, key="pl_out_fmt")
        stem = name.rsplit(".", 1)[0]

        if fmt == "CSV":
            st.download_button(
                label="Download CSV",
                data=result.to_csv(index=False).encode("utf-8"),
                file_name=f"{stem}_cleaned.csv",
                mime="text/csv",
            )
        else:
            buf = io.BytesIO()
            result.to_excel(buf, index=False, engine="openpyxl")
            buf.seek(0)
            st.download_button(
                label="Download Excel",
                data=buf.getvalue(),
                file_name=f"{stem}_cleaned.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


# ── Merge tool ─────────────────────────────────────────────────────
def tool_merge_csv():
    st.title("Merge Data")
    st.caption("Upload two or more files and merge them on a common column.")

    files = st.file_uploader(
        "Upload 2+ files",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        key="mg_upload",
    )

    if not files or len(files) < 2:
        st.info("Upload at least 2 files to enable merge.")
        return

    dfs = []
    for f in files:
        try:
            if f.name.lower().endswith(("xlsx", "xls")):
                dfs.append((f.name, pd.read_excel(f)))
            else:
                dfs.append((f.name, pd.read_csv(f)))
        except Exception as e:
            st.error(f"{f.name}: {e}")

    if len(dfs) < 2:
        return

    for name, df in dfs:
        with st.expander(f"{name}  ·  {len(df):,} rows × {len(df.columns)} cols"):
            st.dataframe(df.head(5), use_container_width=True)

    common = set(dfs[0][1].columns)
    for _, d in dfs[1:]:
        common &= set(d.columns)

    if not common:
        st.warning("No columns are common across all uploaded files.")
        return

    col = st.selectbox("Merge on column", sorted(common))
    how = st.radio("Join type", ["outer", "inner", "left"], horizontal=True)

    if st.button("▶ Merge", type="primary", use_container_width=True):
        result = dfs[0][1]
        for _, d in dfs[1:]:
            result = result.merge(d, on=col, how=how, suffixes=("", "_dup"))

        st.success(f"Merged — {len(result):,} rows × {len(result.columns)} cols.")
        st.dataframe(result.head(20), use_container_width=True, height=320)

        st.download_button(
            "Download merged CSV",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name=f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )


# ── About tool ─────────────────────────────────────────────────────
def tool_about():
    st.title("About this demo")
    st.markdown("""
This is a public **demo build** of the RDB App — the internal tool I built
during my internship at **Rythmos DB, Inc.** (Feb–Apr 2026).

**Production features removed from this build**:
- MongoDB-backed authentication with bcrypt password hashing
- Role-based access control (`user`, `admin`, `super_admin`)
- Security audit logging (every login, change, lockout, reset)
- Admin tools (User Control, Security Logs)
- Account lockout on repeated failed attempts
- Heavy pipeline ops that require external APIs (translation, topic clustering)

**What's kept**:
- Full pipeline UI — step selection, chip-strip pipeline preview, downloads
- Merge tool — multi-file upload with join configuration
- Working operations: normalize headers, remove duplicates, add date metadata

The production build uses MongoDB Atlas, `bcrypt`, `deep-translator`,
and `scikit-learn` (TF-IDF + KMeans topic clusters).

— Neo Balignasay
""")


# ── Sidebar + routing ──────────────────────────────────────────────
TOOLS = [
    {"id": "pipeline", "label": "Data Pipeline", "icon": ":material/tune:"},
    {"id": "merge",    "label": "Merge Data",    "icon": ":material/merge:"},
    {"id": "about",    "label": "About Demo",    "icon": ":material/info:"},
]


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div style="padding: 0.5rem 0 1.2rem; border-bottom: 1px solid rgba(243,236,212,0.12); margin-bottom: 1rem;">'
            '<div style="font-family: \'Archivo Black\', sans-serif; font-size: 1.15rem; '
            'letter-spacing: 0.02em; color: #f3ecd4;">RDB App</div>'
            '<div style="font-family: \'JetBrains Mono\', monospace; font-size: 0.7rem; '
            'color: #d4b73d; letter-spacing: 0.15em; margin-top: 0.2rem;">DEMO BUILD</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if "active_tool" not in st.session_state:
            st.session_state["active_tool"] = "pipeline"

        for t in TOOLS:
            is_active = st.session_state["active_tool"] == t["id"]
            if st.button(
                t["label"],
                key=f"tool_btn_{t['id']}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                icon=t["icon"],
            ):
                if not is_active:
                    st.session_state["active_tool"] = t["id"]
                    st.rerun()

        st.divider()
        st.caption(
            "Portfolio demo · stateless · no login. "
            "View the full write-up on neo-balignasay.onrender.com."
        )


def main():
    render_sidebar()
    active = st.session_state.get("active_tool", "pipeline")

    if active == "pipeline":
        tool_data_pipeline()
    elif active == "merge":
        tool_merge_csv()
    elif active == "about":
        tool_about()


if __name__ == "__main__":
    main()
