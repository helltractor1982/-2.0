// pages/about/about.js
const util = require('../../utils/util.js');

Page({
  data: {
    stats: { total: 0, today: 0, collection: 0 }
  },

  onLoad() {
    this.calculateStats();
  },

  onShow() {
    this.calculateStats();
  },

  calculateStats() {
    const stats = util.getUsageStats();
    const favorites = util.getFavorites();
    this.setData({
      stats: {
        total: stats.total || 0,
        today: stats.today || 0,
        collection: favorites.length || 0
      }
    });
  },

  // 使用帮助
  openDocs() {
    util.showToast('帮助文档开发中', 'none');
  },

  // 意见反馈
  openFeedback() {
    wx.showModal({
      title: '意见反馈',
      content: '感谢您的使用！如有建议或问题，欢迎联系我们。',
      showCancel: false,
      confirmText: '知道了'
    });
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '犬博士 - AI 宠物犬品种智能鉴别助手，快来试试吧！',
      path: '/pages/home/home',
      imageUrl: ''
    };
  }
});
