import streamlit as st

from datetime import date, time, timedelta

from database import (
    init_db,
    get_db,
    StudySession,
    Subject
)

from analytics import (
    calculate_overall_progress,
    calculate_total_hours,
    calculate_completed_hours,
    calculate_pending_hours
)

from ai_planner import generate_ai_plan


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Smart Study Planner",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# INITIALIZE DATABASE
# ==================================================

init_db()


# ==================================================
# TITLE
# ==================================================

st.title("📚 AI Smart Study Planner")

st.write(
    "Plan your study time, create a timetable, "
    "track study hours and complete your sessions."
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📚 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Add Subjects",
        "Create Timetable",
        "Study Sessions",
        "AI Study Plan",
        "Analytics"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    db = get_db()

    sessions = (
        db.query(StudySession)
        .order_by(
            StudySession.study_date,
            StudySession.start_time
        )
        .all()
    )

    total_hours = calculate_total_hours(
        sessions
    )

    completed_hours = calculate_completed_hours(
        sessions
    )

    pending_hours = calculate_pending_hours(
        sessions
    )

    progress = calculate_overall_progress(
        sessions
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Planned Hours",
            f"{total_hours:.1f}"
        )

    with col2:

        st.metric(
            "✅ Completed Hours",
            f"{completed_hours:.1f}"
        )

    with col3:

        st.metric(
            "⏳ Remaining Hours",
            f"{pending_hours:.1f}"
        )

    with col4:

        st.metric(
            "📈 Progress",
            f"{progress:.0f}%"
        )

    st.progress(
        int(progress)
    )

    st.subheader("Today's Study Sessions")

    today_sessions = [
        s for s in sessions
        if s.study_date == date.today()
    ]

    if not today_sessions:

        st.info(
            "No study sessions planned for today."
        )

    else:

        for session in today_sessions:

            status = (
                "✅ Completed"
                if session.completed
                else "⏳ Pending"
            )

            st.write(
                f"**{session.start_time} - "
                f"{session.end_time}** | "
                f"📚 {session.subject} | "
                f"📖 {session.topic} | "
                f"⏱️ {session.duration:.1f} hrs | "
                f"{status}"
            )

    db.close()


# ==================================================
# ADD SUBJECTS
# ==================================================

elif page == "Add Subjects":

    st.header("📚 Add Subjects")

    with st.form("subject_form"):

        name = st.text_input(
            "Subject Name"
        )

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ]
        )

        target_hours = st.number_input(
            "Target Study Hours",
            min_value=0.5,
            max_value=100.0,
            value=2.0,
            step=0.5
        )

        submitted = st.form_submit_button(
            "Add Subject"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter a subject."
                )

            else:

                db = get_db()

                subject = Subject(
                    name=name,
                    difficulty=difficulty,
                    target_hours=target_hours,
                    completed_hours=0
                )

                db.add(subject)
                db.commit()

                db.close()

                st.success(
                    f"{name} added successfully!"
                )

    st.subheader("Your Subjects")

    db = get_db()

    subjects = (
        db.query(Subject)
        .order_by(Subject.name)
        .all()
    )

    if not subjects:

        st.info(
            "No subjects added yet."
        )

    else:

        for subject in subjects:

            st.write(
                f"📚 **{subject.name}** | "
                f"Difficulty: {subject.difficulty} | "
                f"Target: {subject.target_hours} hrs"
            )

    db.close()


# ==================================================
# CREATE TIMETABLE
# ==================================================

elif page == "Create Timetable":

    st.header("🗓️ Create Study Timetable")

    db = get_db()

    subjects = (
        db.query(Subject)
        .order_by(Subject.id)
        .all()
    )

    if not subjects:

        st.warning(
            "Please add subjects first."
        )

        db.close()

    else:

        subject_names = [
            subject.name
            for subject in subjects
        ]

        st.write(
            "Select your available study time."
        )

        col1, col2 = st.columns(2)

        with col1:

            start_time = st.time_input(
                "Daily Start Time",
                value=time(18, 0)
            )

        with col2:

            daily_hours = st.number_input(
                "Study Hours Per Day",
                min_value=1.0,
                max_value=12.0,
                value=3.0,
                step=0.5
            )

        number_of_days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=7
        )

        if st.button(
            "🚀 Generate Timetable"
        ):

            minutes_per_day = int(
                daily_hours * 60
            )

            session_minutes = 60

            current_date = date.today()

            subject_index = 0

            for day in range(
                number_of_days
            ):

                current_start = (
                    start_time.hour * 60
                    + start_time.minute
                )

                minutes_used = 0

                while (
                    minutes_used
                    < minutes_per_day
                ):

                    subject_name = (
                        subject_names[
                            subject_index
                            % len(subject_names)
                        ]
                    )

                    remaining = (
                        minutes_per_day
                        - minutes_used
                    )

                    duration = min(
                        session_minutes,
                        remaining
                    )

                    start_minutes = (
                        current_start
                        + minutes_used
                    )

                    end_minutes = (
                        start_minutes
                        + duration
                    )

                    start_hour = (
                        start_minutes // 60
                    )

                    start_minute = (
                        start_minutes % 60
                    )

                    end_hour = (
                        end_minutes // 60
                    )

                    end_minute = (
                        end_minutes % 60
                    )

                    new_session = StudySession(

                        subject=subject_name,

                        topic=(
                            f"{subject_name} "
                            "Study Session"
                        ),

                        study_date=(
                            current_date
                            + timedelta(days=day)
                        ),

                        start_time=(
                            f"{start_hour:02d}:"
                            f"{start_minute:02d}"
                        ),

                        end_time=(
                            f"{end_hour:02d}:"
                            f"{end_minute:02d}"
                        ),

                        duration=duration / 60,

                        completed=False
                    )

                    db.add(
                        new_session
                    )

                    minutes_used += duration

                    subject_index += 1

            db.commit()

            st.success(
                "🎉 Timetable generated successfully!"
            )

        db.close()


