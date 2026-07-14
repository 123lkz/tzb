const path = require('path')
const { generateApi } = require('swagger-typescript-api')
const prettierSettings = require('./.prettierrc.cjs')

async function generate(prefix, options) {
  return generateApi({
    httpClientType: 'axios', // or "fetch"
    url: `https://tte-api.smartedu.work/vocational_edu_api/api/doc-json`,
    output: path.join(process.cwd(), './api'),
    templates: path.join(process.cwd(), './api/templates'),
    prettier: { ...prettierSettings, parser: 'typescript' },
    codeGenConstructs: () => ({
      Keyword: {
        Object: 'any'
      }
    }),
    generateResponses: true,
    extractRequestParams: false,
    extractRequestBody: false,
    moduleNameIndex: 1,
    defaultResponseAsSuccess: true,
    hooks: {
      onCreateRouteName: (routeNameInfo) => {
        routeNameInfo.usage = routeNameInfo.usage.replace(/.*Controller/, '')
        routeNameInfo.original = routeNameInfo.original.replace(/.*Controller/, '')
        return routeNameInfo
      },
      onPrepareConfig: (c) => {
        c.routes.combined.forEach((module) => {
          let urlPrefix = prefix
          module.routes.forEach((route) => {
            const path = route.request.path
            if (path) {
              route.request.path = route.request.path.replace(prefix, '')
              const parts = route.request.path.split('/').filter((p) => p)
              if (parts.length) {
                urlPrefix = '/' + parts[0]
              }
            }
          })
          module.urlPrefix = urlPrefix
        })
      }
    },
    ...options
  })
}

;(async () => {
  await generate('/zjapi', {
    name: 'api.ts'
  })
})()
