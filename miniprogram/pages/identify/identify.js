// pages/identify/identify.js
const api = require('../../utils/api.js');
const util = require('../../utils/util.js');
const BREEDS = require('../../utils/breeds.js');

Page({
  data: {
    imagePath: '',
    identifying: false,
    identifyTip: 'AI 正在分析中...',
    results: null
  },

  // 拍照
  takePhoto() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['camera'],
      success: (res) => {
        this.setData({ imagePath: res.tempFilePaths[0], results: null });
      }
    });
  },

  // 从相册选择
  choosePhoto() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album'],
      success: (res) => {
        this.setData({ imagePath: res.tempFilePaths[0], results: null });
      }
    });
  },

  // 开始识别
  async startIdentify() {
    if (!this.data.imagePath) return;
    this.setData({ identifying: true, identifyTip: 'AI 正在分析中...' });

    const tips = [
      '正在提取图像特征...',
      '正在匹配品种数据库...',
      '正在计算置信度...',
      '马上揭晓结果！'
    ];
    let tipIndex = 0;
    const tipTimer = setInterval(() => {
      tipIndex = (tipIndex + 1) % tips.length;
      this.setData({ identifyTip: tips[tipIndex] });
    }, 800);

    try {
      const data = await api.identifyBreed(this.data.imagePath, 5);
      clearInterval(tipTimer);

      // 丰富结果数据（添加品种详细信息）
      const results = data.results.map(r => {
        const breed = BREEDS.getBreedById(r.breed_id);
        return { ...r, ...breed };
      });

      this.setData({ identifying: false, results });

      // 保存到历史记录
      util.addHistory({
        imagePath: this.data.imagePath,
        results: results.map(r => ({
          breed_id: r.breed_id,
          name_zh: r.name_zh,
          name_en: r.name_en,
          confidence: r.confidence
        })),
        topBreed: results[0]
      });

      // 更新统计数据
      util.addUsageCount();

      if (data.mock) {
        util.showToast('使用本地模拟识别（后端未连接）', 'none', 2500);
      }
    } catch (err) {
      clearInterval(tipTimer);
      this.setData({ identifying: false });
      util.showToast('识别失败：' + (err.message || '请重试'), 'none');
    }
  },

  // 重新选择图片
  reChoose() {
    this.setData({ imagePath: '', results: null });
  },

  // 查看品种详情
  viewDetail(e) {
    const breedId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: '/pages/detail/detail?breedId=' + breedId });
  },

  // 返回首页
  goHome() {
    wx.switchTab({ url: '/pages/home/home' });
  }
});
