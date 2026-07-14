import * as fs from 'fs'
import * as path from 'path'
import * as ts from 'typescript'

interface MethodData {
  className: string
  name: string
  decorators: string[]
  parameters: string[]
  body: string
  raw: string
}

function extractControllers(directory: string): MethodData[] {
  const files = getAllFiles(directory, 'controller.ts')
  const methods: MethodData[] = []

  let counter = 0
  files.forEach((file) => {
    const fileContent = fs.readFileSync(file, 'utf-8')
    const sourceFile = ts.createSourceFile(file, fileContent, ts.ScriptTarget.ESNext, true)

    ts.forEachChild(sourceFile, (node) => {
      if (ts.isClassDeclaration(node)) {
        const className = node.name?.text || 'AnonymousClass'

        node.members.forEach((member) => {
          if (ts.isMethodDeclaration(member)) {
            const methodName = member.name.getText(sourceFile)
            const decorators = member.modifiers?.map((decorator) => decorator.getText(sourceFile)) || []
            const parameters = member.parameters.map((param) => param.getText(sourceFile))
            const body = member.body?.getText(sourceFile) || ''

            const raw = member.getText(sourceFile)

            methods.push({ className, name: methodName, decorators, parameters, body, raw })

            if (!raw.includes('@Description')) {
              console.log(counter++, className, methodName)
            }
          }
        })
      }
    })
  })

  return methods
}

function getAllFiles(dir: string, ext: string, files: string[] = []): string[] {
  fs.readdirSync(dir).forEach((file) => {
    const filePath = path.join(dir, file)
    if (fs.statSync(filePath).isDirectory()) {
      getAllFiles(filePath, ext, files)
    } else if (filePath.endsWith(ext)) {
      files.push(filePath)
    }
  })
  return files
}

// 示例：提取项目中所有控制器的方法
const controllers = extractControllers('./src')

// write to file
fs.writeFileSync('controllers.json', JSON.stringify(controllers, null, 2))
