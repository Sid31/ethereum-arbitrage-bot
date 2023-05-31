const ArbitrageBot = artifacts.require("ArbitrageBot");

contract("ArbitrageBot", accounts => {
  it("should do something", async () => {
    const botInstance = await ArbitrageBot.deployed();

    // Perform some actions with botInstance and then assert the results...
    // For example, suppose we had a 'balance' function in our contract:
    const balance = await botInstance.balance();
    assert.equal(balance.valueOf(), 100, "Initial balance should be 100");
  });
});
