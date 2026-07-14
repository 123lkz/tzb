# 前程无忧爬虫 - Selenium版本

这是前程无忧Step5爬虫的Selenium版本实现，功能与Playwright版本完全相同。

## 主要特性

- 使用Selenium WebDriver进行网页自动化
- 支持分页爬取（1-50页）
- 智能反爬虫策略
- 自动验证码检测和处理
- 会话轮换机制
- 数据去重和增量更新
- 详细的日志记录

## 安装依赖

```bash
pip install -r requirements_selenium.txt
```

## 环境要求

- Python 3.8+
- Chrome浏览器
- ChromeDriver（可通过webdriver-manager自动管理）

## 使用方法

### 基本使用

```python
from qcwy_spider_step5_selenium import QCWYSpiderStep5Selenium

# 创建爬虫实例
spider = QCWYSpiderStep5Selenium()

# 运行爬虫（启用分页，爬取1-50页）
spider.run(enable_pagination=True, page_range=(1, 50))

# 单页爬取模式
spider.run(enable_pagination=False)
```

### 自定义配置

```python
spider = QCWYSpiderStep5Selenium()

# 自定义页面范围
spider.run(enable_pagination=True, page_range=(1, 10))  # 只爬取前10页

# 修改延迟时间
spider.delay_range = (2, 5)  # 随机延迟2-5秒

# 修改会话限制
spider.max_urls_per_session = 10  # 每个会话最多处理10个URL
```

## 配置说明

### MongoDB配置
- 源数据集合：`qcwy_step2_urls_part1`
- 目标集合：`qcwy_step2_job_raw_part1`
- 日志集合：`qcwy_step2_urls_202505_log_part1`

### 反爬虫配置
- 随机User-Agent
- 随机浏览器指纹
- 模拟人类行为
- 智能延迟策略
- 代理支持（可选）

### 数据过滤
- 自动过滤已爬取的URL
- 日期过滤（默认只爬取2025年6月1日之后的数据）
- 数据去重（基于jobId）

## 与Playwright版本的主要区别

1. **网络监听方式**：
   - Playwright：使用事件监听器实时捕获XHR请求
   - Selenium：使用Chrome DevTools Protocol获取网络日志，实现类似的XHR监听功能

2. **数据提取**：
   - Playwright：主要从网络请求中获取JSON数据
   - Selenium：优先从XHR监听获取，失败时从页面元素提取

3. **异步处理**：
   - Playwright：原生支持异步操作
   - Selenium：使用同步操作，但保持相同的逻辑流程

4. **浏览器管理**：
   - Playwright：自动管理浏览器进程
   - Selenium：需要手动管理ChromeDriver

## XHR监听功能

Selenium版本实现了与Playwright版本相同的XHR监听机制：

- `setup_xhr_listener()`: 设置XHR监听器
- `on_response(page_num)`: 监听指定页码的XHR响应
- 自动过滤`api/job/search-pc`请求
- 支持分页数据的实时监听
- 失败时自动回退到页面元素提取

## 注意事项

1. 确保Chrome浏览器已安装
2. 首次运行时会自动下载ChromeDriver
3. 建议在有头模式下运行以便调试
4. 如遇到验证码，爬虫会自动重启浏览器
5. 网络监听功能需要Chrome DevTools Protocol支持

## 日志文件

爬虫运行时会生成日志文件：
- 文件名格式：`qcwy_spider_step5_selenium_YYYYMMDD_HHMMSS.log`
- 包含详细的运行信息和错误日志

