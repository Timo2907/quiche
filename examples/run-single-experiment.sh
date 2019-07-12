########################### Single Experiment ################################

mn --clean
echo "***** CLEANED UP MININET *****"
start=`date +%s`
echo "Start time:" $(date) "of experiment"
nohup python experiment-quiche.py
sleep 5
chmod +777 nohup.out # for esier handling of the file

#TODO update script so that the script waits until the CLIENT process is finished
#pid=$(pgrep quic_client) #for ephemeral 
#pid=$(ps -ef | grep baseline_quic_client  | grep -v xterm | grep -v grep | awk '{print $2}') #for baseline
#echo $pid
#tail --pid=$pid -f /dev/null
#sleep 5
#echo "***** EXPERIMENT RUN ENDED *****"

end=`date +%s`
runtime=$((end-start))
printf 'Execution time: %dh:%dm:%ds\n' $(($runtime/3600)) $(($runtime%3600/60)) $(($runtime%60))
pkill python
pkill -f quic

mn --clean 
echo "***** CLEANED UP MININET *****"
