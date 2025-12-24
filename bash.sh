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

# Requirements
# jalali_core 1.0.0
# jdatetime   5.2.0
# numpy       2.2.6
# pillow      12.0.0
# pip         23.0.1
# setuptools  65.5.0