## 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   ```bash
   pip install webdriver-manager --upgrade
   ```

2. **XHR监听失败**
   - 检查Chrome版本是否支持DevTools Protocol
   - 运行 `python test_xhr_listener.py` 测试XHR监听功能
   - 自动回退到页面元素提取作为备选方案

3. **验证码频繁出现**
   - 增加延迟时间
   - 减少每个会话的URL数量
   - 考虑使用代理

4. **内存占用过高**
   - 定期重启浏览器
   - 减少并发处理数量

5. **Selenium连接错误**
   ```bash
   # 安装依赖
   pip install -r requirements_selenium.txt
   
   # 运行简单测试
   python simple_test.py
   ```

6. **XHR监听功能不可用**
   - 这是正常现象，爬虫会自动回退到页面元素提取
   - 不影响主要功能，但建议运行 `python test_xhr_listener.py` 进行诊断

7. **Chrome浏览器警告信息**
   - 已添加配置来抑制Chrome内部警告
   - 运行 `python quick_test.py` 验证修复效果
   - 这些警告不影响爬虫功能，可以忽略

### 调试步骤

1. 首先运行快速测试（验证Chrome警告修复）：
   ```bash
   python quick_test.py
   ```

2. 运行基本功能测试：
   ```bash
   python simple_test.py
   ```

3. 测试XHR监听功能：
   ```bash
   python test_xhr_listener.py
   ```

4. 如果测试通过，运行完整爬虫：
   ```bash
   python run_selenium_example.py
   ```

5. 查看日志文件了解详细错误信息

## 性能优化建议

1. 根据网络环境调整延迟时间
2. 合理设置会话轮换频率
3. 监控内存使用情况
4. 定期清理日志文件

## 模拟人类行为修复

### 问题描述
运行爬虫时可能出现以下错误：
```
WARNING - 模拟人类行为失败: Message: move target out of bounds
```

这是因为鼠标移动操作超出了页面边界导致的。

### 解决方案
1. **创建了安全的模拟人类行为模块** (`safe_human_behavior.py`)
2. **使用JavaScript滚动替代鼠标移动**，避免边界问题
3. **添加边界检查和异常处理**
4. **提供三种行为模式选择**：
   - `safe_simulate_human_behavior()`: 完整的人类行为模拟
   - `minimal_human_behavior()`: 最小化行为（只滚动）
   - `no_human_behavior()`: 无行为模拟（用于调试）

### 测试方法
```bash
# 测试模拟人类行为功能
python test_human_behavior.py
```

### 自动修复
爬虫已自动集成安全模块，如果出现边界错误会自动回退到简化行为模式，确保爬虫正常运行。

## 分页功能修复

### 问题描述
运行爬虫时可能出现以下错误：
```
ERROR - goto_next_page 点击下一页失败: Message: 
```

这是因为分页按钮的CSS选择器不正确或按钮还没有加载完成导致的。

### 解决方案
1. **基于实际HTML结构的下一页按钮查找**：
   - 使用精确的CSS选择器：`.el-pagination .btn-next:not([disabled])`
   - 支持父容器选择器：`.pageation .btn-next:not([disabled])`
   - 添加按钮状态检查（显示和启用状态）
   - 滚动到按钮位置确保可见性
   - 添加JavaScript点击作为备选方案

2. **基于实际HTML结构的页面跳转功能**：
   - 使用精确的输入框选择器：`#jump_page` 和 `input.mytxt`
   - 使用精确的跳转按钮选择器：`.jumpPage` 和 `span.jumpPage`
   - 支持回车键跳转
   - 添加JavaScript跳转作为备选方案
   - 增强页面加载等待机制

3. **错误处理机制**：
   - 自动检测是否到达最后一页（按钮被禁用）
   - 提供详细的调试日志
   - 多重备选方案确保功能稳定

### 测试方法
```bash
# 测试分页功能修复
python test_pagination_fix.py
```

### 修复内容
- `goto_next_page()`: 基于实际HTML结构的下一页点击功能
- `jump_to_page()`: 基于实际HTML结构的页面跳转功能
- `check_pagination_exists()`: 基于实际HTML结构的分页检查
- `wait_for_page_load()`: 参考Playwright的页面等待逻辑
- 使用精确的CSS选择器匹配实际页面结构
- 增加JavaScript备选方案
- 改进错误处理和日志记录

## 页面等待逻辑优化（参考Playwright）

### 问题描述
原来的等待逻辑过于复杂，参考Playwright版本的简洁实现，使用类似 `wait_until='networkidle'` 的等待策略。

### 解决方案
1. **参考Playwright的等待策略**：
   - 使用 `wait_for_page_load()` 替代复杂的等待逻辑
   - 模拟 `wait_until='networkidle'` 的行为
   - 等待页面基本元素加载 + 网络空闲

2. **简化的等待机制**：
   - 等待职位列表容器出现
   - 检查职位卡片是否包含必要信息
   - 额外等待1秒确保网络空闲
   - 检测加载状态和空数据提示

3. **灵活的超时设置**：
   - 首次加载：30秒超时
   - 分页加载：15秒超时
   - 可配置的超时参数

### 测试方法
```bash
# 测试等待逻辑优化
python test_wait_logic.py
```

### 实际HTML结构支持
根据您提供的HTML结构，爬虫现在支持：
```html
<div class="pageation">
  <div class="el-pagination is-background">
    <button class="btn-next">下一页</button>
  </div>
  <input id="jump_page" class="mytxt" type="number">
  <span class="jumpPage">跳转</span>
</div>
``` 