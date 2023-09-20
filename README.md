# sdxl_artist_styles_studies
offline version of [sdxl.parrotzone.art](https://sdxl.parrotzone.art/) (つ✧ω✧)つ

# how to use
1. download [grids folder](https://huggingface.co/datasets/parrotzone/sdxl-1.0.zip), unzip and place in the "static" folder OR ```git clone https://huggingface.co/datasets/parrotzone/sdxl-1.0```and change the path ```/static/grids/``` in app.py line 72 to the grids path on your disk, so that you can just easily do ```git pull``` for every new addition
2. on linux/macos run ```./start.sh```
3. on windows, i provided the start.bat file but unsure if it works since i can't test it right now lol. alternatively run ```pip install requirements.txt```(maybe in a venv too, up to you ig) and then ```python app.py```
