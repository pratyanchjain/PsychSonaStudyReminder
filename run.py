from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import select

global my_studies
my_studies = None

def run(receiver, sona_username, sona_password):
    global my_studies
    def find_my_studies():
        global my_studies
        # finding studies done already
        studies = []
        driver.find_element(By.LINK_TEXT, "My Schedule/Credits").click()
        study_table = driver.find_elements(By.XPATH, "//td[@data-title='Study']")
        for blocks in study_table:
            study_title = blocks.find_element(By.TAG_NAME, value="strong")
            studies.append(study_title.text)
        # go back to studies page
        driver.find_element(By.LINK_TEXT, "Studies").click()
        return studies

    def send_email(new_studies):
        text = ""
        text += "New studies available\n"
        for name, link in new_studies:
            text += name + ": " + link
        context = ssl.create_default_context()
        port = 465
        sender = "chutiyakaamkeliye@gmail.com"
        msg = MIMEMultipart("alternative")
        part1 = MIMEText(text, "plain")
        msg.attach(part1)
        msg['Subject'] = "New Psych Studies Available!"
        msg['From'] = sender
        msg['To'] = receiver
        #region 
        password = "bkwl jevt marz fiif" 
        # endregion#

        smtp = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        with smtp as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
    try:
        # starting chromedriver
        driver = webdriver.Chrome()
        # getting website
        driver.get("https://purdue-psych.sona-systems.com/Default.aspx?ReturnUrl=%2fall_exp_participant.aspx")

        # login
        user_button = driver.find_element(By.NAME, value="ctl00$ContentPlaceHolder1$userid")
        user_button.send_keys(sona_username)

        driver.implicitly_wait(0.5)

        password = driver.find_element(By.NAME, value="ctl00$ContentPlaceHolder1$pw")
        password.send_keys(sona_password)

        driver.implicitly_wait(0.5)

        login = driver.find_element(By.NAME, value="ctl00$ContentPlaceHolder1$default_auth_button")
        login.click()

        driver.implicitly_wait(0.5)

        # viewing studies

        view_studies = driver.find_element(By.ID, value="lnkStudySignupLink")
        view_studies.click()

        driver.implicitly_wait(0.5)

        # finding studies done
        if (my_studies == None):
            my_studies = find_my_studies()
        print("Studies Notified/Completed:-")
        for j in my_studies:
            print(j)
        print()
        new_studies = []
        # finding studies
        table = driver.find_element(By.TAG_NAME, value="table")
        titles = table.find_elements(By.CSS_SELECTOR, value="strong a")
        for row in titles:
            if (row.text not in my_studies):
                new_studies.append([row.text, row.get_attribute("href")])        
        if (len(new_studies) > 0):
            send_email(new_studies)
            for a, b in new_studies:
                my_studies.append(a)
            new_studies=[]
        else:
            print("No new studies yet")
        driver.quit()
    except:
        return

def main():
    receiver = input("Please enter the email where you want to receive notifications: ")
    sona_username = input("Please enter your SONA username: ")
    sona_password = input("Please enter your SONA password: ")
    start = time.time()
    while True:
        print("Time elapsed since last scan: ",time.time() - start, " seconds")
        if ((time.time() - start) >= 100 or (time.time() - start) < 1):
            try:
                run(receiver, sona_username, sona_password)
            except:
                time.sleep(100)
            start = time.time()
        input_list = [sys.stdin]
        ready_to_read, _, _ = select.select(input_list, [], [], 5)
        if sys.stdin in ready_to_read:
            input()
            break
main()