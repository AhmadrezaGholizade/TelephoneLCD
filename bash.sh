sudo pacman -S --needed \
    base-devel \
    git \
    openssl \
    zlib \
    xz \
    tk \
    libffi \
    readline \
    bzip2 \
    ncurses \
    sqlite \
    curl

curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

source ~/.bashrc