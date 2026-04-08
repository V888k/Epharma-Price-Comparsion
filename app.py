from serpapi import GoogleSearch
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

# साफ करने के लिए
def cleanprice(stringprice):
    if stringprice is None:
        return None
    try:
        return float(stringprice.replace("₹", "").replace("$", "").replace(",", "").strip())
    except:
        return None


def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "gl": "in",
        "api_key": os.getenv("SERPAPI_KEY")  # 🔐 secure way
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results.get("shopping_results", [])


# UI
c1, c2 = st.columns(2)
c1.image("1562047588EpharmacyLegalAspects.png", width=200)
c2.header("E-Pharmacy Price Comparison System")

st.sidebar.title("Enter Name Of Medicine : ")
med_name = st.sidebar.text_input("Enter Name Here : ")
noofmed = st.sidebar.number_input("Enter Option :", min_value=1, step=1)

if med_name:
    if st.sidebar.button("Compare Price"):

        shopping_results = compare(med_name)

        if not shopping_results:
            st.error("No results found!")
            st.stop()

        # reset lists हर बार
        medicine_company = []
        medicine_price = []

        lowest_price = float('inf')
        lowest_price_index = -1

        # limit results
        limit = min(int(noofmed), len(shopping_results))

        st.sidebar.image(shopping_results[0].get("thumbnail"))

        for i in range(limit):
            raw_price = shopping_results[i].get("price")
            current_price = cleanprice(raw_price)

            medicine_company.append(shopping_results[i].get("source"))
            medicine_price.append(current_price if current_price else 0)

            st.subheader(f"Option {i+1}")
            c1, c2 = st.columns(2)

            c1.write("Company : ")
            c2.write(shopping_results[i].get("source"))

            c1.write("Title : ")
            c2.write(shopping_results[i].get("title"))

            c1.write("Price : ")
            c2.write(raw_price)

            url = shopping_results[i].get("product_link")
            c1.write("Buy Link : ")
            c2.write(f"[Link]({url})")

            # cheapest logic
            if current_price is not None and current_price < lowest_price:
                lowest_price = current_price
                lowest_price_index = i

        # best option
        if lowest_price_index != -1:
            st.title("Best Option : ")
            c1, c2 = st.columns(2)

            best = shopping_results[lowest_price_index]

            c1.write("Company : ")
            c2.write(best.get("source"))

            c1.write("Title : ")
            c2.write(best.get("title"))

            c1.write("Price : ")
            c2.write(best.get("price"))

            url = best.get("product_link")
            c1.write("Buy Link : ")
            c2.write(f"[Link]({url})")

        else:
            st.warning("No valid price found")

        # charts
        df = pd.DataFrame({
            "Company": medicine_company,
            "Price": medicine_price
        })

        st.title("Chart Comparison : ")
        st.bar_chart(df.set_index("Company"))

        fig, ax = plt.subplots()
        ax.pie(medicine_price, labels=medicine_company, autopct='%1.1f%%')
        ax.set_title("Price Distribution")
        st.pyplot(fig)
