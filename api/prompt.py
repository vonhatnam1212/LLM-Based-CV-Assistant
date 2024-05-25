#####################################################
#                 Prompt Templates
#####################################################

templates = {}

# 2.1 Contact information Section
templates[
    "Contact__information"
] = """Extract and evaluate the contact information. \
Output a dictionary with the following keys:
- candidate__name 
- candidate__title
- candidate__location
- candidate__email
- candidate__phone
- candidate__social_media: Extract a list of all social media profiles, blogs or websites.
"""

# 2.2. Summary Section
templates[
    "CV__summary"
] = """Extract the summary and/or career objective section. This is a separate section of the resume. \
If the resume doed not contain a summary and/or career objective section then generate a strong summary with no more than 5 sentences. \
Please include: years of experience, top skills and experiences, some of the biggest achievements, and finally an attractive objective."""


# 2.3. WORK Experience Section

templates[
    "Work__experience"
] = """Extract all work experiences. For each work experience: 
1. Extract the job title.
2. Extract the company.  
3. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
5. Describe roles and jobs .

"""

# 2.4. Projects Section
templates[
    "CV__Projects"
] = """Include any side projects outside the work experience. 
For each project:
1. Extract the title of the project. 
2. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
3. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Describe the project.
"""

# 2.5. Education Section
templates[
    "CV__Education"
] = """Extract all educational background and academic achievements.
For each education achievement:
1. Extract the name of the college or the high school. 
2. Extract the earned degree. Honors and achievements are included.
3. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
"""


# 2.6. Skills
templates[
    "candidate__skills"
] = """Extract the list of soft and hard skills from the skill section. Output a list.
The skill section is a separate section.
"""


# 2.7. Languages
templates[
    "CV__Languages"
] = """Extract all the languages that the candidate can speak. For each language:
1. Extract the language.
2. Extract the fluency. If the fluency is not available, then simply write "unknown".

"""

# 2.8. Certifications
templates[
    "CV__Certifications"
] = """Extraction of all certificates other than education background and academic achievements. \
For each certificate: 
1. Extract the title of the certification. 
2. Extract the name of the organization or institution that issues the certification.
3. Extract the date of certification and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the certification expiry date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
5. Extract any other information listed about the certification. if not found, then simply write "unknown".

"""

ovewview_template = "Rewrite the features below into a paragraph introducing your CV. The paragraph can specifically analyze the strengths of this CV. Please write about 500 words"
