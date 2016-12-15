## cat month 2 year
## build metadata
# for year in {2007..2015}
# do
#   cat /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/snow-$year-01-snow-auto-out.txt /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/nosnow-$year-01.subsample-snow-auto-out.txt > /l/vision/wang203/bagmodel/data/metadata/data$year
#   for i in {2..9}
#   do
#     cat /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/snow-$year-0$i-snow-auto-out.txt >> /l/vision/wang203/bagmodel/data/metadata/data$year
#     cat /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/nosnow-$year-0$i.subsample-snow-auto-out.txt >> /l/vision/wang203/bagmodel/data/metadata/data$year
#   done
#   for i in {10..12}
#   do
#   cat /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/snow-$year-$i-snow-auto-out.txt /l/vision/working/eco/djcran/snow/caffe-output/snow-auto/nosnow-$year-$i.subsample-snow-auto-out.txt >> /l/vision/wang203/bagmodel/data/metadata/data$year
#   done
# done

### format metadata with binpid.py

## metadata::::::binimg -> binpid
# datapath='/l/vision/wang203/bagmodel/data/metadata'
# for year in {2007..2015}
# do
#   awk -F'/' '{print $NF;}' $datapath/binimg$year | awk -F'_' '{print $1;}' > $datapath/pid$year
#   sed 's/@N//g' $datapath/binimg$year | awk '{$4=""; print;}' | paste -d ' ' - $datapath/pid$year > $datapath/binpid$year
#   # rm $datapath/pid$year
# done

# results:::::: cut the end of last batch
# datapath='/l/vision/wang203/bagmodel/data/results'
# for year in {2007..2015}
# do
#   cat $datapath/filename$year'0' $datapath/filename$year'1' | awk -F '_' '{print $1;}' | paste -d ' ' - <(cat $datapath/cutpredi$year'0' $datapath/cutpredi$year'1') <(cat $datapath/cutprob$year'0' $datapath/cutprob$year'1') <(cat $datapath/cutfeature$year'0' $datapath/cutfeature$year'1')  > $datapath/pidfeatureprediprob$year
# done

# ## sort & join
# datapath='/l/vision/wang203/bagmodel/data'
# year=$1
# join -1 4 -2 1 <(sort -k 4 $datapath/metadata/binpid$year) <(sort -k 1 $datapath/results/pidfeatureprediprob$year) | sort -k 2 -k 4 > $datapath/datafile/pidbingtuidsortppredipprobfeature$year
# echo '0 0 0 0 0 0' >> $datapath/datafile/pidbingtuidsortppredipprobfeature$year
year=$1
path='/l/vision/wang203/bagmodel/data/datafile'
# python toppidperuser.py $year
# ##in $datapath/pidbingtuidsortppredipprobfeature2007
# ##out $datapath/toppidlist2007

# awk '{print $3;}' $path/toppidlist$year > $path/toppidgt$year

#awk '{print $2" "$3;}' $path/toppidlist$year | sort | uniq > $path/toppidbingt$year
awk '{print $2" "$4" "$3;}' $path/toppidlist$year | sort -k1 -k2 | uniq > $path/toppidusergt$year


# sed -i '1d' $path/toppiduser$year
# sed -i '1d' $path/toppidbin$year


# awk '{print $4;}' /l/vision/wang203/bagmodel/data/datafile/pidbingtuidsortppredipprobfeature2007 | uniq | wc -l
# wc -l /l/vision/wang203/bagmodel/data/datafile/toppidlist2007


#######################################################################
###########sort -k 4 $datapath/metadata/binpid$year > $datapath/metadata/binpidsort$year
###########sort -k 1 $datapath/results/pidfeatureprediprob$year > $datapath/results/pidfeatureprediprobsort$year
###### for i in {1..9}
###### do 
######   idx = 200$i'0'
######   awk -F '_' '{print $1;}' filename$idx > pid$idx
######   paste -d ' ' pid$idx feature$idx > pidfeature$idx
######   awk '{print }' combine > metadata
######   join (or join script) metadata pidfeature$idx > imgmetafeature$idx
###### 
###### 
###### --sort by user and pick first 3 for each user
