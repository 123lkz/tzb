import type { PositionInfo, MatchReport, ResumeProfile, GraphData } from '~/types'

export const mockPositions: PositionInfo[] = [
  {"id":"pos-001","name":"大模型算法工程师","company":"科大讯飞","industry":"人工智能","province":"安徽","city":"合肥","salaryMin":30,"salaryMax":60,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-15","recruitNumber":5,"description":"负责大语言模型的训练、优化和部署。","responsibilities":["设计并训练大规模语言模型","优化模型推理性能","参与模型压缩和量化","跟踪前沿技术并落地"],"requiredSkills":["Python","PyTorch","Transformer","分布式训练","模型量化"],"optionalSkills":["CUDA","TensorRT","DeepSpeed","Megatron"],"tags":["大模型","深度学习","NLP","AIGC"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-002","name":"数据科学家","company":"字节跳动","industry":"大数据","province":"北京","city":"北京","salaryMin":35,"salaryMax":65,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-14","recruitNumber":3,"description":"负责海量数据分析和建模。","responsibilities":["设计A/B测试","构建用户画像","开发数据仪表盘"],"requiredSkills":["Python","SQL","机器学习","统计学","数据可视化"],"optionalSkills":["Spark","Flink","TensorFlow"],"tags":["数据分析","机器学习","数据产品"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-003","name":"AI应用开发工程师","company":"百度","industry":"人工智能","province":"北京","city":"北京","salaryMin":25,"salaryMax":50,"education":"本科及以上","experience":"1-3年","publishDate":"2026-07-13","recruitNumber":8,"description":"将AI模型能力落地为产品。","responsibilities":["大模型API应用开发","Prompt工程","RAG系统构建"],"requiredSkills":["Python","RESTful API","LLM应用开发","Prompt Engineering","向量数据库"],"optionalSkills":["LangChain","ChromaDB","FastAPI","Docker"],"tags":["AI应用","Prompt","RAG","Agent"],"platform":"智联招聘","positionUrl":""},
  {"id":"pos-004","name":"云原生开发工程师","company":"华为云","industry":"云计算","province":"广东","city":"深圳","salaryMin":25,"salaryMax":45,"education":"本科及以上","experience":"3-5年","publishDate":"2026-07-12","recruitNumber":6,"description":"负责云原生平台核心组件开发。","responsibilities":["微服务架构设计","容器编排优化","DevOps体系建设"],"requiredSkills":["Go","Kubernetes","Docker","微服务架构","CI/CD"],"optionalSkills":["Istio","Prometheus","Envoy","Helm"],"tags":["云原生","K8s","微服务","DevOps"],"platform":"前程无忧","positionUrl":""},
  {"id":"pos-005","name":"计算机视觉工程师","company":"商汤科技","industry":"人工智能","province":"上海","city":"上海","salaryMin":28,"salaryMax":55,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-11","recruitNumber":4,"description":"研究和开发计算机视觉算法。","responsibilities":["前沿CV算法研究","优化模型推理","数据pipeline构建"],"requiredSkills":["Python","PyTorch","OpenCV","图像分类","目标检测"],"optionalSkills":["TensorRT","ONNX","模型蒸馏","多模态"],"tags":["CV","深度学习","智慧城市","自动驾驶"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-006","name":"NLP算法工程师","company":"阿里巴巴","industry":"人工智能","province":"浙江","city":"杭州","salaryMin":35,"salaryMax":65,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-10","recruitNumber":4,"description":"负责自然语言处理算法的研发与优化。","responsibilities":["文本分类与情感分析","信息抽取与知识图谱构建","对话系统开发"],"requiredSkills":["Python","PyTorch","BERT","NLP","Transformers"],"optionalSkills":["TensorFlow","ONNX","FastAPI","Docker"],"tags":["NLP","深度学习","知识图谱","对话系统"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-007","name":"推荐系统工程师","company":"腾讯","industry":"大数据","province":"广东","city":"深圳","salaryMin":30,"salaryMax":55,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-09","recruitNumber":6,"description":"负责推荐系统的设计与优化。","responsibilities":["召回算法开发","排序模型优化","特征工程建设"],"requiredSkills":["Python","C++","机器学习","推荐系统","Spark"],"optionalSkills":["Flink","TensorFlow","Kubernetes"],"tags":["推荐系统","机器学习","大数据"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-008","name":"运维开发工程师","company":"腾讯云","industry":"云计算","province":"广东","city":"广州","salaryMin":20,"salaryMax":40,"education":"本科及以上","experience":"1-3年","publishDate":"2026-07-08","recruitNumber":3,"description":"负责云平台自动化运维工具开发。","responsibilities":["监控系统开发","自动化部署工具","告警平台建设"],"requiredSkills":["Python","Shell","Docker","Prometheus","Ansible"],"optionalSkills":["Go","Kubernetes","Terraform"],"tags":["运维","云原生","自动化","监控"],"platform":"智联招聘","positionUrl":""},
  {"id":"pos-009","name":"嵌入式开发工程师","company":"华为","industry":"物联网","province":"广东","city":"深圳","salaryMin":20,"salaryMax":40,"education":"本科及以上","experience":"3-5年","publishDate":"2026-07-07","recruitNumber":8,"description":"负责物联网终端设备的嵌入式软件开发。","responsibilities":["嵌入式系统开发","驱动调试与优化","通信协议实现"],"requiredSkills":["C","C++","Linux","RTOS","ARM架构"],"optionalSkills":["ZigBee","BLE","MQTT","FreeRTOS"],"tags":["嵌入式","物联网","驱动开发","通信"],"platform":"前程无忧","positionUrl":""},
  {"id":"pos-010","name":"IoT平台架构师","company":"阿里云","industry":"物联网","province":"浙江","city":"杭州","salaryMin":40,"salaryMax":70,"education":"本科及以上","experience":"5-10年","publishDate":"2026-07-06","recruitNumber":2,"description":"负责IoT平台整体架构设计与技术规划。","responsibilities":["IoT平台架构设计","海量设备接入方案","数据治理策略"],"requiredSkills":["Java","分布式系统","微服务","Kubernetes","消息队列"],"optionalSkills":["流式计算","时序数据库","边缘计算"],"tags":["IoT","架构","分布式","平台"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-011","name":"安全研发工程师","company":"奇安信","industry":"信息安全","province":"北京","city":"北京","salaryMin":25,"salaryMax":50,"education":"本科及以上","experience":"1-3年","publishDate":"2026-07-05","recruitNumber":5,"description":"负责安全产品的研发与攻防技术研究。","responsibilities":["安全产品后端开发","漏洞分析与利用","安全检测规则编写"],"requiredSkills":["Python","C","渗透测试","Web安全","逆向分析"],"optionalSkills":["Go","BurpSuite","IDA","Frida"],"tags":["安全","渗透","攻防","逆向"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-012","name":"安全运营工程师","company":"360","industry":"信息安全","province":"北京","city":"北京","salaryMin":18,"salaryMax":35,"education":"本科及以上","experience":"1-3年","publishDate":"2026-07-04","recruitNumber":4,"description":"负责安全运营中心的日常监控与事件响应。","responsibilities":["安全事件分析与处置","威胁情报收集","安全策略优化"],"requiredSkills":["Linux","日志分析","漏洞扫描","Python","安全运维"],"optionalSkills":["ELK","Splunk","SOAR"],"tags":["安全运营","监控","威胁情报","应急响应"],"platform":"智联招聘","positionUrl":""},
  {"id":"pos-013","name":"区块链开发工程师","company":"蚂蚁集团","industry":"区块链","province":"浙江","city":"杭州","salaryMin":30,"salaryMax":55,"education":"本科及以上","experience":"3-5年","publishDate":"2026-07-03","recruitNumber":3,"description":"负责区块链底层平台和应用开发。","responsibilities":["共识算法研发","智能合约开发","跨链协议实现"],"requiredSkills":["Go","Solidity","密码学","分布式系统","区块链"],"optionalSkills":["Rust","Substrate","EVM","零知识证明"],"tags":["区块链","Web3","智能合约","DeFi"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-014","name":"芯片设计工程师","company":"寒武纪","industry":"半导体","province":"上海","city":"上海","salaryMin":40,"salaryMax":80,"education":"硕士及以上","experience":"3-5年","publishDate":"2026-07-02","recruitNumber":5,"description":"负责AI芯片的逻辑设计与验证。","responsibilities":["芯片RTL设计","逻辑综合","时序分析","验证环境搭建"],"requiredSkills":["Verilog","SystemVerilog","VCS","UVM","综合工具"],"optionalSkills":["Python","Perl","TCL","机器学习"],"tags":["芯片设计","半导体","RTL","AI芯片"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-015","name":"量子算法研究员","company":"本源量子","industry":"量子计算","province":"安徽","city":"合肥","salaryMin":35,"salaryMax":70,"education":"博士","experience":"5-10年","publishDate":"2026-07-01","recruitNumber":2,"description":"负责量子计算算法的研究与实现。","responsibilities":["量子算法设计","量子纠错研究","量子模拟器开发"],"requiredSkills":["量子力学","线性代数","Python","Qiskit","量子算法"],"optionalSkills":["Cirq","Q#","C++","Julia"],"tags":["量子计算","量子算法","量子纠错","量子模拟"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-016","name":"后端开发工程师","company":"美团","industry":"互联网","province":"北京","city":"北京","salaryMin":25,"salaryMax":45,"education":"本科及以上","experience":"3-5年","publishDate":"2026-06-30","recruitNumber":10,"description":"负责后端服务的设计与开发。","responsibilities":["高并发系统设计","微服务开发","数据库优化"],"requiredSkills":["Java","Spring Boot","MySQL","Redis","微服务"],"optionalSkills":["Kubernetes","Docker","消息队列","Elasticsearch"],"tags":["后端开发","Java","高并发","微服务"],"platform":"前程无忧","positionUrl":""},
  {"id":"pos-017","name":"前端开发工程师","company":"字节跳动","industry":"互联网","province":"上海","city":"上海","salaryMin":20,"salaryMax":40,"education":"本科及以上","experience":"1-3年","publishDate":"2026-06-29","recruitNumber":8,"description":"负责Web前端应用的开发与优化。","responsibilities":["前端页面开发","组件库建设","性能优化"],"requiredSkills":["JavaScript","TypeScript","React","CSS","前端工程化"],"optionalSkills":["Vue","Webpack","Node.js","Next.js"],"tags":["前端开发","React","TypeScript","Web"],"platform":"BOSS直聘","positionUrl":""},
  {"id":"pos-018","name":"数据库管理员","company":"蚂蚁集团","industry":"数据库","province":"浙江","city":"杭州","salaryMin":20,"salaryMax":40,"education":"本科及以上","experience":"3-5年","publishDate":"2026-06-28","recruitNumber":2,"description":"负责数据库的日常运维与架构优化。","responsibilities":["数据库运维","性能调优","备份恢复策略制定"],"requiredSkills":["MySQL","Redis","数据库优化","Linux","Shell"],"optionalSkills":["MongoDB","TiDB","Elasticsearch","Kafka"],"tags":["数据库","DBA","运维","MySQL"],"platform":"猎聘","positionUrl":""},
  {"id":"pos-019","name":"AI训练师（实习生）","company":"科大讯飞","industry":"人工智能","province":"安徽","city":"合肥","salaryMin":4,"salaryMax":8,"education":"大专及以上","experience":"经验不限","publishDate":"2026-07-16","recruitNumber":15,"description":"负责AI模型的训练数据标注与质量评估。","responsibilities":["数据标注与质检","模型效果评估","标注工具优化建议"],"requiredSkills":["Python","数据分析","沟通能力"],"optionalSkills":["SQL","Excel","基础机器学习"],"tags":["AI训练","数据标注","实习","基础岗位"],"platform":"智联招聘","positionUrl":""},
  {"id":"pos-020","name":"云计算售前工程师","company":"华为云","industry":"云计算","province":"四川","city":"成都","salaryMin":15,"salaryMax":30,"education":"本科及以上","experience":"经验不限","publishDate":"2026-06-25","recruitNumber":5,"description":"负责云计算产品的售前技术支持与方案设计。","responsibilities":["客户需求分析","技术方案编写","产品演示与POC"],"requiredSkills":["云计算基础","沟通表达","方案设计"],"optionalSkills":["AWS","阿里云","Linux","网络基础"],"tags":["云计算","售前","解决方案","技术支持"],"platform":"前程无忧","positionUrl":""}
]
export const industryList = ['人工智能','大数据','云计算','物联网','区块链','信息安全','半导体','量子计算','互联网','数据库']
export const provinceList = ['北京','上海','广东','浙江','安徽','四川']
export const educationOptions = ['学历不限','大专及以上','本科及以上','硕士及以上','博士']
export const experienceOptions = ['经验不限','1-3年','3-5年','5-10年']
export const salaryRangeOptions = [{label:'10K以下',value:[0,10]},{label:'10-20K',value:[10,20]},{label:'20-35K',value:[20,35]},{label:'35K以上',value:[35,999]}]

export function generateMockReport(positionName: string): MatchReport {
  return { id:'report-'+Date.now(), resumeId:'resume-demo', positionId:'pos-demo', positionName, companyName:'示例公司', overallMatchScore:0.76, dimensionScores:{skill:0.72,experience:0.80,responsibility:0.78}, requiredSkillMatchRate:0.71, optionalSkillMatchRate:0.50, skillMatches:[{skill:'Python',required:true,matched:true,evidence:'3年Python经验'},{skill:'PyTorch',required:true,matched:true,evidence:'项目中使用PyTorch'},{skill:'机器学习',required:true,matched:true,evidence:'多个ML项目'},{skill:'分布式训练',required:true,matched:false,evidence:'',gapReason:'无相关经验',suggestion:'学习DeepSpeed'},{skill:'模型量化',required:false,matched:false,evidence:'',gapReason:'未涉及',suggestion:'了解量化技术'}], gaps:[{skill:'分布式训练',importance:'high',reason:'岗位要求大规模分布式训练',suggestion:'学习DeepSpeed'},{skill:'模型量化',importance:'medium',reason:'加分项非必需',suggestion:'了解INT8/FP8'}], strengths:['扎实的Python和深度学习基础','有完整的项目落地经验','学历符合要求'], recommendation:'recommend', confidence:0.85, provenance:{model:'DeepSeek',timestamp:new Date().toISOString()} }
}

export const mockGraphData: GraphData = {
  categories: [{name:'岗位',itemStyle:{color:'#00ffff'}},{name:'技能',itemStyle:{color:'#ff6b6b'}},{name:'行业',itemStyle:{color:'#ffd93d'}},{name:'公司',itemStyle:{color:'#6bcb77'}}],
  nodes: [
    {"id":"pos-01","name":"大模型算法工程师","type":"position","category":0,"symbolSize":50,"description":"大语言模型训练与优化"},
    {"id":"pos-02","name":"计算机视觉工程师","type":"position","category":0,"symbolSize":45,"description":"CV算法研发"},
    {"id":"skill-01","name":"Python","type":"skill","category":1,"symbolSize":30},
    {"id":"skill-02","name":"PyTorch","type":"skill","category":1,"symbolSize":28},
    {"id":"skill-03","name":"Transformer","type":"skill","category":1,"symbolSize":25},
    {"id":"skill-04","name":"分布式训练","type":"skill","category":1,"symbolSize":22},
    {"id":"skill-05","name":"计算机视觉","type":"skill","category":1,"symbolSize":25},
    {"id":"skill-06","name":"OpenCV","type":"skill","category":1,"symbolSize":20},
    {"id":"industry-01","name":"人工智能","type":"industry","category":2,"symbolSize":40,"description":"新一代信息技术核心领域"},
    {"id":"company-01","name":"科大讯飞","type":"company","category":3,"symbolSize":35}
  ],
  edges: [
    {id:'e1',source:'pos-01',target:'skill-01',label:'必需技能',weight:1},
    {id:'e2',source:'pos-01',target:'skill-02',label:'必需技能',weight:1},
    {id:'e3',source:'pos-01',target:'skill-03',label:'核心技能',weight:0.9},
    {id:'e4',source:'pos-01',target:'skill-04',label:'必需技能',weight:0.8},
    {id:'e5',source:'pos-02',target:'skill-01',label:'必需技能',weight:1},
    {id:'e6',source:'pos-02',target:'skill-02',label:'必需技能',weight:1},
    {id:'e7',source:'pos-02',target:'skill-05',label:'核心技能',weight:0.9},
    {id:'e8',source:'pos-02',target:'skill-06',label:'常用技能',weight:0.7},
    {id:'e9',source:'pos-01',target:'industry-01',label:'所属行业',weight:0.5},
    {id:'e10',source:'pos-02',target:'industry-01',label:'所属行业',weight:0.5},
    {id:'e11',source:'pos-01',target:'company-01',label:'招聘公司',weight:0.3}
  ]
}

export const mockResume: ResumeProfile = {
  personalInfo: {name:'张三',phone:'138****8888',email:'zhangsan@example.com',highestEducation:'硕士',workYears:3,currentPosition:'算法工程师',currentCompany:'某科技公司'},
  education: [{school:'中国科学技术大学',degree:'硕士',major:'计算机科学与技术',startDate:'2020-09',endDate:'2023-06'}],
  workExperience: [{company:'某AI公司',position:'算法工程师',startDate:'2023-07',endDate:'至今',responsibilities:['NLP模型训练'],achievements:['推理速度提升40%']}],
  projectExperience: [{name:'智能客服系统',role:'算法工程师',description:'基于BERT构建意图识别',techStack:['Python','PyTorch','BERT'],highlights:['准确率96%']}],
  skills:['Python','PyTorch','NLP','BERT','Transformer','机器学习','MySQL'],
  parsingMethod:'hybrid',confidence:0.92
}

export function getPositionById(id: string): PositionInfo | undefined {
  return mockPositions.find(p => p.id === id)
}

export function filterPositions(params: any) {
  let filtered = [...mockPositions]
  if (params.keyword) { const kw=params.keyword.toLowerCase(); filtered=filtered.filter((p:any)=>p.name.toLowerCase().includes(kw)||p.company.toLowerCase().includes(kw)||p.requiredSkills.some((s:string)=>s.toLowerCase().includes(kw))) }
  if (params.industry) filtered=filtered.filter((p:any)=>p.industry===params.industry)
  if (params.province) filtered=filtered.filter((p:any)=>p.province===params.province)
  if (params.education) filtered=filtered.filter((p:any)=>p.education.includes(params.education.replace('及以上','')))
  if (params.experience) filtered=filtered.filter((p:any)=>p.experience===params.experience)
  if (params.salaryMin) filtered=filtered.filter((p:any)=>p.salaryMax>=params.salaryMin)
  if (params.salaryMax) filtered=filtered.filter((p:any)=>p.salaryMin<=params.salaryMax)
  if (params.sortBy === 'salary_asc') filtered.sort((a:any,b:any)=>(a.salaryMin||0)-(b.salaryMin||0))
  else if (params.sortBy === 'salary_desc') filtered.sort((a:any,b:any)=>(b.salaryMax||0)-(a.salaryMax||0))
  else if (params.sortBy === 'date_desc') filtered.sort((a:any,b:any)=>b.publishDate.localeCompare(a.publishDate))
  else if (params.sortBy === 'recruit_desc') filtered.sort((a:any,b:any)=>b.recruitNumber-(a.recruitNumber))
  const total=filtered.length;const totalPages=Math.ceil(total/params.pageSize)
  const start=(params.page-1)*params.pageSize;const items=filtered.slice(start,start+params.pageSize)
  return {items,total,page:params.page,pageSize:params.pageSize,totalPages}
}


// ===== Homepage dashboard statistics Mock data =====
export const industryStats = [
  { name: "人工智能", value: 6 },
  { name: "大数据", value: 2 },
  { name: "云计算", value: 2 },
  { name: "互联网", value: 2 },
  { name: "物联网", value: 1 },
  { name: "信息安全", value: 1 },
  { name: "区块链", value: 1 },
  { name: "半导体", value: 1 },
  { name: "量子计算", value: 1 },
  { name: "数据库", value: 1 },
  { name: "其他", value: 2 }
]

export const educationStats = [
  { name: "本科及以上", value: 10 },
  { name: "硕士及以上", value: 7 },
  { name: "博士", value: 1 },
  { name: "大专及以上", value: 1 },
  { name: "学历不限", value: 1 }
]

export const experienceStats = [
  { name: "经验不限", value: 2 },
  { name: "1-3年", value: 3 },
  { name: "3-5年", value: 11 },
  { name: "5-10年", value: 4 }
]

export const salaryStats = [
  { range: "0-10K", min: 0, max: 10, count: 1 },
  { range: "10-20K", min: 10, max: 20, count: 2 },
  { range: "20-30K", min: 20, max: 30, count: 6 },
  { range: "30-40K", min: 30, max: 40, count: 6 },
  { range: "40-50K", min: 40, max: 50, count: 3 },
  { range: "50K以上", min: 50, max: 200, count: 2 }
]

export const skillCloud = [
  { name: "Python", value: 80 }, { name: "PyTorch", value: 60 },
  { name: "C++", value: 45 }, { name: "机器学习", value: 40 },
  { name: "深度学习", value: 38 }, { name: "Kubernetes", value: 30 },
  { name: "Docker", value: 28 }, { name: "Go", value: 25 },
  { name: "Java", value: 22 }, { name: "Transformer", value: 20 },
  { name: "NLP", value: 18 }, { name: "分布式系统", value: 35 },
  { name: "Linux", value: 20 }, { name: "模型部署", value: 16 },
  { name: "SQL", value: 15 }, { name: "Spark", value: 14 },
  { name: "OpenCV", value: 13 }, { name: "React", value: 12 },
  { name: "SLAM", value: 10 }, { name: "Rust", value: 8 }
]

export const provinceStats = [
  { name: "北京", value: 5 }, { name: "广东", value: 4 },
  { name: "浙江", value: 4 }, { name: "上海", value: 3 },
  { name: "安徽", value: 3 }, { name: "四川", value: 1 }
]

export const companyRank = [
  { name: "科大讯飞", positions: 2, avgSalary: 41.25 },
  { name: "华为", positions: 2, avgSalary: 37.5 },
  { name: "百度", positions: 1, avgSalary: 37.5 },
  { name: "阿里巴巴", positions: 1, avgSalary: 57.5 },
  { name: "腾讯", positions: 1, avgSalary: 30 },
  { name: "字节跳动", positions: 1, avgSalary: 50 },
  { name: "商汤科技", positions: 1, avgSalary: 41.5 },
  { name: "寒武纪", positions: 1, avgSalary: 70 },
  { name: "蚂蚁集团", positions: 1, avgSalary: 42.5 },
  { name: "大疆创新", positions: 1, avgSalary: 45 }
]
