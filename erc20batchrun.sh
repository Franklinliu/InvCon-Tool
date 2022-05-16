

for list in $(ls ./ERC20)
do 
    echo $list 
    contracts=$(cat ./ERC20/$list | cut -d ',' -f1)
    # echo $contracts
    for contract in ${contracts[@]}
    do
        if [[ $contract == 0x* ]]
        then 
            echo $contract 
            invcon  --eth_address $contract --cached  --workspace ./Experiment/ERC20  
        fi 
    done 
done 