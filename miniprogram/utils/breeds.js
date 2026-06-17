// utils/breeds.js - 品种数据库（30个品种，含完整信息）
const BREEDS = [
  {
    breed_id: '001', name_zh: '西伯利亚雪橇犬', name_en: 'Siberian Husky',
    origin: '俄罗斯西伯利亚', size: '中型犬', group: '工作犬',
    lifespan: '12-15年', weight: '16-27kg', height: '50-60cm',
    temperament: ['活泼', '友善', '调皮', '独立'],
    coat: '双层毛', coatLength: '中等', colors: ['黑白', '灰白', '红白', '纯白'],
    exercise: '高', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，选择高蛋白犬粮，注意控制食量',
    commonDiseases: ['白内障', '髋关节发育不良', '甲状腺功能减退'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛3-4次，换毛季每天梳理',
    funFact: '哈士奇的嚎叫可以传到16公里之外',
    emoji: '🐺'
  },
  {
    breed_id: '002', name_zh: '金毛寻回犬', name_en: 'Golden Retriever',
    origin: '英国苏格兰', size: '大型犬', group: '寻回犬',
    lifespan: '10-12年', weight: '25-34kg', height: '51-61cm',
    temperament: ['温顺', '聪明', '忠诚', '友善', '耐心'],
    coat: '双层毛', coatLength: '中等偏长', colors: ['金黄', '浅金', '奶油色'],
    exercise: '高', trainability: '极高', guardAbility: '低',
    feeding: '每日2次，控制体重避免肥胖，选择大型犬配方',
    commonDiseases: ['髋关节发育不良', '癌症', '皮肤病', '肘关节发育不良'],
    vaccineSchedule: '幼犬6-8周首免，第12周加强，每年补种',
    grooming: '每周梳毛2-3次，换毛季每天梳理',
    funFact: '金毛的智商排名犬类第四，相当于2-3岁儿童的智力',
    emoji: '🦮'
  },
  {
    breed_id: '003', name_zh: '拉布拉多寻回犬', name_en: 'Labrador Retriever',
    origin: '加拿大纽芬兰', size: '大型犬', group: '寻回犬',
    lifespan: '10-14年', weight: '25-36kg', height: '54-62cm',
    temperament: ['友善', '活泼', '忠诚', '聪明', '温和'],
    coat: '短毛', coatLength: '短', colors: ['黑色', '黄色', '巧克力色'],
    exercise: '高', trainability: '极高', guardAbility: '中等',
    feeding: '每日2次，易肥胖需控制食量，选用低脂犬粮',
    commonDiseases: ['髋关节发育不良', '肥胖', '耳部感染', '肘关节发育不良'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1-2次，保持耳朵清洁干燥',
    funFact: '拉布拉多连续30年蝉联美国最受欢迎犬种',
    emoji: '🐕‍🦺'
  },
  {
    breed_id: '004', name_zh: '德国牧羊犬', name_en: 'German Shepherd',
    origin: '德国', size: '大型犬', group: '牧羊犬',
    lifespan: '9-13年', weight: '22-40kg', height: '55-65cm',
    temperament: ['忠诚', '勇敢', '聪明', '自信', '服从'],
    coat: '双层毛', coatLength: '中等', colors: ['黑褐', '纯黑', '黑红', '貂色'],
    exercise: '极高', trainability: '极高', guardAbility: '极高',
    feeding: '每日2次，高蛋白配方，注意关节健康补充',
    commonDiseases: ['髋关节发育不良', '退行性脊髓病', '胃扭转', '皮肤病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次，换毛季每天梳理',
    funFact: '德牧是警犬和军犬中使用率最高的犬种',
    emoji: '🐕'
  },
  {
    breed_id: '005', name_zh: '柯基犬', name_en: 'Pembroke Welsh Corgi',
    origin: '英国威尔士', size: '小型犬', group: '牧羊犬',
    lifespan: '12-15年', weight: '10-14kg', height: '25-30cm',
    temperament: ['聪明', '活泼', '勇敢', '忠诚', '固执'],
    coat: '双层毛', coatLength: '中等', colors: ['红白', '三色', '貂色'],
    exercise: '中高', trainability: '高', guardAbility: '中等',
    feeding: '每日2次，容易发胖需严格控制食量',
    commonDiseases: ['椎间盘疾病', '髋关节发育不良', '白内障', '肥胖'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次，定期修剪指甲',
    funFact: '柯基在威尔士语中的意思是"矮小的狗"',
    emoji: '🐶'
  },
  {
    breed_id: '006', name_zh: '泰迪犬', name_en: 'Toy Poodle',
    origin: '法国', size: '小型犬', group: '伴侣犬',
    lifespan: '12-18年', weight: '2-4kg', height: '24-28cm',
    temperament: ['聪明', '活泼', '敏感', '忠诚', '优雅'],
    coat: '卷毛', coatLength: '长', colors: ['棕色', '黑色', '白色', '灰色', '杏色'],
    exercise: '中等', trainability: '极高', guardAbility: '中等',
    feeding: '每日2-3次，小型犬专用配方，注意口腔健康',
    commonDiseases: ['泪痕', '皮肤病', '髌骨脱位', '牙齿问题'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每4-6周专业美容一次，每日梳理防打结',
    funFact: '贵宾犬是所有犬种中智商排名第二的',
    emoji: '🐩'
  },
  {
    breed_id: '007', name_zh: '边境牧羊犬', name_en: 'Border Collie',
    origin: '英国苏格兰', size: '中型犬', group: '牧羊犬',
    lifespan: '12-15年', weight: '14-20kg', height: '46-56cm',
    temperament: ['聪明', '敏捷', '忠诚', '精力充沛', '好学'],
    coat: '双层毛', coatLength: '中等偏长', colors: ['黑白', '三色', '红白', '蓝陨石'],
    exercise: '极高', trainability: '极高', guardAbility: '中等',
    feeding: '每日2次，高蛋白高能量配方',
    commonDiseases: ['髋关节发育不良', '癫痫', '视网膜萎缩', '对药物敏感'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次',
    funFact: '边境牧羊犬被公认为世界上最聪明的犬种',
    emoji: '🐑'
  },
  {
    breed_id: '008', name_zh: '法国斗牛犬', name_en: 'French Bulldog',
    origin: '法国', size: '小型犬', group: '伴侣犬',
    lifespan: '10-14年', weight: '8-14kg', height: '28-33cm',
    temperament: ['温和', '友善', '爱玩', '忠诚', '安静'],
    coat: '短毛', coatLength: '短', colors: ['虎斑', '奶油', '黑白', '蓝色'],
    exercise: '低', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，易发胖需控制食量，注意食物过敏',
    commonDiseases: ['呼吸困难', '皮肤病', '脊椎疾病', '眼部疾病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1次，注意面部褶皱清洁',
    funFact: '法斗不会游泳，因为头部太重且腿太短',
    emoji: '🐾'
  },
  {
    breed_id: '009', name_zh: '柴犬', name_en: 'Shiba Inu',
    origin: '日本', size: '中型犬', group: '原始犬',
    lifespan: '12-16年', weight: '8-11kg', height: '35-43cm',
    temperament: ['独立', '忠诚', '警觉', '勇敢', '固执'],
    coat: '双层毛', coatLength: '中等', colors: ['赤色', '黑褐', '芝麻', '白色'],
    exercise: '中高', trainability: '中等偏低', guardAbility: '高',
    feeding: '每日2次，选择优质犬粮，注意控制体重',
    commonDiseases: ['髌骨脱位', '皮肤病', '青光眼', '过敏'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次，换毛季每天梳理',
    funFact: '柴犬是日本最古老的犬种之一，可追溯到公元前300年',
    emoji: '🦊'
  },
  {
    breed_id: '010', name_zh: '萨摩耶犬', name_en: 'Samoyed',
    origin: '俄罗斯西伯利亚', size: '大型犬', group: '工作犬',
    lifespan: '12-14年', weight: '16-30kg', height: '48-60cm',
    temperament: ['友善', '温和', '活泼', '忠诚', '爱笑'],
    coat: '双层毛', coatLength: '长', colors: ['纯白', '奶油白', '饼干色'],
    exercise: '高', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，优质犬粮，注意皮肤健康',
    commonDiseases: ['髋关节发育不良', '糖尿病', '皮肤病', '白内障'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛防止打结，每月洗澡1次',
    funFact: '萨摩耶的嘴角天然上翘，被称为"微笑天使"',
    emoji: '☁️'
  },
  {
    breed_id: '011', name_zh: '比熊犬', name_en: 'Bichon Frise',
    origin: '地中海地区', size: '小型犬', group: '伴侣犬',
    lifespan: '12-15年', weight: '5-10kg', height: '23-30cm',
    temperament: ['活泼', '友善', '温柔', '爱玩', '开朗'],
    coat: '卷毛', coatLength: '长', colors: ['纯白', '奶油色', '杏色'],
    exercise: '中等', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，小型犬配方，注意口腔卫生',
    commonDiseases: ['皮肤病', '牙齿问题', '髌骨脱位', '眼部疾病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每4-6周美容一次，每天梳毛',
    funFact: '比熊曾是欧洲皇室最爱的伴侣犬',
    emoji: '☁️'
  },
  {
    breed_id: '012', name_zh: '博美犬', name_en: 'Pomeranian',
    origin: '德国/波兰', size: '小型犬', group: '伴侣犬',
    lifespan: '12-16年', weight: '1.5-3.5kg', height: '18-28cm',
    temperament: ['活泼', '聪明', '好奇', '忠诚', '警惕'],
    coat: '双层毛', coatLength: '长', colors: ['橙色', '奶油', '黑色', '棕色', '白色'],
    exercise: '中等', trainability: '高', guardAbility: '高',
    feeding: '每日2-3次，小型犬专用配方',
    commonDiseases: ['髌骨脱位', '气管塌陷', '牙齿问题', '脱毛'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每2-3天梳毛一次，每6-8周美容',
    funFact: '博美的祖先曾经是大型雪橇犬',
    emoji: '🦁'
  },
  {
    breed_id: '013', name_zh: '哈瓦那犬', name_en: 'Havanese',
    origin: '古巴', size: '小型犬', group: '伴侣犬',
    lifespan: '13-16年', weight: '3-6kg', height: '21-29cm',
    temperament: ['活泼', '友善', '聪明', '开朗', '爱社交'],
    coat: '长毛', coatLength: '长', colors: ['白色', '奶油', '金色', '黑色', '巧克力'],
    exercise: '中等', trainability: '高', guardAbility: '中等',
    feeding: '每日2次，小型犬配方',
    commonDiseases: ['髌骨脱位', '白内障', '心脏病', '耳聋'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛，每6-8周修剪',
    funFact: '哈瓦那犬是古巴唯一的本土犬种，也是国犬',
    emoji: '🐾'
  },
  {
    breed_id: '014', name_zh: '雪纳瑞', name_en: 'Miniature Schnauzer',
    origin: '德国', size: '小型犬', group: '梗犬',
    lifespan: '12-15年', weight: '5-9kg', height: '30-36cm',
    temperament: ['聪明', '活泼', '忠诚', '勇敢', '警觉'],
    coat: '刚毛', coatLength: '中等', colors: ['椒盐色', '纯黑', '黑银'],
    exercise: '中高', trainability: '高', guardAbility: '高',
    feeding: '每日2次，注意胰腺健康，低脂饮食',
    commonDiseases: ['胰腺炎', '膀胱结石', '皮肤病', '眼疾'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每6-8周专业美容一次，每周梳毛2-3次',
    funFact: '雪纳瑞的名字来源于德语"鼻子"，因为它们的胡须很特别',
    emoji: '👨'
  },
  {
    breed_id: '015', name_zh: '约克夏梗', name_en: 'Yorkshire Terrier',
    origin: '英国', size: '小型犬', group: '玩具犬',
    lifespan: '12-16年', weight: '2-3.5kg', height: '15-23cm',
    temperament: ['勇敢', '聪明', '独立', '活泼', '深情'],
    coat: '丝质长毛', coatLength: '长', colors: ['蓝金', '黑金'],
    exercise: '中等', trainability: '中等', guardAbility: '高',
    feeding: '每日2-3次，小型犬配方，注意低血糖',
    commonDiseases: ['髌骨脱位', '气管塌陷', '牙齿问题', '肝门脉分流'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛，长发需定期修剪',
    funFact: '约克夏在二战时期被用作战场通信犬',
    emoji: '🎀'
  },
  {
    breed_id: '016', name_zh: '阿拉斯加雪橇犬', name_en: 'Alaskan Malamute',
    origin: '美国阿拉斯加', size: '大型犬', group: '工作犬',
    lifespan: '10-14年', weight: '32-43kg', height: '58-66cm',
    temperament: ['忠诚', '友善', '独立', '精力充沛', '温顺'],
    coat: '双层毛', coatLength: '中等偏长', colors: ['灰白', '黑白', '红白', '纯白'],
    exercise: '极高', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，大型犬高能量配方',
    commonDiseases: ['髋关节发育不良', '胃扭转', '白内障', '甲状腺功能减退'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛3-4次，换毛季每天梳理',
    funFact: '阿拉斯加是最古老的雪橇犬之一，可以拉动体重数倍的货物',
    emoji: '🐺'
  },
  {
    breed_id: '017', name_zh: '吉娃娃', name_en: 'Chihuahua',
    origin: '墨西哥', size: '超小型犬', group: '玩具犬',
    lifespan: '14-20年', weight: '1-3kg', height: '15-23cm',
    temperament: ['勇敢', '忠诚', '活泼', '警惕', '机灵'],
    coat: '短毛/长毛', coatLength: '短或长', colors: ['多种颜色'],
    exercise: '低', trainability: '中等', guardAbility: '高',
    feeding: '每日2-3次，极小型犬配方，注意低血糖',
    commonDiseases: ['髌骨脱位', '低血糖', '心脏病', '牙齿问题', '气管塌陷'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '短毛每周1次，长毛每日梳毛',
    funFact: '吉娃娃是世界上体型最小的犬种，以墨西哥的一个州命名',
    emoji: '🐭'
  },
  {
    breed_id: '018', name_zh: '罗威纳犬', name_en: 'Rottweiler',
    origin: '德国', size: '大型犬', group: '工作犬',
    lifespan: '8-11年', weight: '35-60kg', height: '56-69cm',
    temperament: ['忠诚', '勇敢', '自信', '冷静', '护主'],
    coat: '短毛', coatLength: '短', colors: ['黑褐'],
    exercise: '高', trainability: '极高', guardAbility: '极高',
    feeding: '每日2次，大型犬配方，注意体重管理',
    commonDiseases: ['髋关节发育不良', '骨癌', '胃扭转', '心脏病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1-2次',
    funFact: '罗威纳曾是古罗马军团的战犬和牧牛犬',
    emoji: '🦍'
  },
  {
    breed_id: '019', name_zh: '中华田园犬', name_en: 'Chinese Rural Dog',
    origin: '中国', size: '中型犬', group: '原生犬',
    lifespan: '12-17年', weight: '12-25kg', height: '40-55cm',
    temperament: ['忠诚', '聪明', '警觉', '独立', '适应性强'],
    coat: '短毛/中毛', coatLength: '短到中等', colors: ['黄', '黑', '白', '花', '棕'],
    exercise: '中高', trainability: '高', guardAbility: '高',
    feeding: '每日2次，适应性好，选择均衡犬粮即可',
    commonDiseases: ['抗病力较强', '寄生虫', '皮肤病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '短毛每周1次，中毛每周2-3次',
    funFact: '中华田园犬已有数千年历史，是中国最古老的犬种之一',
    emoji: '🐕'
  },
  {
    breed_id: '020', name_zh: '松狮犬', name_en: 'Chow Chow',
    origin: '中国', size: '中型犬', group: '原始犬',
    lifespan: '9-15年', weight: '20-32kg', height: '46-56cm',
    temperament: ['独立', '忠诚', '安静', '高傲', '护主'],
    coat: '双层毛', coatLength: '长', colors: ['红', '黑', '蓝', '奶油', '肉桂'],
    exercise: '中等', trainability: '中等偏低', guardAbility: '高',
    feeding: '每日2次，注意皮肤和毛发健康',
    commonDiseases: ['髋关节发育不良', '眼睑内翻', '皮肤病', '胃扭转'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛，每月洗澡1-2次',
    funFact: '松狮犬是唯一拥有蓝黑色舌头的犬种',
    emoji: '🦁'
  },
  {
    breed_id: '021', name_zh: '大丹犬', name_en: 'Great Dane',
    origin: '德国', size: '超大型犬', group: '工作犬',
    lifespan: '7-10年', weight: '45-91kg', height: '71-86cm',
    temperament: ['温柔', '友善', '耐心', '忠诚', '沉稳'],
    coat: '短毛', coatLength: '短', colors: ['黄褐', '虎斑', '黑白', '蓝色', '丑角'],
    exercise: '中等', trainability: '高', guardAbility: '高',
    feeding: '每日2次，超大型犬专用配方，注意胃扭转预防',
    commonDiseases: ['胃扭转', '髋关节发育不良', '心肌病', '骨癌'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1次',
    funFact: '大丹犬被称为"温柔的巨人"，最高可站立超过2米',
    emoji: '🦒'
  },
  {
    breed_id: '022', name_zh: '蝴蝶犬', name_en: 'Papillon',
    origin: '法国/比利时', size: '小型犬', group: '玩具犬',
    lifespan: '13-17年', weight: '2.5-5kg', height: '20-28cm',
    temperament: ['聪明', '活泼', '友善', '警觉', '好奇'],
    coat: '丝质长毛', coatLength: '中等偏长', colors: ['白色配任意色'],
    exercise: '中等', trainability: '极高', guardAbility: '中等',
    feeding: '每日2次，小型犬配方',
    commonDiseases: ['髌骨脱位', '牙齿问题', '眼疾'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次',
    funFact: '蝴蝶犬因耳朵像蝴蝶翅膀而得名，是玩具犬中最聪明的',
    emoji: '🦋'
  },
  {
    breed_id: '023', name_zh: '杜宾犬', name_en: 'Doberman Pinscher',
    origin: '德国', size: '大型犬', group: '工作犬',
    lifespan: '10-13年', weight: '27-45kg', height: '61-72cm',
    temperament: ['忠诚', '勇敢', '聪明', '警觉', '优雅'],
    coat: '短毛', coatLength: '短', colors: ['黑褐', '红褐', '蓝色', '浅黄'],
    exercise: '高', trainability: '极高', guardAbility: '极高',
    feeding: '每日2次，大型犬高蛋白配方',
    commonDiseases: ['扩张型心肌病', '髋关节发育不良', '血友病', '颈椎病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1-2次',
    funFact: '杜宾犬是由一位德国税务官培育的，用于保护自己收税时的安全',
    emoji: '💂'
  },
  {
    breed_id: '024', name_zh: '巴哥犬', name_en: 'Pug',
    origin: '中国', size: '小型犬', group: '玩具犬',
    lifespan: '12-16年', weight: '6-9kg', height: '25-33cm',
    temperament: ['温和', '爱玩', '忠诚', '固执', '安静'],
    coat: '短毛', coatLength: '短', colors: ['杏色', '黑色', '银色'],
    exercise: '低', trainability: '中等偏低', guardAbility: '低',
    feeding: '每日2次，极易发胖需严格控制食量',
    commonDiseases: ['呼吸困难', '眼部疾病', '皮肤病', '肥胖', '脑炎'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1次，面部褶皱需每日清洁',
    funFact: '巴哥犬在中国古代曾是皇室专宠，被誉为"袖犬"',
    emoji: '😛'
  },
  {
    breed_id: '025', name_zh: '西施犬', name_en: 'Shih Tzu',
    origin: '中国西藏', size: '小型犬', group: '玩具犬',
    lifespan: '10-18年', weight: '4-8kg', height: '20-28cm',
    temperament: ['友善', '活泼', '忠诚', '外向', '温和'],
    coat: '长毛', coatLength: '长', colors: ['多种颜色组合'],
    exercise: '中等偏低', trainability: '中等', guardAbility: '低',
    feeding: '每日2次，小型犬配方，注意口腔健康',
    commonDiseases: ['眼疾', '呼吸道疾病', '牙齿问题', '髌骨脱位'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛，每4-6周美容修剪',
    funFact: '西施这个名字来源于中国古代四大美女之一的西施',
    emoji: '👑'
  },
  {
    breed_id: '026', name_zh: '英国斗牛犬', name_en: 'English Bulldog',
    origin: '英国', size: '中型犬', group: '伴侣犬',
    lifespan: '8-12年', weight: '18-25kg', height: '31-40cm',
    temperament: ['温和', '勇敢', '忠诚', '固执', '友善'],
    coat: '短毛', coatLength: '短', colors: ['虎斑', '纯白', '红色', '浅黄', '花斑'],
    exercise: '低', trainability: '中等偏低', guardAbility: '中等',
    feeding: '每日2次，注意体重控制，易过敏体质',
    commonDiseases: ['呼吸困难', '皮肤病', '髋关节发育不良', '心脏病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1-2次，面部褶皱需每日清洁',
    funFact: '英国斗牛犬是英国的国犬，象征着坚韧不拔的精神',
    emoji: '💪'
  },
  {
    breed_id: '027', name_zh: '哈士奇', name_en: 'Siberian Husky',
    origin: '俄罗斯西伯利亚', size: '中型犬', group: '工作犬',
    lifespan: '12-15年', weight: '16-27kg', height: '50-60cm',
    temperament: ['活泼', '友善', '调皮', '独立', '热情'],
    coat: '双层毛', coatLength: '中等', colors: ['黑白', '灰白', '红白', '纯白'],
    exercise: '高', trainability: '中等偏低', guardAbility: '低',
    feeding: '每日2次，高蛋白配方',
    commonDiseases: ['白内障', '髋关节发育不良', '癫痫'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛3-4次，换毛季每天梳理',
    funFact: '哈士奇是拆家小能手，精力充沛需要大量运动',
    emoji: '🐺'
  },
  {
    breed_id: '028', name_zh: '马尔济斯犬', name_en: 'Maltese',
    origin: '马耳他', size: '小型犬', group: '玩具犬',
    lifespan: '12-16年', weight: '2-4kg', height: '20-25cm',
    temperament: ['温柔', '活泼', '忠诚', '爱玩', '胆大'],
    coat: '丝质长毛', coatLength: '长', colors: ['纯白'],
    exercise: '中等', trainability: '中等', guardAbility: '中等',
    feeding: '每日2次，小型犬配方，注意低血糖',
    commonDiseases: ['牙齿问题', '皮肤病', '眼疾', '髌骨脱位'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每天梳毛，每4周美容一次',
    funFact: '马尔济斯已有近3000年历史，是世界上最古老的犬种之一',
    emoji: '🤍'
  },
  {
    breed_id: '029', name_zh: '秋田犬', name_en: 'Akita',
    origin: '日本秋田县', size: '大型犬', group: '工作犬',
    lifespan: '10-15年', weight: '32-59kg', height: '58-71cm',
    temperament: ['忠诚', '勇敢', '独立', '沉着', '护主'],
    coat: '双层毛', coatLength: '中等', colors: ['赤色', '虎斑', '白色', '芝麻'],
    exercise: '中高', trainability: '中等', guardAbility: '极高',
    feeding: '每日2次，大型犬配方',
    commonDiseases: ['髋关节发育不良', '胃扭转', '甲状腺功能减退', '皮肤病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛2-3次，换毛季每天梳理',
    funFact: '忠犬八公就是一只秋田犬，它的故事感动了全世界',
    emoji: '🐕'
  },
  {
    breed_id: '030', name_zh: '比格犬', name_en: 'Beagle',
    origin: '英国', size: '中型犬', group: '猎犬',
    lifespan: '12-15年', weight: '9-16kg', height: '33-41cm',
    temperament: ['友善', '好奇', '活泼', '温和', '爱叫'],
    coat: '短毛', coatLength: '短', colors: ['三色', '柠檬白', '红白'],
    exercise: '中高', trainability: '中等', guardAbility: '中等',
    feeding: '每日2次，容易发胖需控制食量',
    commonDiseases: ['耳部感染', '癫痫', '甲状腺功能减退', '椎间盘疾病'],
    vaccineSchedule: '幼犬6-8周首免，每年加强接种',
    grooming: '每周梳毛1-2次，定期清洁耳朵',
    funFact: '比格犬拥有犬类中最灵敏的嗅觉之一，常被用作检疫犬',
    emoji: '🐰'
  }
];

// 获取所有品种
function getAllBreeds() {
  return BREEDS;
}

// 根据ID获取品种
function getBreedById(id) {
  return BREEDS.find(b => b.breed_id === id) || null;
}

// 搜索品种（按名称、英文名、原产地、性格）
function searchBreeds(keyword) {
  if (!keyword || !keyword.trim()) return getAllBreeds();
  const kw = keyword.trim().toLowerCase();
  return BREEDS.filter(b =>
    b.name_zh.includes(kw) ||
    b.name_en.toLowerCase().includes(kw) ||
    b.origin.includes(kw) ||
    b.temperament.some(t => t.includes(kw))
  );
}

// 按条件筛选品种
function filterBreeds({ size, group, keyword } = {}) {
  let result = BREEDS;
  if (size) result = result.filter(b => b.size === size);
  if (group) result = result.filter(b => b.group === group);
  if (keyword) result = result.filter(b =>
    b.name_zh.includes(keyword) ||
    b.name_en.toLowerCase().includes(keyword.toLowerCase()) ||
    b.origin.includes(keyword) ||
    b.temperament.some(t => t.includes(keyword))
  );
  return result;
}

// 获取所有体型分类
function getAllSizes() {
  return [...new Set(BREEDS.map(b => b.size))];
}

// 获取所有组别
function getAllGroups() {
  return [...new Set(BREEDS.map(b => b.group))];
}

// 获取随机推荐（每日推荐）
function getRandomBreeds(count = 3) {
  const shuffled = [...BREEDS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

// 今日推荐（基于日期确定性随机）
function getDailyRecommendation(count = 3) {
  const today = new Date();
  const seed = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
  const shuffled = [...BREEDS].sort((a, b) => {
    const ha = (a.breed_id.charCodeAt(0) * seed) % 1000;
    const hb = (b.breed_id.charCodeAt(0) * seed) % 1000;
    return ha - hb;
  });
  return shuffled.slice(0, count);
}

// 比较多个品种
function compareBreeds(ids) {
  return ids.map(id => getBreedById(id)).filter(Boolean);
}

module.exports = {
  BREEDS,
  getAllBreeds,
  getBreedById,
  searchBreeds,
  filterBreeds,
  getAllSizes,
  getAllGroups,
  getRandomBreeds,
  getDailyRecommendation,
  compareBreeds
};
