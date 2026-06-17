// pages/home/home.js
const BREEDS = require('../../utils/breeds.js');
const util = require('../../utils/util.js');

Page({
  data: {
    stats: { total: 0, today: 0 },
    favorites: [],
    recommendBreeds: [],
    searchKeyword: ''
  },

  onLoad() {
    this.refreshData();
  },

  onShow() {
    this.refreshData();
  },

  refreshData() {
    const stats = util.getUsageStats();
    const favorites = util.getFavorites();
    const recommendBreeds = BREEDS.getDailyRecommendation(5);

    this.setData({
      stats,
      favorites,
      recommendBreeds
    });
  },

  // 跳转识别页
  goIdentify() {
    wx.switchTab({ url: '/pages/identify/identify' });
  },

  // 跳转百科
  goWiki() {
    wx.switchTab({ url: '/pages/wiki/wiki' });
  },

  // 按体型浏览
  goWikiBySize(e) {
    const size = e.currentTarget.dataset.size;
    wx.switchTab({ url: '/pages/wiki/wiki' });
    // 通过全局数据传递筛选条件
    const app = getApp();
    app.globalData.wikiFilter = { size };
  },

  // 跳转历史记录
  goHistory() {
    wx.switchTab({ url: '/pages/history/history' });
  },

  // 跳转统计
  goStats() {
    wx.navigateTo({ url: '/pages/stats/stats' });
  },

  // 查看品种详情
  viewDetail(e) {
    const breedId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: '/pages/detail/detail?breedId=' + breedId });
  }
});
