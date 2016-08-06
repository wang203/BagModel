# awk '{print $1;}' america2007 | awk -F '/' '{print $NF;}' | awk -F '_' '{print $1;}' > america2007.pid
# awk '{print $1;}' america2008 | awk -F '/' '{print $NF;}' | awk -F '_' '{print $1;}' > america2008.pid
# awk '{print $1;}' america2009 | awk -F '/' '{print $NF;}' | awk -F '_' '{print $1;}' > america2009.pid
# awk '{print $1;}' america2010 | awk -F '/' '{print $NF;}' | awk -F '_' '{print $1;}' > america2010.pid
# 
# 
# paste -d ' ' america2007.pid <(awk '{print $1;}' america2007) | sort -k1 | paste -d ' ' - <(awk '{$1=""; print;}' america2007.piduiddaybinsort) > america2007.pidurluiddaybin
# paste -d ' ' america2008.pid <(awk '{print $1;}' america2008) | sort -k1  | paste -d ' ' - <(awk '{$1=""; print;}' america2008.piduiddaybinsort) > america2008.pidurluiddaybin
# paste -d ' ' america2009.pid <(awk '{print $1;}' america2009) | sort -k1  | paste -d ' ' - <(awk '{$1=""; print;}' america2009.piduiddaybinsort) > america2009.pidurluiddaybin
# paste -d ' ' america2010.pid <(awk '{print $1;}' america2010) | sort -k1  | paste -d ' ' - <(awk '{$1=""; print;}' america2010.piduiddaybinsort) > america2010.pidurluiddaybin
# rm *.pid
# rm *.pidurl

awk '{print $3"_"$4","$1;}' america2010.piduiddaybinsort > america2010.daybinpid4join
# awk '{print $1"_"$2","$3;}' gtsnowall > gtsnowall4join
python joindaybin.py

# cp pidgt.2010 pidgt.2010cp
# sed -i -e 's/_/ /g' pidgt.2010
# sed -i -e 's/,/ /g' pidgt.2010
awk '$4!="" {print $3" "$1" "$2" "$4;}' pidgt.2010 | sort > piddaybingt.2010
