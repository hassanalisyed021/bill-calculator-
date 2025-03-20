import streamlit as st
import pandas as pd

def main():
    st.title("Billing System")
    
    # Initialize session state for storing table data
    if "data" not in st.session_state:
        st.session_state.data = []
    
    # Generate default item name
    item_name = f"Item {len(st.session_state.data) + 1}"
    
    # Input fields for adding new items
    with st.form("item_form"):
        quantity = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Individual Price", min_value=0.01, step=0.01)
        submit = st.form_submit_button("Add Item")
    
    # Add new entry to session state
    if submit and quantity and price:
        st.session_state.data.append({
            "Item Name": item_name,
            "Quantity": quantity,
            "Individual Price": price,
            "Total Price": quantity * price
        })
    
    # Convert data to DataFrame
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.write("### Final Bill")
        edited_df = st.data_editor(df, num_rows="dynamic")
        
        # Save edited data back to session state
        st.session_state.data = edited_df.to_dict(orient='records')
        
        # Display total bill amount
        total_bill = edited_df["Total Price"].sum()
        st.write(f"## Total Bill Amount: ${total_bill:.2f}")
    
    # Reset Button
    if st.button("Reset Bill"):
        st.session_state.data = []
        st.rerun()

if __name__ == "__main__":
    main()
