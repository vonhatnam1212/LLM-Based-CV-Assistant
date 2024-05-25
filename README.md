# LLMs
curl --location --request POST 'http://127.0.0.1:5000/query_CV' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_input" :"1. Educational Qualifications     • Bachelor’s degree in Computer Science, Engineering, Mathematics or related field of study 2. Relevant Knowledge/ Expertise     • 5-10 years experiences in software development and at least 3 years in banking and fintech domain.     • An understanding of bank business processes, fintech solution and constraints. 3. Relevant Experience     • Expert in JAVA language, Spring boot, Hibernate, jpa, and solid work with IDE     • Net Framework should be considered added skill.     • Advanced Knowledge MS SQL, Oracle DBs     • Having knowledge about microservice, Kubernetes, ability to config EKS.     • Experience with source code management like Git, Gitlab, Jira.     • Good understanding on webservice SOAP/Restful, Standard message JSON, XML, OOP, Design pattern ...     • Knowledge on Angular, JS is big plus. 4. Skill     • Ability in English reading and writing (mandatory), and speaking, listening (preferable). 5. Others     • Teamwork, careful, attention to detail, logical thinking.     • Problem-solving skills, ability to work under high pressure and can-do attitude.     • Self-development and motivation skill."
}'

