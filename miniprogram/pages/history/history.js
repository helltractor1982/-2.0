// pages/history/history.js
const util = require('../../utils/util.js');

Page({
  data: {
    history: [],
    batchMode: false,
    selectedIds: []
  },

  onShow() {
    this.loadHistory();
  },

  loadHistory() {
    const history = util.getHistory().map(item => ({
      ...item,
      relativeTime: util.getRelativeTime(item.timestamp)
    }));
    this.setData({ history, selectedIds: [] });
  },

  // 查看识别详情
  viewDetail(e) {
    if (this.data.batchMode) return;
    const item = e.currentTarget.dataset.item;
    if (item.topBreed && item.topBreed.breed_id) {
      wx.navigateTo({
        url: '/pages/detail/detail?breedId=' + item.topBreed.breed_id
      });
    }
  },

  // 查看品种详情
  viewBreedDetail(e) {
    const breedId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: '/pages/detail/detail?breedId=' + breedId });
  },

  // 删除单条记录
  async deleteItem(e) {
    const id = e.currentTarget.dataset.id;
    const confirmed = await util.showConfirm('确认删除', '删除后无法恢复');
    if (confirmed) {
      const history = util.removeHistoryItem(id);
      this.setData({
        history: history.map(item => ({
          ...item,
          relativeTime: util.getRelativeTime(item.timestamp)
        }))
      });
      util.showToast('已删除', 'success');
    }
  },

  // 批量管理模式
  batchManage() {
    this.setData({
      batchMode: !this.data.batchMode,
      selectedIds: []
    });
  },

  // 切换选择
  toggleSelect(e) {
    const id = e.currentTarget.dataset.id;
    let { selectedIds } = this.data;
    const idx = selectedIds.indexOf(id);
    if (idx > -1) {
      selectedIds.splice(idx, 1);
    } else {
      selectedIds.push(id);
    }
    this.setData({ selectedIds });
  },

  // 批量删除
  async batchDelete() {
    if (this.data.selectedIds.length === 0) return;
    const confirmed = await util.showConfirm(
      '批量删除',
      `确认删除选中的 ${this.data.selectedIds.length} 条记录？`
    );
    if (confirmed) {
      let history = util.getHistory();
      history = history.filter(item => !this.data.selectedIds.includes(item.id));
      wx.setStorageSync('identify_history', history);
      this.setData({ selectedIds: [], batchMode: false });
      this.loadHistory();
      util.showToast('已删除', 'success');
    }
  },

  // 全部清除
  async clearAll() {
    const confirmed = await util.showConfirm(
      '清空所有记录',
      '确认清空所有识别历史？此操作不可恢复。'
    );
    if (confirmed) {
      util.clearHistory();
      this.setData({ history: [], batchMode: false, selectedIds: [] });
      util.showToast('已清空', 'success');
    }
  },

  // 去识别
  goIdentify() {
    wx.switchTab({ url: '/pages/identify/identify' });
  }
});
