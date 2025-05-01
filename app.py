import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from utils import (
    load_data, save_pushups, get_statistics, 
    get_random_motivation, check_achievements
)
from workout_plans import (
    BASE_WORKOUT_PLANS, DIFFICULTY_LEVELS,
    get_adjusted_workout_plan, PUSHUP_VARIATIONS
)

# Page configuration
st.set_page_config(
    page_title="Pushup Tracker",
    page_icon="💪",
    layout="wide"
)

# Initialize session state
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'selected_difficulty' not in st.session_state:
    st.session_state.selected_difficulty = "Normal"

# Main title
st.title("💪 Pushup Tracker")

# Sidebar with workout plans and pushup variations
st.sidebar.title("Workout Plans")

# Display pushup variations and their descriptions
st.sidebar.subheader("Pushup Variations")
for variation, details in PUSHUP_VARIATIONS.items():
    with st.sidebar.expander(f"{variation} Pushups"):
        st.write(details["description"])
        st.write(f"Difficulty: {'🟢 Beginner Friendly' if details['beginner_friendly'] else '🔴 Advanced'}")

# Difficulty selection
selected_difficulty = st.sidebar.selectbox(
    "Choose difficulty level:",
    options=list(DIFFICULTY_LEVELS.keys()),
    key="difficulty_selector",
    index=list(DIFFICULTY_LEVELS.keys()).index(st.session_state.selected_difficulty)
)
st.session_state.selected_difficulty = selected_difficulty

# Plan selection
selected_plan = st.sidebar.selectbox(
    "Choose a workout plan:",
    options=list(BASE_WORKOUT_PLANS.keys())
)

if selected_plan:
    st.sidebar.subheader(f"30-Day {selected_plan} Plan ({selected_difficulty})")
    plan_data = get_adjusted_workout_plan(selected_plan, selected_difficulty)
    for day in plan_data:
        pushup_type = day["type"]
        target = day["target"]
        if target == "Rest":
            st.sidebar.text(f"Day {day['day']}: Rest day")
        else:
            st.sidebar.text(f"Day {day['day']}: {target} {pushup_type} pushups")

    # Show difficulty multiplier info
    st.sidebar.info(f"Difficulty Multiplier: {DIFFICULTY_LEVELS[selected_difficulty]}x")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Input section
    st.subheader("Log Your Pushups")

    # Date selection (default to today)
    selected_date = st.date_input(
        "Date",
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )

    # Pushup type selection
    selected_type = st.selectbox(
        "Pushup Type",
        options=list(PUSHUP_VARIATIONS.keys()),
        help="Select the type of pushups you performed"
    )

    # Show description of selected pushup type
    st.info(PUSHUP_VARIATIONS[selected_type]["description"])

    # Pushup count input
    pushup_count = st.number_input(
        "Number of Pushups",
        min_value=0,
        max_value=1000,
        value=0
    )

    # Submit button
    if st.button("Save"):
        save_pushups(str(selected_date), pushup_count, selected_type) #Added selected_type
        st.session_state.show_success = True
        st.rerun()

    if st.session_state.show_success:
        st.success("Pushups logged successfully!")
        st.markdown(f"### {get_random_motivation()}")
        st.session_state.show_success = False

with col2:
    # Statistics
    st.subheader("Your Statistics")
    df = load_data()
    stats = get_statistics(df)

    st.metric("Total Pushups", stats["total_pushups"])
    st.metric("Daily Average", stats["daily_average"])
    st.metric("Current Streak", f"{stats['current_streak']} days")

    if stats["best_day"] is not None:
        st.metric(
            "Best Day",
            f"{stats['best_day']['pushups']} pushups on {stats['best_day']['date'].strftime('%Y-%m-%d')}"
        )

# Progress visualization
st.subheader("Progress Over Time")
if not df.empty:
    fig = px.line(
        df,
        x='date',
        y='pushups',
        title='Your Pushup Progress',
        labels={'date': 'Date', 'pushups': 'Pushups'},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Start logging your pushups to see your progress!")

# Achievements section
st.subheader("🏆 Achievements")
achievements = check_achievements(stats)

if achievements:
    achievement_cols = st.columns(len(achievements))
    for i, achievement in enumerate(achievements):
        with achievement_cols[i]:
            st.markdown(f"### {achievement['name']}")
            st.markdown(f"_{achievement['description']}_")
else:
    st.info("Keep pushing to unlock achievements!")

# Weekly summary - UPDATED SECTION
def get_weekly_statistics(df):
    if df.empty:
        return {}
    df['week'] = df['date'].dt.isocalendar().week
    current_week = df['date'].dt.isocalendar().week.max()
    current_week_data = df[df['week'] == current_week]
    last_week = current_week -1
    last_week_data = df[df['week'] == last_week]
    
    current_week_total = current_week_data['pushups'].sum()
    last_week_total = last_week_data['pushups'].sum() if not last_week_data.empty else 0
    improvement = ((current_week_total - last_week_total) / last_week_total) * 100 if last_week_total >0 else 100
    daily_average = current_week_total / len(current_week_data) if not current_week_data.empty else 0

    best_day = current_week_data.loc[current_week_data['pushups'].idxmax()].to_dict() if not current_week_data.empty else None

    type_breakdown = current_week_data.groupby('type')['pushups'].agg(['sum', 'count', 'mean'])
    type_breakdown = type_breakdown.to_dict('index')

    return {
        "current_week_total": current_week_total,
        "daily_average": daily_average,
        "best_day": best_day,
        "type_breakdown": type_breakdown,
        "improvement":improvement
    }

st.subheader("📊 Weekly Progress Summary")
if not df.empty:
    # Get weekly statistics
    weekly_stats = get_weekly_statistics(df)

    # Weekly Overview
    st.write("### This Week's Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "This Week's Total",
            weekly_stats["current_week_total"],
            f"{weekly_stats['improvement']:.0f}% vs last week"
        )

    with col2:
        st.metric(
            "Daily Average",
            weekly_stats["daily_average"],
            "pushups per day"
        )

    with col3:
        if weekly_stats["best_day"]:
            st.metric(
                "Best Day",
                weekly_stats["best_day"]["pushups"],
                weekly_stats["best_day"]["date"].strftime("%A")
            )

    # Pushup Type Breakdown
    st.write("### Pushup Types This Week")
    if weekly_stats["type_breakdown"]:
        type_data = pd.DataFrame.from_dict(
            weekly_stats["type_breakdown"],
            orient='index'
        ).reset_index()
        type_data.columns = ['Type', 'Total', 'Count', 'Average']

        # Create donut chart for type breakdown
        fig_donut = px.pie(
            type_data,
            values='Total',
            names='Type',
            title='Pushup Types Distribution',
            hole=0.4
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        # Bar chart for daily progress
        current_week = df['date'].dt.isocalendar().week.max()
        daily_progress = df[df['week'] == current_week]
        fig_daily = px.bar(
            daily_progress,
            x='date',
            y='pushups',
            color='type',
            title='Daily Progress This Week',
            labels={'date': 'Date', 'pushups': 'Pushups', 'type': 'Type'}
        )
        st.plotly_chart(fig_daily, use_container_width=True)

        # Display type breakdown as a list
        st.write("#### Detailed Breakdown")
        for _, row in type_data.iterrows():
            pushup_type = row['Type']
            total = int(row['Total'])
            count = int(row['Count'])
            average = row['Average']
            
            st.markdown(f"""
            **{pushup_type} Pushups**
            - Total: {total}
            - Number of sessions: {count}
            - Average per session: {average:.1f}
            ---
            """)
else:
    st.info("Start logging your pushups to see your weekly progress!")