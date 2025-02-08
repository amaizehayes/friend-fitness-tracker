import streamlit as st
from data.workouts import WORKOUT_PLANS
from data.exercises import EXERCISE_DATABASE

def format_exercise(exercise, reps):
    """Helper function to format exercise display"""
    if exercise == 'mobility':
        return f"- {reps}"
    exercise_data = EXERCISE_DATABASE[exercise]
    return f"- {exercise_data['name']}: {reps} {'reps' if isinstance(reps, int) else ''}"

def main():
    st.title("🏋️‍♂️ Complete Workout Program Overview")
    
    st.markdown("""
    This program is designed to build a consistent workout habit using:
    - 🚣‍♂️ Rowing machine
    - 💪 Adjustable dumbbells
    - 🎯 Resistance bands
    
    ### 📅 Weekly Structure
    | Day | Focus | Description |
    |-----|-------|-------------|
    | Monday | Workout A | Full-Body Strength + Rowing |
    | Wednesday | Workout C | Rowing Endurance & Core |
    | Friday | Workout B | Strength & Mobility |
    | Saturday | Workout D | Rowing Intervals & Full-Body Strength |
    """)

    difficulty = st.selectbox("Select difficulty level:", ["beginner", "intermediate"])
    
    workouts = WORKOUT_PLANS[difficulty]
    
    for day, workout in workouts.items():
        st.markdown(f"## {day.title()}'s Workout")
        
        # Warm-up section
        st.markdown("### 🌅 Warm-up")
        for exercise, reps in workout['warmup']:
            st.markdown(format_exercise(exercise, reps))
            
        # Main workout section
        st.markdown("### 💪 Main Workout")
        for exercise, reps in workout['main']:
            st.markdown(format_exercise(exercise, reps))
            
        # Cool-down section
        st.markdown("### 🌙 Cool-down")
        for exercise, reps in workout['cooldown']:
            st.markdown(format_exercise(exercise, reps))
            
        st.markdown("---")
    
    st.markdown("""
    ### 🔄 How to Progress
    
    1. **Weeks 1-2:**
       - 2 rounds per circuit
       - Light weight
       - Focus on form
    
    2. **Weeks 3-4:**
       - 3 rounds per circuit
       - Gradually increase intensity
    
    3. **Weeks 5+:**
       - Increase weight
       - Add reps
       - Extend rowing duration
    
    Remember to:
    - 🎯 Focus on proper form
    - 💧 Stay hydrated
    - 🛏️ Get adequate rest between workouts
    - 📝 Track your progress
    """)

if __name__ == "__main__":
    main()
