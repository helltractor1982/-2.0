/* ============================================================
   犬博士 H5 演示版 - 完整前端逻辑
   ============================================================ */

// ====== 品种数据库 ======
const BREEDS = [
  { id:"001", zh:"西伯利亚雪橇犬", en:"Siberian Husky", origin:"俄罗斯西伯利亚", size:"中型犬", weight:"16-27 kg", height:"51-60 cm", lifespan:"12-15年", shedding:"高", exercise:"高", coat:"中等/双层", personality:["活泼好动","友善外向","独立性强","喜欢群居"], tags:["中型犬","工作犬","高活跃度","适合家庭"], diseases:["白内障","髋关节发育不良","甲状腺功能减退","癫痫"], grooming:"每周梳毛3-4次，换毛季每天梳毛，每月洗澡1次", feeding:"每日进食量约350-450g，避免高脂食物，需补充鱼油", vaccine:"幼犬6-8周首免，每年加强接种狂犬病疫苗和综合疫苗", forbidden:["葡萄","巧克力","洋葱","木糖醇"], emoji:"🐺", desc:"西伯利亚雪橇犬，俗称哈士奇，以双色眼睛和狼样外表著称，性格活泼友善，是广受欢迎的中型工作犬。" },
  { id:"002", zh:"金毛寻回犬", en:"Golden Retriever", origin:"英国苏格兰", size:"大型犬", weight:"25-34 kg", height:"51-61 cm", lifespan:"10-12年", shedding:"高", exercise:"高", coat:"中长/波浪", personality:["温顺友善","聪明好学","耐心","适合家庭"], tags:["大型犬","运动犬","高活跃度","适合家庭","适合初养"], diseases:["髋关节发育不良","肘关节发育不良","白内障","癌症（老年）"], grooming:"每周梳毛2-3次，每月洗澡1-2次，定期修剪耳道毛", feeding:"每日进食量约400-500g，注意控制体重，避免过度喂食", vaccine:"按标准程序，8、12、16周接种，每年加强", forbidden:["葡萄","巧克力","咖啡因","酒精"], emoji:"🐶", desc:"金毛寻回犬是世界上最受欢迎的家庭犬之一，性格温顺聪明，非常适合作为家庭伴侣犬或工作犬。" },
  { id:"003", zh:"拉布拉多寻回犬", en:"Labrador Retriever", origin:"加拿大纽芬兰", size:"大型犬", weight:"25-36 kg", height:"54-62 cm", lifespan:"10-12年", shedding:"中", exercise:"高", coat:"短/直", personality:["温顺","忠诚","聪明","好动"], tags:["大型犬","运动犬","高活跃度","适合家庭","导盲犬"], diseases:["肥胖","髋关节发育不良","肘关节问题","眼部疾病"], grooming:"每周梳毛1-2次，每月洗澡1次", feeding:"每日进食量约400-500g，易胖体质需严格控食", vaccine:"按标准程序接种", forbidden:["葡萄","巧克力","坚果","洋葱"], emoji:"🐕", desc:"拉布拉多寻回犬是全球最受欢迎的犬种之一，广泛用于导盲犬、搜救犬等工作，性格极其温顺友善。" },
  { id:"004", zh:"德国牧羊犬", en:"German Shepherd", origin:"德国", size:"大型犬", weight:"22-40 kg", height:"55-65 cm", lifespan:"9-13年", shedding:"高", exercise:"高", coat:"中等/双层", personality:["忠诚勇敢","智慧","自信","保护性强"], tags:["大型犬","工作犬","高活跃度","警犬","需要训练"], diseases:["髋关节和肘关节发育不良","退行性脊髓病","胃扭转"], grooming:"每周梳毛3次，换毛期每天，定期清洁耳道", feeding:"每日进食量约450-550g，高蛋白饮食，补充关节营养素", vaccine:"6-8周首免，12、16周加强，每年接种", forbidden:["葡萄","巧克力","生蛋白"], emoji:"🦺", desc:"德国牧羊犬是世界上最著名的工作犬之一，广泛用于警察、军队和搜救工作，聪明、忠诚、勇敢。" },
  { id:"005", zh:"柴犬", en:"Shiba Inu", origin:"日本", size:"小型犬", weight:"7-10 kg", height:"35-43 cm", lifespan:"12-15年", shedding:"中", exercise:"中", coat:"短中/双层", personality:["独立自主","聪明","警觉","固执"], tags:["小型犬","非运动犬","中等活跃度","适合公寓"], diseases:["过敏性皮肤病","髌骨脱位","眼部疾病","青光眼"], grooming:"每周梳毛2次，换毛期加频，每月洗澡", feeding:"每日进食量约150-250g，注意营养均衡，避免肥胖", vaccine:"幼犬按标准程序接种，成年后每年加强", forbidden:["葡萄","巧克力","洋葱","大蒜"], emoji:"🦊", desc:"柴犬是日本最古老的犬种之一，外形可爱似狐狸，性格独立，是近年来网络上的超级明星。" },
  { id:"006", zh:"边境牧羊犬", en:"Border Collie", origin:"英国苏格兰边境", size:"中型犬", weight:"14-20 kg", height:"46-56 cm", lifespan:"12-15年", shedding:"中高", exercise:"极高", coat:"中长/双层", personality:["极度聪明","工作狂","精力充沛","敏感"], tags:["中型犬","牧羊犬","极高活跃度","最聪明犬种"], diseases:["髋关节发育不良","眼部疾病（collie eye anomaly）","癫痫"], grooming:"每周梳毛3次，每月洗澡", feeding:"每日进食量约300-400g，需要高能量食物以支持高强度运动", vaccine:"标准接种程序，每年加强", forbidden:["葡萄","巧克力","洋葱"], emoji:"🐾", desc:"边境牧羊犬被公认为世界上最聪明的犬种，精力充沛，需要大量运动和脑力刺激。" },
  { id:"007", zh:"贵宾犬", en:"Poodle", origin:"法国/德国", size:"多种体型", weight:"2-32 kg", height:"24-60 cm", lifespan:"12-18年", shedding:"极低", exercise:"中高", coat:"卷曲/不掉毛", personality:["聪明","活泼","友善","适应性强"], tags:["多种体型","非运动犬","低掉毛","适合过敏者","聪明"], diseases:["髌骨脱位（小型）","髋关节问题（标准）","眼部疾病","皮肤病"], grooming:"每6-8周专业美容修剪，每周梳毛，每月洗澡", feeding:"视体型而定，标准贵宾约300g/天，玩具贵宾约80-100g/天", vaccine:"标准程序，每年加强", forbidden:["葡萄","巧克力","咖啡因"], emoji:"🐩", desc:"贵宾犬极其聪明且几乎不掉毛，有玩具型、迷你型和标准型三种，非常适合城市家庭。" },
  { id:"008", zh:"法国斗牛犬", en:"French Bulldog", origin:"法国", size:"小型犬", weight:"8-14 kg", height:"28-33 cm", lifespan:"10-12年", shedding:"低", exercise:"低", coat:"短/平滑", personality:["温顺","好玩","警觉","忠诚"], tags:["小型犬","伴侣犬","低活跃度","适合公寓","不耐热"], diseases:["呼吸道问题（短吻综合征）","椎间盘疾病","皮肤褶皱感染","眼部问题"], grooming:"每周梳毛，注意清洁面部褶皱，每月洗澡", feeding:"每日进食量约200-250g，易肥胖，需严格控制饮食", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱","高脂食物"], emoji:"🐷", desc:"法国斗牛犬是近年来最受欢迎的城市犬之一，不需要大量运动，适合公寓生活。" },
  { id:"009", zh:"阿拉斯加雪橇犬", en:"Alaskan Malamute", origin:"美国阿拉斯加", size:"大型犬", weight:"34-43 kg", height:"58-64 cm", lifespan:"10-14年", shedding:"极高", exercise:"高", coat:"厚双层", personality:["友善","忠诚","顽皮","独立"], tags:["大型犬","工作犬","高活跃度","不适合热带气候"], diseases:["髋关节发育不良","遗传性多发性神经病","糖尿病"], grooming:"每周梳毛3-4次，换毛期每天，每月洗澡", feeding:"每日进食量约500-600g，高蛋白饮食", vaccine:"标准程序接种，每年加强", forbidden:["葡萄","巧克力","洋葱"], emoji:"🐺", desc:"阿拉斯加雪橇犬是北极地区最古老的雪橇犬品种之一，体型比哈士奇更大，力量更强。" },
  { id:"010", zh:"萨摩耶犬", en:"Samoyed", origin:"俄罗斯西伯利亚", size:"中大型犬", weight:"16-30 kg", height:"46-60 cm", lifespan:"12-14年", shedding:"极高", exercise:"高", coat:"长厚双层", personality:["温顺友善","活泼","聪明","好奇心强"], tags:["中大型犬","工作犬","高活跃度","笑脸犬"], diseases:["遗传性肾小球病","糖尿病","髋关节问题","心脏病"], grooming:"每天梳毛，换毛期加频，每月洗澡", feeding:"每日进食量约350-450g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱"], emoji:"⛄", desc:"萨摩耶犬以其标志性的\"微笑\"表情和雪白毛发著称，被称为\"微笑天使\"。" },
  { id:"011", zh:"博美犬", en:"Pomeranian", origin:"德国/波兰", size:"玩具犬", weight:"1.8-3.2 kg", height:"18-24 cm", lifespan:"12-16年", shedding:"中", exercise:"低", coat:"长双层", personality:["活泼好奇","聪明","自信","话多"], tags:["玩具犬","伴侣犬","低活跃度","适合公寓","话多"], diseases:["气管塌陷","髌骨脱位","牙齿问题","低血糖（幼犬）"], grooming:"每天梳毛，每月专业美容，每3-4周洗澡", feeding:"每日进食量约60-100g，小型犬高卡路里食物", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱"], emoji:"🦁", desc:"博美犬是最受欢迎的玩具犬种之一，外形如毛球，性格活泼，充满自信。" },
  { id:"012", zh:"柯基犬", en:"Corgi", origin:"英国威尔士", size:"小中型犬", weight:"9-14 kg", height:"25-30 cm", lifespan:"12-15年", shedding:"高", exercise:"中高", coat:"中等双层", personality:["聪明机警","友善","勇敢","爱玩"], tags:["小中型犬","牧羊犬","中高活跃度","适合家庭","英国王室御用"], diseases:["椎间盘疾病（长背犬）","髋关节发育不良","渐进性视网膜萎缩"], grooming:"每周梳毛2-3次，每月洗澡", feeding:"每日进食量约180-250g，注意控制体重", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱"], emoji:"🐕", desc:"柯基犬因英国女王的喜爱而闻名，短腿长身，性格聪明友善。" },
  { id:"013", zh:"比格犬", en:"Beagle", origin:"英国", size:"小中型犬", weight:"9-11 kg", height:"33-41 cm", lifespan:"12-15年", shedding:"中", exercise:"高", coat:"短", personality:["温顺","好奇","活跃","爱叫"], tags:["小中型犬","猎犬","高活跃度","嗅觉灵敏","适合家庭"], diseases:["肥胖","椎间盘疾病","耳道感染","眼部问题"], grooming:"每周梳毛，定期清洁耳道，每月洗澡", feeding:"每日进食量约200-270g，易肥胖", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱"], emoji:"🐕", desc:"比格犬嗅觉极其灵敏，是著名的猎犬，也是广受欢迎的家庭犬，性格温顺好玩。" },
  { id:"014", zh:"松狮犬", en:"Chow Chow", origin:"中国", size:"中大型犬", weight:"20-32 kg", height:"43-51 cm", lifespan:"9-15年", shedding:"高", exercise:"中", coat:"厚长双层", personality:["高冷独立","忠诚护家","固执","不爱社交"], tags:["中大型犬","非运动犬","中活跃度","中国原产","独立性强"], diseases:["髋关节发育不良","眼睑内翻","甲状腺问题","皮肤病"], grooming:"每周梳毛3-4次，每月洗澡", feeding:"每日进食量约350-450g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🦁", desc:"松狮犬是中国原产的古老犬种，以其蓝紫色舌头和狮子般外表著称，性格高冷独立。" },
  { id:"015", zh:"中华田园犬", en:"Chinese Rural Dog", origin:"中国", size:"小中型犬", weight:"10-25 kg", height:"40-55 cm", lifespan:"13-16年", shedding:"中", exercise:"中高", coat:"短中", personality:["聪明警觉","忠诚","适应性强","不娇气"], tags:["小中型犬","伴侣犬","高适应性","中国原产","抗病力强"], diseases:["相对健康遗传病少","皮肤寄生虫（农村）","外伤"], grooming:"每月洗澡，定期驱虫", feeding:"每日进食量约200-300g，食物适应性强", vaccine:"狂犬病疫苗必须接种，建议接种综合疫苗", forbidden:["葡萄","巧克力"], emoji:"🐕", desc:"中华田园犬是中国土生土长的犬种，聪明忠诚，适应性极强，是中国传统的伴侣犬。" },
  { id:"016", zh:"泰迪犬（玩具贵宾）", en:"Teddy (Toy Poodle)", origin:"法国", size:"玩具犬", weight:"2-4 kg", height:"24-28 cm", lifespan:"14-18年", shedding:"极低", exercise:"中", coat:"卷曲/不掉毛", personality:["聪明活泼","友善","适应性强","爱撒娇"], tags:["玩具犬","伴侣犬","低掉毛","适合过敏者","聪明"], diseases:["髌骨脱位","渐进性视网膜萎缩","牙齿问题"], grooming:"每6-8周专业美容，每周梳毛", feeding:"每日进食量约80-100g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐩", desc:"泰迪犬即玩具贵宾犬，是中国最受欢迎的宠物犬之一，几乎不掉毛，非常适合城市家庭。" },
  { id:"017", zh:"比熊犬", en:"Bichon Frise", origin:"地中海地区", size:"小型犬", weight:"5-10 kg", height:"23-30 cm", lifespan:"12-15年", shedding:"极低", exercise:"中", coat:"卷曲蓬松", personality:["活泼开朗","友善","温顺","爱玩"], tags:["小型犬","伴侣犬","低掉毛","适合公寓","白色"], diseases:["膀胱结石","皮肤过敏","牙周病","髌骨脱位"], grooming:"每6-8周专业美容，每周梳毛", feeding:"每日进食量约100-150g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"☁️", desc:"比熊犬如棉花糖般可爱，几乎不掉毛，性格开朗友善，是非常受欢迎的城市伴侣犬。" },
  { id:"018", zh:"杜宾犬", en:"Doberman Pinscher", origin:"德国", size:"大型犬", weight:"27-45 kg", height:"63-72 cm", lifespan:"10-13年", shedding:"低", exercise:"高", coat:"短", personality:["忠诚","聪明","勇敢","保护性强"], tags:["大型犬","工作犬","高活跃度","护卫犬","需要训练"], diseases:["心肌病","冯维勒布兰德病","颈椎脊椎脊髓病"], grooming:"每周梳毛，每月洗澡", feeding:"每日进食量约500-600g，高蛋白饮食", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐕", desc:"杜宾犬是著名的护卫犬，外表威武，聪明忠诚，需要良好的训练和社会化。" },
  { id:"019", zh:"大丹犬", en:"Great Dane", origin:"德国", size:"超大型犬", weight:"45-90 kg", height:"71-86 cm", lifespan:"7-10年", shedding:"中", exercise:"中", coat:"短", personality:["温和友善","忠诚","耐心","警觉"], tags:["超大型犬","工作犬","中活跃度","温柔巨人"], diseases:["胃扭转（致命）","心肌病","骨肉瘤","骨关节炎"], grooming:"每周梳毛，每月洗澡", feeding:"每日进食量约600-800g，需要大型犬专用粮防止骨骼问题", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐕", desc:"大丹犬是世界上最高大的犬种之一，外表威武但性格温和，被称为\"温柔的巨人\"。" },
  { id:"020", zh:"西施犬", en:"Shih Tzu", origin:"中国/西藏", size:"玩具犬", weight:"4-7 kg", height:"20-28 cm", lifespan:"10-16年", shedding:"低", exercise:"低", coat:"长直双层", personality:["温柔","友善","开朗","爱依人"], tags:["玩具犬","伴侣犬","低活跃度","低掉毛","中国原产"], diseases:["呼吸道问题（短吻）","眼部问题","肾脏问题","椎间盘疾病"], grooming:"每天梳毛，每3-4周美容，注意清洁眼部", feeding:"每日进食量约100-150g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐶", desc:"西施犬源自中国皇宫，外形高贵优雅，性格温柔友善，是理想的城市伴侣犬。" },
  { id:"021", zh:"腊肠犬", en:"Dachshund", origin:"德国", size:"小型犬", weight:"5-11 kg", height:"20-23 cm", lifespan:"12-16年", shedding:"低", exercise:"中", coat:"短/长/刚毛（三种）", personality:["顽固","好奇","活泼","勇敢"], tags:["小型犬","猎犬","中活跃度","长身短腿","顽固"], diseases:["椎间盘疾病（最易发）","髌骨脱位","渐进性视网膜萎缩"], grooming:"视毛型，短毛每周梳1次，长毛每天梳", feeding:"每日进食量约150-200g，严格控重防脊柱问题", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🌭", desc:"腊肠犬以其超长的身体和短腿著称，是非常受欢迎的小型犬，但需注意保护其脊柱。" },
  { id:"022", zh:"大麦町犬", en:"Dalmatian", origin:"克罗地亚", size:"中大型犬", weight:"23-32 kg", height:"48-61 cm", lifespan:"11-13年", shedding:"高", exercise:"极高", coat:"短", personality:["精力充沛","聪明","外向","活泼"], tags:["中大型犬","非运动犬","极高活跃度","斑点狗","消防车犬"], diseases:["尿结石（高发）","耳聋（约30%有遗传性耳聋）","皮肤过敏"], grooming:"每周梳毛，每月洗澡", feeding:"每日进食量约350-450g，低嘌呤饮食（预防尿结石）", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","高嘌呤食物"], emoji:"🎲", desc:"大麦町犬（斑点狗）因《101忠狗》而家喻户晓，精力充沛，需要大量运动。" },
  { id:"023", zh:"雪纳瑞", en:"Schnauzer", origin:"德国", size:"多种（迷你/标准/巨型）", weight:"4-48 kg", height:"30-70 cm", lifespan:"12-16年", shedding:"极低", exercise:"中高", coat:"硬粗双层", personality:["聪明","活泼","忠诚","机警"], tags:["多种体型","梗类","中高活跃度","低掉毛","胡须"], diseases:["胰腺炎","皮肤病","白内障","尿结石"], grooming:"每6-8周专业美容，保持胡须清洁", feeding:"视体型而定，迷你雪纳瑞每日约120-160g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","高脂食物（易胰腺炎）"], emoji:"👴", desc:"雪纳瑞以其标志性的胡须和眉毛著称，有迷你、标准和巨型三种，几乎不掉毛。" },
  { id:"024", zh:"秋田犬", en:"Akita", origin:"日本", size:"大型犬", weight:"32-59 kg", height:"58-70 cm", lifespan:"10-15年", shedding:"高", exercise:"高", coat:"厚双层", personality:["忠诚","独立","尊严感强","保护性"], tags:["大型犬","工作犬","高活跃度","日本原产","忠犬八公"], diseases:["甲状腺功能减退","髋关节发育不良","免疫系统疾病"], grooming:"每周梳毛2-3次，换毛期每天", feeding:"每日进食量约400-500g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","洋葱"], emoji:"🏔️", desc:"秋田犬是日本最著名的犬种，因\"忠犬八公\"的故事而享誉全球，象征忠诚和好运。" },
  { id:"025", zh:"沙皮犬", en:"Shar Pei", origin:"中国广东", size:"中型犬", weight:"18-29 kg", height:"44-51 cm", lifespan:"8-12年", shedding:"低", exercise:"中", coat:"极短（马毛/刷毛/熊毛）", personality:["忠诚","冷静","独立","保护性强"], tags:["中型犬","非运动犬","中活跃度","中国原产","皱皮犬"], diseases:["皮肤褶皱感染","沙皮犬发热综合征（SPAID）","眼睑内翻","肾脏问题"], grooming:"定期清洁皮肤褶皱，防止感染，每月洗澡", feeding:"每日进食量约300-400g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐷", desc:"沙皮犬是中国古老犬种，以其布满皱纹的皮肤著称，性格忠诚冷静，是独特的伴侣犬。" },
  { id:"026", zh:"喜乐蒂牧羊犬", en:"Shetland Sheepdog", origin:"苏格兰设得兰群岛", size:"小中型犬", weight:"6-12 kg", height:"33-41 cm", lifespan:"12-14年", shedding:"高", exercise:"高", coat:"长厚双层", personality:["聪明","活泼","温顺","敏感"], tags:["小中型犬","牧羊犬","高活跃度","聪明","长毛"], diseases:["MDR1基因突变","Collie眼异常","髌骨脱位","癫痫"], grooming:"每周梳毛3-4次，每月洗澡", feeding:"每日进食量约180-250g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力","某些驱虫药（MDR1基因）"], emoji:"🐕", desc:"喜乐蒂牧羊犬外形似迷你苏格兰牧羊犬，聪明温顺，是受欢迎的家庭犬。" },
  { id:"027", zh:"比利时马里诺斯犬", en:"Belgian Malinois", origin:"比利时", size:"中大型犬", weight:"25-35 kg", height:"56-66 cm", lifespan:"12-14年", shedding:"中", exercise:"极高", coat:"短", personality:["聪明","高度警觉","精力充沛","工作狂"], tags:["中大型犬","牧羊犬","极高活跃度","警犬首选","特种兵犬"], diseases:["髋关节和肘关节发育不良","进行性视网膜萎缩","癫痫"], grooming:"每周梳毛，每月洗澡", feeding:"每日进食量约400-500g，高蛋白工作犬食物", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🦺", desc:"比利时马里诺斯犬是现代最受欢迎的警用、军用犬种，智力超群，工作能力极强。" },
  { id:"028", zh:"澳大利亚牧羊犬", en:"Australian Shepherd", origin:"美国（非澳大利亚）", size:"中型犬", weight:"16-32 kg", height:"46-58 cm", lifespan:"12-15年", shedding:"高", exercise:"极高", coat:"中长/双层", personality:["精力旺盛","聪明","工作狂","爱粘人"], tags:["中型犬","牧羊犬","极高活跃度","大理石花纹"], diseases:["MDR1基因突变","髋关节问题","眼部疾病","癫痫"], grooming:"每周梳毛3-4次，每月洗澡", feeding:"每日进食量约350-450g，高能量食物", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🎨", desc:"澳大利亚牧羊犬是精力极其旺盛的工作犬，以其多彩的大理石花纹毛色著称。" },
  { id:"029", zh:"纽芬兰犬", en:"Newfoundland", origin:"加拿大纽芬兰", size:"超大型犬", weight:"45-70 kg", height:"63-74 cm", lifespan:"8-10年", shedding:"极高", exercise:"中", coat:"厚长双层防水", personality:["温柔","耐心","忠诚","爱孩子"], tags:["超大型犬","工作犬","中活跃度","水上救援犬","保姆犬"], diseases:["髋关节和肘关节发育不良","心脏病（主动脉瓣下狭窄）","胃扭转"], grooming:"每周梳毛3-4次，每月洗澡", feeding:"每日进食量约600-800g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🐋", desc:"纽芬兰犬因其温柔的性格和对孩子的耐心被称为\"保姆犬\"，也是出色的水上救援犬。" },
  { id:"030", zh:"爱尔兰赛特犬", en:"Irish Setter", origin:"爱尔兰", size:"大型犬", weight:"25-32 kg", height:"58-68 cm", lifespan:"12-15年", shedding:"中", exercise:"极高", coat:"中长丝滑", personality:["活泼热情","友善","开朗","精力充沛"], tags:["大型犬","运动犬","极高活跃度","红色猎犬","美丽"], diseases:["髋关节发育不良","进行性视网膜萎缩","癫痫","乳糜泻"], grooming:"每周梳毛2-3次，每月洗澡", feeding:"每日进食量约400-500g", vaccine:"标准程序接种", forbidden:["葡萄","巧克力"], emoji:"🦊", desc:"爱尔兰赛特犬以其火红色的丝滑毛发著称，是最美丽的犬种之一，活泼热情。" }
];

// ====== 状态管理 ======
let currentPage = 'home';
let pageHistory = [];
let currentResult = null;
let currentImageData = null;
let wikiPage = 1;
let wikiFilter = 'all';
let wikiSearch = '';
let compareIds = [];
let altsExpanded = true;
let statsChartInit = false;
let historyData = JSON.parse(localStorage.getItem('dogHistory') || '[]');

// ====== 工具函数 ======
let toastTimer = null;
function showToast(msg, duration = 2500) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), duration);
}

// ====== 页面导航 ======
function showPage(name, addHistory = true) {
  const prev = document.querySelector('.page.active');
  const next = document.getElementById('page-' + name);
  if (!next) return;
  if (prev) prev.classList.remove('active');
  next.classList.add('active');
  if (addHistory && currentPage !== name) pageHistory.push(currentPage);
  currentPage = name;
  // 更新侧边栏导航
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const navItem = document.getElementById('nav-' + name);
  if (navItem) navItem.classList.add('active');
  // 页面特定初始化
  if (name === 'stats' && !statsChartInit) { statsChartInit = true; setTimeout(initCharts, 300); }
  if (name === 'history') renderHistory();
  if (name === 'wiki' && document.getElementById('wiki-breed-list').children.length === 0) { wikiPage = 1; renderWiki(); }
  // 滚动到顶部
  document.querySelector('.main-content').scrollTop = 0;
}

function goBack() {
  const prev = pageHistory.pop() || 'home';
  showPage(prev, false);
}

// ====== 首页初始化 ======
function initHome() {
  const today = new Date().toDateString();
  const seed = today.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  const b = BREEDS[seed % BREEDS.length];
  document.getElementById('daily-recommend').innerHTML = `
    <div style="display:flex;gap:12px;align-items:center;">
      <div style="font-size:48px;">${b.emoji}</div>
      <div style="flex:1;">
        <div style="font-size:17px;font-weight:800;color:var(--text-primary);">${b.zh}</div>
        <div style="font-size:12px;color:var(--text-hint);margin-top:2px;">${b.en} &nbsp;|&nbsp; ${b.origin}</div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:8px;">${b.tags.slice(0,3).map(t=>`<span class="badge badge-primary">${t}</span>`).join('')}</div>
      </div>
      <div style="color:var(--text-hint);font-size:22px;flex-shrink:0;">›</div>
    </div>
    <div style="margin-top:10px;font-size:13px;color:var(--text-secondary);line-height:1.6;">${b.desc.slice(0,80)}...</div>
  `;
  // 点击跳转详情
  document.getElementById('daily-recommend').onclick = () => viewBreedDetail(b.id);
}

function openDailyBreed() {
  const today = new Date().toDateString();
  const seed = today.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  const b = BREEDS[seed % BREEDS.length];
  viewBreedDetail(b.id);
}

// ====== 识别功能 ======
function triggerCamera() {
  document.getElementById('file-input').click();
}

function handleDrop(e) {
  e.preventDefault();
  document.getElementById('upload-zone').classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) processImageFile(file);
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) processImageFile(file);
  e.target.value = '';
}

function processImageFile(file) {
  if (file.size > 10 * 1024 * 1024) { showToast('❌ 图片大小超过10MB，请重新选择'); return; }
  const allowed = ['image/jpeg','image/png','image/webp','image/bmp'];
  if (!allowed.includes(file.type)) { showToast('❌ 不支持的图片格式，请使用JPG/PNG/WEBP/BMP'); return; }
  const reader = new FileReader();
  reader.onload = ev => {
    currentImageData = ev.target.result;
    document.getElementById('preview-img').src = currentImageData;
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('preview-section').style.display = 'block';
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('skeleton-section').style.display = 'none';
  };
  reader.readAsDataURL(file);
}

function useDemo() {
  currentImageData = 'demo';
  const svg = `<svg width="400" height="280" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4A90D9;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#6ab4ff;stop-opacity:1"/>
    </linearGradient></defs>
    <rect width="400" height="280" fill="url(#g)"/>
    <text x="200" y="115" text-anchor="middle" font-size="72" fill="rgba(255,255,255,0.9)">🐕</text>
    <text x="200" y="175" text-anchor="middle" font-size="20" fill="white" font-weight="bold" font-family="sans-serif">演示图片</text>
    <text x="200" y="205" text-anchor="middle" font-size="14" fill="rgba(255,255,255,0.8)" font-family="sans-serif">点击"开始识别"体验AI识别效果</text>
    <text x="200" y="240" text-anchor="middle" font-size="12" fill="rgba(255,255,255,0.6)" font-family="sans-serif">犬博士 · AI 品种识别</text>
  </svg>`;
  document.getElementById('preview-img').src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  document.getElementById('upload-section').style.display = 'none';
  document.getElementById('preview-section').style.display = 'block';
  document.getElementById('result-section').style.display = 'none';
  document.getElementById('skeleton-section').style.display = 'none';
}

function clearPreview() {
  currentImageData = null;
  currentResult = null;
  document.getElementById('upload-section').style.display = 'block';
  document.getElementById('preview-section').style.display = 'none';
  document.getElementById('result-section').style.display = 'none';
  document.getElementById('skeleton-section').style.display = 'none';
}

function clearResult() { clearPreview(); }

async function startIdentify() {
  if (!currentImageData) { showToast('请先选择图片'); return; }
  const btn = document.getElementById('identify-btn');
  btn.disabled = true;
  document.getElementById('preview-section').style.display = 'none';
  document.getElementById('skeleton-section').style.display = 'block';
  document.getElementById('result-section').style.display = 'none';
  document.getElementById('loading-overlay').classList.add('show');

  try {
    // 调用后端 API
    const resp = await fetch('/api/identify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: currentImageData, top_k: 3 })
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(errText || `HTTP ${resp.status}`);
    }

    const json = await resp.json();
    if (json.code !== 0) {
      throw new Error(json.message || '识别失败');
    }

    const apiData = json.data;
    const apiResults = apiData.results || [];

    if (apiResults.length === 0) {
      throw new Error('未识别到任何品种');
    }

    // 将 API 返回的字段映射为前端 BREEDS 格式
    const mappedResults = apiResults.map(r => {
      const breed = BREEDS.find(b => b.id === r.breed_id);
      if (breed) {
        return { ...breed, confidence: r.confidence };
      }
      // 如果本地找不到，用 API 返回的数据
      return {
        id: r.breed_id,
        zh: r.name_zh || r.breed_name_zh || '',
        en: r.name_en || r.breed_name_en || '',
        confidence: r.confidence,
        origin: r.origin || '',
        size: r.size || '',
        weight: r.weight_range || '',
        height: r.height_range || '',
        lifespan: r.lifespan || '',
        shedding: r.shedding || '',
        exercise: r.exercise_need || '',
        coat: r.coat_length || '',
        personality: r.personality || [],
        tags: r.tags || [],
        diseases: r.common_diseases || [],
        grooming: r.grooming || '',
        feeding: r.feeding_tips || '',
        vaccine: r.vaccine_schedule || '',
        forbidden: r.forbidden_foods || [],
        emoji: '🐕',
        desc: r.description || ''
      };
    });

    const result = {
      results: mappedResults,
      inference_time_ms: apiData.inference_time_ms || 0
    };

    currentResult = {
      ...mappedResults[0],
      allResults: mappedResults,
      inference_ms: result.inference_time_ms
    };
    showResult(result);

  } catch (err) {
    console.error('识别失败:', err);
    showToast('识别失败: ' + (err.message || '网络错误'));
    document.getElementById('preview-section').style.display = 'block';
  } finally {
    document.getElementById('loading-overlay').classList.remove('show');
    document.getElementById('skeleton-section').style.display = 'none';
    btn.disabled = false;
  }
}

function mockIdentify(imgData, topK) {
  // 确定性随机：同一张图片返回相同结果
  let seed = imgData === 'demo' ? 42 : (imgData.length * 7 + imgData.charCodeAt(imgData.length - 10));
  function nextRand() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
  const indices = [];
  const used = new Set();
  while (indices.length < topK) {
    const idx = Math.floor(nextRand() * BREEDS.length);
    if (!used.has(idx)) { indices.push(idx); used.add(idx); }
  }
  const mainConf = 0.60 + nextRand() * 0.38;
  const r1 = nextRand();
  const conf2 = (1 - mainConf) * (0.5 + r1 * 0.3);
  const conf3 = 1 - mainConf - conf2;
  const confs = [mainConf, conf2, conf3];
  return {
    results: indices.map((idx, i) => ({ ...BREEDS[idx], confidence: Math.max(0.005, confs[i]) })),
    inference_time_ms: 180 + Math.floor(nextRand() * 600)
  };
}

function showResult(data) {
  const top = data.results[0];
  const pct = (top.confidence * 100).toFixed(1);
  document.getElementById('main-result').innerHTML = `
    <div class="result-header">
      <div class="result-rank">🏆</div>
      <div style="flex:1;">
        <div style="font-size:18px;font-weight:700;">${top.zh}</div>
        <div style="font-size:12px;opacity:0.85;margin-top:2px;">${top.en}</div>
      </div>
      <div class="result-confidence">
        <div class="pct">${pct}%</div>
        <div class="pct-label">置信度</div>
      </div>
    </div>
    <div class="result-body">
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;">
        ${(top.tags||[]).slice(0,4).map(t=>`<span class="badge badge-primary">${t}</span>`).join('')}
      </div>
      <div style="font-size:12px;color:var(--text-hint);margin-bottom:10px;">
        📍 ${top.origin} &nbsp;|&nbsp; ⚖️ ${top.weight} &nbsp;|&nbsp; ⏱️ ${top.lifespan}
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width:0%;"></div></div>
      <div style="text-align:right;font-size:11px;color:var(--text-hint);margin-top:4px;">置信度 ${pct}%</div>
      <div style="margin-top:10px;font-size:13px;color:var(--text-secondary);line-height:1.7;">${top.desc}</div>
      <div style="margin-top:8px;font-size:11px;color:var(--text-hint);">⚡ 推理时间：${data.inference_time_ms}ms</div>
    </div>
  `;
  // 动画进度条
  setTimeout(() => {
    const fill = document.querySelector('#main-result .progress-fill');
    if (fill) fill.style.width = pct + '%';
  }, 100);

  // 备选结果
  const altList = document.getElementById('alt-list');
  altList.innerHTML = data.results.slice(1).map((r, i) => `
    <div class="alt-item" onclick="viewBreedDetail('${r.id}')">
      <div class="alt-rank">#${i+2}</div>
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:600;">${r.zh}</div>
        <div style="font-size:11px;color:var(--text-hint);">${r.en} · ${r.size}</div>
      </div>
      <div>
        <div style="font-size:14px;font-weight:700;color:var(--primary);">${(r.confidence*100).toFixed(1)}%</div>
        <div class="progress-bar" style="width:80px;margin-top:4px;">
          <div class="progress-fill" style="width:0%;background:var(--text-hint);"></div>
        </div>
      </div>
    </div>
  `).join('');
  // 动画备选进度条
  setTimeout(() => {
    document.querySelectorAll('#alt-list .progress-fill').forEach((fill, i) => {
      fill.style.width = (data.results[i+1].confidence * 100) + '%';
    });
  }, 150);

  document.getElementById('result-section').style.display = 'block';
}

function viewDetailFromResult() {
  if (currentResult) viewBreedDetail(currentResult.id);
}

function toggleAlts() {
  const list = document.getElementById('alt-list');
  const toggle = document.getElementById('alt-toggle');
  altsExpanded = !altsExpanded;
  list.style.display = altsExpanded ? 'block' : 'none';
  toggle.textContent = altsExpanded ? '▼' : '▶';
}

function saveToHistory() {
  if (!currentResult) return;
  const record = {
    id: Date.now(),
    breed_id: currentResult.id,
    zh: currentResult.zh,
    en: currentResult.en,
    confidence: currentResult.confidence,
    emoji: currentResult.emoji,
    size: currentResult.size,
    imagePreview: currentImageData !== 'demo' ? currentImageData : null,
    time: new Date().toISOString()
  };
  historyData.unshift(record);
  if (historyData.length > 100) historyData = historyData.slice(0, 100);
  localStorage.setItem('dogHistory', JSON.stringify(historyData));
  showToast('✅ 已保存到历史记录');
}

// ====== 品种详情 ======
function viewBreedDetail(breedId) {
  const b = BREEDS.find(x => x.id === breedId);
  if (!b) { showToast('未找到品种信息'); return; }
  document.getElementById('detail-breed-name').textContent = b.zh;
  document.getElementById('detail-breed-en').textContent = b.en;
  document.getElementById('detail-tags').innerHTML = b.tags.map(t=>`<span class="detail-tag">${t}</span>`).join('');

  const lvMap = {'极低':1,'低':2,'中':3,'中高':4,'高':5,'极高':5};
  const exLv = lvMap[b.exercise] || 3;
  const shLv = lvMap[b.shedding] || 3;
  const dots = (n, max, cls) => Array(max).fill(0).map((_,i)=>`<span class="rating-dot ${i<n?cls:''}"></span>`).join('');

  const favs = JSON.parse(localStorage.getItem('dogFavs') || '[]');
  const isFav = favs.includes(breedId);

  document.getElementById('detail-content').innerHTML = `
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:12px;">📋 基本信息</div>
      <div class="info-grid">
        <div class="info-cell"><div class="info-cell-label">原产地</div><div class="info-cell-value">${b.origin}</div></div>
        <div class="info-cell"><div class="info-cell-label">体型分类</div><div class="info-cell-value">${b.size}</div></div>
        <div class="info-cell"><div class="info-cell-label">体重范围</div><div class="info-cell-value">${b.weight}</div></div>
        <div class="info-cell"><div class="info-cell-label">肩高范围</div><div class="info-cell-value">${b.height}</div></div>
        <div class="info-cell"><div class="info-cell-label">寿命</div><div class="info-cell-value">${b.lifespan}</div></div>
        <div class="info-cell"><div class="info-cell-label">毛发类型</div><div class="info-cell-value">${b.coat}</div></div>
      </div>
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:12px;">💭 性格特点</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
        ${b.personality.map(p=>`<span class="badge badge-primary" style="font-size:13px;padding:6px 12px;">${p}</span>`).join('')}
      </div>
      <div style="font-size:13px;color:var(--text-secondary);line-height:1.8;">${b.desc}</div>
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:12px;">📊 生活需求评级</div>
      <div class="rating-row">
        <div class="rating-label">运动需求</div>
        <div class="rating-dots">${dots(exLv,5,'filled')}</div>
        <span class="badge badge-primary" style="margin-left:8px;">${b.exercise}</span>
      </div>
      <div class="rating-row">
        <div class="rating-label">掉毛程度</div>
        <div class="rating-dots">${dots(shLv,5,'filled-accent')}</div>
        <span class="badge badge-accent" style="margin-left:8px;">${b.shedding}</span>
      </div>
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:12px;">🍽️ 喂养建议</div>
      <div style="font-size:13px;color:var(--text-secondary);line-height:1.8;margin-bottom:12px;">${b.feeding}</div>
      <div style="padding:12px;background:var(--accent-light,#fff3ee);border-radius:8px;">
        <div style="font-size:13px;font-weight:700;color:var(--accent);margin-bottom:6px;">⚠️ 以下食物绝对不能喂：</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          ${b.forbidden.map(f=>`<span class="badge badge-accent">${f}</span>`).join('')}
        </div>
      </div>
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:12px;">🏥 常见疾病</div>
      ${b.diseases.map(d=>`<div class="disease-item"><div class="disease-dot"></div><div>${d}</div></div>`).join('')}
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px;">
      <div class="card-title" style="margin-bottom:8px;">💉 疫苗建议</div>
      <div style="font-size:13px;color:var(--text-secondary);line-height:1.8;">${b.vaccine}</div>
    </div>

    <div style="height:8px;background:var(--bg);"></div>
    <div style="padding:16px 16px 20px;">
      <div class="card-title" style="margin-bottom:8px;">✂️ 美容护理</div>
      <div style="font-size:13px;color:var(--text-secondary);line-height:1.8;margin-bottom:16px;">${b.grooming}</div>
      <button class="btn ${isFav?'btn-accent':'btn-outline'} btn-block" id="fav-btn" onclick="toggleFavorite('${breedId}')">
        ${isFav ? '❤️ 已收藏' : '🤍 加入收藏夹'}
      </button>
    </div>
  `;
  showPage('detail');
}

function toggleFavorite(breedId) {
  let favs = JSON.parse(localStorage.getItem('dogFavs') || '[]');
  const btn = document.getElementById('fav-btn');
  if (favs.includes(breedId)) {
    favs = favs.filter(id => id !== breedId);
    btn.className = 'btn btn-outline btn-block';
    btn.textContent = '🤍 加入收藏夹';
    showToast('取消收藏');
  } else {
    favs.push(breedId);
    btn.className = 'btn btn-accent btn-block';
    btn.textContent = '❤️ 已收藏';
    showToast('❤️ 已加入收藏夹');
  }
  localStorage.setItem('dogFavs', JSON.stringify(favs));
}

// ====== 百科 ======
function getFilteredBreeds() {
  let list = BREEDS;
  if (wikiSearch) {
    const q = wikiSearch.toLowerCase();
    list = list.filter(b => b.zh.includes(q) || b.en.toLowerCase().includes(q) || b.origin.includes(q) || b.tags.some(t=>t.includes(q)));
  }
  if (wikiFilter !== 'all') {
    list = list.filter(b => b.tags.includes(wikiFilter) || b.size.includes(wikiFilter));
  }
  return list;
}

function renderWiki(reset = true) {
  const list = getFilteredBreeds();
  const perPage = 10;
  const container = document.getElementById('wiki-breed-list');
  const start = reset ? 0 : (wikiPage - 1) * perPage;
  const end = wikiPage * perPage;
  const slice = list.slice(reset ? 0 : start, end);
  if (reset) { container.innerHTML = ''; }
  if (reset && list.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">未找到相关品种</div><div class="empty-desc">换个关键词试试</div></div>`;
    document.getElementById('wiki-load-more').style.display = 'none';
    return;
  }
  slice.forEach(b => {
    const isCompare = compareIds.includes(b.id);
    const div = document.createElement('div');
    div.className = 'breed-item';
    div.setAttribute('data-id', b.id);
    div.innerHTML = `
      <div class="breed-avatar">${b.emoji}</div>
      <div class="breed-info">
        <div style="display:flex;align-items:center;gap:8px;">
          <div class="breed-name-zh">${b.zh}</div>
          <label onclick="event.stopPropagation();" style="display:flex;align-items:center;gap:3px;cursor:pointer;">
            <input type="checkbox" ${isCompare?'checked':''} onchange="toggleCompare(this,'${b.id}')" style="width:15px;height:15px;cursor:pointer;accent-color:var(--primary);">
            <span style="font-size:10px;color:var(--text-hint);">对比</span>
          </label>
        </div>
        <div class="breed-name-en">${b.en} · ${b.origin}</div>
        <div class="breed-meta">${b.tags.slice(0,3).map(t=>`<span class="badge badge-primary">${t}</span>`).join('')}</div>
      </div>
      <div style="color:var(--text-hint);font-size:22px;flex-shrink:0;">›</div>
    `;
    div.onclick = () => viewBreedDetail(b.id);
    container.appendChild(div);
  });
  document.getElementById('wiki-load-more').style.display = end < list.length ? 'block' : 'none';
}

function loadMoreBreeds() { wikiPage++; renderWiki(false); }

function onSearchInput() {
  wikiSearch = document.getElementById('wiki-search').value;
  document.getElementById('search-clear').style.display = wikiSearch ? 'block' : 'none';
  wikiPage = 1;
  renderWiki();
}

function clearSearch() {
  document.getElementById('wiki-search').value = '';
  wikiSearch = '';
  document.getElementById('search-clear').style.display = 'none';
  wikiPage = 1;
  renderWiki();
}

function filterBreeds(el, filter) {
  wikiFilter = filter;
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  wikiPage = 1;
  renderWiki();
}

function toggleCompare(cb, breedId) {
  if (cb.checked) {
    if (compareIds.length >= 3) { cb.checked = false; showToast('最多同时对比 3 个品种'); return; }
    compareIds.push(breedId);
  } else {
    compareIds = compareIds.filter(id => id !== breedId);
  }
  document.getElementById('compare-count').textContent = compareIds.length;
  const btn = document.getElementById('compare-btn');
  btn.style.display = compareIds.length >= 2 ? 'block' : 'none';
  const hint = document.getElementById('compare-hint');
  if (compareIds.length === 0) hint.textContent = '勾选2-3个品种可进行横向对比';
  else if (compareIds.length === 1) hint.textContent = '已选 1 个，再选1个即可对比';
  else hint.textContent = `已选 ${compareIds.length} 个品种，点击对比`;
}

function showCompare() {
  if (compareIds.length < 2) { showToast('请至少选择2个品种'); return; }
  const breeds = compareIds.map(id => BREEDS.find(b => b.id === id)).filter(Boolean);
  const fields = [
    ['体型分类','size'], ['体重范围','weight'], ['肩高','height'],
    ['寿命','lifespan'], ['运动需求','exercise'], ['掉毛程度','shedding'],
    ['毛发类型','coat'], ['原产地','origin']
  ];
  const headerRow = `<tr><th style="background:var(--bg);color:var(--text-hint);">对比项目</th>${breeds.map(b=>`<th>${b.zh}<br><span style="font-size:11px;font-weight:400;">${b.en}</span></th>`).join('')}</tr>`;
  const rows = fields.map(([label,key]) =>
    `<tr><td>${label}</td>${breeds.map(b=>`<td style="text-align:center;">${b[key]}</td>`).join('')}</tr>`
  ).join('');
  const personalityRow = `<tr><td>性格</td>${breeds.map(b=>`<td style="text-align:center;">${b.personality.slice(0,2).join('、')}</td>`).join('')}</tr>`;
  const diseaseRow = `<tr><td>常见疾病</td>${breeds.map(b=>`<td style="text-align:center;font-size:12px;">${b.diseases.slice(0,2).join('<br>')}</td>`).join('')}</tr>`;

  document.getElementById('compare-content').innerHTML = `
    <table class="compare-table"><thead>${headerRow}</thead><tbody>${rows}${personalityRow}${diseaseRow}</tbody></table>
  `;
  document.getElementById('compare-modal').classList.add('show');
}

function closeCompare(e) {
  if (!e || e.target === document.getElementById('compare-modal')) {
    document.getElementById('compare-modal').classList.remove('show');
  }
}

// ====== 历史记录 ======
function renderHistory() {
  const list = document.getElementById('history-list');
  const empty = document.getElementById('history-empty');
  const count = document.getElementById('history-count');
  if (historyData.length === 0) {
    list.innerHTML = '';
    empty.style.display = 'block';
    count.textContent = '共 0 条记录';
    return;
  }
  empty.style.display = 'none';
  count.textContent = `共 ${historyData.length} 条记录`;
  list.innerHTML = historyData.map(r => `
    <div class="history-item" onclick="viewBreedDetail('${r.breed_id}')">
      <div class="history-thumb">${r.emoji || '🐕'}</div>
      <div class="history-content">
        <div class="history-breed">${r.zh}</div>
        <div class="history-conf">置信度：${(r.confidence * 100).toFixed(1)}%&nbsp;·&nbsp;${r.size || ''}</div>
        <div class="history-time">${formatTime(r.time)}</div>
      </div>
      <div class="history-del" onclick="event.stopPropagation();deleteHistory(${r.id})">🗑️</div>
    </div>
  `).join('');
}

function deleteHistory(id) {
  historyData = historyData.filter(r => r.id !== id);
  localStorage.setItem('dogHistory', JSON.stringify(historyData));
  renderHistory();
  showToast('已删除记录');
}

function clearAllHistory() {
  if (!confirm('确认清空所有历史记录？此操作不可恢复。')) return;
  historyData = [];
  localStorage.setItem('dogHistory', JSON.stringify(historyData));
  renderHistory();
  showToast('历史记录已清空');
}

function exportCSV() {
  if (historyData.length === 0) { showToast('暂无历史记录'); return; }
  const header = ['时间','品种（中文）','品种（英文）','置信度','体型'];
  const rows = historyData.map(r => [
    new Date(r.time).toLocaleString('zh-CN'),
    r.zh, r.en || '',
    (r.confidence * 100).toFixed(1) + '%',
    r.size || ''
  ]);
  const csv = [header, ...rows].map(row => row.map(v => `"${v}"`).join(',')).join('\n');
  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `犬博士识别历史_${new Date().toLocaleDateString('zh-CN').replace(/\//g,'-')}.csv`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('✅ CSV 文件已导出');
}

function formatTime(iso) {
  const d = new Date(iso);
  const now = new Date();
  const diff = (now - d) / 1000;
  if (diff < 60) return '刚刚';
  if (diff < 3600) return `${Math.floor(diff/60)} 分钟前`;
  if (diff < 86400) return `${Math.floor(diff/3600)} 小时前`;
  return d.toLocaleDateString('zh-CN') + ' ' + d.toLocaleTimeString('zh-CN', {hour:'2-digit',minute:'2-digit'});
}

// ====== 数据统计 - ECharts ======
function initCharts() {
  initBreedDistChart();
  initTrainAccChart();
  initTrainLossChart();
  initConfidenceChart();
  initConfusionChart();
}

function makeEChartSafe(domId) {
  const el = document.getElementById(domId);
  if (!el) return null;
  try { return echarts.init(el, null, { renderer: 'canvas' }); } catch(e) { return null; }
}

function initBreedDistChart() {
  const chart = makeEChartSafe('chart-breed-dist');
  if (!chart) return;
  const data = BREEDS.slice(0,10).map(b => ({
    name: b.zh,
    value: Math.floor(200 + Math.random() * 1800)
  }));
  chart.setOption({
    tooltip: { trigger:'item', formatter: '{b}: {c}次 ({d}%)' },
    legend: { orient:'vertical', right:10, top:'center', textStyle:{fontSize:11} },
    series: [{
      type:'pie', radius:['40%','70%'], center:['35%','50%'],
      avoidLabelOverlap:false, label:{show:false},
      emphasis:{ label:{show:true,fontSize:14,fontWeight:'bold'} },
      data: data,
      color:['#4A90D9','#5ba8f0','#6ab4ff','#FF7B54','#ffa07a','#27ae60','#3498db','#9b59b6','#e67e22','#e74c3c']
    }]
  });
}

function initTrainAccChart() {
  const chart = makeEChartSafe('chart-train-acc');
  if (!chart) return;
  const epochs = Array.from({length:100},(_,i)=>i+1);
  const trainAcc = epochs.map(e => Math.min(0.98, 0.3 + 0.007*e + (Math.random()-0.5)*0.02));
  const valAcc   = epochs.map(e => Math.min(0.96, 0.24 + 0.007*e + (Math.random()-0.5)*0.025));
  chart.setOption({
    tooltip:{trigger:'axis'}, legend:{data:['训练集准确率','验证集准确率'], top:0},
    grid:{top:40,right:20,bottom:30,left:50},
    xAxis:{type:'value',name:'Epoch',min:1,max:100,nameLocation:'end'},
    yAxis:{type:'value',name:'准确率',min:0.2,max:1,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'}},
    series:[
      {name:'训练集准确率',type:'line',data:epochs.map((e,i)=>[e,trainAcc[i]]),smooth:true,lineStyle:{width:2},color:'#4A90D9',showSymbol:false},
      {name:'验证集准确率',type:'line',data:epochs.map((e,i)=>[e,valAcc[i]]),smooth:true,lineStyle:{width:2,type:'dashed'},color:'#FF7B54',showSymbol:false}
    ]
  });
}

function initTrainLossChart() {
  const chart = makeEChartSafe('chart-train-loss');
  if (!chart) return;
  const epochs = Array.from({length:100},(_,i)=>i+1);
  const trainLoss = epochs.map(e => Math.max(0.05, 2.0 - 0.02*e + (Math.random()-0.5)*0.08));
  const valLoss   = epochs.map(e => Math.max(0.08, 2.1 - 0.019*e + (Math.random()-0.5)*0.1));
  chart.setOption({
    tooltip:{trigger:'axis'}, legend:{data:['训练集损失','验证集损失'],top:0},
    grid:{top:40,right:20,bottom:30,left:50},
    xAxis:{type:'value',name:'Epoch',min:1,max:100,nameLocation:'end'},
    yAxis:{type:'value',name:'Loss',min:0,axisLabel:{formatter:v=>v.toFixed(2)}},
    series:[
      {name:'训练集损失',type:'line',data:epochs.map((e,i)=>[e,trainLoss[i]]),smooth:true,lineStyle:{width:2},color:'#4A90D9',showSymbol:false,areaStyle:{opacity:0.1}},
      {name:'验证集损失',type:'line',data:epochs.map((e,i)=>[e,valLoss[i]]),smooth:true,lineStyle:{width:2,type:'dashed'},color:'#FF7B54',showSymbol:false}
    ]
  });
}

function initConfidenceChart() {
  const chart = makeEChartSafe('chart-confidence');
  if (!chart) return;
  const buckets = ['0-10%','10-20%','20-30%','30-40%','40-50%','50-60%','60-70%','70-80%','80-90%','90-100%'];
  const counts = [12, 28, 45, 89, 156, 289, 412, 673, 1456, 2863];
  chart.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{top:20,right:20,bottom:40,left:55},
    xAxis:{type:'category',data:buckets,axisLabel:{fontSize:10,interval:0,rotate:30}},
    yAxis:{type:'value',name:'次数'},
    series:[{type:'bar',data:counts,itemStyle:{color:function(params){return params.dataIndex>=6?'#4A90D9':'#ccd4e0';}},barMaxWidth:30}]
  });
}

