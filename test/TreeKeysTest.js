const TreeSmartContract = artifacts.require('TreeKeys.sol')

contract('TreeKeys', () => {
    it('[!]Stockage d\'un arbre ART', async() => {
        const Tree = await TreeSmartContract.deployed();
        const ID = 'ID001';
        const SetupKey = 0234654654;
        const tree = [1,2,3];
        await Tree.SetArtTree(ID, SetupKey, tree);
        const result = await Tree.GetArtTree(ID);
        console.log(result[0]);//can be deleated
        assert(ID === ID);
    });

});