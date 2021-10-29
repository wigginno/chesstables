# chesstables
Setup:
cd chesstables
bash
virtualenv venv -p $(which python3) 
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt

Start webb app on port xxxx:
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p xxxx --reload
