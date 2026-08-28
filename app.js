const translations = {
  en: {
    "meta.title": "Intelligent Audio Production Resources",
    "meta.description": "A structured index of open resources and recent research for intelligent audio effects, mixing, mastering, spatial audio, and evaluation.",
    "nav.label": "Primary navigation",
    "nav.scope": "Scope",
    "nav.projects": "Projects",
    "nav.datasets": "Datasets",
    "nav.resources": "Resources",
    "nav.papers": "Papers",
    "nav.github": "GitHub",
    "intro.eyebrow": "Open research index",
    "intro.title": "Intelligent Audio Production",
    "intro.lead": "A structured index of open-source projects, models, datasets, and recent research for intelligent audio effects and music production.",
    "intro.statsLabel": "Catalogue coverage",
    "intro.projectsLabel": "Projects",
    "intro.datasetsLabel": "Datasets",
    "intro.papersLabel": "Papers",
    "intro.scopeLabel": "Current scope",
    "intro.imageAlt": "A waveform illustrating intelligent audio production",
    "scope.title": "Field map",
    "scope.description": "The index follows production tasks rather than publication year. Each area collects implementations, pretrained models, datasets, and evaluation resources where available.",
    "scope.audioEffects": "Modeling, estimation, control, and transfer of EQ, dynamics, distortion, reverberation, and other processors.",
    "scope.differentiableProcessing": "Differentiable DSP, audio-effect chains, processing graphs, and optimization tools for production tasks.",
    "scope.representation": "Embeddings and descriptors that capture effect transformations, production style, and perceptual attributes.",
    "scope.mixing": "Automatic, reference-guided, and controllable systems for balancing and processing multitrack music.",
    "scope.mastering": "Systems for loudness, dynamics, tonal balance, reference matching, and final-stage production.",
    "scope.evaluation": "Benchmarks, listening-test protocols, production metrics, and reproducibility tools.",
    "scope.spatialAudio": "Intelligent generation, upmixing, positioning, rendering, HRTF personalization, and evaluation for immersive production.",
    "scope.viewPapers": "View papers",
    "scope.noPapers": "No papers indexed yet",
    "projects.title": "Project index",
    "projects.description": "Entries distinguish source availability, checkpoints, licenses, and reproducibility. Projects are added after their public resources have been checked.",
    "projects.searchPlaceholder": "Project or task",
    "projects.areaFilter": "Filter projects by area",
    "projects.columnProject": "Project",
    "projects.columnArea": "Area",
    "projects.columnAvailable": "Available",
    "projects.columnLicense": "License",
    "projects.columnVerified": "Verified",
    "projects.loading": "Loading verified projects...",
    "projects.empty": "No verified projects match this filter.",
    "projects.loadError": "The project index could not be loaded.",
    "projects.openDetails": "View project details",
    "projects.dialogLabel": "Project details",
    "projects.closeDetails": "Close project details",
    "projects.licenseFilter": "Filter projects by license",
    "projects.capabilityFilter": "Filter projects by availability capability",
    "projects.statusFilter": "Filter projects by availability status",
    "projects.taskFilter": "Filter projects by reviewed task",
    "projects.effectFilter": "Filter projects by reviewed effect",
    "projects.controlApproachFilter": "Filter projects by linked control approach",
    "projects.controlApproachesLabel": "Control approaches",
    "projects.trackScopeFilter": "Filter projects by linked track scope",
    "projects.trackScopesLabel": "Track scope",
    "projects.relatedPapersLabel": "Related papers",
    "projects.noRelatedPapers": "No related paper has been verified.",
    "projects.licenseLabel": "License",
    "projects.licenseStatusLabel": "License status",
    "projects.spdxLabel": "SPDX",
    "projects.evidenceLabel": "Evidence",
    "projects.noEvidence": "No evidence URL recorded.",
    "projects.availabilityLabel": "Availability",
    "projects.taxonomyLabel": "Taxonomy",
    "projects.tasksLabel": "Tasks",
    "projects.effectsLabel": "Effects",
    "projects.noReviewedTaxonomy": "No reviewed taxonomy tags.",
    "projects.linksLabel": "Project links",
    "projects.verifiedLabel": "Verified",
    "datasets.title": "Dataset index",
    "datasets.description": "Common datasets for intelligent audio production, with access terms, data licenses, and verified links to papers and projects that use them.",
    "datasets.searchPlaceholder": "Dataset, task, or content",
    "datasets.areaFilter": "Filter datasets by area",
    "datasets.taskFilter": "Filter datasets by task",
    "datasets.contentFilter": "Filter datasets by content type",
    "datasets.accessFilter": "Filter datasets by access type",
    "datasets.columnDataset": "Dataset",
    "datasets.columnArea": "Area",
    "datasets.columnContent": "Content",
    "datasets.columnAccess": "Access",
    "datasets.columnUsedBy": "Used by",
    "datasets.columnVerified": "Verified",
    "datasets.loading": "Loading verified datasets...",
    "datasets.empty": "No datasets match this filter.",
    "datasets.loadError": "The dataset index could not be loaded.",
    "datasets.openDetails": "View dataset details",
    "datasets.dialogLabel": "Dataset details",
    "datasets.closeDetails": "Close dataset details",
    "datasets.scaleLabel": "Scale",
    "datasets.accessLabel": "Access",
    "datasets.licenseLabel": "Data license",
    "datasets.taxonomyLabel": "Tasks and contents",
    "datasets.contentTypesLabel": "Content types",
    "datasets.relatedPapersLabel": "Papers using this dataset",
    "datasets.relatedProjectsLabel": "Projects using this dataset",
    "datasets.usedDatasetsLabel": "Datasets used",
    "datasets.noRelatedPapers": "No paper usage has been verified yet.",
    "datasets.noRelatedProjects": "No project usage has been verified yet.",
    "datasets.noRelatedDatasets": "No dataset usage has been verified yet.",
    "datasets.linksLabel": "Dataset links",
    "datasets.verifiedLabel": "Verified",
    "datasets.paperCount": "papers",
    "datasets.projectCount": "projects",
    "resources.title": "Reference resources",
    "resources.description": "Bibliographies and field guides are listed separately from runnable implementations.",
    "resources.kind.bibliography": "Bibliography",
    "resources.loading": "Loading reference resources...",
    "resources.loadError": "The reference resources could not be loaded.",
    "papers.title": "Paper index",
    "papers.description": "Papers are collected across the field, with links and concise summaries available in each entry.",
    "papers.agentLabel": "AI paper scout",
    "papers.agentDescription": "A scheduled workflow checks new papers weekly. Candidate metadata is validated before a website update is proposed.",
    "papers.searchPlaceholder": "Title, author, or topic",
    "papers.areaFilter": "Filter papers by area",
    "papers.controlApproachFilter": "Filter papers by control approach",
    "papers.trackScopeFilter": "Filter papers by track scope",
    "papers.recognitionFilter": "Filter papers by recognition",
    "papers.loading": "Loading papers...",
    "papers.empty": "No papers match this filter.",
    "papers.loadError": "The paper index could not be loaded.",
    "papers.automated": "Agent-curated",
    "papers.openDetails": "View details",
    "papers.dialogLabel": "Paper details",
    "papers.closeDetails": "Close paper details",
    "papers.summaryLabel": "Summary",
    "papers.paperLinksLabel": "Paper",
    "papers.openResourcesLabel": "Open resources",
    "papers.noPaperLink": "No public paper link has been verified.",
    "papers.noOpenResources": "No public implementation or model has been verified.",
    "papers.shortNameLabel": "Index name",
    "papers.openSourceAvailable": "Source available",
    "papers.controlApproachesLabel": "Control approach",
    "papers.trackScopesLabel": "Track scope",
    "controls.recognition": "Recognition",
    "controls.allRecognition": "All recognition",
    "recognition.aiHighlight": "AI Highlight",
    "recognition.highImpact": "High Impact",
    "recognition.note": "AI Highlight is a rubric-based model assessment, not peer review. High Impact uses year-normalized Semantic Scholar citations; current-year papers are not ranked.",
    "recognition.methodology": "Methodology",
    "recognition.detailsLabel": "Recognition details",
    "recognition.aiRationaleLabel": "AI assessment",
    "recognition.impactLabel": "Citation impact",
    "recognition.tooRecent": "This paper is too recent for year-normalized citation ranking.",
    "recognition.notAssessed": "Citation impact was not assessed because no exact arXiv or DOI match was available.",
    "recognition.semanticScholar": "View on Semantic Scholar",
    "controls.search": "Search",
    "controls.area": "Area",
    "controls.allAreas": "All areas",
    "controls.license": "License",
    "controls.allLicenses": "All licenses",
    "controls.capability": "Capability",
    "controls.allCapabilities": "All capabilities",
    "controls.status": "Status",
    "controls.allStatuses": "All statuses",
    "controls.task": "Task",
    "controls.allTasks": "All tasks",
    "controls.effect": "Effect",
    "controls.allEffects": "All effects",
    "controls.content": "Content",
    "controls.allContentTypes": "All content types",
    "controls.access": "Access",
    "controls.allAccessTypes": "All access types",
    "controls.controlApproach": "Control approach",
    "controls.allControlApproaches": "All approaches",
    "controls.trackScope": "Track scope",
    "controls.allTrackScopes": "All track scopes",
    "controls.reset": "Reset",
    "pagination.projectsLabel": "Project pages",
    "pagination.datasetsLabel": "Dataset pages",
    "pagination.papersLabel": "Paper pages",
    "pagination.previous": "Previous page",
    "pagination.next": "Next page",
    "control.gradient-based-optimization": "Differentiable optimization",
    "control.derivative-free-optimization": "Derivative-free optimization",
    "control.direct-prediction": "Direct prediction",
    "track.single-track": "Single-track",
    "track.multitrack": "Multitrack",
    "common.later": "Later",
    "community.title": "Help improve the index",
    "community.description": "Submit missing papers, projects, datasets, or corrections through GitHub. Contributions are reviewed before they enter the public index.",
    "community.starAction": "Star on GitHub",
    "community.contributeAction": "Contribute a resource",
    "community.followNote": "If this index is useful, please star or watch the GitHub repository to follow future updates.",
    "footer.maintained": "Maintained by",
    "footer.note": "A living resource for the audio research community.",
    "footer.powered": "Powered by Codex and DeepSeek",
    "area.audio-effects": "Audio effects",
    "area.differentiable-processing": "Differentiable processing",
    "area.representation": "Representation",
    "area.mixing": "Mixing",
    "area.mastering": "Mastering",
    "area.evaluation": "Evaluation",
    "area.spatial-audio": "Spatial audio",
    "link.paper": "Paper",
    "link.project": "Project",
    "link.source": "Source",
    "link.checkpoint": "Checkpoint",
    "link.doi": "DOI",
    "link.dataset": "Dataset",
    "license.status.identified": "Identified",
    "license.status.custom": "Custom",
    "license.status.not-verified": "Not verified",
    "availability.source": "Source",
    "availability.checkpoint": "Checkpoint",
    "availability.inference": "Inference",
    "availability.training": "Training",
    "availability.dataset": "Dataset",
    "availability.status.not-reviewed": "Not reviewed",
    "availability.status.linked": "Linked",
    "availability.status.documented": "Documented",
    "availability.status.tested": "Tested",
    "availability.status.gated": "Gated",
    "availability.status.restricted": "Restricted",
    "availability.status.not-found": "Not found",
    "availability.status.not-applicable": "Not applicable",
    "dataset.access.direct-download": "Direct download",
    "dataset.access.request": "Request access",
    "dataset.access.registration": "Registration",
    "dataset.access.restricted": "Restricted",
    "dataset.access.unavailable": "Unavailable",
    "dataset.access.not-reviewed": "Not reviewed",
    "content.multitrack": "Multitrack",
    "content.stems": "Stems",
    "content.dry-audio": "Dry audio",
    "content.processed-audio": "Processed audio",
    "content.dry-wet-pairs": "Dry/wet pairs",
    "content.effect-parameters": "Effect parameters",
    "content.impulse-responses": "Impulse responses",
    "content.reference-mixes": "Reference mixes",
    "content.annotations": "Annotations",
    "content.text-prompts": "Text prompts",
    "content.synthetic-audio": "Synthetic audio",
    "content.binaural-audio": "Binaural audio",
    "content.ambisonics": "Ambisonics",
    "content.hrtf": "HRTF",
    "content.spatial-metadata": "Spatial metadata",
    "content.video": "Video",
    "task.effect-modeling": "Effect modeling",
    "task.parameter-estimation": "Parameter estimation",
    "task.effect-control": "Effect control",
    "task.effect-transfer": "Effect transfer",
    "task.effect-removal": "Effect removal",
    "task.representation-learning": "Representation learning",
    "task.automatic-mixing": "Automatic mixing",
    "task.mastering": "Mastering",
    "task.evaluation": "Evaluation",
    "task.differentiable-processing": "Differentiable processing",
    "task.spatial-generation": "Spatial generation",
    "task.spatial-mixing": "Spatial mixing",
    "task.spatial-rendering": "Spatial rendering",
    "task.hrtf-personalization": "HRTF personalization",
    "task.spatial-evaluation": "Spatial evaluation",
    "effect.gain": "Gain",
    "effect.equalization": "EQ",
    "effect.compression": "Compression",
    "effect.distortion": "Distortion",
    "effect.reverberation": "Reverb",
    "effect.delay": "Delay",
    "effect.modulation": "Modulation",
    "effect.stereo": "Stereo",
    "effect.filtering": "Filtering",
    "effect.multi-effect": "Multi-effect",
    "effect.other": "Other"
  },
  zh: {
    "meta.title": "智能音频制作资源索引",
    "meta.description": "面向智能音效、混音、母带、空间音频与评测的开放资源及近期研究索引。",
    "nav.label": "主导航",
    "nav.scope": "领域",
    "nav.projects": "项目",
    "nav.datasets": "数据集",
    "nav.resources": "参考资料",
    "nav.papers": "论文",
    "nav.github": "GitHub",
    "intro.eyebrow": "开放研究索引",
    "intro.title": "智能音频制作",
    "intro.lead": "汇总智能音效与音乐制作领域的开源项目、模型、数据集、评测资源及近期研究。",
    "intro.statsLabel": "索引收录规模",
    "intro.projectsLabel": "个项目",
    "intro.datasetsLabel": "个数据集",
    "intro.papersLabel": "篇论文",
    "intro.scopeLabel": "当前范围",
    "intro.imageAlt": "用于说明智能音频制作的音频波形",
    "scope.title": "领域地图",
    "scope.description": "索引按照制作任务而非发表年份组织；每个方向将收录可用的实现、预训练模型、数据集与评测资源。",
    "scope.audioEffects": "均衡、动态、失真、混响及其他处理器的建模、估计、控制与迁移。",
    "scope.differentiableProcessing": "面向制作任务的可微 DSP、音效链、处理图与优化工具。",
    "scope.representation": "描述音效变化、制作风格与感知属性的嵌入及特征。",
    "scope.mixing": "面向多轨音乐平衡与处理的自动混音、参考引导和可控混音系统。",
    "scope.mastering": "响度、动态、音色平衡、参考匹配与终端制作系统。",
    "scope.evaluation": "基准、听音实验流程、制作指标与可复现工具。",
    "scope.spatialAudio": "面向沉浸式制作的智能生成、上混、声像定位、渲染、HRTF 个性化与评测。",
    "scope.viewPapers": "查看论文",
    "scope.noPapers": "暂未收录论文",
    "projects.title": "项目索引",
    "projects.description": "条目分别记录源码、权重、许可证与可复现情况；只有公开资源经过核验后才会加入。",
    "projects.searchPlaceholder": "搜索项目或任务",
    "projects.areaFilter": "按领域筛选项目",
    "projects.columnProject": "项目",
    "projects.columnArea": "领域",
    "projects.columnAvailable": "可用资源",
    "projects.columnLicense": "许可证",
    "projects.columnVerified": "核验时间",
    "projects.loading": "正在加载已核验项目……",
    "projects.empty": "没有符合当前筛选条件的项目。",
    "projects.loadError": "项目索引加载失败。",
    "projects.openDetails": "查看项目详情",
    "projects.dialogLabel": "项目详情",
    "projects.closeDetails": "关闭项目详情",
    "projects.licenseFilter": "按许可证筛选项目",
    "projects.capabilityFilter": "按可用能力筛选项目",
    "projects.statusFilter": "按可用状态筛选项目",
    "projects.taskFilter": "按已核验任务筛选项目",
    "projects.effectFilter": "按已核验效果筛选项目",
    "projects.controlApproachFilter": "按关联论文的参数获取方式筛选项目",
    "projects.controlApproachesLabel": "参数获取方式",
    "projects.trackScopeFilter": "按关联论文的轨道范围筛选项目",
    "projects.trackScopesLabel": "轨道范围",
    "projects.relatedPapersLabel": "关联论文",
    "projects.noRelatedPapers": "暂未核验到关联论文。",
    "projects.licenseLabel": "许可证",
    "projects.licenseStatusLabel": "许可证状态",
    "projects.spdxLabel": "SPDX",
    "projects.evidenceLabel": "证据",
    "projects.noEvidence": "未记录证据链接。",
    "projects.availabilityLabel": "可用性",
    "projects.taxonomyLabel": "分类",
    "projects.tasksLabel": "任务",
    "projects.effectsLabel": "效果",
    "projects.noReviewedTaxonomy": "暂无已核验分类标签。",
    "projects.linksLabel": "项目链接",
    "projects.verifiedLabel": "核验时间",
    "datasets.title": "数据集索引",
    "datasets.description": "汇总智能音频制作常用数据集，并记录访问方式、数据许可证，以及已核验的使用论文和项目。",
    "datasets.searchPlaceholder": "搜索数据集、任务或内容",
    "datasets.areaFilter": "按领域筛选数据集",
    "datasets.taskFilter": "按任务筛选数据集",
    "datasets.contentFilter": "按内容类型筛选数据集",
    "datasets.accessFilter": "按访问方式筛选数据集",
    "datasets.columnDataset": "数据集",
    "datasets.columnArea": "领域",
    "datasets.columnContent": "内容",
    "datasets.columnAccess": "访问方式",
    "datasets.columnUsedBy": "使用情况",
    "datasets.columnVerified": "核验时间",
    "datasets.loading": "正在加载已核验数据集……",
    "datasets.empty": "没有符合当前筛选条件的数据集。",
    "datasets.loadError": "数据集索引加载失败。",
    "datasets.openDetails": "查看数据集详情",
    "datasets.dialogLabel": "数据集详情",
    "datasets.closeDetails": "关闭数据集详情",
    "datasets.scaleLabel": "规模",
    "datasets.accessLabel": "访问方式",
    "datasets.licenseLabel": "数据许可证",
    "datasets.taxonomyLabel": "任务与内容",
    "datasets.contentTypesLabel": "内容类型",
    "datasets.relatedPapersLabel": "使用该数据集的论文",
    "datasets.relatedProjectsLabel": "使用该数据集的项目",
    "datasets.usedDatasetsLabel": "使用的数据集",
    "datasets.noRelatedPapers": "暂未核验到论文使用关系。",
    "datasets.noRelatedProjects": "暂未核验到项目使用关系。",
    "datasets.noRelatedDatasets": "暂未核验到数据集使用关系。",
    "datasets.linksLabel": "数据集链接",
    "datasets.verifiedLabel": "核验时间",
    "datasets.paperCount": "篇论文",
    "datasets.projectCount": "个项目",
    "resources.title": "参考资料",
    "resources.description": "书目与领域导航和可运行实现分开列出，避免混淆。",
    "resources.kind.bibliography": "论文书目",
    "resources.loading": "正在加载参考资料……",
    "resources.loadError": "参考资料加载失败。",
    "papers.title": "论文索引",
    "papers.description": "汇总领域内相关论文，每个条目均可查看论文链接、开源资源与简要介绍。",
    "papers.agentLabel": "AI 论文巡检 Agent",
    "papers.agentDescription": "定时工作流每周检查新论文，并在提出网站更新前核验候选论文的元数据。",
    "papers.searchPlaceholder": "搜索标题、作者或主题",
    "papers.areaFilter": "按领域筛选论文",
    "papers.controlApproachFilter": "按参数获取方式筛选论文",
    "papers.trackScopeFilter": "按轨道范围筛选论文",
    "papers.recognitionFilter": "按精选与影响力筛选论文",
    "papers.loading": "正在加载论文……",
    "papers.empty": "没有符合当前筛选条件的论文。",
    "papers.loadError": "论文索引加载失败。",
    "papers.automated": "Agent 筛选",
    "papers.openDetails": "查看详情",
    "papers.dialogLabel": "论文详情",
    "papers.closeDetails": "关闭论文详情",
    "papers.summaryLabel": "论文简介",
    "papers.paperLinksLabel": "论文链接",
    "papers.openResourcesLabel": "开源资源",
    "papers.noPaperLink": "暂未核验到公开论文链接。",
    "papers.noOpenResources": "暂未核验到公开实现或模型。",
    "papers.shortNameLabel": "索引简称",
    "papers.openSourceAvailable": "已有源码",
    "papers.controlApproachesLabel": "参数获取方式",
    "papers.trackScopesLabel": "轨道范围",
    "controls.recognition": "精选与影响力",
    "controls.allRecognition": "全部标记",
    "recognition.aiHighlight": "AI 精选",
    "recognition.highImpact": "高影响力",
    "recognition.note": "AI 精选是基于公开规则的模型评估，不代表同行评审；高影响力依据 Semantic Scholar 引用量进行同年份归一化，当年论文暂不排名。",
    "recognition.methodology": "查看方法",
    "recognition.detailsLabel": "精选与影响力",
    "recognition.aiRationaleLabel": "AI 评估",
    "recognition.impactLabel": "引用影响力",
    "recognition.tooRecent": "该论文发表时间较近，暂不参与同年份引用排名。",
    "recognition.notAssessed": "未找到可精确匹配的 arXiv 或 DOI 标识，因此未评估引用影响力。",
    "recognition.semanticScholar": "前往 Semantic Scholar",
    "controls.search": "搜索",
    "controls.area": "领域",
    "controls.allAreas": "全部领域",
    "controls.license": "许可证",
    "controls.allLicenses": "全部许可证",
    "controls.capability": "能力",
    "controls.allCapabilities": "全部能力",
    "controls.status": "状态",
    "controls.allStatuses": "全部状态",
    "controls.task": "任务",
    "controls.allTasks": "全部任务",
    "controls.effect": "效果",
    "controls.allEffects": "全部效果",
    "controls.content": "内容",
    "controls.allContentTypes": "全部内容类型",
    "controls.access": "访问方式",
    "controls.allAccessTypes": "全部访问方式",
    "controls.controlApproach": "参数获取方式",
    "controls.allControlApproaches": "全部方式",
    "controls.trackScope": "轨道范围",
    "controls.allTrackScopes": "全部轨道范围",
    "controls.reset": "重置",
    "pagination.projectsLabel": "项目分页",
    "pagination.datasetsLabel": "数据集分页",
    "pagination.papersLabel": "论文分页",
    "pagination.previous": "上一页",
    "pagination.next": "下一页",
    "control.gradient-based-optimization": "可微分优化",
    "control.derivative-free-optimization": "非可微分优化",
    "control.direct-prediction": "直接预测（非迭代）",
    "track.single-track": "单轨",
    "track.multitrack": "多轨",
    "common.later": "后续",
    "community.title": "参与共建",
    "community.description": "欢迎通过 GitHub 补充遗漏的论文、项目和数据集，或提交信息修正。所有贡献经核验后进入公开索引。",
    "community.starAction": "前往 GitHub / Star",
    "community.contributeAction": "提交资源",
    "community.followNote": "如果这个索引对你有帮助，请 Star 或 Watch GitHub 仓库，关注后续更新。",
    "footer.maintained": "维护者：",
    "footer.note": "持续更新的音频研究社区资源。",
    "footer.powered": "由 Codex 与 DeepSeek 提供支持",
    "area.audio-effects": "音频效果",
    "area.differentiable-processing": "可微分音频处理",
    "area.representation": "表征学习",
    "area.mixing": "混音",
    "area.mastering": "母带",
    "area.evaluation": "评测",
    "area.spatial-audio": "空间音频",
    "link.paper": "论文",
    "link.project": "项目主页",
    "link.source": "源码",
    "link.checkpoint": "模型权重",
    "link.doi": "DOI",
    "link.dataset": "数据集",
    "license.status.identified": "已识别",
    "license.status.custom": "自定义",
    "license.status.not-verified": "未核验",
    "availability.source": "源码",
    "availability.checkpoint": "权重",
    "availability.inference": "推理",
    "availability.training": "训练",
    "availability.dataset": "数据集",
    "availability.status.not-reviewed": "未核验",
    "availability.status.linked": "已链接",
    "availability.status.documented": "有文档",
    "availability.status.tested": "已测试",
    "availability.status.gated": "需申请",
    "availability.status.restricted": "受限",
    "availability.status.not-found": "未找到",
    "availability.status.not-applicable": "不适用",
    "dataset.access.direct-download": "直接下载",
    "dataset.access.request": "申请访问",
    "dataset.access.registration": "注册访问",
    "dataset.access.restricted": "受限",
    "dataset.access.unavailable": "不可用",
    "dataset.access.not-reviewed": "未核验",
    "content.multitrack": "多轨音频",
    "content.stems": "分轨",
    "content.dry-audio": "干声音频",
    "content.processed-audio": "已处理音频",
    "content.dry-wet-pairs": "干湿音频对",
    "content.effect-parameters": "音效参数",
    "content.impulse-responses": "脉冲响应",
    "content.reference-mixes": "参考混音",
    "content.annotations": "标注",
    "content.text-prompts": "文本提示",
    "content.synthetic-audio": "合成音频",
    "content.binaural-audio": "双耳音频",
    "content.ambisonics": "Ambisonics",
    "content.hrtf": "HRTF",
    "content.spatial-metadata": "空间元数据",
    "content.video": "视频",
    "task.effect-modeling": "效果建模",
    "task.parameter-estimation": "参数估计",
    "task.effect-control": "效果控制",
    "task.effect-transfer": "效果迁移",
    "task.effect-removal": "效果去除",
    "task.representation-learning": "表征学习",
    "task.automatic-mixing": "自动混音",
    "task.mastering": "母带",
    "task.evaluation": "评测",
    "task.differentiable-processing": "可微分处理",
    "task.spatial-generation": "空间音频生成",
    "task.spatial-mixing": "空间混音",
    "task.spatial-rendering": "空间渲染",
    "task.hrtf-personalization": "HRTF 个性化",
    "task.spatial-evaluation": "空间音频评测",
    "effect.gain": "增益",
    "effect.equalization": "均衡",
    "effect.compression": "压缩",
    "effect.distortion": "失真",
    "effect.reverberation": "混响",
    "effect.delay": "延迟",
    "effect.modulation": "调制",
    "effect.stereo": "立体声",
    "effect.filtering": "滤波",
    "effect.multi-effect": "多效果",
    "effect.other": "其他"
  }
};

