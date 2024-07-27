# sitegenesis
Web site generator

# setup venv
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

# pip install packages
```bash
pip install flask
pip install python-dotenv
pip install 'crewai[tools]'
pip install together
pip install groq
pip install supabase
pip install supabase_auth
pip install vapi_python
pip install gitpython
```

# Link to Relevance AI
https://api-bcbe5a.stack.tryrelevance.com/latest/agents/trigger


# Run dev server on port 3000 for Supabase compatibility
```python
if __name__ == '__main__':
    app.run(port=3000, debug=True)
```

