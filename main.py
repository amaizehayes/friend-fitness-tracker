import streamlit as st
from datetime import datetime
import random
from data.exercises import EXERCISE_DATABASE, MOTIVATIONAL_MESSAGES
from data.workouts import WORKOUT_PLANS
from utils.tracking import load_progress_data, save_workout, get_streak, get_completion_stats
from components.progress import display_streak_counter, display_progress_charts

st.set_page_config(
    page_title="Workout Tracker",
    page_icon="💪",
    layout="wide"
)

# Initialize session state
if 'completed_exercises' not in st.session_state:
    st.session_state.completed_exercises = set()

def main():
    st.title("💪 Daily Workout Tracker")

    # Sidebar
    st.sidebar.header("Workout Settings")
    difficulty = st.sidebar.selectbox("Choose your level:", ["beginner", "intermediate"])

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Today's Workout")
        current_day = datetime.now().strftime('%A').lower()

        # Get workout for today or next available workout
        workout_days = list(WORKOUT_PLANS[difficulty].keys())
        if current_day in workout_days:
            display_workout(WORKOUT_PLANS[difficulty][current_day])
        else:
            st.info("Today is a rest day, but you can still do the next workout:")
            # Find the next available workout
            next_workout_day = workout_days[0]  # Default to first workout
            for day in workout_days:
                if day > current_day:
                    next_workout_day = day
                    break
            st.success(f"Here's your {next_workout_day.title()} workout:")
            display_workout(WORKOUT_PLANS[difficulty][next_workout_day])

    with col2:
        streak = get_streak()
        display_streak_counter(streak)

        st.markdown("---")
        st.subheader("Daily Motivation")
        st.markdown(f"*{random.choice(MOTIVATIONAL_MESSAGES)}*")

    # Progress Section
    st.markdown("---")
    st.header("Your Progress")

    progress_data = load_progress_data()
    total_workouts, completion_rate = get_completion_stats()

    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.metric("Total Workouts", total_workouts)
    with metrics_col2:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")

    display_progress_charts(progress_data)

def display_workout_section(section_name, exercises, start_index):
    completed_exercises = []

    for i, (exercise, reps) in enumerate(exercises, start=start_index):
        exercise_key = f"{exercise}_{i}"

        if exercise == 'mobility':
            st.markdown(f"**{reps}**")
            continue

        exercise_data = EXERCISE_DATABASE[exercise]

        with st.expander(f"{exercise_data['name']} - {reps} {'reps' if isinstance(reps, int) else ''}"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(exercise_data['image_url'], caption=exercise_data['name'])

                # Add video demonstration
                if 'video_url' in exercise_data:
                    st.markdown("### 🎥 Video Demonstration")
                    st.video(exercise_data['video_url'])

            with col2:
                st.markdown(f"**Difficulty:** {exercise_data['difficulty']}")
                st.markdown(f"**Target:** {exercise_data['muscle_group']}")
                st.markdown(f"**Instructions:**\n{exercise_data['description']}")

                is_completed = exercise_key in st.session_state.completed_exercises
                if st.checkbox("Mark as completed", value=is_completed, key=exercise_key):
                    st.session_state.completed_exercises.add(exercise_key)
                    completed_exercises.append(exercise)
                else:
                    if exercise_key in st.session_state.completed_exercises:
                        st.session_state.completed_exercises.remove(exercise_key)

    return completed_exercises

def display_workout(workout_plan):
    st.markdown("### 🌅 Warm-up")
    warmup_exercises = display_workout_section("Warm-up", workout_plan['warmup'], 0)

    st.markdown("### 💪 Main Workout")
    main_exercises = display_workout_section("Main Workout", workout_plan['main'], len(workout_plan['warmup']))

    st.markdown("### 🌙 Cool-down")
    cooldown_exercises = display_workout_section("Cool-down", workout_plan['cooldown'], 
                                               len(workout_plan['warmup']) + len(workout_plan['main']))

    # Check if all exercises are completed
    all_exercises = len([ex for ex, _ in workout_plan['main']])  # Only count main exercises
    completed_main = len([ex for ex in main_exercises if ex != 'mobility'])

    if completed_main == all_exercises:
        if st.button("Save Workout"):
            completed_exercises = [key.split('_')[0] for key in st.session_state.completed_exercises]
            save_workout(difficulty="beginner", exercises_completed=completed_exercises)
            st.success("Great job! Workout saved successfully! 🎉")
            st.balloons()

if __name__ == "__main__":
    main()