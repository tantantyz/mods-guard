sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum makecache
sudo yum install python36u
sudo yum -y install python36u-pip
sudo yum -y install python36u-devel

sudo yum -y install python-pip
pip install pipenv
pipenv install