function initConfusionChart() {
  const chart = makeEChartSafe('chart-confusion');
  if (!chart) return;
  const labels = ['哈士奇','金毛','拉布拉多','德牧','柴犬','边牧','贵宾','法斗'];
  const n = labels.length;
  const data = [];
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      let v;
      if (i === j) v = 80 + Math.floor(Math.random() * 18);
      else { const base = (i===0&&j===2)||(i===2&&j===0)||(i===1&&j===2) ? 8+Math.floor(Math.random()*6) : Math.floor(Math.random()*5); v = base; }
      data.push([j, i, v]);
    }
  }
  chart.setOption({
    tooltip:{position:'top',formatter:params=>`${labels[params.data[1]]} → ${labels[params.data[0]]}: ${params.data[2]}%`},
    grid:{top:30,right:20,bottom:30,left:80},
    xAxis:{type:'category',data:labels,axisLabel:{fontSize:11},splitArea:{show:true}},
    yAxis:{type:'category',data:labels,axisLabel:{fontSize:11},splitArea:{show:true}},
    visualMap:{min:0,max:100,calculable:true,orient:'horizontal',left:'center',bottom:-10,show:false,
      inRange:{color:['#f0f8ff','#4A90D9']}},
    series:[{type:'heatmap',data,emphasis:{itemStyle:{shadowBlur:10}},label:{show:true,fontSize:10}}]
  });
}

// ====== 初始化入口 ======
window.addEventListener('DOMContentLoaded', () => {
  initHome();
  // 响应窗口大小变化
  window.addEventListener('resize', () => {
    if (statsChartInit) {
      ['chart-breed-dist','chart-train-acc','chart-train-loss','chart-confidence','chart-confusion'].forEach(id => {
        const c = echarts.getInstanceByDom(document.getElementById(id));
        if (c) c.resize();
      });
    }
  });
});
