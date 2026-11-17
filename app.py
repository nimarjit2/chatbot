import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="LPU Placement & Career Assistant",
    page_icon="🎓",
    layout="centered"
)

# Knowledge / Manual
MANUAL = """
CAREER SERVICES & PLACEMENT POLICY GUIDE - LPU

The Division of Career Services (DCS) manages all campus recruitment drives,
pre-placement training, internships, and corporate relations.

PLACEMENT REGISTRATION & ELIGIBILITY:
To participate in campus placement drives, students must meet the following criteria:
- Minimum CGPA 6.0 across all semesters with no active backlogs.
- Mandatory 75% attendance in all pre-placement training (PPT) sessions.
- Student must be registered on the official University Placement Portal (Ums Placement Tab).
- Profile verification must be completed by the respective Training and Placement Officer (TPO).

For career guidance and queries, students can visit the DCS Helpdesk, Block 32-102.

DREAM OFFERS & POLICY RULES:
- Once a student secures a "Dream Offer" (defined as a package above 10 LPA), 
  they are generally not permitted to sit for further companies.
- Students with standard offers (below 10 LPA) may be allowed a maximum of 
  one "Dream Upgrade" opportunity.
- All offers made by companies during campus drives are final and binding.
- Declining an accepted offer may lead to debarment from the placement process.

PRE-PLACEMENT TRAINING (PPT):
- Training modules include Aptitude, Technical Coding, Soft Skills, and Mock Interviews.
- Attendance in PPT classes is compulsory. Defaulters will have their placement 
  portal access temporarily blocked.
- Exemption from PPT is granted only for students undergoing approved 
  semester-long full-term internships.

INTERNSHIP-CUM-PLACEMENT (PPO):
- Students selected for a 6-month Internship-cum-Placement (PPO track) must 
  maintain regular progress reports submitted to their faculty coordinator.
- Stipend details and conversion policies depend strictly on the hiring company's terms.
- Conversion to a full-time employee (FTE) depends on satisfactory performance 
  during the internship period.

DRESS CODE & CONDUCT:
- Formal attire (blazer/suit for men, formal ethnic/western wear for women) 
  is mandatory for all placement drives and company presentations.
- Carrying a valid University ID card and multiple copies of updated resumes 
  is compulsory for every drive.
- Any form of malpractice during online or offline assessments results in 
  immediate debarment from all future placement activities.
"""

SYSTEM_PROMPT = """
Answer only from the given manual.
If the answer is not available, say: Information not available in the manual.
Give simple and clear answers.
"""

# Initialize Groq client using st.secrets
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        if not api_key or api_key == "your_groq_api_key_here":
            st.error("Please configure your valid GROQ_API_KEY in `.streamlit/secrets.toml`.")
            st.stop()
        return Groq(api_key=api_key)
    except KeyError:
        st.error("`GROQ_API_KEY` not found in `.streamlit/secrets.toml`.")
        st.stop()
    except FileNotFoundError:
        st.error("`.streamlit/secrets.toml` file not found. Please create it with your `GROQ_API_KEY`.")
        st.stop()

client = get_groq_client()

# App UI Header
st.title("🎓 LPU Placement & Career Chatbot")
st.caption("Ask questions about campus recruitment eligibility, Dream Offers, PPT attendance, and placement guidelines.")

# Sidebar with info & reset button
with st.sidebar:
    st.header("About")
    st.markdown(
        "This assistant answers queries strictly based on the **LPU Career Services & Placement Policy Guide**."
    )
    st.divider()
    st.subheader("Sample Questions")
    st.markdown("""
    - *What is the minimum CGPA for placements?*
    - *What is considered a Dream Offer?*
    - *Where is the DCS Helpdesk located?*
    - *Can I skip PPT if I am doing an internship?*
    """)
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me anything about LPU's Placement Policies, Pre-Placement Training (PPT), or Dream Offers."
        }
    ]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask your placement question..."):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Groq
    with st.chat_message("assistant"):
        with st.spinner("Checking placement manual..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"{MANUAL}\n\nQuestion: {prompt}"}
                    ]
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"An error occurred while communicating with Groq API: {e}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
