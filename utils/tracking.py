import pandas as pd
from datetime import datetime, timedelta
import os

def load_progress_data():
    if not os.path.exists('data/progress.csv'):
        df = pd.DataFrame(columns=['date', 'workout_completed', 'difficulty', 'exercises'])
        df.to_csv('data/progress.csv', index=False)
    return pd.read_csv('data/progress.csv')

def save_workout(difficulty, exercises_completed):
    df = load_progress_data()
    new_entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'workout_completed': True,
        'difficulty': difficulty,
        'exercises': ','.join(exercises_completed)
    }
    df = df.append(new_entry, ignore_index=True)
    df.to_csv('data/progress.csv', index=False)

def get_streak():
    df = load_progress_data()
    if len(df) == 0:
        return 0
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    current_streak = 0
    today = datetime.now().date()
    
    for i in range(len(df)-1, -1, -1):
        if df.iloc[i]['date'].date() == today - timedelta(days=current_streak):
            current_streak += 1
        else:
            break
            
    return current_streak

def get_completion_stats():
    df = load_progress_data()
    if len(df) == 0:
        return 0, 0
    
    total_workouts = len(df)
    completed_workouts = df['workout_completed'].sum()
    completion_rate = (completed_workouts / total_workouts) * 100
    
    return total_workouts, completion_rate
