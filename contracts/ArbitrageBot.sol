// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IUniswap {
    function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);
    function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
}

interface ISushiswap {
    function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);
    function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
}

contract ArbitrageBot {
    address owner;
    IERC20 public token;
    IUniswap uniswap;
    ISushiswap sushiswap;
    
    constructor(address _token, address _uniswap, address _sushiswap) {
        owner = msg.sender;
        token = IERC20(_token);
        uniswap = IUniswap(_uniswap);
        sushiswap = ISushiswap(_sushiswap);
    }

    function arbitrage(uint amountIn, address[] calldata path, uint deadline) external {
        require(msg.sender == owner, "Only owner can initiate arbitrage");

        uint[] memory uniswapAmounts = uniswap.getAmountsOut(amountIn, path);
        uint[] memory sushiswapAmounts = sushiswap.getAmountsOut(amountIn, path);

        require(uniswapAmounts[uniswapAmounts.length-1] > sushiswapAmounts[sushiswapAmounts.length-1], "No arbitrage opportunity");

        token.approve(address(uniswap), amountIn);
        uniswap.swapExactTokensForTokens(amountIn, sushiswapAmounts[sushiswapAmounts.length-1], path, address(this), deadline);

        token.approve(address(sushiswap), uniswapAmounts[uniswapAmounts.length-1]);
        sushiswap.swapExactTokensForTokens(uniswapAmounts[uniswapAmounts.length-1], 0, path, msg.sender, deadline);
    }

    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        token.transfer(owner, token.balanceOf(address(this)));
    }
}
