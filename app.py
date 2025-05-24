import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="🎓 Student Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stPlotlyChart {
        background: transparent !important;
    }
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
        padding: 0 1rem;
    }
    .team-member {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: 500;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .team-member:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    .sidebar .stRadio > label {
        font-size: 14px;
        font-weight: 500;
    }
    .stInfo {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Enhanced Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
        border-right: 3px solid #667eea !important;
    }
    
    .stSidebar > div:first-child {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        border-right: 3px solid #667eea;
    }
    
    .stSidebar .stMarkdown h2 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 1rem 0 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid #667eea !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .stSidebar .stRadio > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid rgba(255, 255, 255, .1) !important;
    }
    
    .stSidebar .stRadio > div > label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        display: flex !important;
        align-items: center !important;
        padding: 0.75rem !important;
        margin: 0.3rem 0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid transparent !important;
    }
    
    .stSidebar .stRadio > div > label:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stSidebar .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        transform: translateX(8px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        font-weight: 600 !important;
    }
    
    .stSidebar .stRadio input[type="radio"] {
        accent-color: #667eea !important;
        margin-right: 0.75rem !important;
        transform: scale(1.2) !important;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric {
        background: transparent;
    }
    
    .plot-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Remove duplicate sidebar styling */
    .css-1d391kg {
        display: none;
    }
    
    /* Ensure single sidebar */
    section[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #2C3E50 0%, #3498DB 100%);
        border-radius: 0 15px 15px 0;
    }
    
    /* Hide duplicate navigation elements */
    .css-17lntkn, .css-pkbazv {
        display: none !important;
    }
    
    /* Main content area styling */
    .block-container {
        padding-top: 2rem;
        max-width: 100%;
    }
    
    /* Sidebar navigation styling */
    .css-1lcbmhc .css-1outpf7 {
        background-color: transparent;
    }
    
    /* Remove extra navigation elements */
    [data-testid="stSidebar"] .css-17lntkn {
        display: none;
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

def create_sunburst_chart():
    sunburst_data = df.groupby(['Department', 'Gender', 'Grade']).size().reset_index(name='Count')
    
    fig = px.sunburst(
        sunburst_data,
        path=['Department', 'Gender', 'Grade'],
        values='Count',
        color='Count',
        color_continuous_scale='Viridis',
        title="🎯 Academic Performance Hierarchy - Department → Gender → Grade Distribution"
    )
    
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=2,
        insidetextorientation='radial',
        textinfo="label+value"
    )
    
    fig.update_layout(
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22
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
    
    # Changed to box plot to avoid NaN size issues
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

def create_attendance_impact():
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
        line=dict(width=4, color='#00ffaa'),
        marker=dict(size=12, color='#00ffaa', line=dict(width=2, color='darkgreen')),
        text=[f'Score: {score:.1f}<br>Students: {count}' for score, count in zip(att_data['Final_Score'], att_data['Count'])],
        textposition='top center',
        textfont=dict(color='white', size=10)
    ))
    
    fig.update_layout(
        title="📅 Attendance Success Correlation - Class Presence vs Final Performance",
        xaxis_title='Attendance (%)',
        yaxis_title='Average Final Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=500,
        showlegend=False
    )
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
        title="📊 Assessment Performance Breakdown - Score Distribution (Violin Plot)",
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
        color_continuous_scale='Blues',
        title="😰 Student Stress vs Academic Performance - Correlation Analysis"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=500,
        coloraxis_colorbar=dict(
            title="Number of Students",
            title_font=dict(color='white'),
            tickfont=dict(color='white'),
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='white',
            borderwidth=1
        )
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

def create_parent_education_impact():
    clean_df = df.dropna(subset=['Parent_Education_Level'])
    clean_df = clean_df[clean_df['Parent_Education_Level'].str.strip() != '']
    
    if clean_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No valid Parent Education data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=20, color="white")
        )
        fig.update_layout(
            title="🎓 Parent Education Impact - Family Background vs Academic Success",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            height=500
        )
        return fig
    
    parent_ed_data = clean_df.groupby('Parent_Education_Level').agg({
        'Total_Score': 'mean',
        'Grade': lambda x: (x == 'A').mean() * 100
    }).reset_index()
    
    parent_ed_data.columns = ['Parent_Education', 'Avg_Score', 'A_Grade_Pct']
    
    counts = clean_df.groupby('Parent_Education_Level').size().reset_index(name='Student_Count')
    parent_ed_data = pd.merge(parent_ed_data, counts, left_on='Parent_Education', right_on='Parent_Education_Level')
    parent_ed_data = parent_ed_data.drop('Parent_Education_Level', axis=1)
    
    parent_ed_data = parent_ed_data.sort_values('Avg_Score', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=parent_ed_data['Parent_Education'],
        y=parent_ed_data['Avg_Score'],
        name='Average Score',
        marker_color='#4ecdc4',
        opacity=0.8,
        text=[f'{score:.1f}' for score in parent_ed_data['Avg_Score']],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Arial Black')
    ))
    
    fig.add_trace(go.Scatter(
        x=parent_ed_data['Parent_Education'],
        y=parent_ed_data['A_Grade_Pct'],
        mode='lines+markers+text',
        name='% A Grades',
        yaxis='y2',
        line=dict(color='#ff6b6b', width=4),
        marker=dict(size=12, color='#ff6b6b', line=dict(width=2, color='white')),
        text=[f'{pct:.1f}%' for pct in parent_ed_data['A_Grade_Pct']],
        textposition='top center',
        textfont=dict(color='white', size=11, family='Arial Black')
    ))
    
    fig.update_layout(
        title="🎓 Parent Education Impact - Academic Performance by Family Background",
        xaxis_title='Parent Education Level',
        yaxis=dict(
            title='Average Score',
            title_font=dict(color='#4ecdc4', size=14),
            tickfont=dict(color='#4ecdc4', size=12),
            range=[0, 100]
        ),
        yaxis2=dict(
            title='Percentage of A Grades',
            overlaying='y',
            side='right',
            title_font=dict(color='#ff6b6b', size=14),
            tickfont=dict(color='#ff6b6b', size=12),
            range=[0, max(parent_ed_data['A_Grade_Pct']) + 10]
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=22,
        height=500,
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='white',
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
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
    "🎯 Performance Hierarchy", "🎓 Parent Education Impact", "📅 Attendance Impact",
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
    st.plotly_chart(create_sunburst_chart(), use_container_width=True)
    st.info("📌 **Insight:** Interactive hierarchy showing the relationship between departments, gender, and grades. Click segments to explore specific branches.")

elif selected_chart == "🎓 Parent Education Impact":
    st.plotly_chart(create_parent_education_impact(), use_container_width=True)
    st.info("📌 **Insight:** Explore how parental education levels affect student performance, A-grade rates, and study habits, revealing the impact of family educational background on academic success.")

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
