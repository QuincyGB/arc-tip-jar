// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ArcTipJar
/// @notice A tiny tipping jar built for Arc mainnet, where the gas token IS USDC.
///         Tips are sent as native value (USDC, 18 decimals on Arc) with an
///         on-chain memo. No custody: value flows straight to the recipient.
contract ArcTipJar {
    event Tip(
        address indexed from,
        address indexed to,
        uint256 amount,
        string memo
    );

    mapping(address => uint256) public totalReceived;
    mapping(address => uint256) public tipCount;
    uint256 public totalTips;

    /// @notice Tip `to` some native USDC with a memo. Value goes directly to `to`.
    /// @param to The recipient of the tip.
    /// @param memo A short public message attached to the tip (e.g. "great thread!").
    function tip(address payable to, string calldata memo) external payable {
        require(msg.value > 0, "ArcTipJar: tip must be > 0");
        require(to != address(0), "ArcTipJar: no zero address");
        require(bytes(memo).length <= 280, "ArcTipJar: memo too long");

        totalReceived[to] += msg.value;
        tipCount[to] += 1;
        totalTips += 1;

        (bool ok, ) = to.call{value: msg.value}("");
        require(ok, "ArcTipJar: transfer failed");

        emit Tip(msg.sender, to, msg.value, memo);
    }
}
