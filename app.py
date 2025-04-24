import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data (make sure the CSVs are in the same directory or use a path)
students_df = pd.read_csv('data/students.csv')
activity_df = pd.read_csv('data/course_activity.csv')
feedback_df = pd.read_csv('data/feedback.csv')

# Merging all data
merged_df = pd.merge(activity_df, students_df, on='Student_ID', how='left')
merged_df = pd.merge(merged_df, feedback_df, on=['Student_ID', 'Course_ID'], how='left')

# Streamlit Sidebar for Navigation
st.sidebar.title("Online Learning Platform Analysis")
option = st.sidebar.selectbox(
    "Choose the section to explore",
    ["EDA", "Visualizations", "Insights", "Trends","Recommendations"]
)

# EDA Section
if option == "EDA":
    st.title("Exploratory Data Analysis (EDA)")

    # Show merged data
    st.subheader("Merged Data Preview")
    st.write(merged_df.head())

    # 1. Overall Average Completion Rate
    st.subheader("1. Overall Average Completion Rate")
    overall_completion_rate = merged_df['Completion_Percentage'].mean()
    st.write(f"Overall Average Completion Rate: {overall_completion_rate:.2f}%")

    # 2. Course with Highest and Lowest Engagement Time
    st.subheader("2. Course with Highest and Lowest Engagement Time")
    engagement_by_course = merged_df.groupby('Course_ID')['Time_Spent_Minutes'].mean().sort_values(ascending=False)
    highest_engagement_course = engagement_by_course.head(1)
    lowest_engagement_course = engagement_by_course.tail(1)
    
    # Display the results in tabular format
    st.write("### Course with Highest Engagement Time:")
    st.write(highest_engagement_course)
    st.write("### Course with Lowest Engagement Time:")
    st.write(lowest_engagement_course)

    # Visualization: Bar plot for engagement by course
    st.subheader("Engagement by Course (Bar Plot)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=engagement_by_course.index, y=engagement_by_course.values, palette="viridis", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title("Average Engagement Time by Course")
    st.pyplot(fig)

    # 3. Engagement by Age Group
    st.subheader("3. Engagement by Age Group")

    # Create 'Age_Group' using pd.cut(), including the 'Unknown' category
    age_bins = [0, 18, 25, 35, 50, 100]
    age_labels = ['<18', '18-25', '26-35', '36-50', '50+']
    merged_df['Age_Group'] = pd.cut(merged_df['Age'], bins=age_bins, labels=age_labels)

    # Explicitly add 'Unknown' category to the 'Age_Group' column
    merged_df['Age_Group'] = merged_df['Age_Group'].cat.add_categories(['Unknown'])

    # Assign 'Unknown' for rows where 'Age' is NaN
    merged_df.loc[merged_df['Age'].isna(), 'Age_Group'] = 'Unknown'

    # Now calculate the average engagement time per age group
    engagement_by_age = merged_df.groupby('Age_Group')['Time_Spent_Minutes'].mean()

    
    # Visualization: Bar plot for engagement by age group
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=engagement_by_age.index, y=engagement_by_age.values, palette="Blues_d", ax=ax)
    ax.set_title("Average Engagement Time by Age Group")
    st.pyplot(fig)

    # 4. Engagement by Location
    st.subheader("4. Engagement by Location")
    engagement_by_location = merged_df.groupby('Location')['Time_Spent_Minutes'].mean().sort_values(ascending=False)
    st.write("Top 5 Locations by Engagement:")
    st.write(engagement_by_location.head())

    # Visualization: Pie chart for engagement by location
    st.subheader("Engagement by Location (Pie Chart)")
    top_locations = engagement_by_location.head(5)  # Top 5 locations
    fig, ax = plt.subplots(figsize=(6, 6))
    top_locations.plot.pie(autopct='%1.1f%%', startangle=90, cmap="Set3", ax=ax)
    ax.set_title("Engagement by Location")
    st.pyplot(fig)

    # 5. Average Feedback Rating per Course
    st.subheader("5. Average Feedback Rating per Course")
    average_feedback_per_course = merged_df.groupby('Course_ID')['Rating'].mean().sort_values(ascending=False)
    st.write("Average Feedback Rating per Course:")
    st.write(average_feedback_per_course)

    # 6. Correlation between Completion Rate and Feedback Rating
    st.subheader("6. Correlation between Completion Rate and Feedback Rating")
    correlation = merged_df[['Completion_Percentage', 'Rating']].corr()
    st.write("Correlation between Completion Rate and Feedback Rating:")
    st.write(correlation)

    # Visualization: Heatmap for correlation matrix
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

    # 7. Top 3 Students based on Engagement and Satisfaction
    st.subheader("7. Top 3 Students based on Engagement and Satisfaction")
    student_engagement = merged_df.groupby('Student_ID')['Time_Spent_Minutes'].mean()
    student_feedback = merged_df.groupby('Student_ID')['Rating'].mean()
    student_segment = pd.DataFrame({
        'Engagement': student_engagement,
        'Satisfaction': student_feedback
    })
    student_segment['ESI'] = student_segment['Engagement'] + student_segment['Satisfaction']
    top_3_students = student_segment.sort_values(by='ESI', ascending=False).head(3)
    st.write("Top 3 Students based on Engagement and Satisfaction:")
    st.write(top_3_students)



