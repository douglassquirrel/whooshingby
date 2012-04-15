log() {
  echo "*** $1"
}

log "Running whooshingby installation script."
if [ "$(id -u)" != "0" ]; then
   log "!!! Must be run as root. Exiting."
   exit 1
fi

log "Installing Apache."
  apt-get install apache2
log "Installing PHP."
  apt-get install libapache2-mod-php5
log "Installing PHPUnit." 
  apt-get install pear
  apt-get upgrade pear
  pear channel-discover pear.phpunit.de
  pear channel-discover pear.symfony-project.com
  pear channel-discover components.ez.no
  pear update-channels
  pear upgrade-all
  pear install --alldeps phpunit/PHPUnit
#log "Installing whooshingby." 
#  mkdir $WB_ROOT
#  cd $WB_ROOT/..
#  git clone git@github.com:douglassquirrel/whooshingby.git
#  chown -R $USER $WB_ROOT
#  sed -e "s:@WB_ROOT:$WB_ROOT:g" -e "s:@HOST:$HOST:g" $WB_ROOT/install/whooshingby.conf | sudo tee /etc/apache2/sites-available/whooshingby.conf
#  a2ensite whooshingby.conf
#  /etc/init.d/apache2 reload

