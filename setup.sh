mkdir -p /gravel/system/
useradd --system --uid 501 --gid 1 \
    --create-home --home-dir /gravel/system/gravelnode \
    gravelnode
ln -sf $PWD/register.py /usr/local/bin/gravelregister

echo "gravelnode ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/gravelnode
chmod 440 /etc/sudoers.d/gravelnode
