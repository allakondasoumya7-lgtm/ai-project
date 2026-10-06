import os

try:
    from google import genai
except ImportError:
    genai = None


def generate_ai_plan(
    subjects,
    available_hours,
    days
):

    # --------------------------------------
    # Try Gemini AI
    # --------------------------------------

    api_key = os.getenv("GOOGLE_API_KEY")

    if genai and api_key:

        try:

            client = genai.Client(
                api_key=api_key
            )

            subject_text = ", ".join(
                subjects
            )

            prompt = f"""
You are an AI study planner.

Create a practical study plan.

Subjects:
{subject_text}

Available study hours per day:
{available_hours}

Number of days:
{days}

Give:
1. Subject
2. Topic
3. Recommended hours
4. Study strategy

Keep the answer simple and practical.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            return (
                "AI plan could not be generated. "
                "Using the normal timetable planner instead."
            )

    # --------------------------------------
    # Fallback plan
    # --------------------------------------

    plan = []

    if not subjects:
        return "Please add subjects first."

    hours_each = available_hours / len(subjects)

    for subject in subjects:

        plan.append(
            f"""
### {subject}

Study time: {hours_each:.1f} hours/day

Recommended method:
- Read concepts
- Make short notes
- Practice questions
- Revise
"""
        )

    return "\n".join(plan)
