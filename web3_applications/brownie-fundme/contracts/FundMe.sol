// SPDX-License-Identifier: MIT


pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe{

    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUsd = 50 * 10 ** 18;
        require(getConversioinRate(msg.value)>=minimumUsd, "You need to spend more ETH");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }


    function getVersion() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256){
        // get the latest eth price
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversioinRate(uint256 ethAmount) public view returns(uint256){
        // get the eth amount in usd that was sent to the user
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }



    modifier onlyOwner{
        require(msg.sender == owner);
        _;

    }


    function withdraw() payable onlyOwner public  {
        // withdraw the money
        msg.sender.transfer(address(this).balance);

        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;}

        funders = new address[](0);
    }



}

