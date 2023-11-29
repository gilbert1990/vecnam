const HDWalletProvider = require("@truffle/hdwallet-provider");

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id:'*', // Match any network ID
    },
    sepolia: {
      provider: function() {
        return new HDWalletProvider(
          "curve host sting urban love include enemy aim evolve surround scheme fence",
          "https://sepolia.infura.io/v3/157cef702c8741df88f4b8f1b2068ef6"
        );
      },
      network_id: 11155111,
      networkCheckTimeout: 5000000,    
      timeoutBlocks: 900,
      gasPrice: 50000000000
    },
  },
  compilers: {
    solc: {
      version: "0.8.13", 
      optimizer:{
        enabled:true,
        runs:200
      }
    },
  },
};
