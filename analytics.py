from database import StudySession


def calculate_overall_progress(sessions):

    if not sessions:
        return 0

    total = len(sessions)

    completed = sum(
        1 for session in sessions
        if session.completed
    )

    return (completed / total) * 100


def calculate_total_hours(sessions):

    return sum(
        session.duration
        for session in sessions
    )


def calculate_completed_hours(sessions):

    return sum(
        session.duration
        for session in sessions
        if session.completed
    )


def calculate_pending_hours(sessions):

    total = calculate_total_hours(sessions)

    completed = calculate_completed_hours(sessions)

    return total - completed
