module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
   publicPath: process.env.NODE_ENV === 'production' ? '/static/dist/' : 'http://localhost:8080',
   outputDir: '../static/dist',
   indexPath: '../../templates/base-vue.html',

   chainWebpack: config => {
     config.devServer
       .public('http://localhost:8080')
       .hotOnly(true)
       .headers({'Access-Control-Allow-Origin': '*'})
       .writeToDisk(filePath => filePath.endsWith('index.html'))
   }
}
