const KeysSmartContract = artifacts.require('MemberKeys.sol')

contract('MemberKeys', () => {
    it('[!]Enregistrement d\'un noeud', async() => {
        const keysART = await KeysSmartContract.deployed();
        const ID = 'ID001';
        const key = '0234654654';
        const numberofkeys = 1;
        await keysART.Register(ID, key, numberofkeys);
        const result = await keysART.isRegistred(ID);
        //console.log(KeysSmartContract.address);//can be deleated
        assert(result === true);
    });

    it('[!]Récupération des clés des membres', async() => {
        const keysART = await KeysSmartContract.deployed();
        const ID = 'ID001';
        const key = '0234654654';
        const numberofkeys = 1;

        const ID2 = 'ID002';
        const key2 = '023465465222';
        const numberofkeys2 = 1;

        await keysART.Register(ID, key, numberofkeys);
        await keysART.Register(ID2, key2, numberofkeys)

        const test = [ID, ID2]
        const result = await keysART.GetMemberKey(test, 2);
        //console.log(result);//can be deleated
        assert((result[0] === key) && (result[1] === key2));
    });

    it('[!]Récupération du nombre de clés éphémeres restantes', async() => {
        const keysART = await KeysSmartContract.deployed();
        const ID = 'ID001';
        const key = '0234654654';
        const numberofkeys = 1;
        await keysART.Register(ID, key, numberofkeys);
        const result = await keysART.GetNumberOfKeysLeft(ID);
        //console.log(result.words[0]);//can be deleated
        assert(result.words[0] === numberofkeys);
    });

    it('[!]Mise à jour du nombre de clés éphémeres restantes', async() => {
        const keysART = await KeysSmartContract.deployed();
        const ID = 'ID001';
        const key = '0234654654';
        const numberofkeys = 1;
        await keysART.Register(ID, key, numberofkeys);
        const toset = 4;
        await keysART.SetNumberOfKeys(ID, toset);
        const result = await keysART.GetNumberOfKeysLeft(ID);
        //console.log(result.words[0]);//can be deleated
        assert(result.words[0] === toset);
    });
});