const Keys = artifacts.require("MemberKeys.sol");
const Tree = artifacts.require("TreeKeys.sol")

module.exports = function (deployer) {
  deployer.deploy(Keys);
  deployer.deploy(Tree);
};
