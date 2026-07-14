;(async () => {
  const fs = require('fs')
  const { exec } = require('child_process')
  const version = require('./version.json')

  const branchName = await getBranchName()
  if (branchName === 'main') {
    // 如果是 main 分支，检查有无其他分支提交
    version.build = parseInt(await getCommitsCount()) + 1
    version.date = new Date().toISOString()
    fs.writeFileSync('./version.json', JSON.stringify(version))
    // await addBuildFileToGit('./version.json')
  }

  function getBranchName() {
    return new Promise((resolve, reject) => {
      exec('git rev-parse --abbrev-ref HEAD', (e, stdout, stderr) => {
        return resolve(stdout.trim())
      })
    })
  }

  function getCommitsCount() {
    return new Promise((resolve, reject) => {
      exec('git rev-list --count HEAD', (e, stdout, stderr) => {
        return resolve(stdout.trim())
      })
    })
  }

  function addBuildFileToGit(filename) {
    return new Promise((resolve, reject) => {
      exec('git add ' + filename, (e, stdout, stderr) => {
        if (e) return reject(e)
        if (stderr) return reject(stderr)
        return resolve(stdout)
      })
    })
  }
})()
