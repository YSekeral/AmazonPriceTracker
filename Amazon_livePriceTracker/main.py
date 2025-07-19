import os
from smtplib import SMTP
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
Bot_Email = os.getenv("EMAIL_ADDRESS")
Bot_passkey = os.getenv("SMTP_PASSWORD")
SMTP_Server = os.getenv("SMTP_SERVER")

Website_link = str(input("Please enter the amazon link to track the price.\n"))
User_email = str(input("Please enter your email that is going to receive the updates for product"))

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
Accept_Language = "en-US,en;q=0.9,tr;q=0.8"
headers = {
    "User-Agent": User_Agent,
    "Accept-Language": Accept_Language
}
response = requests.get(Website_link, headers=headers).text

soup = BeautifulSoup(response, "html.parser")

Price = float(soup.find("span", class_="a-offscreen").getText().split("$")[1])
Price_as_INT = int(Price)

Web_Title = soup.find("span",id="productTitle").getText().strip()

Target_price = int(input("Enter the target price to get notification: \n"))

if Price_as_INT < Target_price:
    print("Deal has been found, preparing to send the email! \n")
    message = f"Subject:Amazon Deal has been found!\n\n {Web_Title} is now {Price}$\n Buy it fast! url: {Website_link}"

    with SMTP(SMTP_Server, port=587) as Connection:
        Connection.starttls()
        Connection.login(Bot_Email,Bot_passkey)
        Connection.sendmail(from_addr=Bot_Email,to_addrs=User_email,msg=message.encode("utf-8"))  #fix this one

    print("Email has been sent to your email address.")

else:
    print("Deal could not be found, please try again later!")



