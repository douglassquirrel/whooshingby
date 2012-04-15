log() {
  echo "*** $1"
}

log "Running whooshingby installation script."
if [ "$(id -u)" != "0" ]; then
   log "!!! Must be run as root. Exiting."
   exit 1
fi

log "Installing Apache."
  apt-get -y install apache2
log "Installing PHP."
  apt-get -y install libapache2-mod-php5
log "Installing PHPUnit." 
  apt-get -y install php-pear
  apt-get -y upgrade php-pear
  pear channel-discover pear.phpunit.de
  pear channel-discover pear.symfony-project.com
  pear channel-discover components.ez.no
  pear update-channels
  pear upgrade-all
  pear install --alldeps phpunit/PHPUnit
#log "Installing whooshingby." 
#  sed -e "s:@WB_ROOT:$WB_ROOT:g" -e "s:@HOST:$HOST:g" $WB_ROOT/install/whooshingby.conf | sudo tee /etc/apache2/sites-available/whooshingby.conf
#  a2ensite whooshingby.conf
#  /etc/init.d/apache2 reload
