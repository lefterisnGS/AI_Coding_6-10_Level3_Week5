# Team AI Showcase

This is a simple Streamlit class project.

What the app does
- reads one small text file for each child
- builds one colorful class webpage
- shows favorite things, course reflections, and dream app ideas
- works well for a team presentation

Project structure
- streamlit_app.py = the app
- course.txt = the class messages
- kids/_TEMPLATE.txt = copy this once per child
- assets/ = the images
- prompts/flux_prompts.md = image prompts
- .streamlit/config.toml = theme settings

What each child edits
Each child edits only one file inside the kids folder.
Important rule:
Change only the words after the colon.

How to run locally
1. Install Python
2. Install requirements:
   pip install -r requirements.txt
3. Run:
   streamlit run streamlit_app.py

GitHub workflow
1. Teacher creates the repository
2. Teacher uploads all starter files
3. Teacher copies kids/_TEMPLATE.txt into one file per child
4. Each child edits only one file
5. Commit the change
6. Refresh the Streamlit app

Images
Save these exact files in assets:
- hero-banner.png
- grandy.png
- team-stickers.png