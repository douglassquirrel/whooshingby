ssh -t $WB_USER@whooshingby-vm "sudo apt-get -y update
sudo apt-get -y install unzip
sudo mkdir $WB_ROOT
sudo chown $WB_USER $WB_ROOT
wget -O $WB_ROOT/whooshingby.zip https://github.com/douglassquirrel/whooshingby/zipball/master
unzip $WB_ROOT/whooshingby.zip -d $WB_ROOT
mv $WB_ROOT/*whooshingby*/* $WB_ROOT
rm -rf $WB_ROOT/whooshingby.zip $WB_ROOT/*-whooshingby-*
sudo WB_ROOT=$WB_ROOT HOST=$HOST $WB_ROOT/install/install.sh"
