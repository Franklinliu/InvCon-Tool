
startaddress="0x2bbad4421e2979fc41acbd1cc8dff467b3c98062"
flag=0
for list in $(ls ./ERC20)
do 
    echo $list 
    contracts=$(cat ./ERC20/$list | cut -d ',' -f1)
    # echo $contracts
    for contract in ${contracts[@]}
    do
        if [ $contract == $startaddress ]
        then 
            flag=$(($flag+1))
            echo $flag 
            echo $contract
            continue 
        fi 
        if [ $flag != 0 ] && [[ $contract == 0x* ]]
        then 
            echo $contract 
            invcon  --eth_address $contract --workspace ./Experiment/ERC20  
        fi 
    done 
done 