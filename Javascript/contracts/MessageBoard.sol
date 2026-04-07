// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract MessageBoard {
    string[] public messages;

    function addMessage(string memory _message) public {
        messages.push(_message);
    }

    function getMessage(uint _index) public view returns (string memory) {
        return messages[_index];
    }

    function getAllMessages() public view returns (string[] memory) {
        return messages;
    }
}