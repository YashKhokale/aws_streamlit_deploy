#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from os import getenv
import boto3
import pandas as pd
import numpy as np
import time
import csv
import sys
from collections import defaultdict
import streamlit as st
import smtplib
import os


prod_list=[]
def main():
    c_email=st.text_input("to Subscribe to our newsletter, enter your email")
    email_sender="adm.07.northeastern@gmail.com"
    password="adm07northeastern"
    subject="ADMG7 Bank: Your daily dose of handpicked Products"
    try:
        body="Hi "+cust_name+",\nBased on your recent interest in our " + str(product)+" service, these are the products you may like: \n1. " + prod_list[0]+"\n2. "+ prod_list[1]+" \n3. "+ prod_list[2]+" \n4. "+ prod_list[3]
    except:
        pass
    if st.button("Subscribe"):
        try:
            #https://myaccount.google.com/security?rapt=AEjHL4OvBvYm7yvRPf8QPwdyRqgz3Y43F04kqsCFMnUv7Xoso_tZ9czjLPkxYVZ7DeYMGlkLDjNl7oI50MvSlupvWJg4IgkO5w
            connection=smtplib.SMTP('smtp.gmail.com',587)
            connection.starttls()
            connection.login(email_sender,password)
            message="subject:{}\n\n{}".format(subject,body)
            connection.sendmail(email_sender,c_email,message)
            connection.quit()
            st.success("Subscribed!")
            
        except:
            pass



personalize_runtime = boto3.client('personalize-runtime')

usr='12344'
auth=pd.read_csv('c_auth.csv')
prod = pd.read_csv('products.csv')
st.image('img/logo.png')
em=st.text_input("enter email ID: ")
if not em:
    st.write("Enter your email ID")
else:
    if em in list(auth["email"]):
        try:
            st.title("Welcome back!")
            id=auth[auth.email==em]['user_Id'].apply(lambda x: str(x))
            usr =id.iloc[0]
            response=personalize_runtime.get_recommendations(
                campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/userproductrecommendation',
                userId=usr,
                filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/purchase-filter"
            )
            t=response["itemList"]
            st.write("---------------------------------------------")
            st.write("Based on your recent purchases, products you might like:")
           
        except:
            st.write("email error")
    else:
        try:
            cust_name=st.text_input("Name:")
            st.write("Welcome ", cust_name,"!")
            response=personalize_runtime.get_recommendations(
                campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/userproductrecommendation',
                userId=usr,
                filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/purchase-filter"
            )
            t=response["itemList"]
        
            st.title("products recommended:")
        except:
            st.write("cold start error")
    
    try:
        col= st.beta_columns([1,1,1,1])
        for i in range(0,4):
            with col[i]:
                item=prod[prod.item_id==t[i]["itemId"]]["item_name"].iloc[0]
                pic=prod[prod.item_id==t[i]["itemId"]]["image"].iloc[0]
                st.write(item)
                pic='img/'+pic
                st.image(pic)
    except:
        st.write("error")
        
    st.write("---------------------------------------------")
    ########################

    st.write("Search Products:")
    try:
        product= st.selectbox('Choose a Product:', prod['item_name'])

        prod_id = prod[prod.item_name==product]["item_id"].iloc[0]



        response=personalize_runtime.get_recommendations(
            campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/item-similarity',
            itemId=prod_id,
            userId=usr,
            filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/similarityfilter"
        )
        t=response["itemList"]
        col= st.beta_columns([1,1,1,1])
        for i in range(0,4):
            with col[i]:
                item =prod[prod.item_id==t[i]["itemId"]]["item_name"].iloc[0]
                pic=prod[prod.item_id==t[i]["itemId"]]["image"].iloc[0]
                st.write(item)
                prod_list.append(item)
                pic='img/'+pic
                st.image(pic)
    except:
        pass
    if __name__=="__main__":
        main()

