module.exports = {
  // tab 的宽度 2 个字符
  tabWidth: 2,
  // 禁止使用 tab 代替空格
  useTabs: false,
  // 结尾不使用分号
  semi: false,
  // 行结尾形式 mac 和 linux 是 \n  windows 是 \r\n
  endOfLine: 'auto',
  // 打印宽度，超过后，会将属性换行
  printWidth: 120,
  // 禁止使用尾随逗号,对象和数组最后一个逗号去掉
  trailingComma: 'none',
  // 在对象字面量中的括号之间添加空格
  bracketSpacing: true,
  // 使用单引号而不是双引号来定义字符串
  singleQuote: true,
  // 当箭头函数只有一个参数时，带着参数前后的括号
  arrowParens: 'always',
  // vue 的 script 和 style 标签中间的内容缩进
  vueIndentScriptAndStyle: false,
  // 将 > 多行 HTML（HTML、JSX、Vue）元素放在最后一行的末尾，而不是单独放在下一行（不适用于自闭合元素
  bracketSameLine: false,
  htmlWhitespaceSensitivity: 'ignore',
  // 根据文件后缀单独定义
  overrides: []
}
