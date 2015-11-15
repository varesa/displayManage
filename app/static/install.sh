#!/bin/env bash

apt-get update && apt-get install -y git puppet

git clone https://github.com/varesa/puppet_nastori_system.git /etc/puppet/modules/nastori_system/
git clone https://github.com/varesa/puppet_nastori_viewer.git /etc/puppet/modules/nastori_viewer/

puppet module install puppetlabs-inifile

puppet apply -e "include nastori_system"
puppet apply -e "include nastori_viewer"
