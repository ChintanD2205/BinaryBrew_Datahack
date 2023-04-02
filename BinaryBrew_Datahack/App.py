from multiprocessing import Value
import streamlit as st
import sys
import pandas as pd
from datetime import date
today = date.today()

mypath = "C:\\Users\\Het\\Desktop\\BinaryBrew_Datahack\\Model"
if mypath not in sys.path:
    sys.path.append(mypath)
import pred_m
data = {'Year':0, 'Kilometers_Driven':0, 'Owner_Type':1, 'Seats':0, 'Mileage(km/kg)':0, 'Engine(CC)':0, 'Power(bhp)':0, 'Location_Bangalore' : 0,    'Location_Chennai':0,  'Location_Coimbatore':0,'Location_Delhi':0,'Location_Hyderabad':0, 'Location_Jaipur':0, 'Location_Kochi':0,'Location_Kolkata':0 , 'Location_Mumbai':0, 'Location_Pune' : 0, 'Fuel_Type_Diesel':0, 'Fuel_Type_LPG':0, 'Fuel_Type_Petrol':0, 'Transmission_Manual':1}

# UI for car information input
st.title("Value Scope")
image_file = st.file_uploader("Upload Car Image", type=["jpg", "jpeg", "png"])

col1,col2,col3=st.columns([2,2,2])
with col1:
    brand = st.text_input("Brand")
with col2:
    year = st.number_input("Year", min_value=1900, max_value=2100, value=2022, step=1)
    data['Year'] = year
with col3:
   Kilometer = st.number_input("Kilometer Driven") 
   data["Kilometers_Driven"] = Kilometer



mileage_units = ["kmpl", "km/kg"]
mileage_units = ["kmpl", "km/kg"]
col1, col2 = st.columns([3, 1])
with col1:
    mileage = st.number_input("Mileage")
    data["Mileage(km/kg)"] = mileage
with col2:
    mileage_unit = st.selectbox("Mileage Unit", mileage_units)


col1,col2,col3=st.columns([2,2,2])
with col1:
    original_price = st.number_input("Original Price (Lakh)")
with col2:
    Owner_Type = st.selectbox("Owner Type",["First Hand","Second Hand","Third Hand", "Other"])
    if Owner_Type=="First Hand":
        data["Owner_Type"] = 1 
    elif Owner_Type=="Second Hand":
        data["Owner_Type"] = 2
    elif Owner_Type=="Third Hand":
        data["Owner_Type"] = 3
    else:
        data["Owner_Type"] = 4
with col3:
    loc = st.text_input("Location")
    for k in data.keys():
        if "Location" in k:
            if loc==k.split("_")[1]:
                data[k] = 1


col1,col2=st.columns([2,2])
with col1:
    Transmission = st.selectbox("Transmission", ["Automatic", "Manual"])
    if Transmission=="Automatic":
        data["Transmission_Manual"] = 1
    else:
        data["Transmission_Manual"] = 0
with col2:
    Fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    if Fuel_type == "Petrol":
        data["Fuel_Type_Petrol"] = 1
    elif Fuel_type == "Diesel":
        data["Fuel_Type_Diesel"] = 1
    else:
        data["Fuel_Type_LPG"] = 1

    
col1,col2,col3=st.columns([2,2,2])
with col1:
    engine = st.number_input("Engine(CC)", step=0.1)
    data["Engine(CC)"] = engine
with col2:
    power = st.number_input("Power (BPH)")
    data["Power(bhp)"] = power
with col3:
    seat = st.selectbox("Seat",("1","4","5","6","7","8"))
    data["Seats"] = seat

    # Create a container for the submit button
submit_container = st.container()

# Add a spacer to center the submit button
submit_container.markdown("<div style='height:50px,width:50%,margin-right:375px;'></div>", unsafe_allow_html=True)

# Add the submit button to the container
with submit_container:
    submit_button=st.button(label="Submit")

inc_factor = 0
i=0
wss = pd.read_excel("Web_Scrap_Data.xlsx")
# Output the selected mileage and mileage unit

# UI for submit button
if submit_button:
    for name in wss.iloc[:,0]:
        if name.split()[0].upper() == brand.split()[0].upper():
            inc_factor = round(wss.iloc[i,5],1)
        i+=1

    price = pred_m.pred(data)

    price += (price*inc_factor)/100
    if today.year-year >5:
        price -= (price*0.08)
    else:
        price -= (price*0.03)
    # Logic to process car information and image
    # This could involve saving the image to a database or performing calculations on the input data
    
    # Show a message to confirm that the form was submitted
    st.success("New Car Price information Generated Below!")
    if(float(price)>=100):
        st.write("New Generated Price : ", round(float(price)/100,2), "Cr")
    else:
        st.write("New Generated Price : ", round(float(price),2), "Lakhs")
    # Display a summary of the car information
    st.write("Summary:") 
    st.write("- Brand:", brand)
    st.write("- Year:", year)
    st.write("- Mileage:", mileage, mileage_unit)
    st.write("- Owner Type:", Owner_Type)
    st.write("- Kilometer Driven:", Kilometer)
    st.write("- Transmission:", Transmission)
    st.write("- Fuel Type:", Fuel_type)
    st.write("- Engine(CC):", engine)
    st.write("- Power (BPH):", power)
    st.write("- Seat:", seat)
    st.write("- Original Price (Lakhs):", original_price)

    

    # Display the uploaded car image, if any
    if image_file is not None:
        st.write("Uploaded Car Image:")
        st.image(image_file, use_column_width=True)
