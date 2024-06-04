
sudo zypper in -t pattern devel_basis devel_C_C++
sudo zypper in pyenv libopenssl-3-devel zlib-devel bzip2 libbz2-devel libffi-devel libopenssl-devel readline-devel sqlite3 sqlite3-devel xz xz-devel tk tk-devel npm22

pyenv install 3.12
pyenv global 3.12.3

// https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv
echo "pyenv init - | source" >> ~/.config/fish/config.fish

test your python version by:
python --version

pip install pipenv --user
fish_add_path ~/.local/bin
sudo npm install -g aws-cdk