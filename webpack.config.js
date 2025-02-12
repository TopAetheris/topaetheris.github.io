const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js', // 入口文件
  output: {
    filename: '[name].[contenthash].js', // 生成带有哈希值的输出文件名
    path: path.resolve(__dirname, 'dist'), // 输出文件夹
  },
  module: {
    rules: [
      {
        test: /\.css$/, // 处理 CSS 文件
        use: ['style-loader', 'css-loader'], // 使用 style-loader 和 css-loader
      },
      {
        test: /\.(jpg|png|gif|svg)$/, // 处理图片文件
        use: ['file-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html', // 使用你的 HTML 模板文件
    }),
  ],
  mode: 'production', // 设置为生产模式
};
