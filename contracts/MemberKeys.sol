pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT

contract MemberKeys {

    struct Member {
        uint Ephkeys;
        uint   NumberOfKeys;
    }

    mapping (string => bool )  RegistredMembers;//check the ID if the member is registred
    mapping (string => Member) Members; //ID points to the infos

    function Register(string memory _ID, uint Keys, uint NumberOfKeys) public {
        Member memory _new = Member(Keys, NumberOfKeys);
        RegistredMembers[_ID] = true;
        Members[_ID] = _new;
    }

    function isRegistred(string memory _ID) public view returns (bool) {
        if (!RegistredMembers[_ID]) {return false ;}
        return true ;
    }

    function GetMemberKey(string[] memory _ID, uint size) public view returns (uint[] memory){
        uint[] memory returnedkeys = new uint[](size);
        for (uint i=0; i<size; i++) {
            returnedkeys[i] = Members[_ID[i]].Ephkeys;
        }
        return returnedkeys;
    }

    function GetNumberOfKeysLeft(string memory _ID) public view returns (uint){
        return Members[_ID].NumberOfKeys;
    }

    function SetNumberOfKeys(string memory _ID, uint _NumberOfKeys) public {
        Members[_ID].NumberOfKeys = _NumberOfKeys ;
    }

    function DecNumberOfKeys(string memory _ID) public {
        uint keys = GetNumberOfKeysLeft(_ID);
        require(keys > 0);
        SetNumberOfKeys(_ID, keys -1);
    }

    function sayHello() public pure returns (string memory) {
        return '[!] This smart contract is working';
    }
}
