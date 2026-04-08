from serpapi import GoogleSearch
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 


medicine_company = []
medicine_price = []
def cleanprice (stringprice) : 
    if stringprice is None :
        return None 
    return float(stringprice.replace("₹","").replace("$","").replace(",","").strip())

def compare(med_name) :
    client = serpapi.Client(api_key="1eb7966bba89a9a96f97edd08c1abc67729ac56c4a9a109c272a128019629e8a")
    results = client.search({
    "engine": "google_shopping",
    "q": med_name ,
    "gl" : "in"
    })
    shopping_results = results["shopping_results"]
    return shopping_results

c1,c2 = st.columns(2)
c1.image("1562047588EpharmacyLegalAspects.png",width=200)
c2.header("E-Pharmacy Price Comparison System")


"""------------------------------------------------------"""

st.sidebar.title("Enter Name Of Medicine : ")
med_name = st.sidebar.text_input("Enter Name Here : ")
noofmed = st.sidebar.text_input("Enter Option : ")


if med_name is not None : 
    if st.sidebar.button("Compare Price") :
        shopping_results = compare(med_name)

        lowest_price = float('inf')
        lowest_price_index = -1

        st.sidebar.image(shopping_results[0].get("thumbnail"))
                                
        for i in range(int(noofmed)) :
            raw_price = shopping_results[i].get("price")
            current_price = cleanprice(raw_price)

            medicine_company.append(shopping_results[i].get("source"))
            medicine_price.append(current_price)

            st.title(f"Option {i+1}")
            c1,c2 = st.columns(2)

            c1.write("Company : ")
            c2.write(shopping_results[i].get("source"))

            c1.write("Title : ")
            c2.write(shopping_results[i].get("title"))

            c1.write("Price : ")
            c2.write(shopping_results[i].get("price"))

            url = shopping_results[i].get("product_link")
            c1.write("Buy Link : ")
            c2.write("[Link](%s)"%url)
            """____________________________________________________________________"""

            if (  current_price is not None and current_price < lowest_price ) :
                lowest_price = current_price 
                lowest_price_index = i


        # best option 

        st.title("Best Option : ")
        c1,c2 = st.columns(2)

        c1.write("Company : ")
        c2.write(shopping_results[lowest_price_index].get("source"))

        c1.write("Title : ")
        c2.write(shopping_results[lowest_price_index].get("title"))

        c1.write("Price : ")
        c2.write(shopping_results[lowest_price_index].get("price"))

        url = shopping_results[lowest_price_index].get("product_link")
        c1.write("Buy Link : ")
        c2.write("[Link](%s)"%url)

        # graph
        df = pd.DataFrame(medicine_price,medicine_company)
        st.title("Chart Comparison : ")
        st.bar_chart(df)

        fig, ax = plt.subplots()
        ax.pie(medicine_price, labels=medicine_company, autopct='%1.1f%%', shadow=True)
        ax.set_title("Price Distribution")
        ax.axis("equal")
        st.pyplot(fig)