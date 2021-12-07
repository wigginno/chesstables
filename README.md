# chesstables
Setup:
cd chesstables
bash
virtualenv venv -p $(which python3) 
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt

Start web app on port xxxx:
Change port number in app/webapp.py to any unused port
source ./venv/bin/activate
python app/webapp.py

Run web app forever (requires the npm package "forever"):
forever start -c python app/webapp.py
