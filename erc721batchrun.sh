

for list in $(ls ./ERC721)
do 
    echo $list 
    contracts=$(cat ./ERC721/$list | cut -d ',' -f1)
    # echo $contracts
    for contract in ${contracts[@]}
    do
        if [[ $contract == 0x* ]]
        then 
            echo $contract 
            invcon  --eth_address $contract --cached  --workspace ./Experiment/ERC721  
        fi 
    done 
done 