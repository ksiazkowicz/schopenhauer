const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');


module.exports = {
    entry: {
        "main": ['bootstrap-loader', './theme/ts/application.ts',],
        "minimal": "bootstrap-loader/lib/bootstrap.loader?extractStyles&configFilePath=../../../theme/.bootstraprc-minimal!bootstrap-loader/no-op.js", // minimal bundle with just the stuff to display the page properly before it fully loads
    },
    output: {
        path: path.resolve('./theme/bundles/'),
        publicPath: '/static/bundles/',
        filename: "[name]-[hash].js"
    },
    resolve: {
        // Add '.ts' and '.tsx' as a resolvable extension.
        extensions: [".webpack.js", ".web.js", ".ts", ".tsx", ".js"]
    },
    module: {
        rules: [{
            test: /\.scss$/,
            use: ["style-loader", "css-loader", "sass-loader"]
        }, {
            test: /\.css$/,
            use: ["style-loader", "css-loader",]
        }, {
            test: /\.tsx?$/,
            use: 'ts-loader',
            exclude: /node_modules/
        }, {
            test: /\.(png|svg|jpg|jpeg|gif)$/,
            use: 'file-loader'
        }, {
            test: /\.(woff|woff2|eot|ttf|otf)$/,
            use: [
                'file-loader'
            ]
        }]
    },
    externals: {
        'django': 'django'
    },
    plugins: [
        new ExtractTextPlugin({ filename: '[name].css', allChunks: true }),
        new CleanWebpackPlugin(['theme/bundles']),
        new BundleTracker({ filename: './webpack-stats.json' }),
        new webpack.ProvidePlugin({
            '$': 'jquery',
            'jQuery': 'jquery',
            'window.jQuery': 'jquery',
        })
    ]
};