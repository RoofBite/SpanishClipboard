# SpanishClipboard
![SpanishClipboard-screenshot](https://user-images.githubusercontent.com/85451799/132259634-e7192f1a-ae4a-483b-93fc-afa3eab48963.png)

**Live version: https://spanish-clipboard.herokuapp.com/login/**

**Dependencies can be found in requirements.txt file**

## How to run project with Docker: <br>

Value of variable secret_key in settings.py https://github.com/RoofBite/SpanishClipboard/blob/be80f64a5711794600fe6c78d25cd27564d87062/clipboard_project/settings.py#L16 is stored in enviroment variable, it should be set before starting the project.

Then run commands in terminal: <br>
docker-compose build  <br>
docker run -p 8000:8000 spanish-clipboard

Go to:
http://localhost:8000/