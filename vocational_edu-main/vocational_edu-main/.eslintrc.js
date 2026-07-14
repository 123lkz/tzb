module.exports = {
  root: true,
  env: {
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/vue3-recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@typescript-eslint/parser",
    ecmaVersion: "latest",
    sourceType: "module",
  },
  // 自定义全局规则
  rules: {
    "space-before-function-paren": [
      "error",
      {
        anonymous: "always",
        named: "never",
        asyncArrow: "always",
      },
    ],
    "no-trailing-spaces": "error", // 一行结束后面不要有空格
    "no-multiple-empty-lines": [
      "warn",
      {
        max: 1,
      },
    ],
    "padding-line-between-statements": [
      "error",
      {
        blankLine: "always",
        prev: "function",
        next: "function",
      },
    ],
    "keyword-spacing": [
      "error",
      {
        before: true,
        after: true,
      },
    ],
    "no-var": "error", // 使用 let 或 const 而不是 var
    eqeqeq: ["error", "always"], // 使用 === 和 !==
    "no-else-return": "error",
    "import/no-named-as-default": "off", // export default 使用 import 引入的时候自定义一个 name 即可
    "n/no-callback-literal": "off", // callback literal
    "import/named": "off", // import 引入方法，针对 echarts 和 lodash es 引入
    "no-unused-expressions": "warn", // 三目运算 warn 无用运行，解决：做好使用 if
    "no-inner-declarations": "off",
    "no-else-return": "error", // 如果 if 语句里面有 return,后面不能跟 else 语句
  },
};