const state = {
  language: getInitialLanguage(),
  projects: [],
  datasets: [],
  resources: [],
  papers: [],
  loaded: false,
  pages: {
    projects: 1,
    datasets: 1,
    papers: 1
  },
  activeProjectId: null,
  activeDatasetId: null,
  activePaperId: null
};

const elements = {
  projectRows: document.querySelector("#project-rows"),
  projectSearch: document.querySelector("#project-search"),
  projectArea: document.querySelector("#project-area-filter"),
  projectControl: document.querySelector("#project-control-filter"),
  projectTrack: document.querySelector("#project-track-filter"),
  projectLicense: document.querySelector("#project-license-filter"),
  projectCapability: document.querySelector("#project-capability-filter"),
  projectStatus: document.querySelector("#project-status-filter"),
  projectTask: document.querySelector("#project-task-filter"),
  projectEffect: document.querySelector("#project-effect-filter"),
  projectTaskControl: document.querySelector("#project-task-control"),
  projectEffectControl: document.querySelector("#project-effect-control"),
  projectFilterReset: document.querySelector("#project-filter-reset"),
  projectCount: document.querySelector("#project-count"),
  projectPagination: document.querySelector("#project-pagination"),
  projectPrevious: document.querySelector("#project-previous"),
  projectPage: document.querySelector("#project-page"),
  projectNext: document.querySelector("#project-next"),
  datasetRows: document.querySelector("#dataset-rows"),
  datasetSearch: document.querySelector("#dataset-search"),
  datasetArea: document.querySelector("#dataset-area-filter"),
  datasetTask: document.querySelector("#dataset-task-filter"),
  datasetContent: document.querySelector("#dataset-content-filter"),
  datasetAccess: document.querySelector("#dataset-access-filter"),
  datasetFilterReset: document.querySelector("#dataset-filter-reset"),
  datasetCount: document.querySelector("#dataset-count"),
  datasetPagination: document.querySelector("#dataset-pagination"),
  datasetPrevious: document.querySelector("#dataset-previous"),
  datasetPage: document.querySelector("#dataset-page"),
  datasetNext: document.querySelector("#dataset-next"),
  resourceList: document.querySelector("#resource-list"),
  paperList: document.querySelector("#paper-list"),
  paperSearch: document.querySelector("#paper-search"),
  paperArea: document.querySelector("#paper-area-filter"),
  paperControl: document.querySelector("#paper-control-filter"),
  paperTrack: document.querySelector("#paper-track-filter"),
  paperRecognition: document.querySelector("#paper-recognition-filter"),
  paperCount: document.querySelector("#paper-count"),
  paperPagination: document.querySelector("#paper-pagination"),
  paperPrevious: document.querySelector("#paper-previous"),
  paperPage: document.querySelector("#paper-page"),
  paperNext: document.querySelector("#paper-next"),
  heroProjectCount: document.querySelector("#hero-project-count"),
  heroDatasetCount: document.querySelector("#hero-dataset-count"),
  heroPaperCount: document.querySelector("#hero-paper-count"),
  fieldPaperLinks: document.querySelectorAll(".field-map-link"),
  projectDialog: document.querySelector("#project-dialog"),
  projectDialogClose: document.querySelector("#project-dialog-close"),
  projectDialogContent: document.querySelector("#project-dialog-content"),
  datasetDialog: document.querySelector("#dataset-dialog"),
  datasetDialogClose: document.querySelector("#dataset-dialog-close"),
  datasetDialogContent: document.querySelector("#dataset-dialog-content"),
  paperDialog: document.querySelector("#paper-dialog"),
  paperDialogClose: document.querySelector("#paper-dialog-close"),
  paperDialogContent: document.querySelector("#paper-dialog-content")
};

