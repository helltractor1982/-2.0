// pages/wiki/wiki.js
const BREEDS = require('../../utils/breeds.js');
const util = require('../../utils/util.js');

Page({
  data: {
    searchKeyword: '',
    activeSize: '',
    sortAsc: true,
    sizes: BREEDS.getAllSizes(),
    displayBreeds: [],
    favorites: [],
    compareList: []
  },

  onLoad() {
    this.initData();
  },

  onShow() {
    this.setData({ favorites: util.getFavorites() });
    // 检查是否有来自首页的筛选
    const app = getApp();
    if (app.globalData.wikiFilter) {
      const { size } = app.globalData.wikiFilter;
      this.setData({ activeSize: size });
      app.globalData.wikiFilter = null;
    }
    this.applyFilters();
  },

  initData() {
    const allBreeds = BREEDS.getAllBreeds();
    this.setData({
      displayBreeds: allBreeds,
      favorites: util.getFavorites()
    });
  },

  // 搜索输入
  onSearchInput(e) {
    this.setData({ searchKeyword: e.detail.value });
  },

  // 搜索确认
  onSearch() {
    this.setData({ searchKeyword: e.detail.value.trim() });
    this.applyFilters();
  },

  // 清除搜索
  clearSearch() {
    this.setData({ searchKeyword: '' });
    this.applyFilters();
  },

  // 按体型筛选
  filterBySize(e) {
    const size = e.currentTarget.dataset.size;
    this.setData({ activeSize: this.data.activeSize === size ? '' : size });
    this.applyFilters();
  },

  // 切换排序
  toggleSort() {
    this.setData({ sortAsc: !this.data.sortAsc });
    this.applyFilters();
  },

  // 应用筛选
  applyFilters() {
    const { searchKeyword, activeSize, sortAsc } = this.data;
    let breeds = BREEDS.filterBreeds({ size: activeSize, keyword: searchKeyword });
    breeds.sort((a, b) => {
      const cmp = a.name_zh.localeCompare(b.name_zh, 'zh');
      return sortAsc ? cmp : -cmp;
    });
    this.setData({ displayBreeds: breeds });
  },

  // 查看详情
  viewDetail(e) {
    const breedId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: '/pages/detail/detail?breedId=' + breedId });
  },

  // ====== 对比功能 ======
  toggleCompare(e) {
    const breedId = e.currentTarget.dataset.id;
    let { compareList } = this.data;
    const idx = compareList.indexOf(breedId);
    if (idx > -1) {
      compareList.splice(idx, 1);
    } else {
      if (compareList.length >= 3) {
        util.showToast('最多对比3个品种', 'none');
        return;
      }
      compareList.push(breedId);
    }
    this.setData({ compareList });
  },

  clearCompare() {
    this.setData({ compareList: [] });
  },

  startCompare() {
    if (this.data.compareList.length < 2) {
      util.showToast('至少选择2个品种进行对比', 'none');
      return;
    }
    // 跳转到详情页对比（通过传递多个ID）
    wx.navigateTo({
      url: '/pages/detail/detail?breedId=' + this.data.compareList[0] + '&compareIds=' + this.data.compareList.join(',')
    });
  },

  onShareAppMessage() {
    return {
      title: '犬博士品种百科 - 60+犬种知识大全',
      path: '/pages/wiki/wiki'
    };
  }
});
