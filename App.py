from multiprocessing import Value
import streamlit as st

# UI for car information input
st.title("Car Information")
image_file = st.file_uploader("Upload Car Image", type=["jpg", "jpeg", "png"])

col1,col2,col3=st.columns([2,2,2])
with col1:
    brand = st.text_input("Brand")
with col2:
    year = st.number_input("Year", min_value=1900, max_value=2100, value=2022, step=1)
with col3:
   Kilometer = st.number_input("Kilometer Driven") 


mileage_units = ["kmpl", "km/kg"]
mileage_units = ["kmpl", "km/kg"]
col1, col2 = st.columns([3, 1])
with col1:
    mileage = st.number_input("Mileage")
with col2:
    mileage_unit = st.selectbox("Mileage Unit", mileage_units)


col1,col2=st.columns([2,2])
with col1:
    original_price = st.number_input("Original Price (Lakh)")
with col2:
    Owner_Type = st.selectbox("Owner Type",["First Hand","Second Hand","Other"])



col1,col2=st.columns([2,2])
with col1:
    Transmission = st.selectbox("Transmission", ["Automatic", "Manual"])
with col2:
    Fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])

    
col1,col2,col3=st.columns([2,2,2])
with col1:
    engine = st.number_input("Engine(CC)", step=0.1)
with col2:
    power = st.number_input("Power (BPH)")
with col3:
    seat = st.selectbox("Seat",("1","4","5","6","7","8"))

    # Create a container for the submit button
submit_container = st.container()

# Add a spacer to center the submit button
submit_container.markdown("<div style='height:50px,width:50%,margin-right:375px;'></div>", unsafe_allow_html=True)

# Add the submit button to the container
with submit_container:
    submit_button=st.button(label="Submit")




# Output the selected mileage and mileage unit

# UI for submit button
if submit_button:


    # Logic to process car information and image
    # This could involve saving the image to a database or performing calculations on the input data
    
    # Show a message to confirm that the form was submitted
    st.success("New Car Price information Generated Below!")
    
    # Display a summary of the car information
    st.write("Summary:") 
    st.write("- Brand:", brand), st.write("- Year:", year)
    st.write("- Mileage:", mileage, mileage_unit), st.write("- Value (Lakh):",Value)
    st.write("- Owner Type:", Owner_Type)
    st.write("- Kilometer Driven:", Kilometer)
    st.write("- Transmission:", Transmission)
    st.write("- Fuel Type:", Fuel_type)
    st.write("- Engine(CC):", engine)
    st.write("- Power (BPH):", power)
    st.write("- Seat:", seat)
    st.write("- Original Price:", original_price)
    

    # Display the uploaded car image, if any
    if image_file is not None:
        st.write("Uploaded Car Image:")
        st.image(image_file, use_column_width=True)
