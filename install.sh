#!/usr/bin/bash

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv --version
pyenv install 3.12.0
pyenv global 3.12.0
python3.12 -m pip install --upgrade aws-sam-cli
exec $SHELL -l
