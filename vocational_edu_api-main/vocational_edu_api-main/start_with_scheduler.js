// 启动应用并测试定时任务
const { spawn } = require('child_process')
const axios = require('axios')

const BASE_URL = 'http://localhost:8569/zjapi'

// 启动应用
console.log('🚀 启动应用...')
const app = spawn('npm', ['run', 'dev'], {
  stdio: 'pipe',
  shell: true
})

let appStarted = false

// 监听应用输出
app.stdout.on('data', (data) => {
  const output = data.toString()
  console.log(output)

  // 检查应用是否启动完成
  if (output.includes('Application is running on') || output.includes('Server is running')) {
    if (!appStarted) {
      appStarted = true
      console.log('\n✅ 应用启动成功！')

      // 等待2秒后开始测试
      setTimeout(() => {
        testScheduler()
      }, 2000)
    }
  }
})

app.stderr.on('data', (data) => {
  console.error('应用错误:', data.toString())
})

app.on('close', (code) => {
  console.log(`应用退出，代码: ${code}`)
})

// 测试定时任务功能
async function testScheduler() {
  console.log('\n🧪 开始测试定时任务功能...')

  try {
    // 1. 检查缓存健康状态
    console.log('\n📊 检查缓存健康状态...')
    const healthResponse = await axios.get(`${BASE_URL}/position/screen/cache/health`)
    console.log('缓存健康状态:', JSON.stringify(healthResponse.data.health, null, 2))

    // 2. 手动触发预热缓存
    console.log('\n🔥 手动触发预热缓存...')
    const preWarmResponse = await axios.post(`${BASE_URL}/position/screen/cache/prewarm`, {})
    console.log('预热结果:', preWarmResponse.data.message)

    // 3. 检查缓存统计
    console.log('\n📈 检查缓存统计...')
    const statsResponse = await axios.get(`${BASE_URL}/position/screen/cache/stats`)
    console.log('缓存统计:', JSON.stringify(statsResponse.data.stats, null, 2))

    // 4. 测试接口响应速度
    console.log('\n⚡ 测试接口响应速度...')
    const testParams = { dateType: 'month', caliberType: 'all' }

    const start = Date.now()
    const response = await axios.get(`${BASE_URL}/position/screen/trend/data`, {
      params: testParams
    })
    const duration = Date.now() - start
    console.log(`接口响应时间: ${duration}ms`)

    if (duration < 1000) {
      console.log('✅ 缓存工作正常，响应时间很快！')
    } else {
      console.log('⚠️ 响应时间较慢，可能缓存未生效')
    }

    console.log('\n🎉 定时任务测试完成！')
    console.log('\n📅 定时任务时间表：')
    console.log('  - 每天 01:30 - 清理过期缓存')
    console.log('  - 每天 01:45 - 清理base缓存')
    console.log('  - 每天 02:00 - 预热缓存')
    console.log('  - 每天 14:00 - 清理昨天的大屏缓存')
    console.log('  - 每小时 - 检查缓存统计')
    console.log('  - 每周日 04:00 - 完全清理缓存')

    console.log('\n💡 定时任务已启用，应用将在后台运行...')
    console.log('💡 按 Ctrl+C 停止应用')
  } catch (error) {
    console.error('❌ 测试失败:', error.message)
    if (error.response) {
      console.error('响应数据:', error.response.data)
    }
  }
}

// 优雅关闭
process.on('SIGINT', () => {
  console.log('\n🛑 正在关闭应用...')
  app.kill('SIGINT')
  process.exit(0)
})

process.on('SIGTERM', () => {
  console.log('\n🛑 正在关闭应用...')
  app.kill('SIGTERM')
  process.exit(0)
})