const availabilityCapabilities = ["source", "checkpoint", "inference", "training", "dataset"];
const availabilityStatuses = ["linked", "documented", "tested", "gated", "restricted", "not-found", "not-applicable", "not-reviewed"];
const datasetAccessStatuses = ["direct-download", "request", "registration", "restricted", "unavailable", "not-reviewed"];
const controlApproaches = ["gradient-based-optimization", "derivative-free-optimization", "direct-prediction"];
const trackScopes = ["single-track", "multitrack"];
const PAGE_SIZE = 10;

function getInitialLanguage() {
  try {
    const saved = localStorage.getItem("iap-language");
    if (saved === "en" || saved === "zh") return saved;
  } catch (_) {
    // Storage can be unavailable in strict privacy modes.
  }
  return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
}

function t(key) {
  return translations[state.language][key] ?? translations.en[key] ?? key;
}

function localized(value) {
  if (typeof value === "string") return value;
  return value?.[state.language] ?? value?.en ?? "";
}

function createTextElement(tagName, className, text) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  element.textContent = text;
  return element;
}

function isArxivLink(item) {
  try {
    return new URL(item.url).hostname.toLowerCase().endsWith("arxiv.org");
  } catch (_) {
    return false;
  }
}

function linkLabel(item) {
  if (item.label === "paper" && isArxivLink(item)) return "arXiv";
  const translated = t(`link.${item.label}`);
  return translated === `link.${item.label}` ? item.label : translated;
}

