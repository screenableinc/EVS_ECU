import requests
from bs4 import BeautifulSoup
import getpass
import os
import json
import urllib
from urllib.parse import urlsplit,parse_qs
# import ssl
# ssl.match_hostname = lambda cert, hostname: True

data = {"__VIEWSTATE":"","__VIEWSTATEGENERATOR":"",'ctl00$MainContent$UserName': '', 'ctl00$MainContent$Password': '','ctl00$MainContent$Button1':'Log In'}
login = "https://sms.unilus.ac.zm/Students/Login.aspx"
studentPortal = "https://sms.unilus.ac.zm/Students/StudentPortal.aspx"

data3="__VIEWSTATE=%2FwEPDwUJLTYyNDUwMzcxD2QWAmYPDxYEHg9fX0FudGlYc3JmVG9rZW4FIDQ2ODI0MGUwNDY4OTRiNzFhODkxODZlOGEyYjdlMjU1HhJfX0FudGlYc3JmVXNlck5hbWVlZBYCAgMPZBYCAjsPZBYCAgEPFgIeBFRleHRlZGSYfDbBYQeqTbHpoV0ysz0noyUBEGfyxf7CupOnJyTwQQ%3D%3D&__VIEWSTATEGENERATOR=6B7E562E&__EVENTVALIDATION=%2FwEdAAbC8fWV9rbtEnUUTO%2B30OTn45a3adTEMpbjbWP0qDUy5sfvyjIx4eNfJAMrZe%2FGRMD%2FtZrOiYJPSwQdWShmXqFGz70%2FezTD4x4Y4%2BibsTHKkPnd3wctyww89JbDbeLvgrj95U3uhcH6AO9EWLLpD4HX4dx0ziJdkcpv1Wlyu6gNJg%3D%3D&ctl00%24MainContent%24User=Student&ctl00%24MainContent%24UserName=ECA1713710&ctl00%24MainContent%24Password=w1530977&ctl00%24MainContent%24Button1=Log+In"
def auth(base_url, target_url, username, password):
    with requests.Session() as s:
        page = s.get(base_url)
        s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        s.headers["Host"]="www.unilus.ac.zm"
        s.headers["Content-Type"]="application/x-www-form-urlencoded"
        soup = BeautifulSoup(page.content,"html.parser")
        print(soup)
        data["ctl00$MainContent$UserName"]=username
        data["ctl00$MainContent$Password"]=password
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        # data["__EVENTVALIDATION"] = "/wEdAAYEoTOtV4atCjZ1wHOAPOEX45a3adTEMpbjbWP0qDUy5sfvyjIx4eNfJAMrZe/GRMD/tZrOiYJPSwQdWShmXqFGz70/ezTD4x4Y4+ibsTHKkPnd3wctyww89JbDbeLvgrgbYxgx6AQ8fCmWPgUXagkMK7rM995fqHBTko6MGL6u3A=="
        data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

        query = urlsplit("http://www.kl.com/?"+urllib.parse.urlencode(data)).query
        params = parse_qs(query)
        query2 = urlsplit("http://www.kl.com/?" + data3).query
        params2 = parse_qs(query2)

        # print(urllib.parse.urldecode(data))

        # /wEdAAYEoTOtV4atCjZ1wHOAPOEX45a3adTEMpbjbWP0qDUy5sfvyjIx4eNfJAMrZe/GRMD/tZrOiYJPSwQdWShmXqFGz70/ezTD4x4Y4+ibsTHKkPnd3wctyww89JbDbeLvgrgbYxgx6AQ8fCmWPgUXagkMK7rM995fqHBTko6MGL6u3A==
        print(s.cookies)
        s.post(base_url, data=data)
        open_page = s.get(target_url)

        #Check content
        if str(open_page.text).__contains__("action=\"./Login.aspx\""):
            
            print("failed")
            return "fail","Credential Error"

        else:
            # store session
            #  id and return

            print("success")
            return "success",open_page.text


auth(base_url=login,target_url=studentPortal,username="ECA1713710",password="w1530977")