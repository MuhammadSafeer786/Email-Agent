# Email Agent
### This agent listens for incomming emails and replies them according to previous emails and/or using context from project files

## Setup

1. Create folders for storing data:
   - `knowledge_base/` → stores previous emails  
   - `project_files/` → stores relevant project files  

2. Enable IMAP access in your email account settings. For Gmail users, create an app password if two-factor authentication is enabled.
3.  create .env file and set following variables

```
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

3. Run the project

```
python main.py
```