function createLinkList(links, className = "") {
  const list = document.createElement("div");
  list.className = ["link-list", className].filter(Boolean).join(" ");
  links.forEach((item) => {
    const link = document.createElement("a");
    link.href = item.url;
    link.textContent = linkLabel(item);
    link.target = "_blank";
    link.rel = "noreferrer";
    list.append(link);
  });
  return list;
}

function createTagList(areas, tagName = "div") {
  const list = document.createElement(tagName);
  list.className = "tag-list";
  areas.forEach((area) => list.append(createTextElement("span", "tag", t(`area.${area}`))));
  return list;
}

function paperControlApproaches(paper) {
  return Array.isArray(paper.controlApproaches) ? paper.controlApproaches : [];
}

function projectControlApproaches(project) {
  const values = project.relations.paperIds.flatMap((paperId) => {
    const paper = state.papers.find((item) => item.id === paperId);
    return paper ? paperControlApproaches(paper) : [];
  });
  return [...new Set(values)];
}

function createControlApproachList(values, tagName = "div") {
  const list = document.createElement(tagName);
  list.className = "tag-list control-approach-list";
  values.forEach((value) => list.append(createTextElement("span", "tag control-tag", t(`control.${value}`))));
  return list;
}

function paperTrackScopes(paper) {
  return Array.isArray(paper.trackScopes) ? paper.trackScopes : [];
}

function projectTrackScopes(project) {
  const values = project.relations.paperIds.flatMap((paperId) => {
    const paper = state.papers.find((item) => item.id === paperId);
    return paper ? paperTrackScopes(paper) : [];
  });
  return [...new Set(values)];
}

function createTrackScopeList(values, tagName = "div") {
  const list = document.createElement(tagName);
  list.className = "tag-list track-scope-list";
  values.forEach((value) => list.append(createTextElement("span", "tag track-tag", t(`track.${value}`))));
  return list;
}

function createRecognitionBadges(paper, tagName = "span") {
  const list = document.createElement(tagName);
  list.className = "recognition-badges";
  if (paper.aiAssessment?.rating === "highlighted") {
    list.append(createTextElement("span", "recognition-badge ai-highlight-badge", t("recognition.aiHighlight")));
  }
  if (paper.impact?.status === "high-impact") {
    list.append(createTextElement("span", "recognition-badge high-impact-badge", t("recognition.highImpact")));
  }
  return list;
}

function matchesRecognition(paper, recognition) {
  if (recognition === "ai-highlight") return paper.aiAssessment?.rating === "highlighted";
  if (recognition === "high-impact") return paper.impact?.status === "high-impact";
  return true;
}

function paginate(items, collection) {
  const totalPages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));
  state.pages[collection] = Math.min(Math.max(state.pages[collection], 1), totalPages);
  const startIndex = (state.pages[collection] - 1) * PAGE_SIZE;
  return {
    items: items.slice(startIndex, startIndex + PAGE_SIZE),
    start: items.length ? startIndex + 1 : 0,
    end: Math.min(startIndex + PAGE_SIZE, items.length),
    page: state.pages[collection],
    totalPages
  };
}

function updatePagination(collection, pagination) {
  const refs = {
    projects: [elements.projectPagination, elements.projectPrevious, elements.projectPage, elements.projectNext],
    datasets: [elements.datasetPagination, elements.datasetPrevious, elements.datasetPage, elements.datasetNext],
    papers: [elements.paperPagination, elements.paperPrevious, elements.paperPage, elements.paperNext]
  }[collection];
  const [container, previous, status, next] = refs;
  container.hidden = pagination.totalPages <= 1;
  previous.disabled = pagination.page <= 1;
  next.disabled = pagination.page >= pagination.totalPages;
  status.textContent = state.language === "zh"
    ? `第 ${pagination.page} / ${pagination.totalPages} 页`
    : `Page ${pagination.page} of ${pagination.totalPages}`;
}

function updateResultCount(element, collection, pagination, filteredCount, totalCount) {
  const nouns = {
    projects: ["project", "projects", "个项目"],
    datasets: ["dataset", "datasets", "个数据集"],
    papers: ["paper", "papers", "篇论文"]
  }[collection];
  if (state.language === "zh") {
    element.textContent = filteredCount === totalCount
      ? `显示 ${pagination.start}-${pagination.end}，共 ${totalCount} ${nouns[2]}`
      : `显示 ${pagination.start}-${pagination.end}，筛选结果 ${filteredCount} ${nouns[2]}（总计 ${totalCount}）`;
    return;
  }
  const noun = filteredCount === 1 ? nouns[0] : nouns[1];
  element.textContent = filteredCount === totalCount
    ? `Showing ${pagination.start}-${pagination.end} of ${totalCount} ${noun}`
    : `Showing ${pagination.start}-${pagination.end} of ${filteredCount} matching ${noun} (${totalCount} total)`;
}

function resetPageAndRender(collection, render) {
  state.pages[collection] = 1;
  render();
}

function changePage(collection, delta, render) {
  state.pages[collection] += delta;
  render();
  document.querySelector(`#${collection}`).scrollIntoView({ behavior: "smooth", block: "start" });
}

function populateAreaFilter(select, items) {
  const selected = select.value || "all";
  const areas = [...new Set(items.flatMap((item) => item.areas))].sort((a, b) => t(`area.${a}`).localeCompare(t(`area.${b}`), state.language));
  select.replaceChildren();
  const all = document.createElement("option");
  all.value = "all";
  all.textContent = t("controls.allAreas");
  select.append(all);
  areas.forEach((area) => {
    const option = document.createElement("option");
    option.value = area;
    option.textContent = t(`area.${area}`);
    select.append(option);
  });
  select.value = areas.includes(selected) ? selected : "all";
}

function populateSelect(select, values, allLabelKey, labelForValue) {
  const selected = select.value || "all";
  select.replaceChildren();
  const all = document.createElement("option");
  all.value = "all";
  all.textContent = t(allLabelKey);
  select.append(all);
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labelForValue(value);
    select.append(option);
  });
  select.value = values.includes(selected) ? selected : "all";
}

function projectLicenseFilterValue(project) {
  if (project.license.spdx) return `spdx:${project.license.spdx}`;
  if (project.license.status === "not-verified") return "status:not-verified";
  return `name:${project.license.en}`;
}

function populateProjectLicenseFilter() {
  const selected = elements.projectLicense.value || "all";
  const options = new Map();
  state.projects.forEach((project) => {
    const value = projectLicenseFilterValue(project);
    const label = value === "status:not-verified"
      ? t("license.status.not-verified")
      : project.license.spdx ?? localized(project.license);
    options.set(value, label);
  });

  const sortedOptions = [...options.entries()].sort(([, left], [, right]) => left.localeCompare(right, state.language));
  elements.projectLicense.replaceChildren();
  const all = document.createElement("option");
  all.value = "all";
  all.textContent = t("controls.allLicenses");
  elements.projectLicense.append(all);
  sortedOptions.forEach(([value, label]) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    elements.projectLicense.append(option);
  });
  elements.projectLicense.value = options.has(selected) ? selected : "all";
}

function reviewedTaxonomyValues(field) {
  return [...new Set(
    state.projects
      .filter((project) => project.taxonomy?.reviewStatus === "reviewed")
      .flatMap((project) => project.taxonomy?.[field] ?? [])
  )].sort((a, b) => t(`${field === "tasks" ? "task" : "effect"}.${a}`).localeCompare(
    t(`${field === "tasks" ? "task" : "effect"}.${b}`),
    state.language
  ));
}

function populateProjectFilters() {
  populateAreaFilter(elements.projectArea, state.projects);
  const projectApproaches = controlApproaches.filter((approach) => (
    state.projects.some((project) => projectControlApproaches(project).includes(approach))
  ));
  populateSelect(
    elements.projectControl,
    projectApproaches,
    "controls.allControlApproaches",
    (approach) => t(`control.${approach}`)
  );
  const availableTrackScopes = trackScopes.filter((scope) => (
    state.projects.some((project) => projectTrackScopes(project).includes(scope))
  ));
  populateSelect(
    elements.projectTrack,
    availableTrackScopes,
    "controls.allTrackScopes",
    (scope) => t(`track.${scope}`)
  );
  populateProjectLicenseFilter();
  populateSelect(elements.projectCapability, availabilityCapabilities, "controls.allCapabilities", (capability) => t(`availability.${capability}`));
  populateSelect(elements.projectStatus, availabilityStatuses, "controls.allStatuses", (status) => t(`availability.status.${status}`));

  const taskValues = reviewedTaxonomyValues("tasks");
  const effectValues = reviewedTaxonomyValues("effects");
  elements.projectTaskControl.hidden = taskValues.length === 0;
  elements.projectEffectControl.hidden = effectValues.length === 0;
  populateSelect(elements.projectTask, taskValues, "controls.allTasks", (task) => t(`task.${task}`));
  populateSelect(elements.projectEffect, effectValues, "controls.allEffects", (effect) => t(`effect.${effect}`));
}

