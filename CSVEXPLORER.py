
import streamlit as st
import pandas as pd

def read_file(file):
    try:
        if hasattr(file, 'type') and file.type is not None:
            if 'excel' in file.type.lower():
                df = pd.read_excel(file)
            elif file.type == 'text/csv':
                df = pd.read_csv(file, encoding='latin-1')
            else:
                st.error("Unsupported file format")
                return None
            return df
        else:
            st.error("Invalid file")
            return None
    except Exception as e:
        st.error("Error reading file:", e)
        return None
def read_file(file):
    try:
        if file.type == 'application/vnd.ms-excel':
            data = io.BytesIO(file.read())
            df = pd.read_excel(data)
        elif file.type == 'text/csv':
            df = pd.read_csv(file, encoding='latin-1')
        else:
            st.error("Unsupported file format")
            return None
        return df
    except Exception as e:
        st.error("Error reading file:", e)
        return None


def main():
    st.title("CSV/Excel FILE EXPLORER")
    
    # Upload file
    uploaded_file = st.file_uploader("Upload CSV/Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
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





















