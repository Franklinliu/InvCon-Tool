module.exports = {
    devServer: {
      port: 3000,
      proxy: {
        '^/api': {
          target: 'http://155.69.148.241:8080',
          changeOrigin: true,
          pathRewrite: {'^/api': '/'},
        //   logLevel: 'debug' 
        },
      }
    }
  }