function datasetTaxonomyValues(field) {
  const prefix = field === "tasks" ? "task" : "content";
  return [...new Set(state.datasets.flatMap((dataset) => dataset.taxonomy[field]))]
    .sort((left, right) => t(`${prefix}.${left}`).localeCompare(t(`${prefix}.${right}`), state.language));
}

function populateDatasetFilters() {
  populateAreaFilter(elements.datasetArea, state.datasets);
  populateSelect(elements.datasetTask, datasetTaxonomyValues("tasks"), "controls.allTasks", (task) => t(`task.${task}`));
  populateSelect(
    elements.datasetContent,
    datasetTaxonomyValues("contentTypes"),
    "controls.allContentTypes",
    (contentType) => t(`content.${contentType}`)
  );
  const availableStatuses = datasetAccessStatuses.filter((status) => state.datasets.some((dataset) => dataset.access.status === status));
  populateSelect(
    elements.datasetAccess,
    availableStatuses,
    "controls.allAccessTypes",
    (status) => t(`dataset.access.${status}`)
  );
}

function updateFieldPaperLinks() {
  elements.fieldPaperLinks.forEach((link) => {
    const area = link.dataset.paperArea;
    const areaName = t(`area.${area}`);
    if (!state.loaded) {
      const label = t("scope.viewPapers");
      link.querySelector(".field-paper-count").textContent = label;
      link.setAttribute("aria-label", `${label}: ${areaName}`);
      return;
    }
    const count = state.papers.filter((paper) => paper.areas.includes(area)).length;
    const label = state.language === "zh"
      ? `查看 ${count} 篇论文`
      : `View ${count} ${count === 1 ? "paper" : "papers"}`;
    link.querySelector(".field-paper-count").textContent = label;
    link.setAttribute("aria-label", `${label}: ${areaName}`);
  });
}

function updateCatalogueStats() {
  if (!state.loaded) return;
  elements.heroProjectCount.textContent = state.projects.length;
  elements.heroDatasetCount.textContent = state.datasets.length;
  elements.heroPaperCount.textContent = state.papers.length;
}

function showPapersForArea(area) {
  if (!state.papers.some((paper) => paper.areas.includes(area))) return;
  elements.paperSearch.value = "";
  elements.paperArea.value = area;
  elements.paperControl.value = "all";
  elements.paperTrack.value = "all";
  elements.paperRecognition.value = "all";
  state.pages.papers = 1;
  renderPapers();
  document.querySelector("#papers").scrollIntoView({ behavior: "smooth", block: "start" });
}

function createProjectRow(project) {
  const row = document.createElement("tr");
  const projectCell = document.createElement("td");
  const button = document.createElement("button");
  button.className = "project-open";
  button.type = "button";
  button.setAttribute("aria-haspopup", "dialog");
  button.setAttribute("aria-controls", "project-dialog");
  button.setAttribute("aria-label", `${t("projects.openDetails")}: ${project.name}`);
  button.addEventListener("click", () => openProjectDialog(project));
  button.append(
    createTextElement("span", "project-name", project.name),
    createTextElement("span", "project-description", localized(project.description))
  );
  projectCell.append(button);

  const areaCell = document.createElement("td");
  areaCell.append(createTagList(project.areas));
  const linksCell = document.createElement("td");
  linksCell.append(createLinkList(project.links));

  row.append(
    projectCell,
    areaCell,
    linksCell,
    createTextElement("td", "", localized(project.license)),
    createTextElement("td", "", project.lastVerified)
  );
  return row;
}

function renderProjects() {
  const query = elements.projectSearch.value.trim().toLocaleLowerCase(state.language);
  const selectedArea = elements.projectArea.value;
  const selectedControl = elements.projectControl.value;
  const selectedTrack = elements.projectTrack.value;
  const selectedLicense = elements.projectLicense.value;
  const selectedCapability = elements.projectCapability.value;
  const selectedStatus = elements.projectStatus.value;
  const selectedTask = elements.projectTask.value;
  const selectedEffect = elements.projectEffect.value;
  const filtered = state.projects.filter((project) => {
    const approaches = projectControlApproaches(project);
    const scopes = projectTrackScopes(project);
    const matchesArea = selectedArea === "all" || project.areas.includes(selectedArea);
    const matchesControl = selectedControl === "all" || approaches.includes(selectedControl);
    const matchesTrack = selectedTrack === "all" || scopes.includes(selectedTrack);
    const matchesLicense = selectedLicense === "all" || projectLicenseFilterValue(project) === selectedLicense;
    const availabilityEntries = availabilityCapabilities.map((capability) => [capability, project.availability[capability]]);
    const matchesCapability = selectedCapability === "all"
      || (
        project.availability[selectedCapability]
        && (
          selectedStatus === "all"
            ? project.availability[selectedCapability].status !== "not-reviewed"
            : project.availability[selectedCapability].status === selectedStatus
        )
      );
    const matchesStatus = selectedStatus === "all"
      || (
        selectedCapability === "all"
          ? availabilityEntries.some(([, entry]) => entry.status === selectedStatus)
          : matchesCapability
      );
    const matchesTask = selectedTask === "all" || project.taxonomy?.tasks?.includes(selectedTask);
    const matchesEffect = selectedEffect === "all" || project.taxonomy?.effects?.includes(selectedEffect);
    const searchable = [
      project.name,
      project.description.en,
      project.description.zh,
      localized(project.license),
      t(`license.status.${project.license.status}`),
      ...project.areas.map((area) => t(`area.${area}`)),
      ...(project.taxonomy?.tasks ?? []).map((task) => t(`task.${task}`)),
      ...(project.taxonomy?.effects ?? []).map((effect) => t(`effect.${effect}`)),
      ...approaches.map((approach) => t(`control.${approach}`)),
      ...scopes.map((scope) => t(`track.${scope}`)),
      ...availabilityEntries.flatMap(([capability, entry]) => [t(`availability.${capability}`), t(`availability.status.${entry.status}`)])
    ]
      .join(" ")
      .toLocaleLowerCase(state.language);
    return matchesArea && matchesControl && matchesTrack && matchesLicense && matchesCapability && matchesStatus && matchesTask && matchesEffect && searchable.includes(query);
  });
  const pagination = paginate(filtered, "projects");

  elements.projectRows.replaceChildren();
  if (filtered.length === 0) {
    const row = document.createElement("tr");
    const cell = createTextElement("td", "empty", t("projects.empty"));
    cell.colSpan = 5;
    row.append(cell);
    elements.projectRows.append(row);
  } else {
    pagination.items.forEach((project) => elements.projectRows.append(createProjectRow(project)));
  }
  updateResultCount(elements.projectCount, "projects", pagination, filtered.length, state.projects.length);
  updatePagination("projects", pagination);
}

function createEvidenceLinks(urls) {
  if (!urls?.length) return createTextElement("p", "dialog-empty", t("projects.noEvidence"));
  const links = urls.map((url, index) => ({
    label: `${t("projects.evidenceLabel")} ${index + 1}`,
    url
  }));
  return createLinkList(links, "paper-dialog-links");
}

function createLabeledValue(label, value) {
  const item = document.createElement("div");
  item.className = "project-fact";
  item.append(
    createTextElement("dt", "", label),
    createTextElement("dd", "", value)
  );
  return item;
}

function createTokenList(values, prefix, emptyText) {
  if (!values.length) return createTextElement("p", "dialog-empty", emptyText);
  const list = document.createElement("div");
  list.className = "tag-list";
  values.forEach((value) => list.append(createTextElement("span", "tag", t(`${prefix}.${value}`))));
  return list;
}

function appendProjectDialogSection(container, title, body) {
  const section = document.createElement("section");
  section.className = "paper-dialog-section";
  section.append(createTextElement("h3", "", title), body);
  container.append(section);
}

function createRelatedPapers(project) {
  const related = project.relations.paperIds
    .map((paperId) => state.papers.find((paper) => paper.id === paperId))
    .filter(Boolean);
  if (!related.length) return createTextElement("p", "dialog-empty", t("projects.noRelatedPapers"));
  const list = document.createElement("div");
  list.className = "related-paper-list";
  related.forEach((paper) => {
    const paperLink = paper.links.find((link) => link.label === "paper" || link.label === "doi") ?? paper.links[0];
    const link = document.createElement("a");
    link.href = paperLink.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = paper.title;
    list.append(link);
  });
  return list;
}

function createLicenseDetails(project) {
  const wrapper = document.createElement("div");
  wrapper.className = "project-detail-stack";
  const facts = document.createElement("dl");
  facts.className = "project-facts";
  facts.append(
    createLabeledValue(t("projects.licenseLabel"), localized(project.license)),
    createLabeledValue(t("projects.licenseStatusLabel"), t(`license.status.${project.license.status}`)),
    createLabeledValue(t("projects.spdxLabel"), project.license.spdx ?? "—")
  );
  wrapper.append(facts, createEvidenceLinks(project.license.evidenceUrl ? [project.license.evidenceUrl] : []));
  return wrapper;
}

function createAvailabilityDetails(project) {
  const list = document.createElement("div");
  list.className = "availability-list";
  availabilityCapabilities.forEach((capability) => {
    const entry = project.availability[capability];
    const item = document.createElement("div");
    item.className = "availability-item";
    const heading = document.createElement("div");
    heading.className = "availability-heading";
    heading.append(
      createTextElement("strong", "", t(`availability.${capability}`)),
      createTextElement("span", `availability-status status-${entry.status}`, t(`availability.status.${entry.status}`))
    );
    item.append(heading, createEvidenceLinks(entry.evidence));
    list.append(item);
  });
  return list;
}