# Visualizations Section
elif option == "Visualizations":
    st.title("📊 Visualizations")

    # 1. Engagement by Course (Bar Chart)
    st.subheader("1. Average Engagement by Course")
    engagement_by_course = merged_df.groupby('Course_ID')['Time_Spent_Minutes'].mean().sort_values()
    fig1, ax1 = plt.subplots()
    engagement_by_course.plot(kind='bar', color='lightblue', ax=ax1)
    ax1.set_title("Average Time Spent by Course")
    ax1.set_xlabel("Course ID")
    ax1.set_ylabel("Avg. Time Spent (minutes)")
    st.pyplot(fig1)

    # 2. Engagement by Gender (Bar Chart)
    st.subheader("2. Average Engagement by Gender")
    engagement_by_gender = merged_df.groupby('Gender')['Time_Spent_Minutes'].mean()
    fig2, ax2 = plt.subplots()
    engagement_by_gender.plot(kind='bar', color='orchid', ax=ax2)
    ax2.set_title("Average Time Spent by Gender")
    ax2.set_xlabel("Gender")
    ax2.set_ylabel("Avg. Time Spent (minutes)")
    st.pyplot(fig2)

    # 3. Engagement by Age Group (Bar Chart)
    st.subheader("3. Average Engagement by Age Group")
    merged_df['Age_Group'] = pd.cut(merged_df['Age'], bins=[0, 18, 25, 35, 50, 100], labels=['<18', '18-25', '26-35', '36-50', '50+'])
    engagement_by_age = merged_df.groupby('Age_Group')['Time_Spent_Minutes'].mean()
    fig3, ax3 = plt.subplots()
    engagement_by_age.plot(kind='bar', color='lightgreen', ax=ax3)
    ax3.set_title("Avg. Time Spent by Age Group")
    ax3.set_xlabel("Age Group")
    ax3.set_ylabel("Avg. Time Spent (minutes)")
    st.pyplot(fig3)

    # 4. Feedback Ratings by Course (Box Plot)
    st.subheader("4. Feedback Ratings by Course")
    fig4, ax4 = plt.subplots()
    sns.boxplot(data=merged_df, x='Course_ID', y='Rating', palette='pastel', ax=ax4)
    ax4.set_title("Feedback Ratings by Course")
    ax4.set_xlabel("Course ID")
    ax4.set_ylabel("Feedback Score")
    st.pyplot(fig4)

    # 5. Engagement Trend Over Time (Line Plot)
    st.subheader("5. Engagement Trend Over Time")
    merged_df['Enrolment_Date'] = pd.to_datetime(merged_df['Enrolment_Date'])
    merged_df['Month'] = merged_df['Enrolment_Date'].dt.to_period('M').astype(str)
    monthly_engagement = merged_df.groupby('Month')['Time_Spent_Minutes'].mean()
    fig5, ax5 = plt.subplots()
    monthly_engagement.plot(kind='line', marker='o', linestyle='-', color='dodgerblue', ax=ax5)
    ax5.set_title("Avg. Engagement Over Time")
    ax5.set_xlabel("Month")
    ax5.set_ylabel("Avg. Time Spent (minutes)")
    plt.xticks(rotation=45)
    st.pyplot(fig5)

elif option == "Insights":
    st.title("💡 Key Insights")

    st.markdown("## 🔍 Top 5 Data-Driven Insights")

    st.markdown("""
    **1. 🏆 Highest Engagement Observed in Course `DM101`**  
    Learners spent the most average time (~102.4 minutes) on `DM101`, suggesting either higher interest or greater content depth. In contrast, `PY202` saw the lowest engagement (~93.9 minutes), indicating possible disinterest or easier content.

    **2. 👶 Younger Students Are More Engaged**  
    Students under 18 years old spent the most time on courses. Engagement steadily decreases with age, indicating that younger learners are more involved or have fewer distractions.

    **3. 👩‍🎓 Gender Differences in Engagement**  
    Female learners showed slightly higher engagement time on average than male learners, hinting at differences in study behavior or preferences.

    **4. ⭐ Feedback Ratings Show Variation Across Courses**  
    Courses like `DM101` and `AI203` receive more consistent and higher feedback ratings, indicating good content or instructor quality. Wider variation in other courses may suggest inconsistent experiences.

    **5. 📅 Engagement Peaks Around Specific Dates**  
    Time-based analysis revealed spikes in learning activity during specific months, possibly aligning with academic schedules, exams, or course launches.

    ---
    """)

    st.markdown("## 🌟 Additional Actionable Insights")

    st.markdown("""
    **6. 📝 Sparse Feedback Data Requires Attention**  
    Over 500 feedback entries are missing, pointing to low response rates. Consider prompting feedback after course completion to improve data coverage and course improvement.

    **7. 🧩 Low Completion Percentages Suggest Dropout Risk**  
    Many students show high engagement but relatively low course completion. This may indicate unclear objectives, overly difficult content, or lack of motivation near course end.

    **8. 📍 Potential for Location-Based Personalization**  
    Though not explored in detail yet, student location data can offer insight into regional engagement levels — useful for customizing content, language, or scheduling.

    **9. 📊 Imbalanced Course Engagement Distribution**  
    Some courses receive disproportionately higher engagement than others. Understanding why could help improve less engaging courses through redesign or marketing.

    **10. 🔍 Age Group `36-50` and `50+` Show Low or Missing Engagement**  
    Engagement data for older age groups is either missing or significantly low, possibly due to smaller sample size or lack of digital accessibility. Further data collection can help confirm this trend.

    ---
    """)


