import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import get_internship_recommendations

st.set_page_config(
    page_title="AI Recommendations – Internship Hub",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Refined card styles for clean, minimal and equal sizes
st.markdown("""
<style>
.card {
    background: white;
    border-radius: 20px;
    padding: 1.7rem 1.3rem 1.5rem 1.3rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 5px 18px rgba(102, 126, 234, 0.13);
    border: 1px solid #f0f0f5;
    position: relative;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
.card-content { flex: 1;}
.badge {
    position: absolute;
    top: 1.1rem; right: 1.2rem;
    padding: 0.26em 0.82em;
    border-radius: 11px;
    font-size: 0.84rem;
    font-weight: 500;
    background: rgba(102,126,234,.08);
    color: #3a436c;
    border: 1.2px solid #cad6f4;
    letter-spacing: .01em;
    box-shadow: none;
    z-index: 2;
}
.skill-chip {
    background: #f6f8fc;
    border: 1px solid #e7ecfa;
    color: #50628a;
    padding: 0.24em 0.75em;
    border-radius: 12px;
    font-size: 0.87rem;
    font-weight: 500;
    margin-right: 0.2em;
    margin-bottom: 0.21em;
    display: inline-block;
}
.card h3 {
    font-size: 1.14rem;
    font-weight: 800;
    margin-bottom: 0.10rem;
    color: #26324a;
}
@media (max-width: 1160px) {
    .card { min-height: 370px;}
}
@media (max-width: 900px) {
    .card { min-height: 420px;}
}
</style>
""", unsafe_allow_html=True)

def display_recommendation_card(internship, rank):
    match_score = internship.get('match_score', 0)
    ai_analysis = internship.get('ai_analysis', {})

    st.markdown(f"""
    <div class="card">
      <div class="badge">{match_score}%</div>
      <div class="card-content">
        <h3>#{rank} {internship['title']}</h3>
        <div style="color:#667eea;font-weight:600;margin-bottom:6px;">{internship['company']}</div>
        <div style="color:#8a96af;font-size:.98rem;margin-bottom:9px;">📍 {internship['location']} &nbsp; 💰 ₹{internship['stipend']}</div>
        <div style="margin-bottom:1.1em;">
          <span style="font-size:.96em;font-weight:600;color:#556;line-height:24px;">Skills:</span><br>
          {" ".join([f'<span class="skill-chip">{skill}</span>' for skill in internship['skills']])}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("AI Analysis", expanded=False):
        st.markdown("**Skill Alignment:**")
        st.write(ai_analysis.get('skill_alignment', 'Analysis pending...'))
        st.markdown("**Strengths:**")
        st.write(ai_analysis.get('key_strengths', 'Analysis pending...'))
        st.markdown("**Areas to Improve:**")
        st.write(ai_analysis.get('areas_for_improvement', 'Analysis pending...'))
        st.markdown("**Why This Match?**")
        st.write(ai_analysis.get('recommendation_reason', 'Analysis pending...'))

def show_grid(recommendations, n_columns=3):
    for i in range(0, len(recommendations), n_columns):
        cols = st.columns(n_columns)
        for j, internship in enumerate(recommendations[i:i+n_columns]):
            with cols[j]:
                display_recommendation_card(internship, i + j + 1)

def main():
    st.markdown('<div style="max-width:1200px;margin:auto;">', unsafe_allow_html=True)
    st.markdown('''
        <div style="text-align:center;font-size:2.15rem;font-weight:900;
        background: linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎯 AI-Powered Internship Recommendations</div>
        <div style="text-align:center; color: #666; font-size:1.10rem; margin-bottom:2.2rem;">
        Personalized internship matches based on your profile
        </div>
    ''', unsafe_allow_html=True)
    if 'user_info' not in st.session_state:
        st.warning("Please provide your information first to get personalized recommendations.")
        if st.button("← Go to Input Page"):
            st.switch_page("pages/2_Input.py")
        return

    if 'recommendations' not in st.session_state:
        with st.spinner("🤖 Analyzing your profile with AI..."):
            try:
                st.session_state.recommendations = get_internship_recommendations(st.session_state.user_info)
            except Exception as e:
                st.error(f"Error getting recommendations: {str(e)}")
                st.session_state.recommendations = []

    recommendations = st.session_state.recommendations

    if not recommendations:
        st.markdown('<h4 style="color:#718096;text-align:center;">No recommendations available</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Input"):
                st.switch_page("pages/2_Input.py")
        with col2:
            if st.button("🔄 Retry"):
                del st.session_state['recommendations']
                st.rerun()
        return

    # Stats
    high_match = len([r for r in recommendations if r.get('match_score', 0) >= 80])
    medium_match = len([r for r in recommendations if 60 <= r.get('match_score', 0) < 80])
    st.markdown(f"""
    <div style="display:flex;gap:2rem;justify-content:center;margin-bottom:2rem;">
        <div style="text-align:center;padding:1rem;background:white;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
        <b style="font-size:2rem;color:#667eea;">{len(recommendations)}</b><br> <span style="color:#718096;font-size:0.99rem;">Total Matches</span></div>
        <div style="text-align:center;padding:1rem;background:white;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
        <b style="font-size:2rem;color:#48bb78;">{high_match}</b><br> <span style="color:#718096;font-size:0.99rem;">High Match (80%+)</span></div>
        <div style="text-align:center;padding:1rem;background:white;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
        <b style="font-size:2rem;color:#ed8936;">{medium_match}</b><br> <span style="color:#718096;font-size:0.99rem;">Good Match (60-79%)</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Filtering
    with st.expander("🔍 Filter Recommendations", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_score = st.slider("Minimum Match Score", 0, 100, 0)
        with col2:
            locations = list(set([r['location'] for r in recommendations]))
            selected_locations = st.multiselect("Location", ["All"] + locations, default=["All"])
        with col3:
            stipend_range = st.selectbox("Stipend Range", ["All", "10K-15K", "16K-20K", "21K+"])

    filtered = recommendations
    if min_score > 0:
        filtered = [r for r in filtered if r.get('match_score', 0) >= min_score]
    if selected_locations and "All" not in selected_locations:
        filtered = [r for r in filtered if r['location'] in selected_locations]
    if stipend_range != "All":
        # Make sure stipend is just digits (strip "K" or "k" or extra chars)
        def stipend_number(stipend):
            clean = ''.join(c for c in stipend if c.isdigit())
            return int(clean) if clean else 0
        if stipend_range == "10K-15K":
            filtered = [r for r in filtered if stipend_number(r['stipend']) <= 15]
        elif stipend_range == "16K-20K":
            filtered = [r for r in filtered if 16 <= stipend_number(r['stipend']) <= 20]
        elif stipend_range == "21K+":
            filtered = [r for r in filtered if stipend_number(r['stipend']) >= 21]
    st.markdown(f"<h4>📋 Showing {len(filtered)} recommendations</h4>", unsafe_allow_html=True)
    if not filtered:
        st.info("No internships match your current filters. Try adjusting the criteria.")
    else:
        show_grid(filtered, n_columns=3)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Input"):
            st.switch_page("pages/2_Input.py")
    with col2:
        if st.button("🔄 Refresh Analysis"):
            del st.session_state['recommendations']
            st.rerun()
    with col3:
        if st.button("🏠 Back to Home"):
            st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
