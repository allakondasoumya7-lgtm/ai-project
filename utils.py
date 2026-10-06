from datetime import date


def days_until_exam(exam_date):

    return max(
        0,
        (exam_date - date.today()).days
    )


def difficulty_label(difficulty):

    if difficulty >= 8:
        return "🔴 Hard"

    if difficulty >= 6:
        return "🟡 Medium"

    return "🟢 Easy"


def score_status(
    current_score,
    target_score
):

    if current_score >= target_score:
        return "🎯 Target Achieved"

    difference = (
        target_score -
        current_score
    )

    return (
        f"{difference:.1f}% more needed"
    )
