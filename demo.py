# import requests
from models import Solutions
import re
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import time
import socket

url_major = ['https://my.uq.edu.au/programs-courses/program_list.html?acad_prog=2425']
url_detail = ['https://my.uq.edu.au/programs-courses/course.html?course_code=']


def findCourseCodes(url: list):
    socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
    header = {'User-Agent': 'Mozilla/5.0'}
    # download a website
    # url = ['https://my.uq.edu.au/programs-courses/program_list.html?acad_prog=2425']
    # simulate the step of sending request
    for i in url:
        request = urllib.request.Request(i, headers=header)
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, 'html.parser')
            code = soup.find('div', attrs={'class': 'courselist'})
            # unit = soup.find('td', attrs={'class': 'unit'})
            # title = soup.find('td', attrs={'class': 'title'})
            # 把对象转变为字符串
            cod = str(code)
            # 正则抓取课程编号
            tmp_coursecode = re.findall(r'course_code=.*?"', cod, re.S)
            solution = Solutions()
            coursecode = solution.getCourseCode(tmp_coursecode)
            print(coursecode)
            # 保存课程编号
            solution.saveCourseCode()
            response.close()
        except urllib.error.URLError as e:
            print(e.reason)
        time.sleep(1)


def findCourseDetails(url: list, code: list):   # url是url前缀，code是course code，加一块是destination，一个list
    socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
    header = {'User-Agent': 'Mozilla/5.0'}
    destination = []
    for i in code:
        tmp = url[0] + i
        destination.append(tmp)
    for i in destination:
        request = urllib.request.Request(i, headers=header)
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, 'html.parser')
            coursedetail = soup.find('p', attrs={'id': 'course-summary'})
            solution = Solutions()
            solution.getCourseDetail(coursedetail.text)
            print(coursedetail.text)
            # 保存课程编号
            solution.saveCourseDetail()
            response.close()
        except urllib.error.URLError as e:
            print(e.reason)
        time.sleep(1)


findCourseCodes(url_major)
solution = Solutions()
solution.loadCourseCode()
# print(solution.subject_course)  # 这玩意儿也是课程编号
findCourseDetails(url_detail, solution.subject_course)