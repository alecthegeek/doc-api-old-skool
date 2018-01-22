#!/usr/bin/env bash

# Assume we are using Bash

# NOTE: This script assumes it's working on a clean install of Debian
# If you already have Ruby or Python environments already set up this script
# may stop them working. Use with disrection.

sudo apt-get update
sudo apt-get dist-upgrade -y

# Add core doc tools
sudo apt-get install -y plantuml graphviz make m4 vim-gtk git python3-venv python3-dev python3-wheel python3-setuptools python3-pip python3-pandocfilters python3-psutil python3-wheel

# Actually need to manually install later version of plantuml because Debian version is so out of date
# This is a dirty hack
sudo wget https://downloads.sourceforge.net/project/plantuml/1.2018.0/plantuml.1.2018.0.jar -O /usr/share/plantuml/plantuml.jar

# Install a Python virtual env

VENV_HOME=~/py3venv/pandoc

mkdir -p $VENV_HOME
python3 -m venv $VENV_HOME
source $VENV_HOME/bin/activate

echo >> ~/.bashrc
echo "# Added for install of Python venv in $VENV_HOME $(date)" >> ~/.bashrc
echo source $VENV_HOME/bin/activate >> ~/.bashrc

# Can't install Pandoc from standard repos because it's very out of date
wget https://github.com/jgm/pandoc/releases/download/2.1/pandoc-2.1-1-amd64.deb -P /tmp
sudo dpkg --install /tmp/pandoc*.deb

# Want to build PDF files with Pandoc, need latex
sudo apt-get install -y texlive

# Want x ref for figures in Pandoc
pip install --upgrade wheel
pip install --upgrade --pre pandoc-fignos

sudo apt-get -y autoremove
sudo apt-get clean

# Tools to help publish on GitHub

# Setup Ruby for Gollum
sudo apt-get install -y rbenv ruby-build  git gcc libssl-dev libreadline-dev zlib1g-dev

sudo apt-get -y autoremove
sudo apt-get clean

rbenv version

echo >> ~/.bashrc
echo "# Added for install of Ruby rbenv $(date)" >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc 
eval "$(rbenv init -)"

rversion=$(rbenv install -l | grep -E '^ +[0-9.]+$'| tail -1)
rbenv install $rversion
rbenv global $rversion

# Install Gollum for Preview
sudo apt-get -y install libicu-dev
gem install gollum rdiscount github-markdown charlock_holmes


# Install gh-md-toc  from https://github.com/ekalinin/github-markdown-toc

if ! which gh-md-toc ; then
  [[ -d ~/bin ]] || mkdir ~/bin
  wget https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc -O ~/bin/gh-md-toc
  chmod a+x ~/bin/gh-md-toc

  echo >> ~/.bashrc
  echo "# Added for install of gh-md-toc $(date)" >> ~/.bashrc
  echo 'PATH=~/bin:$PATH' >> ~/.bashrc
  echo >> ~/.bashrc
fi

echo "Pease restart terminal to pick up env changes"

