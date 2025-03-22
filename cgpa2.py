import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f0f2f6;
        }
        div.block-container {
            max-width: 900px;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            background: white;
        }
        .stButton>button {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .semester-box {
            padding: 15px;
            margin: 5px;
            background: #e3f2fd;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def calculate_required_gpa(current_cgpa, target_cgpa, total_past_credits, future_credits_list):
    """Calculate required GPA per remaining semester and final CGPA."""
    total_credits = total_past_credits + sum(future_credits_list)
    total_grade_points_needed = target_cgpa * total_credits
    current_grade_points = current_cgpa * total_past_credits
    remaining_grade_points = total_grade_points_needed - current_grade_points

    total_future_credits = sum(future_credits_list)

    if total_future_credits <= 0:
        return None, None

    required_gpa = remaining_grade_points / total_future_credits

    # Ensure required GPA does not exceed the maximum
    final_cgpa = min(target_cgpa, max(current_cgpa, target_cgpa))

    return required_gpa, final_cgpa


def cgpa_to_percentage(cgpa, scale):
    """Convert CGPA to percentage based on scale."""
    if scale == 4:
        return round((cgpa / 4) * 100, 2)
    elif scale == 10:
        return round((cgpa / 10) * 100, 2)
    return None


def display_semester_credits_horizontal(semester_credits, label):
    """Display semester credits horizontally using Streamlit columns."""
    st.markdown(f"### 📚 {label} Semester Credits")

    # Display credits horizontally
    cols = st.columns(len(semester_credits))

    for col, credits in zip(cols, semester_credits):
        with col:
            st.markdown(
                f"""
                <div class="semester-box">
                    {credits} credits
                </div>
                """,
                unsafe_allow_html=True
            )


def main():
    st.title("🎓 Targets GPA Analyzer")

    # Fixed credits per semester
    semester_credits = [19, 21, 20, 19, 21, 23, 22, 10]  # Sem 1 to Sem 8

    # Sidebar for inputs
    st.sidebar.header("📊 Input Details")

    # GPA scale dropdown
    scale = st.sidebar.selectbox("Select GPA Scale", [4, 10], index=0)

    # Number of semesters completed
    num_past_semesters = st.sidebar.slider("Number of semesters completed", 1, 8, 1)
    total_past_credits = sum(semester_credits[:num_past_semesters])

    # Current CGPA
    current_cgpa = st.sidebar.number_input(
        f"Current CGPA (0-{scale}) after {num_past_semesters} semesters",
        min_value=0.0, max_value=float(scale), value=2.0, step=0.1
    )

    # Target CGPA
    target_cgpa = st.sidebar.number_input(
        f"Target CGPA (0-{scale})",
        min_value=0.0, max_value=float(scale), value=3.0, step=0.1
    )

    # Number of future semesters
    remaining_semesters = 8 - num_past_semesters

    if remaining_semesters > 0:
        num_future_semesters = st.sidebar.slider(
            f"Number of future semesters to calculate for (1-{remaining_semesters})",
            1, remaining_semesters, 1
        )
    else:
        st.warning("No future semesters remaining!")
        return

    # Future semester credits
    future_credits_list = semester_credits[num_past_semesters:num_past_semesters + num_future_semesters]

    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])

    if col2.button("📈 Calculate Target GPA"):
        required_gpa, final_cgpa = calculate_required_gpa(
            current_cgpa, target_cgpa, total_past_credits, future_credits_list
        )

        if required_gpa is None:
            st.error("No future credits provided. Unable to calculate GPA.")
            return

        # Convert CGPA to percentage
        current_percentage = cgpa_to_percentage(current_cgpa, scale)
        target_percentage = cgpa_to_percentage(target_cgpa, scale)
        final_percentage = cgpa_to_percentage(final_cgpa, scale)

        # Display results
        st.subheader("📌 Results")
        st.write(f"**Current CGPA:** {current_cgpa:.2f} ({current_percentage:.2f}%) "
                 f"(after {num_past_semesters} semesters, {total_past_credits} credits)")
        st.write(f"**Target CGPA:** {target_cgpa:.2f} ({target_percentage:.2f}%)")

        if required_gpa > scale:
            st.error(f"🚫 It's impossible to reach your target CGPA with the selected future semesters.")
            st.write(f"You would need a GPA of **{required_gpa:.2f}** per semester, which exceeds the {scale}.0 scale limit.")
        else:
            st.success(f"✅ To reach your target CGPA, you need to achieve a GPA of **{required_gpa:.2f}** "
                       f"per semester across the next {num_future_semesters} semesters "
                       f"({sum(future_credits_list)} credits total).")
            st.write(f"If you achieve this, your final CGPA will be approximately: "
                     f"**{final_cgpa:.2f}** ({final_percentage:.2f}%)")

        # Display semester credits horizontally
        st.markdown("### 🗓️ Semester Credits Breakdown")
        
        # Display past semesters horizontally
        display_semester_credits_horizontal(semester_credits[:num_past_semesters], "Past")
        
        # Display future semesters horizontally
        display_semester_credits_horizontal(future_credits_list, "Future")


if __name__ == "__main__":
    main()
