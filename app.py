import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with dark theme
st.set_page_config(
    page_title="Student Performance Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better visibility on dark background
st.markdown("""
<style>
    .stPlotlyChart {
        background-color: rgba(0,0,0,0) !important;
    }
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 h2, .st-emotion-cache-16txtl3 h3 {
        color: white !important;
    }
    .st-emotion-cache-16txtl3 p, .st-emotion-cache-16txtl3 ol, .st-emotion-cache-16txtl3 ul, .st-emotion-cache-16txtl3 dl {
        color: #f0f0f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Students_Grading_Dataset.csv")
    # Handle missing values
    df = df.replace("", np.nan)
    
    # Convert numeric columns to appropriate types
    numeric_cols = ['Attendance (%)', 'Midterm_Score', 'Final_Score', 'Assignments_Avg',
                    'Quizzes_Avg', 'Participation_Score', 'Projects_Score', 'Total_Score',
                    'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

df = load_data()

# Title and header section
st.title("Student Academic Performance Dashboard")

# Team member section
st.markdown("""
### Team Members
- Mai Vũ Như Quỳnh
- Lê Ngọc Khánh
- Võ Thị Tuyết Mai
- Phạm Nguyễn Tường Lam
- Ngô Quỳnh Anh
- Trần Quang Thiện Thông
""")

# Introduction text
st.markdown("""
This dashboard analyzes the academic performance and related factors of students based on various metrics.
Explore the visualizations by selecting different charts from the sidebar.
""")

# Show raw data if requested
with st.expander("Show Raw Data"):
    st.dataframe(df)

# Sidebar navigation
st.sidebar.title("Navigation")
chart_options = [
    "1. Distribution of Final Grades",
    "2. Average Performance by Department",
    "3. Grade Distribution by Gender",
    "4. Grade Distribution Hierarchy",
    "5. Study Hours vs Total Score",
    "6. Attendance Impact on Final Score",
    "7. Distribution of Score Components",
    "8. Internet Access Impact on Performance",
    "9. Stress Level vs Performance",
    "10. Parent Education & Student Performance"
]
selected_chart = st.sidebar.radio("Select a chart to view:", chart_options)

# Display selected chart
if selected_chart == "1. Distribution of Final Grades":
    st.subheader("1. Distribution of Final Grades")
    grade_counts = df['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    grade_counts = grade_counts.sort_values(by='Grade')
    
    fig1 = px.bar(grade_counts, x='Grade', y='Count', 
                 color='Grade', text='Count',
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig1.update_layout(
        xaxis_title='Grade', 
        yaxis_title='Number of Students',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This bar chart shows the distribution of final grades (A, B, C, D, F) across the student population.
    
    **How to interpret:** Higher bars indicate more students achieving that particular grade. This helps identify the most common 
    grade outcomes and overall class performance.
    """)

elif selected_chart == "2. Average Performance by Department":
    st.subheader("2. Average Performance by Department")
    dept_avg = df.groupby('Department')['Total_Score'].mean().reset_index()
    dept_avg = dept_avg.sort_values(by='Total_Score', ascending=True)
    
    fig2 = px.bar(dept_avg, y='Department', x='Total_Score',
                 color='Department', text_auto='.2f',
                 orientation='h',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(
        yaxis_title='Department', 
        xaxis_title='Average Total Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This horizontal bar chart displays the average total score achieved by students in each academic department.
    
    **How to interpret:** Longer bars represent higher average scores. This visualization helps identify which departments have 
    students with the strongest or weakest academic performance.
    """)

elif selected_chart == "3. Grade Distribution by Gender":
    st.subheader("3. Grade Distribution by Gender")
    
    # Create two columns for the pie charts
    col1, col2 = st.columns(2)
    
    # Filter data by gender
    male_grades = df[df['Gender'] == 'Male']['Grade'].value_counts().reset_index()
    female_grades = df[df['Gender'] == 'Female']['Grade'].value_counts().reset_index()
    
    # Male pie chart
    with col1:
        st.write("Male Students")
        fig3a = px.pie(male_grades, values='count', names='Grade',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig3a.update_traces(textposition='inside', textinfo='percent+label')
        fig3a.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig3a, use_container_width=True)
    
    # Female pie chart
    with col2:
        st.write("Female Students")
        fig3b = px.pie(female_grades, values='count', names='Grade',
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig3b.update_traces(textposition='inside', textinfo='percent+label')
        fig3b.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig3b, use_container_width=True)
    
    # Add explanatory note after both pie charts
    st.info("""
    **About this chart:** These pie charts show the grade distribution separately for male and female students.
    
    **How to interpret:** Each slice represents the percentage of students achieving a specific grade within each gender group.
    This helps identify any potential gender-based differences in academic achievement patterns.
    """)

elif selected_chart == "4. Grade Distribution Hierarchy":
    st.subheader("4. Grade Distribution Hierarchy")
    
    # Prepare data for sunburst chart - count students by department, gender and grade
    sunburst_data = df.groupby(['Department', 'Gender', 'Grade']).size().reset_index(name='Count')
    
    # Create sunburst chart with line separations
    fig4 = px.sunburst(
        sunburst_data,
        path=['Department', 'Gender', 'Grade'],
        values='Count',
        color='Grade',
        color_discrete_sequence=px.colors.qualitative.Bold,
        maxdepth=2
    )
    
    # Add line separations
    fig4.update_traces(
        marker_line_color='black',      # Black lines for contrast
        marker_line_width=2,            # Thicker lines for better visibility
        insidetextorientation='radial'  # Text follows the radial direction
    )
    
    fig4.update_layout(
        height=700,
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This sunburst chart shows the hierarchical relationship between departments, gender, and grades.
    
    **How to interpret:** Moving from the center outward, each ring represents a different category level. The innermost ring shows departments,
    the middle ring shows gender, and the outer ring shows grades. The size of each segment indicates the number of students in that category.
    **Tip:** Click on segments to zoom in and explore specific branches of the hierarchy.
    """)

elif selected_chart == "5. Study Hours vs Total Score":
    st.subheader("5. Study Hours vs Total Score")
    
    # Add grade selection widget in the sidebar
    available_grades = sorted(df['Grade'].unique())
    selected_grades = st.multiselect(
        "Select grades to display:",
        options=available_grades,
        default=available_grades,
        key="grade_selector"
    )
    
    # Filter data based on selected grades
    if not selected_grades:  # If no grade is selected, show a message
        st.warning("Please select at least one grade to display.")
    else:
        filtered_df = df[df['Grade'].isin(selected_grades)]
        
        # Create a bubble chart with smaller dots
        fig5 = px.scatter(filtered_df, 
                         x='Study_Hours_per_Week', 
                         y='Total_Score',
                         size='Final_Score',
                         color='Grade',
                         hover_name='Student_ID',
                         size_max=15,
                         opacity=0.7)
        
        fig5.update_layout(
            xaxis_title='Study Hours per Week',
            yaxis_title='Total Score',
            showlegend=True,
            height=700,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        # Add explanatory note
        st.info("""
        **About this chart:** This scatter plot shows the relationship between weekly study hours and total academic scores.
        
        **How to interpret:** Each dot represents a student, with the size indicating their final score. The position shows their 
        study hours (x-axis) and total score (y-axis). Colors represent different grades.
        
        **Tip:** Use the grade selector above to filter which grades are displayed.
        """)

elif selected_chart == "6. Attendance Impact on Final Score":
    st.subheader("6. Attendance Impact on Final Score")
    
    # Calculate the lowest non-zero attendance value
    min_attendance = df['Attendance (%)'].replace(0, np.nan).min()
    
    # Create optimized bins focusing on where data exists
    if min_attendance < 50:
        # If there's data below 50%, create bins with smaller steps for lower ranges
        att_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    else:
        # If no data below 50%, focus bins on the 50-100% range
        att_bins = [50, 60, 70, 75, 80, 85, 90, 95, 100]
    
    # Group by attendance bins
    df['Attendance_Bin'] = pd.cut(df['Attendance (%)'], 
                                 bins=att_bins,
                                 include_lowest=True)
    
    # Get average final score per bin
    att_avg = df.groupby('Attendance_Bin')['Final_Score'].mean().reset_index()
    att_avg['Attendance_Mid'] = [(interval.left + interval.right)/2 for interval in att_avg['Attendance_Bin']]
    att_avg = att_avg.sort_values('Attendance_Mid')
    
    # Count students in each bin
    att_count = df.groupby('Attendance_Bin').size().reset_index(name='Count')
    att_count['Attendance_Mid'] = [(interval.left + interval.right)/2 for interval in att_count['Attendance_Bin']]
    
    # Merge datasets
    att_data = pd.merge(att_avg, att_count, on=['Attendance_Bin', 'Attendance_Mid'])
    
    # Create figure
    fig6 = go.Figure()
    
    # Add line for average score
    fig6.add_trace(go.Scatter(
        x=att_data['Attendance_Mid'],
        y=att_data['Final_Score'],
        mode='lines+markers',
        name='Avg Final Score',
        line=dict(width=3, color='#00ffaa'),
        marker=dict(
            size=10, 
            color='#00ffaa',
            line=dict(width=2, color='darkgreen')
        )
    ))
    
    # Add information about student count as hover text
    hover_text = [f"Attendance: {x:.1f}%<br>Students: {y}" 
                 for x, y in zip(att_data['Attendance_Mid'], att_data['Count'])]
    
    # Add markers showing student counts
    fig6.add_trace(go.Scatter(
        x=att_data['Attendance_Mid'],
        y=att_data['Final_Score'],
        mode='markers',
        marker=dict(
            size=att_data['Count'].apply(lambda x: min(max(x*2, 5), 25)),
            color='rgba(0, 255, 170, 0.3)',
            line=dict(width=1, color='#00ffaa')
        ),
        name='Student Count',
        text=hover_text,
        hoverinfo='text'
    ))
    
    fig6.update_layout(
        xaxis=dict(
            title='Attendance (%)',
            tickmode='array',
            tickvals=att_data['Attendance_Mid'],
            ticktext=[f"{int(x.left)}-{int(x.right)}%" for x in att_data['Attendance_Bin']]
        ),
        yaxis_title='Average Final Score',
        hovermode='closest',
        height=700,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This line chart shows the relationship between class attendance rates and final exam scores.
    
    **How to interpret:** The line shows average final scores at different attendance levels. The size of each dot indicates 
    the number of students in that attendance range. Generally, a rising trend suggests that higher attendance correlates with 
    better final scores.
    """)

elif selected_chart == "7. Distribution of Score Components":
    st.subheader("7. Distribution of Score Components")
    score_cols = ['Midterm_Score', 'Final_Score', 'Assignments_Avg', 
                  'Quizzes_Avg', 'Projects_Score']
    
    # Prepare data for violin plot
    score_df = pd.melt(df[score_cols], 
                       value_vars=score_cols,
                       var_name='Assessment Type', 
                       value_name='Score')
    
    fig7 = px.violin(score_df, x='Assessment Type', y='Score',
                    box=True,
                    points='all',
                    color='Assessment Type',
                    color_discrete_sequence=px.colors.qualitative.Vivid)
    fig7.update_layout(
        xaxis_title='Assessment Type', 
        yaxis_title='Score',
        showlegend=False,
        height=700,  # Increased height
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig7, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This violin plot shows the distribution of scores across different assessment types.
    
    **How to interpret:** The width of each "violin" shows the density of scores at that value. Wider sections indicate more students 
    received that score. The boxplot inside shows the median (middle line), interquartile range (box), and outliers (points beyond the whiskers).
    This helps compare the score patterns across different assignments and exams.
    """)

elif selected_chart == "8. Internet Access Impact on Performance":
    st.subheader("8. Internet Access Impact on Performance")
    
    # Calculate grade distribution by internet access
    internet_grade = df.pivot_table(
        index='Internet_Access_at_Home',
        columns='Grade',
        aggfunc='size',
        fill_value=0
    ).reset_index()
    
    # Convert to percentages for better comparison
    grade_cols = [col for col in internet_grade.columns if col != 'Internet_Access_at_Home']
    for i, row in internet_grade.iterrows():
        total = sum(row[grade_cols])
        for col in grade_cols:
            internet_grade.loc[i, col] = (row[col] / total) * 100
    
    # Create stacked bar chart
    fig8 = go.Figure()
    
    for grade in ['A', 'B', 'C', 'D', 'F']:
        if grade in internet_grade.columns:
            fig8.add_trace(go.Bar(
                x=internet_grade['Internet_Access_at_Home'],
                y=internet_grade[grade],
                name=f'Grade {grade}',
                text=internet_grade[grade].round(1).astype(str) + '%',
                textposition='inside'
            ))
    
    fig8.update_layout(
        barmode='stack',
        xaxis_title='Internet Access at Home',
        yaxis_title='Percentage of Students (%)',
        legend_title='Grade',
        hovermode='x',
        height=700,  # Increased height
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig8, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This stacked bar chart shows the percentage distribution of grades for students with and without internet access at home.
    
    **How to interpret:** Each bar segment represents the percentage of students achieving a specific grade. The full height of each bar is 100%.
    This visualization helps assess whether internet access at home influences academic performance.
    """)

elif selected_chart == "9. Stress Level vs Performance":
    st.subheader("9. Stress Level vs Performance")
    
    # Create a pivot table for stress level vs grade
    stress_grade = df.groupby(['Stress_Level (1-10)', 'Grade']).size().reset_index(name='Count')
    stress_grade['Stress_Level (1-10)'] = stress_grade['Stress_Level (1-10)'].round().astype(int)
    stress_pivot = stress_grade.pivot_table(
        index='Stress_Level (1-10)', 
        columns='Grade', 
        values='Count',
        aggfunc='sum',
        fill_value=0
    )
    
    # Create heatmap
    fig9 = px.imshow(
        stress_pivot,
        labels=dict(x="Grade", y="Stress Level (1-10)", color="Number of Students"),
        x=stress_pivot.columns,
        y=stress_pivot.index,
        color_continuous_scale='Viridis'  # Better for dark backgrounds
    )
    
    fig9.update_layout(
        xaxis_title='Grade',
        yaxis_title='Stress Level (1-10)',
        height=700,  # Increased height
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig9, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This heatmap displays the relationship between student stress levels and their final grades.
    
    **How to interpret:** Each cell shows how many students with a particular stress level (y-axis) achieved a specific grade (x-axis).
    Darker colors indicate a higher number of students. This visualization helps identify whether certain stress levels are associated with 
    better or worse academic performance.
    """)

elif selected_chart == "10. Parent Education & Student Performance":
    st.subheader("10. Parent Education & Student Performance")
    
    # Fill missing values
    df['Parent_Education_Level'] = df['Parent_Education_Level'].fillna('Not Reported')
    
    # Calculate average score by parent education level
    edu_avg = df.groupby('Parent_Education_Level')['Total_Score'].mean().reset_index()
    
    # Calculate percentage of A and B grades by parent education level
    top_grades = df.groupby('Parent_Education_Level')['Grade'].apply(
        lambda x: (x.isin(['A', 'B']).sum() / len(x)) * 100
    ).reset_index(name='Top_Grade_Percentage')
    
    # Merge the datasets
    edu_data = pd.merge(edu_avg, top_grades, on='Parent_Education_Level')
    
    # Sort by average score for better visualization
    edu_data = edu_data.sort_values(by='Total_Score', ascending=False)
    
    # Create combined chart with darker colors for better visibility
    fig10 = go.Figure()
    
    # Add bar chart for average scores
    fig10.add_trace(go.Bar(
        x=edu_data['Parent_Education_Level'],
        y=edu_data['Total_Score'],
        name='Avg Total Score',
        marker_color='#0088ff',  # Blue for bars
        text=edu_data['Total_Score'].round(1),
        textposition='auto',
        textfont=dict(color='white')
    ))
    
    # Add line chart for percentage of top grades
    fig10.add_trace(go.Scatter(
        x=edu_data['Parent_Education_Level'],
        y=edu_data['Top_Grade_Percentage'],
        name='A/B Grade %',
        mode='lines+markers',
        line=dict(color='#ff5500', width=3),  # Orange for line
        marker=dict(size=12, color='#ff5500'),
        yaxis='y2'
    ))
    
    # Set up layout with dual y-axes with different colors for titles
    fig10.update_layout(
        xaxis=dict(
            title='Parent Education Level',
            tickangle=-30
        ),
        yaxis=dict(
            title='Average Total Score',
            titlefont=dict(color='#ffaa66'),  # Lighter orange for title, different from the graph
            tickfont=dict(color='#ffaa66'),
        ),
        yaxis2=dict(
            title='Students with A/B Grades (%)',
            titlefont=dict(color='#ffaa66'),  # Lighter orange for title, different from the graph
            tickfont=dict(color='#ffaa66'),
            anchor='x',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color='white')
        ),
        height=700,  # Increased height
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig10, use_container_width=True)
    
    # Add explanatory note
    st.info("""
    **About this chart:** This combined chart shows the relationship between parent education level and student performance.
    
    **How to interpret:** 
    - Blue bars (left axis): Average total score for students with each parent education level
    - Orange line (right axis): Percentage of students achieving A or B grades for each parent education level
    
    This visualization helps assess whether parent education background influences student academic achievement.
    """)

# Footer
st.markdown("---")
st.caption("Student Performance Analysis Dashboard | Created with Streamlit")
