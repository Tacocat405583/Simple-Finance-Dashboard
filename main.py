#UI library
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os

st.set_page_config(page_title = "Simple Finance Dashboard", layout = "wide",page_icon="💰💰💰")

category_file = "categories.json"

if "categories" not in st.session_state: #will be stored in state so you can access it later
    st.session_state["categories"] = {
        "Uncategorized": []
    }

if os.path.exists(category_file):
    with open("categories.json","r") as f:
        st.session_state.categories = json.load(f) #easy way to load json data into a python dictionary
    
def save_categories():
    with open(category_file,"w") as f:
        json.dump(st.session_state.categories, f) #save the categories to a json file

def categorize_transactions(df):
    df["Category"] = "Uncategorized"  #new collumn called Cateogry and set it to Uncategorized by default
    for category, keywords in st.session_state.categories.items(): #This iterates over all categories the user has defined in st.session_state.categories
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower() for keyword in keywords] #normalize 

        for idx, row in df.iterrows(): # this function only works with another function alongside it as this will jus change if the json files is updated
            details = row["Details"].lower()
            if details in lowered_keywords:
                df.at[idx,"Category"] = category #set the category for the transaction

    return df

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns] #strip will get rid of white spaces
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)  #make them string,replace commas with an empty string, and convert to float
        
        df["Date"]  = pd.to_datetime(df["Date"],format="%d %b %Y") #convert the date column to datetime format adn to use datime operations


        return categorize_transactions(df)  #categorize the transactions based on the categories in session state
    

    except Exception as e:
        st.error(f"Error loading the file: {str(e)}")
        return None
    
def add_keyword(category,keyword):
    keyword = keyword.strip() #remove whitespaces
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False



def main():
    st.title("Simple Finance Dashboard")

    uploaded_file = st.file_uploader("Upload your CSV file",type=["csv"]) #can use comas to add other file types
    
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit/Credit"]=="Debit"].copy()
            creditsdf = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1,tab2 = st.tabs(["Expenses (Debits)","Payments (Credits)"])

            with tab1:
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.success(f"Category '{new_category}' added successfully!") #wont run since re are using session state
                        st.rerun()
                        
                
                st.subheader("Your Expenses")
                edited_df = st.data_editor( #list of collumns that you want to show in the data editor
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date":st.column_config.DateColumn("Date",format = "DD/MMM/YYYY"),
                        "Amount":st.column_config.NumberColumn("Amount",format = "%.2f AED"),
                        "Category":st.column_config.SelectboxColumn(
                            "Category",
                            options = list(st.session_state.categories.keys()),
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key = "category_editor"
                )

                save_button = st.button("Apply Changes",type = "primary")
                if save_button:
                    for idx,row in edited_df.iterrows():
                        new_category = row["Category"]
                        if row["Category"] == st.session_state.debits_df.at[idx,"Category"]: #Ignore if no change made
                            continue

                        details = row["Details"]  ##if change was made, update the category
                        st.session_state.debits_df.at[idx,"Category"] = new_category #this will update the category in the original dataframe
                        add_keyword(new_category, details)  #add the keyword to the category


                #Categorize the transactions again to ensure all categories are updated
                st.subheader("Expense Summary")
                category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index() #reset index to get a dataframe instead of a series
                category_totals = category_totals.sort_values("Amount",ascending=False)

                st.dataframe(category_totals,
                             column_config={
                                 "Amount":st.column_config.NumberColumn("Amount",format = "%.2f AED"),
                             },
                             use_container_width=True,
                             hide_index=True   

                             )
                
                #Chart
                fig = px.pie(
                    category_totals,
                    values = "Amount",
                    names = "Category",
                    title= "Expense Distribution by Category",
                )

                st.plotly_chart(fig,user_container_width=True)
                        


            with tab2:
                st.subheader("Income Summary")
                total_pament = creditsdf["Amount"].sum()
                st.metric("Total Income",f"{total_pament:,.2f} AED")
                st.write(creditsdf)


main()