function createTaxonomyDetails(project) {
  const wrapper = document.createElement("div");
  wrapper.className = "project-detail-stack";
  if (project.taxonomy.reviewStatus !== "reviewed") {
    wrapper.append(createTextElement("p", "dialog-empty", t("projects.noReviewedTaxonomy")));
    return wrapper;
  }
  const groups = document.createElement("div");
  groups.className = "taxonomy-groups";
  const tasks = document.createElement("div");
  tasks.append(
    createTextElement("h4", "", t("projects.tasksLabel")),
    createTokenList(project.taxonomy.tasks, "task", t("projects.noReviewedTaxonomy"))
  );
  const effects = document.createElement("div");
  effects.append(
    createTextElement("h4", "", t("projects.effectsLabel")),
    createTokenList(project.taxonomy.effects, "effect", t("projects.noReviewedTaxonomy"))
  );
  groups.append(tasks, effects);
  wrapper.append(groups, createEvidenceLinks(project.taxonomy.evidence));
  return wrapper;
}

function renderProjectDialog(project) {
  const heading = document.createElement("div");
  heading.className = "paper-dialog-heading";
  heading.append(
    createTextElement("h2", "", project.name),
    createTextElement("p", "paper-dialog-summary", localized(project.description)),
    createTagList(project.areas)
  );

  const facts = document.createElement("dl");
  facts.className = "project-facts";
  facts.append(createLabeledValue(t("projects.verifiedLabel"), project.lastVerified));

  elements.projectDialogContent.replaceChildren(heading, facts);
  const approaches = projectControlApproaches(project);
  if (approaches.length) {
    appendProjectDialogSection(
      elements.projectDialogContent,
      t("projects.controlApproachesLabel"),
      createControlApproachList(approaches)
    );
  }
  const scopes = projectTrackScopes(project);
  if (scopes.length) {
    appendProjectDialogSection(
      elements.projectDialogContent,
      t("projects.trackScopesLabel"),
      createTrackScopeList(scopes)
    );
  }
  appendProjectDialogSection(elements.projectDialogContent, t("projects.relatedPapersLabel"), createRelatedPapers(project));
  appendProjectDialogSection(
    elements.projectDialogContent,
    t("datasets.usedDatasetsLabel"),
    createRelatedDatasets(project.id, "projects")
  );
  appendProjectDialogSection(elements.projectDialogContent, t("projects.licenseLabel"), createLicenseDetails(project));
  appendProjectDialogSection(elements.projectDialogContent, t("projects.availabilityLabel"), createAvailabilityDetails(project));
  appendProjectDialogSection(elements.projectDialogContent, t("projects.taxonomyLabel"), createTaxonomyDetails(project));
  appendProjectDialogSection(elements.projectDialogContent, t("projects.linksLabel"), createLinkList(project.links, "paper-dialog-links"));
}

function openProjectDialog(project) {
  state.activeProjectId = project.id;
  renderProjectDialog(project);
  if (typeof elements.projectDialog.showModal === "function") {
    if (!elements.projectDialog.open) elements.projectDialog.showModal();
  } else {
    elements.projectDialog.setAttribute("open", "");
  }
}

function closeProjectDialog() {
  if (typeof elements.projectDialog.close === "function") {
    elements.projectDialog.close();
  } else {
    elements.projectDialog.removeAttribute("open");
    state.activeProjectId = null;
  }
}

function datasetUsageLabel(dataset) {
  const paperCount = dataset.relations.papers.length;
  const projectCount = dataset.relations.projects.length;
  if (state.language === "zh") {
    return `${paperCount} ${t("datasets.paperCount")} · ${projectCount} ${t("datasets.projectCount")}`;
  }
  return `${paperCount} ${paperCount === 1 ? "paper" : t("datasets.paperCount")} · ${projectCount} ${projectCount === 1 ? "project" : t("datasets.projectCount")}`;
}

function createDatasetRow(dataset) {
  const row = document.createElement("tr");
  const datasetCell = document.createElement("td");
  const button = document.createElement("button");
  button.className = "project-open";
  button.type = "button";
  button.setAttribute("aria-haspopup", "dialog");
  button.setAttribute("aria-controls", "dataset-dialog");
  button.setAttribute("aria-label", `${t("datasets.openDetails")}: ${dataset.name}`);
  button.addEventListener("click", () => openDatasetDialog(dataset));
  button.append(
    createTextElement("span", "project-name", dataset.name),
    createTextElement("span", "project-description", localized(dataset.description))
  );
  datasetCell.append(button);

  const areaCell = document.createElement("td");
  areaCell.append(createTagList(dataset.areas));
  const contentCell = document.createElement("td");
  contentCell.append(createTokenList(dataset.taxonomy.contentTypes, "content", ""));
  const accessCell = document.createElement("td");
  accessCell.append(createTextElement(
    "span",
    `availability-status status-${dataset.access.status}`,
    t(`dataset.access.${dataset.access.status}`)
  ));

  row.append(
    datasetCell,
    areaCell,
    contentCell,
    accessCell,
    createTextElement("td", "dataset-usage", datasetUsageLabel(dataset)),
    createTextElement("td", "", dataset.lastVerified)
  );
  return row;
}

function renderDatasets() {
  const query = elements.datasetSearch.value.trim().toLocaleLowerCase(state.language);
  const selectedArea = elements.datasetArea.value;
  const selectedTask = elements.datasetTask.value;
  const selectedContent = elements.datasetContent.value;
  const selectedAccess = elements.datasetAccess.value;
  const filtered = state.datasets.filter((dataset) => {
    const matchesArea = selectedArea === "all" || dataset.areas.includes(selectedArea);
    const matchesTask = selectedTask === "all" || dataset.taxonomy.tasks.includes(selectedTask);
    const matchesContent = selectedContent === "all" || dataset.taxonomy.contentTypes.includes(selectedContent);
    const matchesAccess = selectedAccess === "all" || dataset.access.status === selectedAccess;
    const searchable = [
      dataset.name,
      dataset.description.en,
      dataset.description.zh,
      dataset.scale.en,
      dataset.scale.zh,
      dataset.license.en,
      dataset.license.zh,
      t(`dataset.access.${dataset.access.status}`),
      ...dataset.areas.map((area) => t(`area.${area}`)),
      ...dataset.taxonomy.tasks.map((task) => t(`task.${task}`)),
      ...dataset.taxonomy.effects.map((effect) => t(`effect.${effect}`)),
      ...dataset.taxonomy.contentTypes.map((contentType) => t(`content.${contentType}`))
    ].join(" ").toLocaleLowerCase(state.language);
    return matchesArea && matchesTask && matchesContent && matchesAccess && searchable.includes(query);
  });
  const pagination = paginate(filtered, "datasets");

  elements.datasetRows.replaceChildren();
  if (!filtered.length) {
    const row = document.createElement("tr");
    const cell = createTextElement("td", "empty", t("datasets.empty"));
    cell.colSpan = 6;
    row.append(cell);
    elements.datasetRows.append(row);
  } else {
    pagination.items.forEach((dataset) => elements.datasetRows.append(createDatasetRow(dataset)));
  }
  updateResultCount(elements.datasetCount, "datasets", pagination, filtered.length, state.datasets.length);
  updatePagination("datasets", pagination);
}

function createDatasetRelationList(relations, type) {
  if (!relations.length) {
    return createTextElement(
      "p",
      "dialog-empty",
      t(type === "papers" ? "datasets.noRelatedPapers" : "datasets.noRelatedProjects")
    );
  }
  const list = document.createElement("div");
  list.className = "dataset-relation-list";
  relations.forEach((relation) => {
    const record = type === "papers"
      ? state.papers.find((paper) => paper.id === relation.id)
      : state.projects.find((project) => project.id === relation.id);
    if (!record) return;
    const row = document.createElement("div");
    row.className = "dataset-relation-item";
    const openButton = document.createElement("button");
    openButton.type = "button";
    openButton.className = "dataset-relation-open";
    openButton.textContent = type === "papers" ? record.title : record.name;
    openButton.addEventListener("click", () => {
      closeDatasetDialog();
      if (type === "papers") openPaperDialog(record);
      else openProjectDialog(record);
    });
    const evidence = document.createElement("a");
    evidence.href = relation.evidenceUrl;
    evidence.target = "_blank";
    evidence.rel = "noreferrer";
    evidence.textContent = t("projects.evidenceLabel");
    row.append(openButton, evidence);
    list.append(row);
  });
  return list;
}

function createRelatedDatasets(recordId, type) {
  const related = state.datasets
    .map((dataset) => ({
      dataset,
      relation: dataset.relations[type].find((item) => item.id === recordId)
    }))
    .filter((item) => item.relation);
  if (!related.length) return createTextElement("p", "dialog-empty", t("datasets.noRelatedDatasets"));

  const list = document.createElement("div");
  list.className = "dataset-relation-list";
  related.forEach(({ dataset, relation }) => {
    const row = document.createElement("div");
    row.className = "dataset-relation-item";
    const openButton = document.createElement("button");
    openButton.type = "button";
    openButton.className = "dataset-relation-open";
    openButton.textContent = dataset.name;
    openButton.addEventListener("click", () => {
      if (type === "papers") closePaperDialog();
      else closeProjectDialog();
      openDatasetDialog(dataset);
    });
    const evidence = document.createElement("a");
    evidence.href = relation.evidenceUrl;
    evidence.target = "_blank";
    evidence.rel = "noreferrer";
    evidence.textContent = t("projects.evidenceLabel");
    row.append(openButton, evidence);
    list.append(row);
  });
  return list;
}

function createDatasetTaxonomy(dataset) {
  const wrapper = document.createElement("div");
  wrapper.className = "project-detail-stack";
  const groups = document.createElement("div");
  groups.className = "taxonomy-groups dataset-taxonomy-groups";
  const tasks = document.createElement("div");
  tasks.append(
    createTextElement("h4", "", t("projects.tasksLabel")),
    createTokenList(dataset.taxonomy.tasks, "task", "")
  );
  const effects = document.createElement("div");
  effects.append(
    createTextElement("h4", "", t("projects.effectsLabel")),
    createTokenList(dataset.taxonomy.effects, "effect", "—")
  );
  const contents = document.createElement("div");
  contents.append(
    createTextElement("h4", "", t("datasets.contentTypesLabel")),
    createTokenList(dataset.taxonomy.contentTypes, "content", "")
  );
  groups.append(tasks, effects, contents);
  wrapper.append(groups, createEvidenceLinks(dataset.taxonomy.evidence));
  return wrapper;
}

