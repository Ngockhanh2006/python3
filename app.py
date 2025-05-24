import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tenacity import _unset

st.set_page_config(
    page_title="🎓 Student Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

st.markdown("""
<script>
function detectAndApplyTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const root = document.documentElement;
    
    if (prefersDark) {
        root.setAttribute('data-theme', 'dark');
        root.style.setProperty('--detected-theme', 'dark');
    } else {
        root.setAttribute('data-theme', 'light');
        root.style.setProperty('--detected-theme', 'light');
    }
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (e.matches) {
            root.setAttribute('data-theme', 'dark');
            root.style.setProperty('--detected-theme', 'dark');
        } else {
            root.setAttribute('data-theme', 'light');
            root.style.setProperty('--detected-theme', 'light');
        }
    });
}

detectAndApplyTheme();
document.addEventListener('DOMContentLoaded', detectAndApplyTheme);
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: #ffffff;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --accent-primary: #4285f4;
        --accent-secondary: #34a853;
        --border-color: #dee2e6;
        --shadow-color: rgba(0, 0, 0, 0.1);
        --gradient-start: #4285f4;
        --gradient-end: #34a853;
        --sidebar-bg: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --info-color: #17a2b8;
        --metric-shadow: 0 4px 12px rgba(66, 133, 244, 0.2);
    }
    
    [data-theme="dark"], 
    :root[data-theme="dark"] {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1a1a;
        --bg-card: rgba(255, 255, 255, 0.05);
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --accent-primary: #667eea;
        --accent-secondary: #764ba2;
        --border-color: rgba(255, 255, 255, 0.1);
        --shadow-color: rgba(0, 0, 0, 0.4);
        --gradient-start: #667eea;
        --gradient-end: #764ba2;
        --sidebar-bg: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        --success-color: #20c997;
        --warning-color: #fd7e14;
        --danger-color: #e74c3c;
        --info-color: #6f42c1;
        --metric-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    @media (prefers-color-scheme: dark) {
        :root:not([data-theme]) {
            --bg-primary: #0e1117;
            --bg-secondary: #1a1a1a;
            --bg-card: rgba(255, 255, 255, 0.05);
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --accent-primary: #667eea;
            --accent-secondary: #764ba2;
            --border-color: rgba(255, 255, 255, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.4);
            --gradient-start: #667eea;
            --gradient-end: #764ba2;
            --sidebar-bg: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            --success-color: #20c997;
            --warning-color: #fd7e14;
            --danger-color: #e74c3c;
            --info-color: #6f42c1;
            --metric-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
    }
    
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease;
    }
    
    .main {
        background-color: var(--bg-primary) !important;
    }
    
    .main .block-container {
        background-color: var(--bg-primary) !important;
        padding: 2rem !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background-color: var(--bg-primary) !important;
    }
    
    [data-testid="stAppViewContainer"] .main .block-container {
        background-color: var(--bg-primary) !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--metric-shadow);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: var(--metric-shadow);
        color: white;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px var(--shadow-color);
    }
    
    .stSelectbox > div > div {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stMultiSelect > div > div {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stTextInput > div > div > input {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .css-1d391kg, .stSidebar > div:first-child {
        background: var(--sidebar-bg) !important;
        border-right: 3px solid var(--accent-primary) !important;
    }
    
    .stSidebar .stMarkdown h2 {
        color: var(--text-primary) !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 1rem 0 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid var(--accent-primary) !important;
        text-shadow: 0 2px 4px var(--shadow-color) !important;
    }
    
    .stSidebar .stRadio > div {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px);
    }
    
    .stSidebar .stRadio > div > label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        display: flex !important;
        align-items: center !important;
        padding: 0.75rem !important;
        margin: 0.3rem 0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    .stSidebar .stRadio > div > label:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        transform: translateX(5px) !important;
    }
    
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
        padding: 0 1rem;
    }
    
    .team-member {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 500;
        box-shadow: var(--metric-shadow);
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
    }
    
    .team-member:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px var(--shadow-color);
    }
    
    .stInfo {
        background: rgba(66, 133, 244, 0.1) !important;
        border-left: 4px solid var(--accent-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }
    
    .stSuccess {
        background: rgba(40, 167, 69, 0.1) !important;
        border-left: 4px solid var(--success-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border-left: 4px solid var(--warning-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1) !important;
        border-left: 4px solid var(--danger-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stPlotlyChart {
        background: transparent !important;
    }
    
    .js-plotly-plot {
        background: transparent !important;
    }
    
    .stDataFrame {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="metric-container"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px var(--shadow-color) !important;
    }
    
    [data-testid="metric-container"] > div {
        color: var(--text-primary) !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--metric-shadow) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Students_Grading_Dataset.csv")
    df = df.replace("", np.nan)
    numeric_cols = ['Attendance (%)', 'Midterm_Score', 'Final_Score', 'Assignments_Avg',
                    'Quizzes_Avg', 'Participation_Score', 'Projects_Score', 'Total_Score',
                    'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def create_grade_distribution():
    grade_counts = df['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    grade_counts = grade_counts.sort_values(by='Grade')
    
    fig = px.bar(grade_counts, x='Grade', y='Count',
                 color='Grade', text='Count',
                 color_discrete_sequence=px.colors.qualitative.Vivid,
                 title="🎓 Academic Excellence Distribution - Final Grade Analysis")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=500,
        showlegend=False
    )
    return fig

def create_department_performance():
    dept_avg = df.groupby('Department')['Total_Score'].mean().reset_index()
    dept_avg = dept_avg.sort_values(by='Total_Score', ascending=True)
    
    fig = px.bar(dept_avg, y='Department', x='Total_Score',
                 color='Department', text_auto='.1f',
                 orientation='h',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 title="🏆 Departmental Performance Leaderboard - Average Scores by Faculty")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=500,
        showlegend=False
    )
    return fig

def create_gender_grade_distribution():
    male_grades = df[df['Gender'] == 'Male']['Grade'].value_counts().reset_index()
    female_grades = df[df['Gender'] == 'Female']['Grade'].value_counts().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨 Male Students")
        fig_male = px.pie(male_grades, values='count', names='Grade',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_male.update_traces(textposition='inside', textinfo='percent+label+value')
        fig_male.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_male, use_container_width=True)
    
    with col2:
        st.markdown("### 👩 Female Students")
        fig_female = px.pie(female_grades, values='count', names='Grade',
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_female.update_traces(textposition='inside', textinfo='percent+label+value')
        fig_female.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_female, use_container_width=True)

def create_performance_hierarchy():
    grade_counts = df['Grade'].value_counts()
    dept_grade_counts = df.groupby(['Department', 'Grade']).size().reset_index(name='count')
    
    labels = ['All Students'] + list(df['Department'].unique()) + \
             [f"{dept}-{grade}" for dept in df['Department'].unique() for grade in ['A', 'B', 'C', 'D', 'F'] if len(df[(df['Department']==dept) & (df['Grade']==grade)]) > 0]
    
    parents = [''] + ['All Students'] * len(df['Department'].unique()) + \
              [dept for dept in df['Department'].unique() for grade in ['A', 'B', 'C', 'D', 'F'] if len(df[(df['Department']==dept) & (df['Grade']==grade)]) > 0]
    
    values = [len(df)] + [len(df[df['Department']==dept]) for dept in df['Department'].unique()] + \
             [len(df[(df['Department']==dept) & (df['Grade']==grade)]) for dept in df['Department'].unique() for grade in ['A', 'B', 'C', 'D', 'F'] if len(df[(df['Department']==dept) & (df['Grade']==grade)]) > 0]
    
    colors = ['#2E3440',
              '#5E81AC', '#88C0D0', '#81A1C1', '#8FBCBB', '#A3BE8C',
              '#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD',
              '#5E81AC', '#88C0D0', '#81A1C1', '#8FBCBB', '#A3BE8C',
              '#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD']
    
    text_labels = []
    for i, (label, value) in enumerate(zip(labels, values)):
        if ('-' in label):
            dept, grade = label.split('-')
            percentage = (value / len(df[df['Department']==dept])) * 100
            text_labels.append(f"{grade}<br>{value} students<br>({percentage:.1f}%)")
        elif (label != 'All Students' and label in df['Department'].unique()):
            percentage = (value / len(df)) * 100
            text_labels.append(f"{label}<br>{value} students<br>({percentage:.1f}%)")
        else:
            text_labels.append(f"{label}<br>{value} students")
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        text=text_labels,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Students: %{value}<br>Percentage: %{percentParent}<extra></extra>',
        maxdepth=3,
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color="#FFFFFF", width=3)
        ),
        textfont=dict(
            size=11,
            color="#2E3440",
            family="Arial Black"
        ),
        insidetextorientation='radial'
    ))
    
    fig.update_layout(
        title="🎯 Student Performance Hierarchy<br><sub>Interactive breakdown by department and grade with student counts</sub>",
        title_font_size=18,
        font=dict(color='#2E3440', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=650
    )
    
    return fig

def create_study_hours_scatter():
    available_grades = sorted(df['Grade'].unique())
    selected_grades = st.multiselect(
        "🎯 Select grades to display:",
        options=available_grades,
        default=available_grades,
        key="grade_selector"
    )
    
    if not selected_grades:
        st.warning("⚠️ Please select at least one grade to display.")
        return None
    
    filtered_df = df[df['Grade'].isin(selected_grades)]
    
    fig = px.box(filtered_df,
                 x='Grade',
                 y='Study_Hours_per_Week',
                 color='Grade',
                 points="all",
                 title="📚 Study Hours Distribution by Grade",
                 color_discrete_sequence=px.colors.qualitative.Set1)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=600,
        xaxis_title='Grade',
        yaxis_title='Study Hours per Week',
        showlegend=False
    )
    
    fig.update_traces(
        marker=dict(size=8, opacity=0.7),
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    )
    
    return fig

def create_attendance_impact(theme='auto'):
    min_attendance = df['Attendance (%)'].replace(0, np.nan).min()
    att_bins = [50, 60, 70, 75, 80, 85, 90, 95, 100] if min_attendance >= 50 else [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    df['Attendance_Bin'] = pd.cut(df['Attendance (%)'], bins=att_bins, include_lowest=True)
    
    att_avg = df.groupby('Attendance_Bin')['Final_Score'].mean().reset_index()
    att_avg['Attendance_Mid'] = [(interval.left + interval.right) / 2 for interval in att_avg['Attendance_Bin']]
    att_avg = att_avg.sort_values('Attendance_Mid')
    
    att_count = df.groupby('Attendance_Bin').size().reset_index(name='Count')
    att_count['Attendance_Mid'] = [(interval.left + interval.right) / 2 for interval in att_count['Attendance_Bin']]
    
    att_data = pd.merge(att_avg, att_count, on=['Attendance_Bin', 'Attendance_Mid'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=att_data['Attendance_Mid'],
        y=att_data['Final_Score'],
        mode='lines+markers+text',
        name='Average Final Score',
        line=dict(width=4, color='#00AA88'),
        marker=dict(size=12, color='#00AA88', line=dict(width=2, color='#006B5A')),
        text=[f'Score: {score:.1f}<br>Students: {count}' for score, count in zip(att_data['Final_Score'], att_data['Count'])],
        textposition='top center',
        textfont=dict(size=10, family='Arial Bold'),
        hovertemplate='<b>Attendance: %{x:.0f}%</b><br>' +
                      'Average Final Score: %{y:.1f}<br>' +
                      'Number of Students: %{customdata}<br>' +
                      '<extra></extra>',
        customdata=att_data['Count']
    ))
    
    fig.update_layout(
        title="📅 Attendance Success Correlation - Class Presence vs Final Performance",
        xaxis_title='Attendance (%)',
        yaxis_title='Average Final Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=22,
        height=500,
        margin=dict(l=80, r=80, t=100, b=80),
        showlegend=False,
        xaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            showline=True,
            linecolor='rgba(128,128,128,0.5)',
            linewidth=1,
            range=[att_data['Attendance_Mid'].min()-5, att_data['Attendance_Mid'].max()+5]
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            showline=True,
            linecolor='rgba(128,128,128,0.5)',
            linewidth=1
        )
    )
    
    fig.add_trace(go.Scatter(
        mode='lines',
        name='Trend',
        line=dict(dash='dash', width=2, color='rgba(255,100,100,0.8)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    return fig

def create_score_distribution():
    score_cols = ['Midterm_Score', 'Final_Score', 'Assignments_Avg', 'Quizzes_Avg', 'Projects_Score']
    
    fig = go.Figure()
    
    for i, col in enumerate(score_cols):
        data = df[col].dropna()
        
        fig.add_trace(go.Violin(
            y=data,
            name=col.replace('_', ' '),
            box_visible=True,
            meanline_visible=True,
            fillcolor=px.colors.qualitative.Vivid[i % len(px.colors.qualitative.Vivid)],
            opacity=0.7,
            x0=col.replace('_', ' ')
        ))
    
    fig.update_layout(
        title="📊 Assessment Performance Breakdown - Score Distribution",
        xaxis_title='Assessment Type',
        yaxis_title='Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=600,
        showlegend=False
    )
    
    return fig

def create_internet_impact():
    internet_grade = df.pivot_table(
        index='Internet_Access_at_Home',
        columns='Grade',
        aggfunc='size',
        fill_value=0
    ).reset_index()
    
    grade_cols = [col for col in internet_grade.columns if col != 'Internet_Access_at_Home']
    for i, row in internet_grade.iterrows():
        total = sum(row[grade_cols])
        for col in grade_cols:
            internet_grade.loc[i, col] = (row[col] / total) * 100
    
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    
    for i, grade in enumerate(['A', 'B', 'C', 'D', 'F']):
        if grade in internet_grade.columns:
            fig.add_trace(go.Bar(
                x=internet_grade['Internet_Access_at_Home'],
                y=internet_grade[grade],
                name=f'Grade {grade}',
                text=internet_grade[grade].round(1).astype(str) + '%',
                textposition='inside',
                marker_color=colors[i % len(colors)]
            ))
    
    fig.update_layout(
        barmode='stack',
        title="🌐 Digital Divide Impact - Internet Access vs Academic Achievement",
        xaxis_title='Internet Access at Home',
        yaxis_title='Percentage of Students (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=600
    )
    return fig

def create_stress_heatmap():
    stress_grade = df.groupby(['Stress_Level (1-10)', 'Grade']).size().reset_index(name='Count')
    stress_grade['Stress_Level (1-10)'] = stress_grade['Stress_Level (1-10)'].round().astype(int)
    stress_pivot = stress_grade.pivot_table(
        index='Stress_Level (1-10)',
        columns='Grade',
        values='Count',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = px.imshow(
        stress_pivot,
        labels=dict(x="Grade", y="Stress Level (1-10)", color="Students"),
        x=stress_pivot.columns,
        y=stress_pivot.index,
        color_continuous_scale='RdYlBu_r',
        title="😰 Student Stress vs Academic Performance - Correlation Analysis"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=22,
        height=500,
        margin=dict(l=80, r=120, t=100, b=80),
        coloraxis_colorbar=dict(
            title="Number of Students",
            title_font=dict(size=12),
            tickfont=dict(size=11),
            bgcolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            len=0.8
        ),
        xaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            showgrid=False
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            showgrid=False
        )
    )
    
    for i, stress_level in enumerate(stress_pivot.index):
        for j, grade in enumerate(stress_pivot.columns):
            value = stress_pivot.iloc[i, j]
            if value > 0:
                text_color = 'white' if value > stress_pivot.values.max() * 0.6 else 'black'
                fig.add_annotation(
                    x=j,
                    y=i,
                    text=str(value),
                    showarrow=False,
                    font=dict(color=text_color, size=11, family='Arial Bold')
                )
    
    return fig

def create_sleep_analysis():
    sleep_bins = [0, 4, 5, 6, 7, 8, 9, 12]
    sleep_labels = ['<4h', '4-5h', '5-6h', '6-7h', '7-8h', '8-9h', '9h+']
    
    df['Sleep_Group'] = pd.cut(df['Sleep_Hours_per_Night'], 
                              bins=sleep_bins, 
                              labels=sleep_labels,
                              include_lowest=True)
    
    sleep_stats = df.groupby('Sleep_Group').agg({
        'Total_Score': 'mean',
        'Stress_Level (1-10)': 'mean',
        'Grade': lambda x: (x == 'A').mean() * 100
    }).reset_index()
    
    sleep_stats.columns = ['Sleep_Hours', 'Avg_Score', 'Avg_Stress', 'A_Grade_Percentage']
    sleep_counts = df.groupby('Sleep_Group').size().reset_index(name='Count')
    sleep_stats = pd.merge(sleep_stats, sleep_counts, left_on='Sleep_Hours', right_on='Sleep_Group')
    sleep_stats.drop('Sleep_Group', axis=1, inplace=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=sleep_stats['Sleep_Hours'],
        y=sleep_stats['Avg_Score'],
        name='Average Score',
        marker_color='#4287f5',
        opacity=0.8,
        text=sleep_stats['Avg_Score'].round(1),
        textposition='auto'
    ))
    
    fig.add_trace(go.Scatter(
        x=sleep_stats['Sleep_Hours'],
        y=sleep_stats['A_Grade_Percentage'],
        mode='lines+markers',
        name='% A Grades',
        yaxis='y2',
        line=dict(color='#ff9500', width=3),
        marker=dict(size=10, color='#ff9500')
    ))
    
    fig.update_layout(
        title="😴 Sleep Quality Impact - Rest Duration vs Academic Excellence",
        xaxis_title='Sleep Hours per Night',
        yaxis=dict(
            title='Average Score',
            title_font=dict(color='#4287f5'),
            tickfont=dict(color='#4287f5')
        ),
        yaxis2=dict(
            title='% A Grades',
            overlaying='y',
            side='right',
            title_font=dict(color='#ff9500'),
            tickfont=dict(color='#ff9500')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=600
    )
    return fig

def create_grade_distribution_by_income():
    df_clean = df.dropna(subset=['Family_Income_Level', 'Grade'])
    
    grade_income = df_clean.groupby(['Family_Income_Level', 'Grade']).size().unstack(fill_value=0)
    
    grade_colors = {
        'A': '#00AA55',
        'B': '#8B4FB3',
        'C': '#E67C00',
        'D': '#0088CC',
        'F': '#CC3355'
    }
    
    fig = go.Figure()
    
    income_levels = grade_income.index.tolist()
    
    for grade in ['A', 'B', 'C', 'D', 'F']:
        if grade in grade_income.columns:
            fig.add_trace(
                go.Bar(
                    x=income_levels,
                    y=grade_income[grade],
                    name=f'Grade {grade}',
                    marker_color=grade_colors[grade],
                    text=grade_income[grade],
                    textposition='inside',
                    textfont=dict(color='white', size=12, family='Arial Bold'),
                    hovertemplate=f'<b>Grade {grade}</b><br>' +
                                  'Income Level: %{x}<br>' +
                                  'Number of Students: %{y}<br>' +
                                  '<extra></extra>'
                )
            )
    
    text_color = 'var(--text-primary)'
    grid_color = 'var(--border-color)'
    
    fig.update_layout(
        title=dict(
            text="💰 Income vs Grades - Student Distribution Analysis",
            font=dict(size=22),
        ),
        xaxis_title="Family Income Level",
        yaxis_title="Number of Students",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=600,
        barmode='stack',
        margin=dict(l=100, r=100, t=120, b=120),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        xaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            showline=True,
            linecolor='rgba(128,128,128,0.5)',
            linewidth=1,
            tickangle=0,
            categoryorder='array',
            categoryarray=['Low', 'Medium', 'High']
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            showline=True,
            linecolor='rgba(128,128,128,0.5)',
            linewidth=1
        )
    )
    
    total_students_by_income = df_clean.groupby('Family_Income_Level').size()
    
    annotations = []
    for i, income_level in enumerate(income_levels):
        total_students = total_students_by_income[income_level]
        total_height = grade_income.loc[income_level].sum()
        annotations.append(
            dict(
                x=income_level,
                y=total_height + total_height * 0.05,
                text=f"Total: {total_students}",
                showarrow=False,
                font=dict(size=11, family='Arial Bold', color='yellow'),
                xanchor='center',
                bgcolor='black',
                bordercolor='rgba(255,255,255,0)',
                borderwidth=1,
                borderpad=4
            )
        )
    
    fig.update_layout(annotations=annotations)
    
    return fig

df = load_data()

st.markdown("""
<div class="main-header">
    <h1>🎓 Student Academic Performance Dashboard</h1>
    <p>Comprehensive analysis of student performance metrics and factors</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Total Students</h3>
        <h2>{}</h2>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    avg_score = df['Total_Score'].mean()
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Average Score</h3>
        <h2>{:.1f}</h2>
    </div>
    """.format(avg_score), unsafe_allow_html=True)

with col3:
    top_grade_pct = (df['Grade'] == 'A').mean() * 100
    st.markdown("""
    <div class="metric-card">
        <h3>🏆 A Grade Rate</h3>
        <h2>{:.1f}%</h2>
    </div>
    """.format(top_grade_pct), unsafe_allow_html=True)

with col4:
    avg_attendance = df['Attendance (%)'].mean()
    st.markdown("""
    <div class="metric-card">
        <h3>📅 Avg Attendance</h3>
        <h2>{:.1f}%</h3>
    </div>
    """.format(avg_attendance), unsafe_allow_html=True)

st.markdown("### 👥 Research Team")
team_members = [
    "Mai Vũ Như Quỳnh", "Lê Ngọc Khánh", "Võ Thị Tuyết Mai",
    "Phạm Nguyễn Tường Lam", "Ngô Quỳnh Anh", "Lưu Minh Đăng"
]

st.markdown('<div class="team-grid">', unsafe_allow_html=True)
cols = st.columns(3)
for i, member in enumerate(team_members):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="team-member" style="margin-bottom: 1.5rem;">
            {member}
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📋 View Dataset", expanded=False):
    st.dataframe(df, use_container_width=True)

chart_options = [
    "📊 Grade Distribution", "🏢 Department Performance", "👫 Gender Analysis",
    "🎯 Performance Hierarchy", "💰 Income vs Grades", "📅 Attendance Impact",
    "📈 Score Components", "🌐 Internet Access Effect", "😰 Stress Analysis", "😴 Sleep Impact"
]

selected_chart = st.sidebar.radio("Select Analysis:", chart_options)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

if selected_chart == "📊 Grade Distribution":
    st.plotly_chart(create_grade_distribution(), use_container_width=True)
    st.info("📌 **Insight:** This visualization shows the distribution of final grades across all students, helping identify overall class performance patterns.")

elif selected_chart == "🏢 Department Performance":
    st.plotly_chart(create_department_performance(), use_container_width=True)
    st.info("📌 **Insight:** Compare average performance across different academic departments to identify strengths and areas for improvement.")

elif selected_chart == "👫 Gender Analysis":
    create_gender_grade_distribution()
    st.info("📌 **Insight:** Analyze grade distribution patterns between male and female students to identify any gender-based performance differences.")

elif selected_chart == "🎯 Performance Hierarchy":
    st.plotly_chart(create_performance_hierarchy(), use_container_width=True)
    st.info("📌 **Insight:** Interactive hierarchy showing the relationship between departments, gender, and grades. Click segments to explore specific branches.")

elif selected_chart == "💰 Income vs Grades":
    st.plotly_chart(create_grade_distribution_by_income(), use_container_width=True)
    st.info("📌 **Insight:** This visualization shows the distribution of grades across different family income levels using parallel columns, making it easy to compare grade counts between income groups.")

elif selected_chart == "📅 Attendance Impact":
    st.plotly_chart(create_attendance_impact(), use_container_width=True)
    st.info("📌 **Insight:** Demonstrates how class attendance correlates with final exam performance, supporting the importance of regular attendance.")

elif selected_chart == "📈 Score Components":
    st.plotly_chart(create_score_distribution(), use_container_width=True)
    st.info("📌 **Insight:** Compare score distributions across different assessment types to understand performance patterns in various evaluation methods.")

elif selected_chart == "🌐 Internet Access Effect":
    st.plotly_chart(create_internet_impact(), use_container_width=True)
    st.info("📌 **Insight:** Analyze how home internet access affects academic performance, highlighting digital divide impacts on education.")

elif selected_chart == "😰 Stress Analysis":
    st.plotly_chart(create_stress_heatmap(), use_container_width=True)
    st.info("📌 **Insight:** Heatmap showing the relationship between student stress levels and academic grades, helping identify optimal stress ranges.")

elif selected_chart == "😴 Sleep Impact":
    st.plotly_chart(create_sleep_analysis(), use_container_width=True)
    st.info("📌 **Insight:** Examine how sleep duration affects academic performance and A-grade achievement rates, supporting healthy sleep habits.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;'>
    <h4>🎓 Student Performance Analytics Dashboard</h4>
    <p>Powered by Streamlit • Data-driven Educational Insights</p>
</div>
""", unsafe_allow_html=True)
