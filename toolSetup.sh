#!/usr/bin/env bash

# Assume we are using Bash

sudo apt-get update
sudo apt-get dist-upgrade -y

# Add core doc tools
sudo apt-get install -y plantuml graphviz make m4 vim-gtk git python3-pip python3-dev python3-setuptools python3-wheel
# Can't install Pandoc from standard repos because it's very out of date
cd /tmp
wget https://github.com/jgm/pandoc/releases/download/2.1/pandoc-2.1-1-amd64.deb
sudo dpkg --install pandoc*.deb

# Want to build PDF files with Pandoc, need latex
sudo apt-get install -y texlive

# Want x ref for figures in Pandoc
pip install --upgrade --pre pandoc-figno


# GitHub specific set up tools

# Setup Ruby for Gollum
sudo apt-get install -y rbenv ruby-build  git gcc libssl-dev libreadline-dev zlib1g-dev

rbenv version

echo 'eval "$(rbenv init -)"' >> ~/.bashrc 
eval "$(rbenv init -)"

rversion=$(rbenv install -l | grep -E '^ +[0-9.]+$'| tail -1)
rbenv install $rversion
rbenv global $rversion

# Install Gollum for for Preview
sudo apt-get -y install libicu-dev
gem install gollum rdiscount github-markdown charlock_holmes


# Install gh-md-toc  from https://github.com/ekalinin/github-markdown-toc

mkdir ~/bin
wget https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc -o ~/bin/gh-md-toc
chmod a+x ~/bin/gh-md-toc

if [[ ! -x ~/bin/gh-md-toc ]] ; then
  # Only works on GNU systems? Beware Mac users
  printf '\n# Added for install of gh-md-toc %(%F)T\nPATH=~/bin:$PATH\n' >> ~/.bashrc
  echo "PATH updated. Please restart terminal session"
fi

