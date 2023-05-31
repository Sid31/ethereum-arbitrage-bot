// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/ArbitrageBot.sol";

contract TestArbitrageBot {
    ArbitrageBot bot;

    // Define the addresses
    address token = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2); // Replace with the actual token address
    address uniswap = address(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D); // Replace with the actual Uniswap address
    address sushiswap = address(0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F); // Replace with the actual Sushiswap address

    constructor() {
        // The address of the ArbitrageBot contract to be tested
        bot = new ArbitrageBot(token, uniswap, sushiswap);

        // Add checks here
        // Example: Assert.equal(bot.balanceOf(address(this)), amountIn, "Arbitrage did not increase bot's balance");
    }
    // Test the arbitrage() function
// Test the arbitrage() function
function testArbitrage() public {
    // Set an example amount and path
    uint amountIn = 1 ether; // Example amount
    address[] memory path = new address[](2); // Example path
    path[0] = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2); // Example address
    path[1] = address(0x6B175474E89094C44Da98b954EedeAC495271d0F); // Example address
    uint deadline = block.timestamp + 1 hours; // Example deadline

    // Call the arbitrage() function
    bot.arbitrage(amountIn, path, deadline);

    // Add checks here
    uint expectedBalance = amountIn; // Expected balance after the arbitrage trade
    IERC20 tokenContract = IERC20(path[0]); // assuming the token contract at path[0]
    uint actualBalance = tokenContract.balanceOf(address(bot));
    Assert.equal(actualBalance, expectedBalance, "Balance after arbitrage trade did not match expected balance");
}


    
}