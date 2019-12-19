# il pourrait il y avoir des problèmes avec pip 
python3 -m pip uninstall pip

pip3 install --user --upgrade pip
pip3 install --user -r requirements.txt
python3 index.py