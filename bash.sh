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

timedatectl set-timezone Asia/Tehran

curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

source ~/.bashrc

pip install -r requirements.txt

sudo cp ./tests/test_events/servicefile.ini /etc/systemd/system/phone-monitor.service
systemctl daemon-reload
systemctl enable phone_monitor.service
systemctl start phone_monitor.service



