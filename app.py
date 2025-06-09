import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="🎓 Student Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

def format_field_name(field_name):
    """Format field names by replacing underscores with spaces and title casing"""
    return field_name.replace('_', ' ').title()

# Keep CSS styling for visual appeal
st.markdown("""
<style>
    /* All your existing styles remain here */
    /* I've kept your comprehensive styling for visual consistency */
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

    /* Your other styles remain here */
    
    /* Adding new interactive control styles */
    .interactive-control {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .filter-container {
        background: var(--bg-secondary);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid var(--accent-primary);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-secondary);
        border-radius: 4px 4px 0px 0px;
        padding: 8px 16px;
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        color: white;
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


def display_header_metrics(df):
    """Displays the header and key metrics at the top of the dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Student Academic Performance Dashboard</h1>
        <p>Interactive analysis of student performance factors and outcomes</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Total Students</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_score = df['Total_Score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Average Score</h3>
            <h2>{avg_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        top_grade_pct = (df['Grade'] == 'A').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏆 A Grade Rate</h3>
            <h2>{top_grade_pct:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_attendance = df['Attendance (%)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 Avg Attendance</h3>
            <h2>{avg_attendance:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)


def interactive_grade_distribution(df):
    """Creates an interactive grade distribution visualization with filters"""
    st.markdown("### 📊 Academic Performance Analysis")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            departments = ['All'] + sorted(df['Department'].unique().tolist())
            selected_dept = st.selectbox('Select Department:', departments, key='grade_dept_filter')
            
        with col2:
            genders = ['All'] + sorted(df['Gender'].unique().tolist())
            selected_gender = st.selectbox('Select Gender:', genders, key='grade_gender_filter')
            
        with col3:
            income_levels = ['All'] + sorted(df['Family_Income_Level'].dropna().unique().tolist())
            selected_income = st.selectbox('Select Income Level:', income_levels, key='grade_income_filter')
        
        # Additional visualization options
        view_type = st.radio("View Type:", ["Count", "Percentage"], horizontal=True, key='grade_view_type')
        show_details = st.checkbox("Show Details", value=False, key='grade_show_details')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_income != 'All':
        filtered_df = filtered_df[filtered_df['Family_Income_Level'] == selected_income]
    
    # Create visualization
    grade_counts = filtered_df['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    grade_counts = grade_counts.sort_values(by='Grade')
    
    if view_type == "Percentage":
        total = grade_counts['Count'].sum()
        grade_counts['Value'] = (grade_counts['Count'] / total) * 100
        y_title = 'Percentage of Students (%)'
        text_format = '.1f'
        suffix = '%'
    else:
        grade_counts['Value'] = grade_counts['Count']
        y_title = 'Number of Students'
        text_format = ''
        suffix = ''
    
    fig = px.bar(
        grade_counts, 
        x='Grade', 
        y='Value',
        color='Grade', 
        text=grade_counts['Value'].round(1).astype(str) + suffix,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title=f"Grade Distribution {f'for {selected_dept}' if selected_dept != 'All' else ''}"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=18,
        height=500,
        yaxis_title=y_title,
        xaxis_title='Grade',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if show_details:
        st.markdown("#### Grade Distribution Details")
        
        # Create a summary table
        # Always calculate total even if it's already calculated in "Percentage" view
        total = grade_counts['Count'].sum()
        
        summary_df = pd.DataFrame({
            'Grade': grade_counts['Grade'],
            'Count': grade_counts['Count'],
            'Percentage': ((grade_counts['Count'] / total) * 100).round(1).astype(str) + '%'
        })
        
        # Add average scores for each grade - with error handling
        avg_scores = []
        for grade in summary_df['Grade']:
            grade_filtered = filtered_df[filtered_df['Grade'] == grade]
            if len(grade_filtered) > 0:
                avg = grade_filtered['Total_Score'].mean()
                avg_scores.append(f"{avg:.1f}")
            else:
                avg_scores.append("N/A")  # Handle case with no students in this grade
        
        summary_df['Avg Score'] = avg_scores
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Display additional insights - but only if we have data
        if len(filtered_df) > 0:
            with st.expander("📊 Statistical Analysis"):
                col1, col2 = st.columns(2)
                with col1:
                    most_common_grade = grade_counts.loc[grade_counts['Count'].idxmax(), 'Grade']
                    st.metric("Most Common Grade", most_common_grade)
                    
                with col2:
                    # Avoid division by zero
                    if filtered_df.shape[0] > 0:
                        a_b_rate = filtered_df[filtered_df['Grade'].isin(['A', 'B'])].shape[0] / filtered_df.shape[0] * 100
                        st.metric("A&B Success Rate", f"{a_b_rate:.1f}%")
                    else:
                        st.metric("A&B Success Rate", "N/A")
        else:
            st.warning("No data available for the selected filters")


def interactive_performance_factors(df):
    """Creates an interactive visualization for analyzing performance factors"""
    st.markdown("### 🧠 Performance Factors Analysis")
    
    with st.container():
        
        # Create tabs for different factor analysis
        tab1, tab2, tab3 = st.tabs(["📚 Study Habits", "😴 Sleep Analysis", "😰 Stress Impact"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                min_study, max_study = int(df['Study_Hours_per_Week'].min()), int(df['Study_Hours_per_Week'].max())
                study_range = st.slider("Study Hours per Week:", min_study, max_study, (min_study, max_study))
            
            with col2:
                attendance_threshold = st.slider("Minimum Attendance (%):", 0, 100, 0)
                
            show_trend = st.checkbox("Show Trendline", value=True)
            
            # Filter data based on selections
            study_df = df[(df['Study_Hours_per_Week'] >= study_range[0]) & 
                          (df['Study_Hours_per_Week'] <= study_range[1]) &
                          (df['Attendance (%)'] >= attendance_threshold)]
            
            # Create scatter plot of study hours vs. scores
            fig = px.scatter(
                study_df,
                x='Study_Hours_per_Week',
                y='Total_Score',
                color='Grade',
                hover_name='Student_ID',
                hover_data=['Department', 'Attendance (%)', 'Gender'],
                color_discrete_sequence=px.colors.qualitative.Bold,
                opacity=0.7,
                title=f"Study Hours vs. Performance (N={len(study_df)})"
            )
            
            if show_trend:
                fig.update_layout(
                    shapes=[{
                        'type': 'line',
                        'x0': study_df['Study_Hours_per_Week'].min(),
                        'y0': np.polyval(np.polyfit(study_df['Study_Hours_per_Week'], study_df['Total_Score'], 1), 
                                        study_df['Study_Hours_per_Week'].min()),
                        'x1': study_df['Study_Hours_per_Week'].max(),
                        'y1': np.polyval(np.polyfit(study_df['Study_Hours_per_Week'], study_df['Total_Score'], 1), 
                                        study_df['Study_Hours_per_Week'].max()),
                        'line': {
                            'color': 'rgba(255,255,255,0.5)',
                            'width': 2,
                            'dash': 'dash',
                        }
                    }]
                )
                
                # Calculate correlation
                corr = study_df['Study_Hours_per_Week'].corr(study_df['Total_Score']).round(3)
                fig.add_annotation(
                    x=study_df['Study_Hours_per_Week'].max() * 0.9,
                    y=study_df['Total_Score'].max() * 0.9,
                    text=f"Correlation: {corr}",
                    showarrow=False,
                    font=dict(color="white", size=14),
                    bgcolor="rgba(0,0,0,0.5)",
                    bordercolor="white",
                    borderwidth=1,
                    borderpad=4
                )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=500,
                xaxis_title="Weekly Study Hours",
                yaxis_title="Total Score"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                sleep_display = st.radio(
                    "Display Option:",
                    ["Sleep Hours Distribution", "Sleep vs Performance"],
                    horizontal=True
                )
            
            with col2:
                selected_grades = st.multiselect(
                    "Filter Grades:",
                    options=sorted(df['Grade'].unique().tolist()),
                    default=sorted(df['Grade'].unique().tolist())
                )
            
            # Filter data based on selections
            sleep_df = df[df['Grade'].isin(selected_grades)]
            
            if sleep_display == "Sleep Hours Distribution":
                # Create sleep distribution by grade
                sleep_bins = [0, 4, 5, 6, 7, 8, 9, 12]
                sleep_labels = ['<4h', '4-5h', '5-6h', '6-7h', '7-8h', '8-9h', '9h+']
                
                sleep_df['Sleep_Group'] = pd.cut(
                    sleep_df['Sleep_Hours_per_Night'],
                    bins=sleep_bins,
                    labels=sleep_labels,
                    include_lowest=True
                )
                
                sleep_grade = sleep_df.groupby(['Sleep_Group', 'Grade']).size().reset_index(name='Count')
                
                fig = px.bar(
                    sleep_grade,
                    x='Sleep_Group',
                    y='Count',
                    color='Grade',
                    title="Sleep Hours Distribution by Grade",
                    barmode='stack',
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
            else:  # Sleep vs Performance
                fig = px.box(
                    sleep_df,
                    x='Grade',
                    y='Sleep_Hours_per_Night',
                    color='Grade',
                    notched=True,
                    points="all",
                    title="Sleep Hours vs Academic Performance",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
                fig.update_traces(
                    jitter=0.3,
                    pointpos=-1.8,
                    marker=dict(size=8, opacity=0.6)
                )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistical summary
            with st.expander("Sleep Statistics by Grade"):
                stats_df = sleep_df.groupby('Grade')['Sleep_Hours_per_Night'].agg([
                    ('Average', 'mean'),
                    ('Median', 'median'),
                    ('Min', 'min'),
                    ('Max', 'max')
                ]).reset_index()
                
                stats_df['Average'] = stats_df['Average'].round(2)
                stats_df['Median'] = stats_df['Median'].round(2)
                stats_df['Min'] = stats_df['Min'].round(2)
                stats_df['Max'] = stats_df['Max'].round(2)
                
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                visualization_type = st.radio(
                    "Visualization Type:",
                    ["Heatmap", "Scatter Plot"],
                    horizontal=True
                )
                
            with col2:
                performance_metric = st.selectbox(
                    "Performance Metric:",
                    ["Total_Score", "Final_Score", "Midterm_Score", "Assignments_Avg"]
                )
            
            if visualization_type == "Heatmap":
                # Create stress level heatmap
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
                    title="😰 Student Stress vs Academic Performance"
                )
                
                # Add text annotations
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
            else:
                # Create scatter plot of stress vs performance
                fig = px.scatter(
                    df,
                    x='Stress_Level (1-10)',
                    y=performance_metric,
                    color='Grade',
                    title=f"Stress Level vs {performance_metric.replace('_', ' ')}",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
                fig.update_traces(marker=dict(size=12, opacity=0.7), selector=dict(mode='markers'))
                
                # Add manual trendline using numpy
                stress_clean = df['Stress_Level (1-10)'].dropna()
                performance_clean = df[performance_metric].dropna()
                
                # Filter to matching indices
                valid_indices = stress_clean.index.intersection(performance_clean.index)
                if len(valid_indices) > 1:
                    x_vals = df.loc[valid_indices, 'Stress_Level (1-10)']
                    y_vals = df.loc[valid_indices, performance_metric]
                    
                    # Calculate trendline
                    z = np.polyfit(x_vals, y_vals, 1)
                    p = np.poly1d(z)
                    
                    x_range = np.linspace(x_vals.min(), x_vals.max(), 100)
                    y_range = p(x_range)
                    
                    # Add trendline
                    fig.add_trace(go.Scatter(
                        x=x_range,
                        y=y_range,
                        mode='lines',
                        name='Trend Line',
                        line=dict(color='rgba(255,255,255,0.8)', width=2, dash='dash')
                    ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add analytical insights
            stress_corr = df['Stress_Level (1-10)'].corr(df[performance_metric])
            
            if abs(stress_corr) < 0.2:
                correlation_strength = "weak"
            elif abs(stress_corr) < 0.6:
                correlation_strength = "moderate"
            else:
                correlation_strength = "strong"
                
            st.info(f"📊 **Analysis:** There is a **{correlation_strength}** correlation ({stress_corr:.3f}) between stress level and {performance_metric.replace('_', ' ')}.")
            
        st.markdown('</div>', unsafe_allow_html=True)


def interactive_demographic_analysis(df):
    """Creates an interactive visualization for analyzing demographic factors"""
    st.markdown("### 👨‍👩‍👧‍👦 Demographic Factors Analysis")
    
    with st.container():
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Get available categorical columns dynamically
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            # Remove columns that are not useful for demographic analysis
            exclude_cols = ['Student_ID', 'Grade', 'Department']
            available_factors = [col for col in categorical_cols if col not in exclude_cols]
            
            # Add commonly expected demographic columns if they exist
            potential_factors = ["Family_Income_Level", "Internet_Access_at_Home", "Gender", "Transport_Mode"]
            final_factors = []
            
            for factor in potential_factors:
                if factor in df.columns:
                    final_factors.append(factor)
            
            # Add any other categorical columns not in the potential list
            for factor in available_factors:
                if factor not in final_factors:
                    final_factors.append(factor)
            
            if not final_factors:
                st.error("No demographic factors available for analysis.")
                return
                
            primary_factor_labels = {f: format_field_name(f) for f in final_factors}
            
            primary_factor = st.selectbox(
                "Primary Factor:",
                options=final_factors,
                format_func=lambda x: primary_factor_labels[x],
                key='primary_factor'
            )
            
        with col2:
            secondary_factor = st.selectbox(
                "Secondary Factor (Color):",
                ["Grade", "Department", "None"],
                key='secondary_factor'
            )
            
        with col3:
            plot_type = st.selectbox(
                "Plot Type:",
                ["Bar Chart", "Pie Chart", "Grouped Bar Chart"],
                key='demographic_plot_type'
            )
        
        # Additional controls
        normalize = st.checkbox("Show Percentages", value=False, key='normalize_chart')
        show_stats = st.checkbox("Show Statistical Summary", value=False, key='show_stats')
        
        # Filter and prepare data
        demo_df = df.copy()
        demo_df = demo_df.dropna(subset=[primary_factor])
        
        # Check if we have data for the selected factor
        if len(demo_df[primary_factor].unique()) == 0:
            st.error(f"No data available for {primary_factor_labels[primary_factor]}. Please select another factor.")
            return

        if secondary_factor != "None":
            demo_df = demo_df.dropna(subset=[secondary_factor])
            
        # Show data availability info
        st.info(f"📊 Analyzing {len(demo_df)} students with available {primary_factor_labels[primary_factor]} data")
        
        # Create the visualization based on selections
        if plot_type == "Bar Chart":
            if secondary_factor == "None" or normalize:
                if normalize:
                    # Create percentage stacked bar chart
                    temp_df = demo_df.groupby(primary_factor)[secondary_factor].value_counts(normalize=True).mul(100).reset_index(name='Percentage')
                    fig = px.bar(
                        temp_df,
                        x=primary_factor,
                        y='Percentage',
                        color=secondary_factor,
                        text_auto='.1f',
                        title=f"Distribution by {primary_factor.replace('_', ' ')}",
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                    fig.update_layout(yaxis_title='Percentage (%)')
                else:
                    # Create simple count bar chart
                    counts = demo_df[primary_factor].value_counts().reset_index()
                    counts.columns = [primary_factor, 'Count']
                    fig = px.bar(
                        counts,
                        x=primary_factor,
                        y='Count',
                        text='Count',
                        title=f"Distribution by {primary_factor.replace('_', ' ')}",
                        color=primary_factor,
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    fig.update_layout(showlegend=False)
            else:
                # Create grouped bar chart
                grouped = demo_df.groupby([primary_factor, secondary_factor]).size().reset_index(name='Count')
                fig = px.bar(
                    grouped,
                    x=primary_factor,
                    y='Count',
                    color=secondary_factor,
                    text='Count',
                    barmode='group',
                    title=f"{secondary_factor.replace('_', ' ')} Distribution by {primary_factor.replace('_', ' ')}",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
        elif plot_type == "Pie Chart":
            if secondary_factor != "None":
                # Create a donut chart with secondary factor as inner ring
                primary_counts = demo_df[primary_factor].value_counts()
                
                fig = go.Figure()
                
                # Add pie chart for primary factor
                fig.add_trace(go.Pie(
                    labels=primary_counts.index,
                    values=primary_counts.values,
                    name=primary_factor.replace('_', ' '),
                    hole=0.5,
                    textinfo='label+percent',
                    marker_colors=px.colors.qualitative.Bold[:len(primary_counts)]
                ))
                
                # Add annotation in the center
                fig.update_layout(
                    annotations=[dict(
                        text=primary_factor.replace('_', ' '),
                        x=0.5, y=0.5,
                        font_size=15,
                        showarrow=False
                    )]
                )
            else:
                # Simple pie chart
                primary_counts = demo_df[primary_factor].value_counts().reset_index()
                primary_counts.columns = [primary_factor, 'Count']
                
                fig = px.pie(
                    primary_counts,
                    values='Count',
                    names=primary_factor,
                    title=f"Distribution by {primary_factor.replace('_', ' ')}",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
        elif plot_type == "Grouped Bar Chart":
            if secondary_factor == "None":
                st.warning("Please select a secondary factor for grouped bar chart")
                return
                
            # Create grouped bar chart
            grouped = demo_df.groupby([primary_factor, secondary_factor]).size().reset_index(name='Count')
            
            if normalize:
                # Calculate percentages within each primary factor group
                total = grouped.groupby(primary_factor)['Count'].transform('sum')
                grouped['Percentage'] = (grouped['Count'] / total) * 100
                
                fig = px.bar(
                    grouped,
                    x=primary_factor,
                    y='Percentage',
                    color=secondary_factor,
                    text=grouped['Percentage'].round(1).astype(str) + '%',
                    title=f"{secondary_factor.replace('_', ' ')} Distribution by {primary_factor.replace('_', ' ')}",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_layout(yaxis_title='Percentage (%)')
            else:
                fig = px.bar(
                    grouped,
                    x=primary_factor,
                    y='Count',
                    color=secondary_factor,
                    text='Count',
                    title=f"{secondary_factor.replace('_', ' ')} Distribution by {primary_factor.replace('_', ' ')}",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical summary if requested
        if show_stats and secondary_factor != "None":
            st.markdown("#### Statistical Summary")
            
            # Create a contingency table
            cont_table = pd.crosstab(demo_df[primary_factor], demo_df[secondary_factor])
            st.dataframe(cont_table, use_container_width=True)
            
            # Check if table is suitable for chi-square test (no empty cells, sufficient observations)
            if cont_table.shape[0] > 1 and cont_table.shape[1] > 1 and (cont_table < 5).sum().sum() == 0:
                try:
                    # Run chi-square test to see if there's a significant relationship
                    from scipy.stats import chi2_contingency
                    chi2, p, dof, expected = chi2_contingency(cont_table)
                    
                    if p < 0.05:
                        st.success(f"📊 There is a statistically significant relationship between {primary_factor.replace('_', ' ')} and {secondary_factor.replace('_', ' ')} (p={p:.4f})")
                    else:
                        st.info(f"📊 No statistically significant relationship found between {primary_factor.replace('_', ' ')} and {secondary_factor.replace('_', ' ')} (p={p:.4f})")
                except Exception as e:
                    st.warning(f"Cannot perform statistical test: {e}")
            else:
                st.warning("⚠️ Not enough data for a valid statistical test. Some categories have fewer than 5 observations.")

# Add a new function after interactive_demographic_analysis

def correlation_analysis(df):
    """Creates an interactive correlation heatmap of performance metrics"""
    st.markdown("### 🔄 Performance Correlation Analysis")
    
    with st.container():
        
        # Select which variables to include
        col1, col2 = st.columns(2)
        
        with col1:
            correlation_vars = st.multiselect(
                "Select Variables:",
                options=['Total_Score', 'Midterm_Score', 'Final_Score', 'Assignments_Avg', 
                         'Quizzes_Avg', 'Participation_Score', 'Projects_Score', 
                         'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night', 
                         'Attendance (%)'],
                default=['Total_Score', 'Midterm_Score', 'Final_Score', 'Study_Hours_per_Week'],
                format_func=lambda x: format_field_name(x)
            )
        
        with col2:
            correlation_method = st.selectbox(
                "Correlation Method:",
                options=["pearson", "spearman"],
                format_func=lambda x: "Pearson (linear)" if x == "pearson" else "Spearman (rank-based)"
            )
            
            show_values = st.checkbox("Show Correlation Values", value=True)
        
        if len(correlation_vars) < 2:
            st.warning("Please select at least 2 variables to calculate correlations")
            st.markdown('</div>', unsafe_allow_html=True)
            return
            
        # Calculate correlation matrix
        corr_df = df[correlation_vars].corr(method=correlation_method)
        
        # Set up mask to hide upper triangle (redundant data)
        mask = np.triu(np.ones_like(corr_df, dtype=bool))
        
        # Create heatmap
        fig = px.imshow(
            corr_df,
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            text_auto='.2f' if show_values else None,
            labels=dict(color="Correlation"),
            title=f"Correlation Matrix ({correlation_method.capitalize()})"
        )
        
        # Update layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=600,
            xaxis_title="",
            yaxis_title=""
        )
        
        # Display heatmap
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation guide
        with st.expander("📊 How to Interpret Correlations"):
            st.markdown("""
            - **Strong Positive Correlation (0.7 to 1.0)**: As one variable increases, the other increases significantly
            - **Moderate Positive Correlation (0.3 to 0.7)**: As one variable increases, the other tends to increase
            - **Weak Positive Correlation (0.0 to 0.3)**: As one variable increases, the other increases slightly
            - **No Correlation (0)**: No relationship between variables
            - **Negative Correlation (-1.0 to 0)**: As one variable increases, the other decreases
            
            The **Pearson** method measures linear relationships, while **Spearman** captures monotonic relationships (even if not linear).
            """)
            
        st.markdown('</div>', unsafe_allow_html=True)

# Add another function for student progress analysis

def student_progress_analysis(df):
    """Creates an interactive visualization of student progress from midterm to final"""
    st.markdown("### 📈 Student Progress Analysis")
    
    with st.container():
        
        # Filter controls
        col1, col2 = st.columns(2)
        
        with col1:
            departments = ['All'] + sorted(df['Department'].unique().tolist())
            progress_dept = st.selectbox('Department:', departments, key='progress_dept')
            
        with col2:
            view_type = st.radio(
                "View Type:",
                ["Improvement Distribution", "Midterm vs Final Comparison"],
                horizontal=True,
                key='progress_view_type'
            )
        
        # Filter data based on selection
        if progress_dept != 'All':
            progress_df = df[df['Department'] == progress_dept].copy()
        else:
            progress_df = df.copy()
            
        # Calculate improvement metrics
        progress_df['Improvement'] = progress_df['Final_Score'] - progress_df['Midterm_Score']
        progress_df['Improvement_Percentage'] = (progress_df['Improvement'] / progress_df['Midterm_Score'] * 100).round(1)
        
        # Create visualization based on selected view type
        if view_type == "Improvement Distribution":
            # Create improvement distribution chart
            fig = px.histogram(
                progress_df,
                x='Improvement',
                color='Grade',
                marginal="box",
                histnorm='percent',
                title=f"Score Improvement Distribution {f'for {progress_dept}' if progress_dept != 'All' else ''}",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={"Improvement": "Final Score - Midterm Score", "count": "Percentage of Students"}
            )
            
            # Add a vertical line at zero improvement
            fig.add_vline(x=0, line_dash="dash", line_color="red")
            
        else:  # Midterm vs Final Comparison
            # Create scatter plot comparing midterm to final scores
            fig = px.scatter(
                progress_df,
                x='Midterm_Score',
                y='Final_Score',
                color='Grade',
                hover_name='Student_ID',
                hover_data=['Department', 'Improvement'],
                color_discrete_sequence=px.colors.qualitative.Bold,
                opacity=0.7,
                title=f"Midterm vs Final Performance {f'for {progress_dept}' if progress_dept != 'All' else ''}",
                labels={"Midterm_Score": "Midterm Score", "Final_Score": "Final Score"}
            )
            
            # Add diagonal line (y=x) representing no change
            max_score = max(progress_df['Midterm_Score'].max(), progress_df['Final_Score'].max())
            fig.add_trace(
                go.Scatter(
                    x=[0, max_score],
                    y=[0, max_score],
                    mode='lines',
                    line=dict(color='gray', dash='dash'),
                    name='No Change'
                )
            )
        
        # Update layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=500
        )
        
        # Display visualization
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_improvement = progress_df['Improvement'].mean()
            improvement_color = "green" if avg_improvement > 0 else "red"
            st.metric(
                "Average Improvement",
                f"{avg_improvement:.2f} points",
                delta=f"{avg_improvement:.1f}"
            )
            
        with col2:
            improved_pct = (progress_df['Improvement'] > 0).mean() * 100
            st.metric(
                "Students Improved",
                f"{improved_pct:.1f}%",
                delta=None
            )
            
        with col3:
            most_improved = progress_df.loc[progress_df['Improvement'].idxmax()]
            st.metric(
                "Max Improvement",
                f"{most_improved['Improvement']:.2f} points",
                delta=None
            )
            
        st.markdown('</div>', unsafe_allow_html=True)

# Update the main function to include new visualizations

def main():
    # Load the data
    df = load_data()
    
    # Display header and metrics
    display_header_metrics(df)
    
    # Sidebar for global filters and navigation
    st.sidebar.title("Dashboard Controls")
    
    # Data Overview
    with st.sidebar.expander("📋 Data Overview", expanded=False):
        st.dataframe(df.describe(), use_container_width=True)
        
        if st.button("View Raw Dataset"):
            st.dataframe(df, use_container_width=True)
    
    # Navigation through key sections
    analysis_type = st.sidebar.radio(
        "Select Analysis Section:",
        ["Academic Performance", "Performance Factors", "Demographic Analysis", 
         "Correlation Analysis", "Progress Analysis"]
    )
    
    # Display selected analysis
    if analysis_type == "Academic Performance":
        interactive_grade_distribution(df)
        
    elif analysis_type == "Performance Factors":
        interactive_performance_factors(df)
        
    elif analysis_type == "Demographic Analysis":
        interactive_demographic_analysis(df)
    
    elif analysis_type == "Correlation Analysis":
        correlation_analysis(df)
        
    elif analysis_type == "Progress Analysis":
        student_progress_analysis(df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;'>
        <h4>🎓 Student Performance Analytics Dashboard</h4>
        <p>Interactive Educational Data Analysis • Built with Streamlit and Plotly</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
