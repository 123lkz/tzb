module.exports = {
  parser: '@typescript-eslint/parser',
  extends: ['plugin:@typescript-eslint/recommended', 'plugin:prettier/recommended'],
  parserOptions: { ecmaVersion: 2018, sourceType: 'module' },
  rules: {
    /* 主要使用 prettier 来进行 format */
    'space-before-function-paren': [
      // 在 function 定义左括号之前不允许任何空格后跟
      'error',
      {
        anonymous: 'always',
        named: 'never',
        asyncArrow: 'always'
      }
    ],
    'no-trailing-spaces': 'error', // 一行结束后面不要有空格
    'no-multiple-empty-lines': [
      'warn',
      {
        max: 1
      }
    ],
    'padding-line-between-statements': [
      'error',
      {
        blankLine: 'always',
        prev: 'function',
        next: 'function'
      }
    ],
    'keyword-spacing': [
      'error',
      {
        before: true,
        after: true
      }
    ],
    /* code lint 代码规范校验 */
    'import/no-named-as-default': 'off', // export default 使用 import 引入的时候自定义一个 name 即可
    'n/no-callback-literal': 'off', // callback literal
    'import/named': 'off', // import 引入方法，针对 echarts 和 lodash es 引入
    'no-unused-expressions': 'warn', // 三目运算 warn 无用运行，解决：做好使用 if
    'no-inner-declarations': 'off',
    'no-var': 'error', // 使用 let 或 const 而不是 var
    eqeqeq: ['error', 'always'], // 使用 === 和 !==
    'no-else-return': 'error', // 如果 if 语句里面有 return,后面不能跟 else 语句
    /* typescript lint */
    '@typescript-eslint/no-explicit-any': 'off', // ts any 类型的使用
    '@typescript-eslint/no-var-requires': 'off', // monorepo 项目中保存 import/require 两种引用
    'no-async-promise-executor': 'off',
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/no-unused-vars': 'off',
    '@typescript-eslint/no-unsafe-declaration-merging': 'off',
    quotes: ['error', 'single', { avoidEscape: true }],
    semi: ['error', 'never'],
    'prettier/prettier': [
      'error',
      {
        singleQuote: true,
        semi: false
      }
    ]
  }
}
