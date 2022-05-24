module.exports = {
    devServer: {
      disableHostCheck: true,
      port: 3000,
      proxy: {
        '^/api': {
          target: 'http://www.smartcontractsecurity.org',
          changeOrigin: true
        },
      }
    }
  }
