const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}

const env = process.env.NODE_ENV || "develop";
const parsedEnv = DotEnv.config({
  path: resolve(`.env.${env}`),
}).parsed;

module.exports = function () {
  return parsedEnv;
};
