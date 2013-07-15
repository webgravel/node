mkdir -p /gravel/system/
useradd --system --uid 501 --gid 1 \
    --create-home --home-dir /gravel/system/gravelnode \
    gravelnode
ln -sf $PWD/register.py /usr/local/bin/gravelregister

echo "gravelnode ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/gravelnode
chmod 440 /etc/sudoers.d/gravelnode

GHOME=/gravel/system/gravelnode
if [ ! -e $GHOME/.ssh/id_rsa ]; then
    sudo -u gravelnode mkdir $GHOME/.ssh/
    sudo -u gravelnode ssh-keygen -f $GHOME/.ssh/id_rsa -N ''

    echo
    echo "Run on master:"
    echo
    echo gravel register `hostname` \""$(cat $GHOME/.ssh/id_rsa.pub)"\"
    echo
fi