function renderDatasetDialog(dataset) {
  const heading = document.createElement("div");
  heading.className = "paper-dialog-heading";
  heading.append(
    createTextElement("h2", "", dataset.name),
    createTextElement("p", "paper-dialog-summary", localized(dataset.description)),
    createTagList(dataset.areas)
  );

  const facts = document.createElement("dl");
  facts.className = "project-facts dataset-facts";
  facts.append(
    createLabeledValue(t("datasets.scaleLabel"), localized(dataset.scale)),
    createLabeledValue(t("datasets.accessLabel"), t(`dataset.access.${dataset.access.status}`)),
    createLabeledValue(t("datasets.licenseLabel"), localized(dataset.license)),
    createLabeledValue(t("datasets.verifiedLabel"), dataset.lastVerified)
  );

  elements.datasetDialogContent.replaceChildren(heading, facts);
  appendProjectDialogSection(
    elements.datasetDialogContent,
    t("datasets.relatedPapersLabel"),
    createDatasetRelationList(dataset.relations.papers, "papers")
  );
  appendProjectDialogSection(
    elements.datasetDialogContent,
    t("datasets.relatedProjectsLabel"),
    createDatasetRelationList(dataset.relations.projects, "projects")
  );
  appendProjectDialogSection(elements.datasetDialogContent, t("datasets.taxonomyLabel"), createDatasetTaxonomy(dataset));

  const evidence = [...new Set([dataset.access.evidenceUrl, dataset.license.evidenceUrl].filter(Boolean))];
  appendProjectDialogSection(elements.datasetDialogContent, t("projects.evidenceLabel"), createEvidenceLinks(evidence));
  appendProjectDialogSection(
    elements.datasetDialogContent,
    t("datasets.linksLabel"),
    createLinkList(dataset.links, "paper-dialog-links")
  );
}

function openDatasetDialog(dataset) {
  state.activeDatasetId = dataset.id;
  renderDatasetDialog(dataset);
  if (typeof elements.datasetDialog.showModal === "function") {
    if (!elements.datasetDialog.open) elements.datasetDialog.showModal();
  } else {
    elements.datasetDialog.setAttribute("open", "");
  }
}

function closeDatasetDialog() {
  if (typeof elements.datasetDialog.close === "function") {
    elements.datasetDialog.close();
  } else {
    elements.datasetDialog.removeAttribute("open");
    state.activeDatasetId = null;
  }
}

function createResourceEntry(resource) {
  const article = document.createElement("article");
  article.className = "resource-entry";

  const identity = document.createElement("div");
  identity.className = "resource-identity";
  identity.append(
    createTextElement("span", "resource-kind", t(`resources.kind.${resource.kind}`)),
    createTextElement("h3", "", resource.name)
  );

  const details = document.createElement("div");
  details.className = "resource-details";
  details.append(
    createTextElement("p", "", localized(resource.description)),
    createTagList(resource.areas),
    createLinkList(resource.links, "resource-links")
  );
  article.append(identity, details);
  return article;
}

function renderResources() {
  elements.resourceList.replaceChildren();
  state.resources.forEach((resource) => elements.resourceList.append(createResourceEntry(resource)));
}

function createPaperEntry(paper) {
  const article = document.createElement("article");
  article.className = "paper-entry";

  const button = document.createElement("button");
  button.className = "paper-open";
  button.type = "button";
  button.setAttribute("aria-haspopup", "dialog");
  button.setAttribute("aria-controls", "paper-dialog");
  button.setAttribute("aria-label", `${t("papers.openDetails")}: ${paper.title}`);
  button.addEventListener("click", () => openPaperDialog(paper));

  const heading = document.createElement("span");
  heading.className = "paper-heading";
  const identity = document.createElement("span");
  identity.className = "paper-identity";
  if (paper.shortName) {
    identity.append(createTextElement("span", "paper-short-name", paper.shortName));
  }
  const title = createTextElement("span", "paper-title", paper.title);
  identity.append(title);
  const metadata = createTextElement("span", "paper-meta", `${paper.venue} · ${paper.published}`);
  heading.append(identity, metadata);

  const authors = createTextElement("span", "paper-authors", paper.authors.join(", "));
  const details = document.createElement("span");
  details.className = "paper-details";
  details.append(createTagList(paper.areas, "span"));
  if (paperControlApproaches(paper).length) {
    details.append(createControlApproachList(paperControlApproaches(paper), "span"));
  }
  if (paperTrackScopes(paper).length) {
    details.append(createTrackScopeList(paperTrackScopes(paper), "span"));
  }
  const recognitionBadges = createRecognitionBadges(paper);
  if (recognitionBadges.childElementCount) details.append(recognitionBadges);
  if (paper.curation === "agent") {
    details.append(createTextElement("span", "agent-badge", t("papers.automated")));
  }
  if (paper.links.some((link) => link.label === "source")) {
    details.append(createTextElement("span", "source-badge", t("papers.openSourceAvailable")));
  }
  details.append(createTextElement("span", "paper-open-label", t("papers.openDetails")));

  button.append(heading, authors, details);
  article.append(button);
  return article;
}

function appendDialogSection(container, title, links, emptyMessage) {
  const section = document.createElement("section");
  section.className = "paper-dialog-section";
  section.append(createTextElement("h3", "", title));
  if (links.length) {
    section.append(createLinkList(links, "paper-dialog-links"));
  } else {
    section.append(createTextElement("p", "dialog-empty", emptyMessage));
  }
  container.append(section);
}

function renderPaperDialog(paper) {
  const paperLinks = paper.links
    .filter((link) => link.label === "paper" || link.label === "doi")
    .sort((a, b) => Number(isArxivLink(b)) - Number(isArxivLink(a)));
  const openResourceLinks = paper.links.filter((link) => !["paper", "doi"].includes(link.label));

  const heading = document.createElement("div");
  heading.className = "paper-dialog-heading";
  if (paper.shortName) {
    heading.append(createTextElement("p", "paper-dialog-short-name", `${t("papers.shortNameLabel")}: ${paper.shortName}`));
  }
  heading.append(
    createTextElement("h2", "", paper.title),
    createTextElement("p", "paper-meta", `${paper.venue} · ${paper.published}`),
    createTextElement("p", "paper-authors", paper.authors.join(", ")),
    createTagList(paper.areas)
  );

  const summarySection = document.createElement("section");
  summarySection.className = "paper-dialog-section";
  summarySection.append(
    createTextElement("h3", "", t("papers.summaryLabel")),
    createTextElement("p", "paper-dialog-summary", localized(paper.summary))
  );

  elements.paperDialogContent.replaceChildren(heading, summarySection);
  if (paperControlApproaches(paper).length) {
    appendProjectDialogSection(
      elements.paperDialogContent,
      t("papers.controlApproachesLabel"),
      createControlApproachList(paperControlApproaches(paper))
    );
  }
  if (paperTrackScopes(paper).length) {
    appendProjectDialogSection(
      elements.paperDialogContent,
      t("papers.trackScopesLabel"),
      createTrackScopeList(paperTrackScopes(paper))
    );
  }
  const recognitionSection = document.createElement("section");
  recognitionSection.className = "paper-dialog-section recognition-details";
  recognitionSection.append(createTextElement("h3", "", t("recognition.detailsLabel")));
  if (paper.aiAssessment?.rating === "highlighted") {
    const assessment = document.createElement("div");
    assessment.className = "recognition-detail";
    assessment.append(
      createRecognitionBadges({aiAssessment: paper.aiAssessment, impact: {status: "standard"}}, "div"),
      createTextElement("p", "recognition-detail-label", t("recognition.aiRationaleLabel")),
      createTextElement("p", "paper-dialog-summary", localized(paper.aiAssessment.rationale)),
      createTextElement(
        "p",
        "recognition-meta",
        state.language === "zh"
          ? `评估模型：${paper.aiAssessment.assessor} · 规则版本 ${paper.aiAssessment.rubricVersion} · ${paper.aiAssessment.assessedAt}`
          : `Assessed by ${paper.aiAssessment.assessor} · rubric ${paper.aiAssessment.rubricVersion} · ${paper.aiAssessment.assessedAt}`
      )
    );
    recognitionSection.append(assessment);
  }
  const impact = paper.impact;
  const impactDetail = document.createElement("div");
  impactDetail.className = "recognition-detail";
  impactDetail.append(createTextElement("p", "recognition-detail-label", t("recognition.impactLabel")));
  if (impact?.status === "high-impact" || impact?.status === "standard") {
    if (impact.status === "high-impact") {
      impactDetail.prepend(createRecognitionBadges({aiAssessment: {rating: "standard"}, impact}, "div"));
    }
    impactDetail.append(
      createTextElement(
        "p",
        "paper-dialog-summary",
        state.language === "zh"
          ? `${impact.citationCount} 次引用 · ${impact.influentialCitationCount} 次高影响引用 · ${paper.year} 年收录论文中第 ${impact.yearRank}/${impact.cohortSize} 名`
          : `${impact.citationCount} citations · ${impact.influentialCitationCount} influential · rank ${impact.yearRank}/${impact.cohortSize} among indexed ${paper.year} papers`
      ),
      createTextElement(
        "p",
        "recognition-meta",
        state.language === "zh" ? `数据更新：${impact.measuredAt}` : `Measured ${impact.measuredAt}`
      )
    );
    if (impact.sourceUrl) {
      const source = document.createElement("a");
      source.href = impact.sourceUrl;
      source.target = "_blank";
      source.rel = "noreferrer";
      source.textContent = t("recognition.semanticScholar");
      impactDetail.append(source);
    }
  } else {
    impactDetail.append(
      createTextElement(
        "p",
        "dialog-empty",
        t(impact?.status === "too-recent" ? "recognition.tooRecent" : "recognition.notAssessed")
      )
    );
  }
  recognitionSection.append(impactDetail);
  elements.paperDialogContent.append(recognitionSection);
  appendProjectDialogSection(
    elements.paperDialogContent,
    t("datasets.usedDatasetsLabel"),
    createRelatedDatasets(paper.id, "papers")
  );
  appendDialogSection(elements.paperDialogContent, t("papers.paperLinksLabel"), paperLinks, t("papers.noPaperLink"));
  appendDialogSection(elements.paperDialogContent, t("papers.openResourcesLabel"), openResourceLinks, t("papers.noOpenResources"));
}

