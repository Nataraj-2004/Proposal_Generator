import streamlit as st
from streamlit_lottie import st_lottie
import requests

from legal_docs import generate_legal_document
from company_profiles import generate_company_profile
from project_lists import generate_project_list
from contacts import generate_contact_list

# Page config
st.set_page_config(
    page_title="AI Proposal Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Utility to fetch Lottie animations
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Preload animations
lottie_banner = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_legal = load_lottie_url("https://assets3.lottiefiles.com/datafiles/VNYFv9cFVX2EPXb/data.json")
lottie_profile = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_jmF4yL.json")
lottie_projects = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_jXklBo.json")
lottie_contacts = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_iwmd6pyr.json")

# Sidebar navigation
st.sidebar.title("🚀 Navigator")
section = st.sidebar.radio("", [
    "🏛️ Legal Documents",
    "🏢 Company Profiles",
    "📊 Project Suggestions",
    "📇 Contact Manager"
])

# Banner
with st.container():
    cols = st.columns([3,1])
    with cols[0]:
        st.title("🤖 AI-Powered Proposal Generator")
        st.markdown(
            "Generate professional proposals with AI-driven cover letters, legal docs, "
            "company profiles, project analyses, and contact lists—all in one elegant app."
        )
    with cols[1]:
        if lottie_banner:
            st_lottie(lottie_banner, height=150, key="banner")

# 1. Legal Documents
if section == "🏛️ Legal Documents":
    st.subheader("🔖 Legal Documents")
    if lottie_legal:
        st_lottie(lottie_legal, height=150, key="legal")

    project_name = st.text_input("Project Name", "Renewable Energy Project")
    num = st.number_input("Number of firms", 2, 10, 2)
    parties = []
    st.markdown("**Enter each firm/person and role**")
    for i in range(num):
        name = st.text_input(f"Name #{i+1}", key=f"ld_name_{i}")
        role = st.text_input(f"Role #{i+1}", key=f"ld_role_{i}")
        parties.append({"name": name, "role": role})
    lang = st.selectbox("Language", ["english","portuguese","spanish"], key="ld_lang")

    if st.button("Generate Legal Docs"):
        with st.spinner("Generating…"):
            poa = generate_legal_document("power_of_attorney", parties[:2], project_name, lang)
            loa = generate_legal_document("letter_of_association", parties, project_name, lang)
        st.success("✅ Generated!")
        st.expander("Edit Power of Attorney").text_area("POA", poa, height=200)
        st.expander("Edit Letter of Association").text_area("LOA", loa, height=200)
        if st.button("Save Legal Docs"):
            st.session_state['poa'] = poa
            st.session_state['loa'] = loa
            st.toast("Legal documents saved")

# 2. Company Profiles
elif section == "🏢 Company Profiles":
    st.subheader("🏷 Company Profiles")
    if lottie_profile:
        st_lottie(lottie_profile, height=150, key="profile")

    n = st.number_input("How many companies?", 1, 5, 1)
    firms = []
    for i in range(n):
        st.markdown(f"**Company #{i+1}**")
        name = st.text_input("Name", key=f"cp_name_{i}")
        desc = st.text_area("Description", key=f"cp_desc_{i}")
        certs = st.text_area("Certifications (one per line)", key=f"cp_certs_{i}")
        achs = st.text_area("Achievements (one per line)", key=f"cp_achs_{i}")
        rel = st.text_input("Relevance to project", key=f"cp_rel_{i}")
        firms.append({
            "name": name, "description": desc,
            "certifications": [c.strip() for c in certs.splitlines() if c],
            "achievements": [a.strip() for a in achs.splitlines() if a],
            "relevance": rel
        })
    lang = st.selectbox("Language", ["english","portuguese","spanish"], key="cp_lang")

    if st.button("Generate Profiles"):
        profiles = {}
        with st.spinner("Building profiles…"):
            for f in firms:
                profiles[f["name"]] = generate_company_profile(f, f["relevance"], lang)
        st.success("✅ Done")
        for name, prof in profiles.items():
            st.expander(name).write(prof)
        if st.button("Save Profiles"):
            st.session_state['profiles'] = profiles
            st.toast("Profiles saved")

# 3. Project Suggestions
elif section == "📊 Project Suggestions":
    st.subheader("📈 Project Relevance & AI Ideas")
    if lottie_projects:
        st_lottie(lottie_projects, height=150, key="projects")

    cur = st.text_area("Current Project Description")
    m = st.number_input("Past projects count", 1, 10, 3)
    past = []
    for i in range(m):
        past.append({
            "title": st.text_input(f"Title #{i+1}", key=f"pl_title_{i}"),
            "description": st.text_area(f"Desc #{i+1}", key=f"pl_desc_{i}")
        })
    if st.button("Analyze & Suggest"):
        with st.spinner("Analyzing…"):
            res = generate_project_list(cur, past)
        st.success("✅ Analysis Complete")
        st.markdown("**Relevancy Scores:**")
        for e in res["evaluations"]:
            st.write(f"- **{e['title']}**: {e['score']}/100 — {e['rationale']}")
        st.markdown("**AI-Suggested Projects:**")
        for r in res["additional_recommendations"]:
            st.write(f"- **{r['title']}** — {r['description']}")
        if st.button("Save Suggestions"):
            st.session_state['projects'] = res
            st.toast("Suggestions saved")

# 4. Contact Manager
elif section == "📇 Contact Manager":
    st.subheader("👥 Contacts")
    if lottie_contacts:
        st_lottie(lottie_contacts, height=150, key="contacts")

    c = st.number_input("How many contacts?", 1, 10, 2)
    contacts = []
    for i in range(c):
        contacts.append({
            "name": st.text_input(f"Name #{i+1}", key=f"ct_name_{i}"),
            "role": st.text_input(f"Role #{i+1}", key=f"ct_role_{i}"),
            "email": st.text_input(f"Email #{i+1}", key=f"ct_email_{i}"),
            "phone": st.text_input(f"Phone #{i+1}", key=f"ct_phone_{i}")
        })
    order = st.selectbox("Order by", ["name","role","email"], key="ct_sort")
    if st.button("Generate Contacts"):
        with st.spinner("Formatting…"):
            formatted = generate_contact_list(contacts, order)
        st.success("✅ Done")
        st.expander("Contact List").write(formatted.replace("\n", "  \n"))
        if st.button("Save Contacts"):
            st.session_state['contacts'] = formatted
            st.toast("Contacts saved")
