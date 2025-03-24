import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from groq import Groq
import time
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("Missing GROQ_API_KEY in environment variables")

def init_streamlit():
    st.set_page_config(page_title="BrandPulse AI", layout="wide")
    
    # Update custom CSS with new background
    st.markdown("""
    <style>
    /* Coffee Color Palette */
    :root {
        --coffee-dark: #3a2618;      /* Dark Roast */
        --coffee-medium: #8b4513;    /* Medium Roast */
        --coffee-light: #c68f65;     /* Light Roast */
        --cream: #e6d5c9;            /* Cream */
        --mint: #98c1a9;             /* Complementary Green */
        --caramel: #d4a76a;          /* Caramel Accent */
        --mocha: #7b5d4f;            /* Mocha */
        --espresso: #4a3428;         /* Espresso */
    }
    
    /* Modern Dark Theme with Coffee Tones */
    .stApp {
        background-image: linear-gradient(rgba(20, 14, 10, 0.75), rgba(30, 20, 15, 0.85)), 
            url('https://cdn.dribbble.com/userupload/36521817/file/original-f4f6de2ea8cb1e71ea872587ccb15c78.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: #e6d5c9;
    }
    
    /* Add subtle animation to gradient */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Dashboard Cards with Warm Glass Effect */
    .dashboard-card, .competitor-card {
        background: linear-gradient(145deg, var(--espresso), var(--coffee-dark)) !important;
        backdrop-filter: blur(20px);
        border: 1px solid var(--caramel) !important;
        box-shadow: 0 8px 32px rgba(20, 10, 5, 0.3);
    }
    
    /* Marketing-focused Header with Coffee Gradient */
    .header {
        background: linear-gradient(90deg, #c68f65, #8b4513);
        color: #fff5eb;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 2.5em;
        font-weight: 600;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(198, 143, 101, 0.2);
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: rgba(42, 42, 74, 0.9);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Results Container */
    .results-container {
        background: linear-gradient(135deg, rgba(42, 42, 74, 0.9), rgba(26, 26, 46, 0.9));
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        margin: 5px;
    }
    
    .status-badge.success {
        background: rgba(46, 213, 115, 0.2);
        color: #2ed573;
        border: 1px solid rgba(46, 213, 115, 0.4);
    }
    
    /* Input Fields with Enhanced Coffee Style */
    .stTextInput > div > div > input {
        background-color: var(--espresso) !important;
        color: var(--cream) !important;
        border: 2px solid var(--coffee-medium) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--caramel) !important;
        box-shadow: 0 0 10px rgba(212, 167, 106, 0.3) !important;
        background-color: var(--coffee-dark) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(230, 213, 201, 0.6) !important;
    }
    
    /* Buttons with Rich Coffee Gradient */
    .stButton > button {
        background: linear-gradient(135deg, var(--coffee-medium), var(--mocha)) !important;
        color: var(--cream) !important;
        border: 1px solid var(--caramel) !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        font-size: 14px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--coffee-light), var(--coffee-medium)) !important;
        border-color: var(--mint) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(139, 69, 19, 0.2) !important;
    }
    
    /* Selectbox with Coffee Style */
    .stSelectbox > div > div {
        background-color: rgba(44, 28, 20, 0.9) !important;
        border: 2px solid #8b4513 !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #c68f65 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #e6d5c9 !important;
    }
    
    /* Number Input with Coffee Style */
    .stNumberInput > div > div > input {
        background-color: rgba(44, 28, 20, 0.9) !important;
        color: #e6d5c9 !important;
        border: 2px solid #8b4513 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #c68f65 !important;
        box-shadow: 0 0 10px rgba(198, 143, 101, 0.3) !important;
    /* Tables */
    .dataframe {
        width: 100%;
        margin: 20px 0;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 15px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: linear-gradient(90deg, #6c63ff, #ff4b6c);
        color: white;
        padding: 15px;
        text-align: left;
    }
    
    .dataframe td {
        padding: 12px 15px;
        border-bottom: 1px solid rgba(108, 99, 255, 0.1);
    }
    
    /* Add custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Inter:wght@400;500&display=swap');
    
    /* Enhanced Competitor Analysis Card */
    .competitor-card {
        background: rgba(42, 42, 74, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #6c63ff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-box {
        background: linear-gradient(145deg, rgba(152, 193, 169, 0.1), rgba(212, 167, 106, 0.1)) !important;
        background: linear-gradient(145deg, rgba(108, 99, 255, 0.15), rgba(255, 75, 108, 0.15));
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(108, 99, 255, 0.2);
    }
    
    .recommendation-box {
        background: linear-gradient(145deg, rgba(255, 75, 108, 0.1), rgba(108, 99, 255, 0.1));
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #ff4b6c;
    }
    
    .recommendation-item {
        margin: 10px 0;
        padding: 10px;
        background: rgba(42, 42, 74, 0.3);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("BrandPulse AI")

class MarketingAgencyAutomation:
    def __init__(self):
        self.groq = groq_client
        self.session = requests.Session()

    def _get_completion(self, prompt: str) -> str:
        try:
            completion = self.groq.chat.completions.create(
                model="mistral-saba-24b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {e}")
            return None

    def seo_optimizer(self, url: str, keywords: List[str]) -> Dict[str, Any]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ""
            meta_desc = soup.find("meta", {"name": "description"})
            meta_desc = meta_desc["content"] if meta_desc else ""
            h1_tags = [h1.text.strip() for h1 in soup.find_all("h1")]
            analysis_prompt = f"""
            Analyze this webpage SEO for:
            URL: {url}
            Title: {title}
            Meta Description: {meta_desc}
            H1 Tags: {', '.join(h1_tags)}
            Target Keywords: {', '.join(keywords)}
            Provide recommendations for:
            1. Title optimization
            2. Meta description improvements
            3. Content structure
            4. Keyword placement
            5. Technical SEO improvements
            """
            seo_analysis = self._get_completion(analysis_prompt)
            return {
                "url": url,
                "current_title": title,
                "current_meta": meta_desc,
                "current_h1": h1_tags,
                "recommendations": seo_analysis
            }
        except Exception as e:
            return {"error": str(e)}

    def competitor_watchdog(self, competitors: List[str], keywords: List[str]) -> Dict[str, Any]:
        competitor_data = {}
        for competitor in competitors:
            # First, get a quick summary
            summary_prompt = f"""
            Provide a concise 3-point summary of {competitor}'s key strengths and market positioning:
            1. Primary competitive advantage
            2. Target audience focus
            3. Market differentiation
            Keep each point brief and actionable.
            """
            quick_summary = self._get_completion(summary_prompt)
            
            # Main analysis prompt
            analysis_prompt = f"""
            Provide a detailed competitive analysis for {competitor} focusing on:
            1. Content Strategy:
               - Content types and formats used
               - Publishing frequency and consistency
               - Content quality and engagement metrics
               - Target audience alignment and reach
            
            2. Keyword Analysis:
               - Usage of target keywords: {', '.join(keywords)}
               - Keyword density and placement strategy
               - Related keywords and semantic relevance
               - Overall SEO optimization effectiveness
            
            3. Market Presence:
               - Brand positioning and market share
               - Unique selling propositions (USPs)
               - Customer engagement and loyalty
               - Brand authority and credibility indicators
            
            4. Competitive Advantages:
               - Key strengths and core competencies
               - Notable weaknesses and gaps
               - Market opportunities to exploit
               - Potential threats to address
            
            5. Actionable Recommendations:
               - Immediate actions (next 30 days):
                 * Specific tactical improvements
                 * Quick wins and low-hanging fruit
               - Strategic initiatives (next 90 days):
                 * Long-term competitive advantages
                 * Market positioning improvements
               - Resource allocation suggestions:
                 * Required investments
                 * Expected outcomes
            
            Format each section with clear bullet points and specific examples.
            """
            competitor_analysis = self._get_completion(analysis_prompt)
            
            # Metrics analysis
            metrics_prompt = f"""
            Based on the website {competitor}, provide detailed metrics with justification:
            1. Content Quality Score (0-100):
               - Writing quality
               - Visual appeal
               - User engagement
            
            2. Keyword Optimization Level (0-100):
               - Keyword relevance
               - Content optimization
               - Technical SEO
            
            3. Market Position Strength (0-100):
               - Brand authority
               - Market share
               - Competitive advantage
            
            4. Brand Authority Score (0-100):
               - Industry presence
               - Social proof
               - Thought leadership
            
            For each metric, provide a specific score and brief justification.
            """
            metrics_analysis = self._get_completion(metrics_prompt)
            
            competitor_data[competitor] = {
                "quick_summary": quick_summary,
                "analysis": competitor_analysis,
                "metrics": metrics_analysis
            }
        return competitor_data

    def post_creator(self, topic: str, platform: str, tone: str = "professional") -> Dict[str, Any]:
        content_prompt = f"""
        Create a {platform} post about {topic} with a {tone} tone.
        Include:
        1. Main post content
        2. Relevant hashtags
        3. Call to action
        4. Best posting time recommendation
        """
        content = self._get_completion(content_prompt)
        return {"platform": platform, "content": content, "topic": topic, "created_at": datetime.now().isoformat()}

    def smart_email_manager(self, campaign_type: str, audience: List[Dict[str, Any]]) -> Dict[str, Any]:
        email_templates = {}
        for segment in audience:
            email_prompt = f"""
            Create an email campaign for:
            Campaign Type: {campaign_type}
            Audience Segment: {segment}
            Include:
            1. Subject line options
            2. Email body
            3. Call to action
            4. Personalization elements
            """
            email_content = self._get_completion(email_prompt)
            email_templates[segment["segment_name"]] = {
                "content": email_content,
                "subject_lines": self.generate_subject_lines(campaign_type, segment),
                "send_time": self.optimize_send_time(segment)
            }
        return email_templates

    def generate_subject_lines(self, campaign_type: str, segment: Dict[str, Any]) -> List[str]:
        prompt = f"Generate 5 engaging subject lines for {campaign_type} campaign targeting {segment['segment_name']}"
        return self._get_completion(prompt).split("\n")

    def optimize_send_time(self, segment: Dict[str, Any]) -> str:
        if segment.get("characteristics") == "first_time_buyers":
            return "14:00 PM"
        elif segment.get("characteristics") == "repeat_buyers":
            return "09:00 AM"
        return "10:00 AM"

def main():
    init_streamlit()
    
    try:
        marketing_system = MarketingAgencyAutomation()
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        st.info("Please set up your API key in the .env file:\nGROQ_API_KEY=your_groq_api_key_here")
        return

    # Define tabs
    tab1, tab2 = st.tabs(["Individual Analysis", "Comprehensive"])

    # Tab 1: Individual Analysis
    with tab1:
        st.subheader("Individual Analysis Tools")
        
        tool = st.selectbox("Select Tool:", 
                           ["SEO Optimizer", "Competitor Watchdog", "Post Creator", "Smart Email Manager"],
                           key="individual_tool")

        if tool == "SEO Optimizer":
            url = st.text_input("Website URL:", placeholder="https://example.com", key="ind_seo_url")
            keywords = st.text_input("Target Keywords:", placeholder="e.g., keyword1, keyword2", key="ind_seo_keywords")
            if st.button("Analyze SEO", key="ind_seo_button"):
                if url and keywords:
                    with st.spinner("Analyzing SEO..."):
                        keywords_list = [k.strip() for k in keywords.split(',')]
                        results = marketing_system.seo_optimizer(url, keywords_list)
                        if "error" in results:
                            st.error(f"SEO analysis failed: {results['error']}")
                        else:
                            st.subheader("SEO Analysis Results")
                            st.write(f"Title: {results['current_title']}")
                            st.write(f"Meta Description: {results['current_meta']}")
                            st.write(f"H1 Tags: {', '.join(results['current_h1'])}")
                            st.write("Recommendations:")
                            st.write(results['recommendations'])

        elif tool == "Competitor Watchdog":
            num_competitors = st.number_input("Number of competitors:", min_value=1, max_value=5, value=1, key="ind_comp_num")
            keywords = st.text_input("Keywords to track:", placeholder="e.g., keyword1, keyword2", key="ind_comp_keywords")
            competitors = []
            cols = st.columns(2)
            for i in range(int(num_competitors)):
                with cols[i % 2]:
                    comp_url = st.text_input(f"Competitor {i+1} URL:", key=f"ind_comp_url_{i}")
                    competitors.append(comp_url)
            if st.button("Analyze Competitors", key="ind_comp_button"):
                if all(competitors) and keywords:
                    with st.spinner("Analyzing competitors..."):
                        keywords_list = [k.strip() for k in keywords.split(',')]
                        results = marketing_system.competitor_watchdog(competitors, keywords_list)
                        
                        # Display detailed analysis for each competitor
                        for competitor, data in results.items():
                            st.markdown(f'<div class="competitor-card">', unsafe_allow_html=True)
                            st.subheader(f"Analysis for {competitor}")
                            
                            # Display metrics in a grid
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### Key Metrics")
                                st.markdown(f'<div class="metric-box">{data["metrics"]}</div>', unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("### Quick Summary")
                                st.markdown(f'<div class="metric-box">{data["quick_summary"]}</div>', unsafe_allow_html=True)
                            
                            # Parse and display analysis sections
                            analysis_text = data['analysis']
                            sections = {
                                "Content Strategy": "",
                                "Keyword Analysis": "",
                                "Market Presence": "",
                                "Competitive Advantages": "",
                                "Actionable Recommendations": ""
                            }
                            
                            # Parse sections
                            current_section = ""
                            current_content = []
                            
                            for line in analysis_text.split('\n'):
                                if any(section in line for section in sections.keys()):
                                    if current_section and current_content:
                                        sections[current_section] = '\n'.join(current_content)
                                        current_content = []
                                    current_section = next(section for section in sections.keys() if section in line)
                                elif current_section and line.strip():
                                    current_content.append(line)
                            
                            if current_section and current_content:
                                sections[current_section] = '\n'.join(current_content)
                            
                            # Display sections in tabs
                            analysis_tabs = st.tabs(list(sections.keys()))
                            
                            for tab, (section_name, content) in zip(analysis_tabs, sections.items()):
                                with tab:
                                    if content:
                                        st.markdown(content)
                                    else:
                                        st.markdown("*Analysis for this section is being generated...*")
                            
                            st.markdown("---")
                            st.markdown('</div>', unsafe_allow_html=True)

        elif tool == "Post Creator":
            content_type = st.selectbox("Content Type:", ["Social Media Post", "Blog Post", "Marketing Copy"], key="ind_content_type")
            col1, col2 = st.columns(2)
            with col1:
                topic = st.text_input("Topic:", key="ind_content_topic")
                # Set platform based on content type
                if content_type == "Social Media Post":
                    platform = st.selectbox("Platform:", ["LinkedIn", "Twitter", "Facebook", "Instagram"], key="ind_content_platform")
                else:
                    platform = content_type  # Use content type as platform for Blog Post and Marketing Copy
            with col2:
                tone = st.selectbox("Tone:", ["Professional", "Casual", "Friendly", "Formal"], key="ind_content_tone")
            if st.button("Generate Content", key="ind_content_button"):
                if topic:
                    with st.spinner("Generating content..."):
                        post = marketing_system.post_creator(topic, platform, tone.lower())
                        st.subheader("Generated Content")
                        st.write(post['content'])

        elif tool == "Smart Email Manager":
            col1, col2, col3 = st.columns(3)
            with col1:
                brand_name = st.text_input("Brand Name:", key="ind_brand_name")
            with col2:
                industry = st.text_input("Industry:", key="ind_industry")
            with col3:
                campaign_type = st.selectbox("Campaign Type:", ["Welcome Series", "Promotional", "Newsletter", "Re-engagement", "Product Launch"], key="ind_email_type")
            num_segments = st.number_input("Number of segments:", min_value=1, max_value=3, value=1, key="ind_email_segments")
            segments = []
            for i in range(int(num_segments)):
                st.markdown(f"### Segment {i+1}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    name = st.text_input("Segment name:", key=f"ind_email_seg_name_{i}", placeholder="e.g., New Customers")
                with col2:
                    characteristics = st.selectbox("Characteristics:", ["First-time Buyers", "Repeat Customers", "VIP Members", "Inactive Users"], key=f"ind_email_seg_char_{i}")
                with col3:
                    previous_engagement = st.select_slider("Engagement Level:", options=["Very Low", "Low", "Medium", "High", "Very High"], key=f"ind_engagement_{i}")
                if name:
                    segments.append({"segment_name": name.strip(), "characteristics": characteristics, "engagement": previous_engagement})
            if st.button("Generate Campaign", key="ind_email_button"):
                if brand_name and segments:
                    with st.spinner("Crafting your email campaign..."):
                        results = marketing_system.smart_email_manager(campaign_type, segments)
                        for segment_name, email in results.items():
                            st.subheader(f"Campaign for {segment_name}")
                            st.write(email['content'])

    # Tab 2: Comprehensive
    with tab2:
        st.subheader("Comprehensive Marketing Analysis Dashboard")
        
        with st.expander("Input Your Business Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                main_url = st.text_input("Your Website URL:", placeholder="https://example.com", key="comp_url")
                brand_name = st.text_input("Brand Name:", key="comp_brand")
            with col2:
                keywords = st.text_input("Target Keywords (comma-separated):", placeholder="e.g., keyword1, keyword2", key="comp_comp_keywords")
                industry = st.text_input("Industry:", key="comp_industry")

        with st.expander("Competitor Details"):
            num_competitors = st.number_input("Number of Competitors:", min_value=1, max_value=3, value=1, key="comp_num_comp")
            competitors = []
            for i in range(num_competitors):
                comp_url = st.text_input(f"Competitor {i+1} URL:", key=f"comp_comp_url_{i}")
                competitors.append(comp_url)

        st.markdown("### Analysis Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()

        if st.button("Generate Comprehensive Report", key="comp_button"):
            if not all([main_url, brand_name, industry]) or not all(competitors):
                st.error("Please fill in all required fields")
                return
            
            with st.spinner("Generating comprehensive marketing analysis..."):
                current_date = datetime(2025, 3, 24)
                keywords_list = [k.strip() for k in keywords.split(',')] if keywords else ["generic"]

                status_text.text("Step 1/4: Analyzing SEO...")
                seo_results = marketing_system.seo_optimizer(main_url, keywords_list)
                progress_bar.progress(0.25)

                status_text.text("Step 2/4: Analyzing competitors...")
                competitor_results = marketing_system.competitor_watchdog(competitors, keywords_list)
                progress_bar.progress(0.5)

                status_text.text("Step 3/4: Generating content ideas...")
                content_results = marketing_system.post_creator(f"{industry} trends", "LinkedIn", "professional")
                progress_bar.progress(0.75)

                status_text.text("Step 4/4: Creating email strategy...")
                audience = [
                    {"segment_name": "New Customers", "characteristics": "First-time Buyers", "engagement": "Medium"},
                    {"segment_name": "Returning Customers", "characteristics": "Repeat Customers", "engagement": "High"}
                ]
                email_results = marketing_system.smart_email_manager("Promotional", audience)
                progress_bar.progress(0.9)

                status_text.text("Compiling final report with deadlines...")
                competitor_str = ", ".join(competitors)
                summary_prompt = f"""
                Create a comprehensive marketing analysis report based on:
                Website: {main_url}
                Brand: {brand_name}
                Industry: {industry}
                Keywords: {', '.join(keywords_list)}
                Competitors: {competitor_str}
                SEO Analysis: {seo_results.get('recommendations', 'N/A')}
                Competitor Insights: {', '.join([f"{comp}: {data['analysis']}" for comp, data in competitor_results.items()])}
                Content Suggestions: {content_results['content']}
                Email Strategy: {', '.join([f"{seg}: {data['content'][:100]}..." for seg, data in email_results.items()])}
                
                Provide a detailed report with:
                1. Executive Summary
                2. Current Market Position
                3. Competitive Landscape
                4. Marketing Opportunities
                5. Action Plan with specific deadlines starting from {current_date.strftime('%Y-%m-%d')}:
                   - Short-term actions (within 1 week)
                   - Medium-term actions (within 1 month)
                   - Long-term actions (within 3 months)
                """
                comprehensive_report = marketing_system._get_completion(summary_prompt)
                progress_bar.progress(1.0)

                st.markdown("---")
                st.subheader("Comprehensive Marketing Analysis Report")
                
                # Full report section first
                with st.expander("Full Report", expanded=True):
                    st.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Brand:** {brand_name}")
                    st.markdown(comprehensive_report)

                st.markdown("### Action Plan Timeline")
                deadlines = {
                    "Short-term (1 week)": current_date + timedelta(weeks=1),
                    "Medium-term (1 month)": current_date + timedelta(weeks=4),
                    "Long-term (3 months)": current_date + timedelta(weeks=12)
                }
                for term, deadline in deadlines.items():
                    st.write(f"**{term}:** {deadline.strftime('%Y-%m-%d')}")

                # Key Findings Summary moved after full report
                st.markdown("### Key Findings Summary")
                summary_data = {
                    "Aspect": ["Website", "Industry", "Keywords", "Competitors"],
                    "Details": [main_url, industry, ", ".join(keywords_list), competitor_str]
                }
                st.table(summary_data)

                # Competitive Landscape Analysis section with scores
                st.markdown("### Competitive Analysis & Scoring")

                # Display detailed analysis for each competitor
                for competitor, data in competitor_results.items():
                    st.markdown(f'<div class="competitor-card">', unsafe_allow_html=True)
                    st.subheader(f"Analysis for {competitor}")
                    
                    # Display metrics in a grid
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### Key Metrics")
                        st.markdown(f'<div class="metric-box">{data["metrics"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("### Quick Summary")
                        st.markdown(f'<div class="metric-box">{data["quick_summary"]}</div>', unsafe_allow_html=True)
                    
                    # Parse and display analysis sections
                    analysis_text = data['analysis']
                    sections = {
                        "Content Strategy": "",
                        "Keyword Analysis": "",
                        "Market Presence": "",
                        "Competitive Advantages": "",
                        "Actionable Recommendations": ""
                    }
                    
                    # Parse sections
                    current_section = ""
                    current_content = []
                    
                    for line in analysis_text.split('\n'):
                        if any(section in line for section in sections.keys()):
                            if current_section and current_content:
                                sections[current_section] = '\n'.join(current_content)
                                current_content = []
                            current_section = next(section for section in sections.keys() if section in line)
                        elif current_section and line.strip():
                            current_content.append(line)
                    
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Display sections in tabs
                    analysis_tabs = st.tabs(list(sections.keys()))
                    
                    for tab, (section_name, content) in zip(analysis_tabs, sections.items()):
                        with tab:
                            if content:
                                st.markdown(content)
                            else:
                                st.markdown("*Analysis for this section is being generated...*")
                    
                    st.markdown("---")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="Download Report",
                    data=comprehensive_report,
                    file_name=f"{brand_name}_marketing_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                status_text.text("Report complete!")

if __name__ == "__main__":
    main()
