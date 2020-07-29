from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import argparse
import time
import datetime
from dateutil.tz import *
import os


class TikTokBot:
    def __init__(self, who_can_view, video_path, date_time):
        path = os.path.dirname(os.path.abspath(__file__))
        self.driver = webdriver.Chrome(f'{path}/chromedriver')
        self.executor_url = self.driver.command_executor._url
        self.session_id = self.driver.session_id
        print(self.executor_url, self.session_id)
        self.driver.get('https://tiktok.com')

        while True:
            try:
                cookies = self.driver.get_cookies()
                cookies = [i for i in cookies if i['name'] == 'sessionid']
                if cookies:
                    print('session:', cookies[0])
                    break
                else:
                    time.sleep(1)
            except KeyError:
                print('Make sure to login')
                time.sleep(10)

        self.url = self.driver.current_url
        print(self.url)

        # takes you to the upload page
        while True:
            try:
                self.driver.find_element_by_xpath('//a[@href="https://www.tiktok.com/upload/?lang=en"]').click()
                break
            except NoSuchElementException:
                time.sleep(1)

        # upload video from files
        while True:
            try:
                self.driver.find_element_by_xpath('//input[contains(@name, "upload-btn")]').send_keys(video_path)
                break
            except NoSuchElementException:
                time.sleep(2)

        # set caption
        self.driver.find_element_by_xpath('//div[contains(@class, "notranslate public-DraftEditor-content")]').send_keys('Uploaded by a bot #bot #cs #cool')

        if who_can_view == 'Public':
            self.driver.find_element_by_xpath('//label[contains(text(), "Public")]').click()
        elif who_can_view == 'Friends only':
            self.driver.find_element_by_xpath('//label[contains(text(), "Friends only")]').click()
        else:
            self.driver.find_element_by_xpath('//label[contains(text(), "Private")]').click()

        # make sure video is uploaded
        while True:
            try:
                video = self.driver.find_element_by_css_selector('video[src^="http://"]')
                source = video.get_attribute('src')
                print('video uploaded')
                print('temp video source:', source)
                break
            except NoSuchElementException:
                print('video uploading...')
                time.sleep(10)

        # check for when to post
        d, t = date_time.split()
        y, m, d = d.split('-')
        hour, minute = t.split(':')

        dt = datetime.datetime(int(y), int(m), int(d), int(hour), int(minute), 0, tzinfo=tzlocal())
        dt.strftime('%X %x %Z')
        now = datetime.datetime.now(tz=tzlocal())
        while datetime.datetime.now(tz=tzlocal()) < dt:
            print('checking...')
            time.sleep(10)

        # click submit
        print('submitting...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Upload ")]').click()
        print('done')
        time.sleep(120)


def main():
    parser = argparse.ArgumentParser(description='This bot allows you to upload your TikTok videos at a set time, as long as you login.')
    parser.add_argument("--privacy", choices=['Private', 'Friends only', 'Public'], help="Private, Friends only, or Public", required=True)
    parser.add_argument("--video_path", help="Absolute path to video, i.e. /Users/username/Downloads/IMG_1648.MOV", required=True)
    parser.add_argument("--date_time", help="Enter date and time you want the video to post, i.e. 2020-07-27 00:48", required=True)
    args = parser.parse_args()
    TikTokBot(who_can_view=args.privacy, video_path=args.video_path, date_time=args.date_time)


if __name__ == '__main__':
    main()
