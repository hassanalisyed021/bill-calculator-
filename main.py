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
        price = st.number_input("Individual Price", min_value=0.01, step=0.01, format="%.2f")
        submit = st.form_submit_button("Add Item")
    
    # Add new entry to session state
    if submit and quantity and price:
        st.session_state.data.append({
            "Item Name": item_name,
            "Quantity": int(quantity),
            "Individual Price": float(price),
            "Total Price": float(quantity) * float(price)
        })
    
    # Convert data to DataFrame
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        
        # Ensure total price updates in the table
        df["Total Price"] = df["Quantity"].astype(float) * df["Individual Price"].astype(float)
        
        # Calculate total bill amount
        total_bill = df["Total Price"].sum()
        
        # Append total bill amount as last row
        total_row = {"Item Name": "Total", "Quantity": "", "Individual Price": "", "Total Price": f"Rs.{total_bill:.2f}"}
        df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
        
        st.write("### Final Bill")
        edited_df = st.data_editor(df, num_rows="dynamic")
        
        # Save edited data back to session state (excluding total row)
        st.session_state.data = edited_df[:-1].to_dict(orient='records')
        st.write(f"## Total Bill Amount: Rs{total_bill:.2f}")
    
    # Reset Button
    if st.button("Reset Bill"):
        st.session_state.data = []
        st.rerun()

if __name__ == "__main__":
    main()
