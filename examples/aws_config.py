# AWS Configuration Template
# 
# INSTRUCTIONS:
# 1. Copy this file to your project directory
# 2. Fill in your AWS credentials (get from owner)
# 3. Add "aws_config.py" to your .gitignore
# 4. Import in notebooks/scripts as needed
#
# WARNING: Never commit this file to git!

AWS_ACCESS_KEY_ID = 'paste-your-access-key-here'
AWS_SECRET_ACCESS_KEY = 'paste-your-secret-key-here'
AWS_DEFAULT_REGION = 'us-east-1'

# Usage in notebook/script:
# 
# import os
# from aws_config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# 
# os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
# os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
# os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION
# 
# from immigration_corpus import load_data
# df = load_data(files=[0, 1, 2])