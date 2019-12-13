# install pyenv
#curl https://pyenv.run | bash
#exec $SHELL

# create env
#pyenv virtualenv 3.8.0 venv
# activate env
#pyenv shell env
python3.7 -m venv env
pip install --upgrade pip
pip install matplotlib numpy PyInquirer pandas