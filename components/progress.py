import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def display_streak_counter(streak):
    st.markdown(
        f"""
        <div style='text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h2>Current Streak</h2>
            <h1 style='color: #FF4B4B;'>{streak} days</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_progress_charts(progress_data):
    if len(progress_data) == 0:
        st.info("Start working out to see your progress!")
        return

    # Weekly completion rate
    df = pd.DataFrame(progress_data)
    df['date'] = pd.to_datetime(df['date'])
    weekly_completion = df.resample('W', on='date')['workout_completed'].mean() * 100

    fig_weekly = px.line(
        weekly_completion,
        title='Weekly Workout Completion Rate',
        labels={'value': 'Completion Rate (%)', 'date': 'Week'}
    )
    fig_weekly.update_traces(line_color='#FF4B4B')
    st.plotly_chart(fig_weekly)

    # Exercise distribution
    exercise_counts = df['exercises'].str.split(',').explode().value_counts()
    fig_exercises = px.pie(
        values=exercise_counts.values,
        names=exercise_counts.index,
        title='Exercise Distribution'
    )
    st.plotly_chart(fig_exercises)
