
import streamlit as st
import pandas as pd

def generate_questions(df):
    questions = []
    for index, row in df.iterrows():
        for column in range(len(row) - 1):  # Iterate over all columns except the last one
            current_value = row.iloc[column]
            next_value = row.iloc[column + 1]
            if pd.notna(current_value) and pd.notna(next_value):
                question = f"What is {current_value}?"
                answer = str(next_value)
                questions.append((index, column, question, answer))
    return questions

def read_file(uploaded_file):
    try:
        if uploaded_file is not None:
            if uploaded_file.type == 'application/vnd.ms-excel':
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.type == 'text/csv':
                df = pd.read_csv(uploaded_file, encoding='latin-1')
            else:
                st.error("Unsupported file format")
                return None
            return df
        else:
            st.error("No file uploaded")
            return None
    except Exception as e:
        st.error("Error reading file:", e)
        return None

def main():
    st.title("CSV/Excel FILE EXPLORER")
    
    # Upload file
    uploaded_file = st.file_uploader("Upload CSV/Excel file", type=["csv", "xlsx"])
    
    # Read data from file
    df = read_file(uploaded_file)
        
    if df is not None:
        # Display the uploaded data
        st.write("Uploaded data:")
        st.write(df)
        
        # Check if DataFrame has any rows
        if not df.empty:
            # Get unique rows in the DataFrame
            unique_rows = df.index.tolist()
            
            # Select a row to explore
            selected_row = st.selectbox("Select a row to explore", unique_rows)
            
            # Check if selected row index is valid
            if selected_row >= 0 and selected_row < len(df):
                # Display information for the selected row
                st.write("Selected row:")
                st.write(df.iloc[selected_row])
                
                # Option to show educational questions
                show_questions = st.checkbox("Show Questions to study the file")
                
                if show_questions:
                    # Generate educational questions based on the selected row data
                    st.subheader("Questions:")
                    questions = generate_questions(df)
                    for index, column, question, answer in questions:
                        st.write(f"Question: {question}")
                        unique_key = f"{index}_{column}"  # Unique key for each text_input
                        user_answer = st.text_input("Your answer", key=unique_key)
                        if user_answer.strip() == answer:
                            st.write("Correct!")
                        elif user_answer.strip() != "":
                            st.write("Incorrect. The correct answer is:", answer)
            else:
                st.write("Invalid row index selected.")
        else:
            st.write("No valid rows to select.")

if __name__ == "__main__":
    main()





