# ==================================================
# STUDY SESSIONS
# ==================================================

elif page == "Study Sessions":

    st.header("⏰ Study Sessions")

    db = get_db()

    sessions = (
        db.query(StudySession)
        .order_by(
            StudySession.study_date,
            StudySession.start_time
        )
        .all()
    )

    if not sessions:

        st.info(
            "No study sessions available."
        )

    else:

        for session in sessions:

            col1, col2, col3, col4 = (
                st.columns(
                    [2, 3, 3, 2]
                )
            )

            with col1:

                st.write(
                    f"📅 {session.study_date}"
                )

            with col2:

                st.write(
                    f"📚 **{session.subject}**"
                )

                st.write(
                    session.topic
                )

            with col3:

                st.write(
                    f"⏰ {session.start_time} - "
                    f"{session.end_time}"
                )

                st.write(
                    f"⌛ {session.duration:.1f} hours"
                )

            with col4:

                if session.completed:

                    st.success(
                        "Completed ✅"
                    )

                else:

                    if st.button(
                        "Mark Completed",
                        key=f"complete_{session.id}"
                    ):

                        session.completed = True

                        db.commit()

                        st.rerun()

            st.divider()

    db.close()


# ==================================================
# AI STUDY PLAN
# ==================================================

elif page == "AI Study Plan":

    st.header("🤖 AI Study Plan")

    db = get_db()

    subjects = (
        db.query(Subject)
        .all()
    )

    db.close()

    if not subjects:

        st.warning(
            "Please add subjects first."
        )

    else:

        subject_names = [
            subject.name
            for subject in subjects
        ]

        st.write(
            "Subjects:"
        )

        st.write(
            ", ".join(subject_names)
        )

        available_hours = st.number_input(
            "Available Hours Per Day",
            min_value=1.0,
            max_value=12.0,
            value=3.0,
            step=0.5
        )

        days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=7
        )

        if st.button(
            "🤖 Generate AI Plan"
        ):

            with st.spinner(
                "Creating your study plan..."
            ):

                plan = generate_ai_plan(
                    subject_names,
                    available_hours,
                    days
                )

            st.markdown(
                plan
            )


# ==================================================
# ANALYTICS
# ==================================================

elif page == "Analytics":

    st.header("📊 Study Analytics")

    db = get_db()

    sessions = (
        db.query(StudySession)
        .order_by(
            StudySession.study_date
        )
        .all()
    )

    db.close()

    if not sessions:

        st.info(
            "No study data available."
        )

    else:

        total_hours = (
            calculate_total_hours(
                sessions
            )
        )

        completed_hours = (
            calculate_completed_hours(
                sessions
            )
        )

        pending_hours = (
            calculate_pending_hours(
                sessions
            )
        )

        progress = (
            calculate_overall_progress(
                sessions
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Planned",
                f"{total_hours:.1f} hrs"
            )

        with col2:

            st.metric(
                "Completed",
                f"{completed_hours:.1f} hrs"
            )

        with col3:

            st.metric(
                "Remaining",
                f"{pending_hours:.1f} hrs"
            )

        st.subheader(
            "Overall Progress"
        )

        st.progress(
            int(progress)
        )

        st.write(
            f"You have completed "
            f"**{progress:.1f}%** of your "
            f"planned study sessions."
        )

        st.subheader(
            "Session Details"
        )

        for session in sessions:

            status = (
                "Completed"
                if session.completed
                else "Pending"
            )

            st.write(
                f"📚 {session.subject} | "
                f"{session.study_date} | "
                f"{session.duration:.1f} hrs | "
                f"{status}"
            )