elif option == "Recommendations":
    st.title("📌 Recommendations")

    st.markdown("Based on the data analysis and insights gathered, here are some practical and strategic recommendations:")

    st.markdown("""
    ### ✅ 1. **Improve Feedback Collection Mechanism**
    - Introduce **in-app feedback prompts** after course completion.
    - Offer small **incentives (certificates, badges)** to encourage feedback submission.
    - Ensure feedback questions are **clear and quick** to answer.

    ### ✅ 2. **Revise Courses with Low Engagement (e.g., `PY202`)**
    - Review the course structure, content difficulty, and instructor delivery.
    - Add **interactive elements (quizzes, videos)** to boost engagement.
    - Collect qualitative feedback to pinpoint improvement areas.

    ### ✅ 3. **Personalize Learning Based on Age Groups**
    - Create **custom learning paths**: more gamified content for `<18`, flexible modules for `26+`.
    - Consider attention span and device accessibility for each age bracket.

    ### ✅ 4. **Promote High-Performing Courses (e.g., `DM101`)**
    - Highlight in dashboards or newsletters as **“Most Engaging”**.
    - Use learner testimonials and high ratings as part of **marketing content**.

    ### ✅ 5. **Targeted Engagement Campaigns**
    - Use time-based trends to launch **seasonal learning challenges** (e.g., before exams or holidays).
    - Send reminders or tips based on **low-completion behaviors** to nudge learners forward.

    ### ✅ 6. **Gender-Based Customization**
    - Study why female students are more engaged, and **apply those successful methods** to design more inclusive courses.
    - Conduct **focus group surveys** to understand motivational differences.

    ### ✅ 7. **Explore Regional Content Strategies**
    - Use `Location` data to localize content or offer **regional-language support**.
    - Schedule webinars or doubt-clearing sessions by **time zone or region**.

    ### ✅ 8. **Add a Progress Tracker with Visual Feedback**
    - Visual completion bars and milestone badges can help students **stay motivated and track performance**.
    - Send personalized nudges to students who pause progress.

    ---
    These recommendations are data-backed and can significantly improve the learning experience, feedback quality, and overall platform engagement.
    """)

elif option == "Trends":
    st.title("📊 Trends Over Time")

    # Extracting time-based data: Assuming Date column is in `activity_df`
    activity_df['Date'] = pd.to_datetime(activity_df['Date'], format='%d/%m/%Y', errors='coerce')
    
    # Trend for average engagement time by month
    st.subheader("1. Monthly Trend of Average Engagement Time")
    
    # Calculate the monthly average engagement time
    monthly_engagement = activity_df.groupby(activity_df['Date'].dt.to_period('M'))['Time_Spent_Minutes'].mean()
    
    # Plotting the trend for average engagement time
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_engagement.plot(ax=ax, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Time Spent (Minutes)')
    ax.set_title('Average Engagement Time by Month')
    st.pyplot(fig)

    # Trend for Course Completion Percentage over time
    st.subheader("2. Course Completion Percentage Trend Over Time")
    
    # Assuming you have 'Completion_Percentage' in your `activity_df`
    # If not, you can replace it with a relevant column for completion status
    monthly_completion = activity_df.groupby(activity_df['Date'].dt.to_period('M'))['Completion_Percentage'].mean()
    
    # Plotting the trend for course completion percentage
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_completion.plot(ax=ax, marker='o', color='g', linestyle='-', linewidth=2, markersize=6)
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Completion Percentage')
    ax.set_title('Course Completion Percentage Over Time')
    st.pyplot(fig)

    # Trend of student enrolments over time
    st.subheader("3. Student Enrolments Trend Over Time")
    
    # Assuming 'Enrolment_Date' in `students_df` contains the enrolment date
    students_df['Enrolment_Date'] = pd.to_datetime(students_df['Enrolment_Date'], format='%d/%m/%Y', errors='coerce')
    monthly_enrolments = students_df.groupby(students_df['Enrolment_Date'].dt.to_period('M'))['Student_ID'].count()
    
    # Plotting the trend for student enrolments
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_enrolments.plot(ax=ax, marker='o', color='purple', linestyle='-', linewidth=2, markersize=6)
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Enrolments')
    ax.set_title('Student Enrolments Over Time')
    st.pyplot(fig)
