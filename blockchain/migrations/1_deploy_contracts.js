const ManagementUser = artifacts.require("ManagementUser");
/* Permite que otros lenguejes puedan aceder */
module.exports = function (deployer) {
  deployer.deploy(ManagementUser);
};