function openPaperDialog(paper) {
  state.activePaperId = paper.id;
  renderPaperDialog(paper);
  if (typeof elements.paperDialog.showModal === "function") {
    if (!elements.paperDialog.open) elements.paperDialog.showModal();
  } else {
    elements.paperDialog.setAttribute("open", "");
  }
}

function closePaperDialog() {
  if (typeof elements.paperDialog.close === "function") {
    elements.paperDialog.close();
  } else {
    elements.paperDialog.removeAttribute("open");
    state.activePaperId = null;
  }
}

function renderPapers() {
  const query = elements.paperSearch.value.trim().toLocaleLowerCase(state.language);
  const selectedArea = elements.paperArea.value;
  const selectedControl = elements.paperControl.value;
  const selectedTrack = elements.paperTrack.value;
  const selectedRecognition = elements.paperRecognition.value;
  const filtered = state.papers.filter((paper) => {
    const matchesArea = selectedArea === "all" || paper.areas.includes(selectedArea);
    const approaches = paperControlApproaches(paper);
    const scopes = paperTrackScopes(paper);
    const matchesControl = selectedControl === "all" || approaches.includes(selectedControl);
    const matchesTrack = selectedTrack === "all" || scopes.includes(selectedTrack);
    const matchesRecognitionFilter = matchesRecognition(paper, selectedRecognition);
    const searchable = [
      paper.shortName ?? "",
      paper.title,
      paper.authors.join(" "),
      paper.summary.en,
      paper.summary.zh,
      ...paper.areas.map((area) => t(`area.${area}`)),
      ...approaches.map((approach) => t(`control.${approach}`)),
      ...scopes.map((scope) => t(`track.${scope}`)),
      ...(paper.aiAssessment?.rating === "highlighted" ? [t("recognition.aiHighlight")] : []),
      ...(paper.impact?.status === "high-impact" ? [t("recognition.highImpact")] : [])
    ]
      .join(" ")
      .toLocaleLowerCase(state.language);
    return matchesArea && matchesControl && matchesTrack && matchesRecognitionFilter && searchable.includes(query);
  });
  const pagination = paginate(filtered, "papers");

  elements.paperList.replaceChildren();
  if (filtered.length === 0) {
    elements.paperList.append(createTextElement("p", "empty", t("papers.empty")));
  } else {
    pagination.items.forEach((paper) => elements.paperList.append(createPaperEntry(paper)));
  }
  updateResultCount(elements.paperCount, "papers", pagination, filtered.length, state.papers.length);
  updatePagination("papers", pagination);
}

function applyTranslations() {
  document.documentElement.lang = state.language === "zh" ? "zh-CN" : "en";
  document.title = t("meta.title");
  document.querySelector('meta[name="description"]').content = t("meta.description");
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
  });
  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    element.alt = t(element.dataset.i18nAlt);
  });
  document.querySelectorAll("[data-language]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.language === state.language));
  });
  populateProjectFilters();
  populateDatasetFilters();
  populateAreaFilter(elements.paperArea, state.papers);
  populateSelect(
    elements.paperControl,
    controlApproaches.filter((approach) => state.papers.some((paper) => paperControlApproaches(paper).includes(approach))),
    "controls.allControlApproaches",
    (approach) => t(`control.${approach}`)
  );
  populateSelect(
    elements.paperTrack,
    trackScopes.filter((scope) => state.papers.some((paper) => paperTrackScopes(paper).includes(scope))),
    "controls.allTrackScopes",
    (scope) => t(`track.${scope}`)
  );
  updateCatalogueStats();
  updateFieldPaperLinks();
  if (state.projects.length) renderProjects();
  if (state.datasets.length) renderDatasets();
  if (state.resources.length) renderResources();
  if (state.papers.length) renderPapers();
  if (elements.paperDialog.open && state.activePaperId) {
    const activePaper = state.papers.find((paper) => paper.id === state.activePaperId);
    if (activePaper) renderPaperDialog(activePaper);
  }
  if (elements.projectDialog.open && state.activeProjectId) {
    const activeProject = state.projects.find((project) => project.id === state.activeProjectId);
    if (activeProject) renderProjectDialog(activeProject);
  }
  if (elements.datasetDialog.open && state.activeDatasetId) {
    const activeDataset = state.datasets.find((dataset) => dataset.id === state.activeDatasetId);
    if (activeDataset) renderDatasetDialog(activeDataset);
  }
}

function setLanguage(language) {
  state.language = language;
  try {
    localStorage.setItem("iap-language", language);
  } catch (_) {
    // The page still works when storage is unavailable.
  }
  applyTranslations();
}

async function loadData() {
  try {
    const [projectsResponse, datasetsResponse, resourcesResponse, papersResponse] = await Promise.all([
      fetch("data/projects.json", { cache: "no-store" }),
      fetch("data/datasets.json", { cache: "no-store" }),
      fetch("data/resources.json", { cache: "no-store" }),
      fetch("data/papers.json", { cache: "no-store" })
    ]);
    if (!projectsResponse.ok || !datasetsResponse.ok || !resourcesResponse.ok || !papersResponse.ok) throw new Error("Data request failed");
    const [projectData, datasetData, resourceData, paperData] = await Promise.all([
      projectsResponse.json(),
      datasetsResponse.json(),
      resourcesResponse.json(),
      papersResponse.json()
    ]);
    state.projects = projectData.projects;
    state.datasets = datasetData.datasets;
    state.resources = resourceData.resources;
    state.papers = paperData.papers;
    state.loaded = true;
    applyTranslations();
  } catch (_) {
    elements.projectRows.replaceChildren();
    const row = document.createElement("tr");
    const projectError = createTextElement("td", "empty", t("projects.loadError"));
    projectError.colSpan = 5;
    row.append(projectError);
    elements.projectRows.append(row);
    elements.datasetRows.replaceChildren();
    const datasetRow = document.createElement("tr");
    const datasetError = createTextElement("td", "empty", t("datasets.loadError"));
    datasetError.colSpan = 6;
    datasetRow.append(datasetError);
    elements.datasetRows.append(datasetRow);
    elements.resourceList.replaceChildren(createTextElement("p", "empty", t("resources.loadError")));
    elements.paperList.replaceChildren(createTextElement("p", "empty", t("papers.loadError")));
    elements.projectCount.textContent = "";
    elements.datasetCount.textContent = "";
    elements.paperCount.textContent = "";
    elements.projectPagination.hidden = true;
    elements.datasetPagination.hidden = true;
    elements.paperPagination.hidden = true;
  }
}

document.querySelectorAll("[data-language]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.language));
});
elements.projectSearch.addEventListener("input", () => resetPageAndRender("projects", renderProjects));
elements.projectArea.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectControl.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectTrack.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectLicense.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectCapability.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectStatus.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectTask.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectEffect.addEventListener("change", () => resetPageAndRender("projects", renderProjects));
elements.projectFilterReset.addEventListener("click", () => {
  elements.projectSearch.value = "";
  elements.projectArea.value = "all";
  elements.projectControl.value = "all";
  elements.projectTrack.value = "all";
  elements.projectLicense.value = "all";
  elements.projectCapability.value = "all";
  elements.projectStatus.value = "all";
  elements.projectTask.value = "all";
  elements.projectEffect.value = "all";
  resetPageAndRender("projects", renderProjects);
});
elements.datasetSearch.addEventListener("input", () => resetPageAndRender("datasets", renderDatasets));
elements.datasetArea.addEventListener("change", () => resetPageAndRender("datasets", renderDatasets));
elements.datasetTask.addEventListener("change", () => resetPageAndRender("datasets", renderDatasets));
elements.datasetContent.addEventListener("change", () => resetPageAndRender("datasets", renderDatasets));
elements.datasetAccess.addEventListener("change", () => resetPageAndRender("datasets", renderDatasets));
elements.datasetFilterReset.addEventListener("click", () => {
  elements.datasetSearch.value = "";
  elements.datasetArea.value = "all";
  elements.datasetTask.value = "all";
  elements.datasetContent.value = "all";
  elements.datasetAccess.value = "all";
  resetPageAndRender("datasets", renderDatasets);
});
elements.paperSearch.addEventListener("input", () => resetPageAndRender("papers", renderPapers));
elements.paperArea.addEventListener("change", () => resetPageAndRender("papers", renderPapers));
elements.paperControl.addEventListener("change", () => resetPageAndRender("papers", renderPapers));
elements.paperTrack.addEventListener("change", () => resetPageAndRender("papers", renderPapers));
elements.paperRecognition.addEventListener("change", () => resetPageAndRender("papers", renderPapers));
elements.projectPrevious.addEventListener("click", () => changePage("projects", -1, renderProjects));
elements.projectNext.addEventListener("click", () => changePage("projects", 1, renderProjects));
elements.datasetPrevious.addEventListener("click", () => changePage("datasets", -1, renderDatasets));
elements.datasetNext.addEventListener("click", () => changePage("datasets", 1, renderDatasets));
elements.paperPrevious.addEventListener("click", () => changePage("papers", -1, renderPapers));
elements.paperNext.addEventListener("click", () => changePage("papers", 1, renderPapers));
elements.fieldPaperLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showPapersForArea(link.dataset.paperArea);
  });
});
elements.projectDialogClose.addEventListener("click", closeProjectDialog);
elements.projectDialog.addEventListener("click", (event) => {
  if (event.target === elements.projectDialog) closeProjectDialog();
});
elements.projectDialog.addEventListener("close", () => {
  state.activeProjectId = null;
});
elements.datasetDialogClose.addEventListener("click", closeDatasetDialog);
elements.datasetDialog.addEventListener("click", (event) => {
  if (event.target === elements.datasetDialog) closeDatasetDialog();
});
elements.datasetDialog.addEventListener("close", () => {
  state.activeDatasetId = null;
});
elements.paperDialogClose.addEventListener("click", closePaperDialog);
elements.paperDialog.addEventListener("click", (event) => {
  if (event.target === elements.paperDialog) closePaperDialog();
});
elements.paperDialog.addEventListener("close", () => {
  state.activePaperId = null;
});

applyTranslations();
loadData();
