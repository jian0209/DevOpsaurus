const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}

const LOCAL = false;
const DotEnv = require("dotenv");
const parsedEnv = LOCAL
  ? DotEnv.config({
      path: resolve(".env.local"),
    }).parsed
  : DotEnv.config({
      path: resolve(`.env.${process.env.NODE_ENV}`),
    }).parsed;

module.exports = function () {
  return parsedEnv;
};
