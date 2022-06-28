recruiter = {'name': 'recruiter', 'designation': 'HR', 'company': 'ABC Tech Solutions', 'email': 'recruiter@xyz.com',
             'date_of_birth': '1980-01-01', 'gender': 'Male', 'mobile_number': 9111111111,
             'about_company': 'ABC Tech Solutions was established in 1990 to provides technology and consulting services',
             'website': 'https://www.abctech.com/' ,'password': 'Pass@123'}

testrecruiter = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                 'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                 'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                 'website': 'https://www.itservices.com/' ,'password': 'Word@123'}

seeker = {'name': 'seeker', 'email': 'seeker@abc.com', 'date_of_birth': '1995-01-01', 'gender': 'Male', 'mobile_number': 8111111111,
          'address': 'Chennai, Tamilnadu', 'password': 'Test@456', 'course': 'MBA', 'specialization': 'Marketing and Finance',
          'course_type': 'Part-time', 'college': 'Anna University', 'percentage': '78', 'year_of_passing': '2018', 'skills': 'Marketing, Financial reporting, Analytical ability',
          'summary': 'To achieve the objectives of the company with honesty and fairness and to continuously upgrade my knowledge and skills.',
          'experience_level': 'Experienced', 'designation': 'Marketing Analyst',
          'responsibilities': 'Tracking advertising costs, researching consumer behavior and exploring market trends and opportunities.',
          'company': 'Branded Marketing', 'location': 'Chennai', 'worked_from': '2018-06-01', 'to': '2020-01-01'}

testseeker = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
              'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
              'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
              'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
              'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}


from job.models import *
from user.models import *
import requests
import json
from django.contrib.auth import get_user_model


def create_admin(**params):
    return get_user_model().objects.create_admin(**params)


def create_user(**params):
    return get_user_model().objects.create_user(**params)

# try:
#     create_admin(**recruiter)
# except:
#     print('none')
# try:
#     create_admin(**testrecruiter)
# except:
#     print('none')
# try:
#     create_user(**seeker)
# except:
#     print('none')
# try:
#     create_user(**testseeker)
# except:
#     print('none')

payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
response = requests.post('http://127.0.0.1:8000/login/', data=payload)
response_content = json.loads(response.content.decode('utf-8'))
token = response_content['token']

payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
           'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
           'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
response = self.client.post('http://127.0.0.1:8000/postjob/', data=payload, format='json', headers={'Authorization': 'Token ' + token})
response_content = response.content.decode('utf-8')


payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
response = self.client.post('http://127.0.0.1:8000/login/', data=payload)
response_content = json.loads(response.content.decode('utf-8'))
token = response_content['token']

payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
           'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
           'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
response = self.client.post('http://127.0.0.1:8000/postjob/', data=payload, format='json', headers={'Authorization': 'Token ' + token})
response_content = response.content.decode('utf-8')
