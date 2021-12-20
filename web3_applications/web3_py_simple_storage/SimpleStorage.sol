pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favouriteNumber = 5;
    bool favouriteBool = true;
    string favouriteString = "String";
    int256 favouriteInteger = -5;
    address favouriteAddress = 0x26a78cd6FE2f363d138ADdBBEd469E1B491d4A9B;
    bytes32 favouriteBytes = "cat";
    // this is a comment


    struct People {
        uint256 favouriteNumber;
        string name;
    }

    //People public person = People({favouriteNumber:2, name: "JJ"});

    //array
    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    //store function
    function store (uint256 _favouriteNumber) public {
        favouriteNumber = _favouriteNumber;
    }

    //retrieval function
    function retrieve() public view returns(uint256){
        return favouriteNumber + 500;
    }

    function AddPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People({favouriteNumber: _favouriteNumber, name: _name}));
        nameToFavouriteNumber[_name] = _favouriteNumber;

    }

}


