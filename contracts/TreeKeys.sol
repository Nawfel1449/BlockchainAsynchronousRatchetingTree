pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT

contract TreeKeys {
    struct ART_Tree {
        uint   SetupKey;
        uint [] tree;    
    }
    struct Update {
        uint MembrePublicKey;
        uint [] Path_To_Root;
    }

    struct Groupe {
        string TreeID;
        uint   index;
        //uint   KeyUsed;
    }

    mapping (string => ART_Tree) ART_Trees;//maps tree ID to its info
    mapping (string => Update []) Updates; //maps tree ID to its update
    mapping (string => Groupe []) MemberGroups; //maps Id of a member to his groupe

    function SetArtTree(string memory _Tree_ID, uint _SetupKey, uint [] memory _Tree ) public{
        ART_Trees[_Tree_ID] = ART_Tree(_SetupKey, _Tree);
    }

    function GetArtTree(string memory _Tree_ID) view public returns (uint [] memory){
        return ART_Trees[_Tree_ID].tree;
    }

    function GetSetupKey(string memory _Tree_ID) view public returns (uint){
        return ART_Trees[_Tree_ID].SetupKey;
    }

    function SetUpdate(string memory _Tree_ID, uint [] memory _Path_To_Root, uint _MembrePublicKey) public{
        Update memory update = Update(_MembrePublicKey, _Path_To_Root);
        Updates[_Tree_ID].push(update);
    }

    function GetUpdates(string memory _Tree_ID) view public returns (Update [] memory){
        return Updates[_Tree_ID];
    }

    function sayHello() public pure returns (string memory) {
        return '[!] This smart contract is working';
    }
}