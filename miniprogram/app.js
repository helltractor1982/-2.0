// app.js - 犬博士小程序入口
const BREEDS = require('./utils/breeds.js');

App({
  onLaunch() {
    // 初始化本地存储
    const history = wx.getStorageSync('identify_history') || [];
    const favorites = wx.getStorageSync('favorites') || [];
    const stats = wx.getStorageSync('usage_stats') || { total: 0, today: 0, date: '' };

    // 重置每日统计
    const today = new Date().toDateString();
    if (stats.date !== today) {
      stats.today = 0;
      stats.date = today;
      wx.setStorageSync('usage_stats', stats);
    }

    this.globalData.history = history;
    this.globalData.favorites = favorites;
    this.globalData.stats = stats;
    this.globalData.breeds = BREEDS;

    console.log('[犬博士] 小程序启动完成');
    console.log('[犬博士] 已加载 ' + BREEDS.length + ' 个品种数据');
  },

  onShow() {
    // 小程序切前台时刷新数据
    this.globalData.history = wx.getStorageSync('identify_history') || [];
    this.globalData.favorites = wx.getStorageSync('favorites') || [];
  },

  globalData: {
    apiBase: 'http://localhost:8000/api',
    history: [],
    favorites: [],
    stats: { total: 0, today: 0, date: '' },
    breeds: [],
    // 从后端识别或本地模拟
    useLocalMock: true
  }
});
