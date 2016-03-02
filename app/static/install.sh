#!/bin/env bash

apt-get update && apt-get install -y git puppet

git clone https://github.com/varesa/puppet_nastori_system.git /etc/puppet/modules/nastori_system/
git clone https://github.com/varesa/puppet_nastori_viewer.git /etc/puppet/modules/nastori_viewer/
git clone https://github.com/varesa/puppet_nastori_connection.git /etc/puppet/modules/nastori_connection/

puppet module install puppetlabs-inifile
puppet module install puppetlabs-vcsrepo

puppet apply -e "include nastori_system"
puppet apply -e "include nastori_viewer"
