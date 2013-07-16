mkdir -p /gravel/system/node

GHOME=/gravel/system/node/home
useradd --system --uid 501 --gid 1 \
    --create-home --home-dir $GHOME \
    gravelnode

echo "gravelnode ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/gravelnode
chmod 440 /etc/sudoers.d/gravelnode || exit 1

if [ ! -e $GHOME/.ssh/id_rsa ]; then
    sudo -u gravelnode mkdir $GHOME/.ssh/ || exit 1
    sudo -u gravelnode ssh-keygen -f $GHOME/.ssh/id_rsa -N '' || exit 1

    echo
    echo "Run on master:"
    echo
    echo gravel register `hostname` \""$(cat $GHOME/.ssh/id_rsa.pub)"\"
    echo
fi
