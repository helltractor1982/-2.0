// utils/util.js - 通用工具函数

/**
 * 格式化日期
 * @param {Date|number} date 日期对象或时间戳
 * @param {string} format 格式字符串 (YYYY-MM-DD HH:mm:ss)
 */
function formatDate(date, format = 'YYYY-MM-DD HH:mm') {
  if (!date) return '';
  const d = typeof date === 'number' ? new Date(date) : new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');
  const second = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second);
}

/**
 * 获取相对时间描述
 */
function getRelativeTime(timestamp) {
  const now = Date.now();
  const diff = now - timestamp;
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diff < minute) return '刚刚';
  if (diff < hour) return Math.floor(diff / minute) + '分钟前';
  if (diff < day) return Math.floor(diff / hour) + '小时前';
  if (diff < 7 * day) return Math.floor(diff / day) + '天前';
  return formatDate(timestamp, 'MM-DD HH:mm');
}

/**
 * Toast 提示
 */
function showToast(title, icon = 'none', duration = 2000) {
  wx.showToast({ title, icon, duration, mask: false });
}

/**
 * 确认对话框
 */
function showConfirm(title, content, confirmText = '确定', cancelText = '取消') {
  return new Promise((resolve) => {
    wx.showModal({
      title,
      content,
      confirmText,
      cancelText,
      success(res) { resolve(res.confirm); },
      fail() { resolve(false); }
    });
  });
}

/**
 * Loading 加载
 */
function showLoading(title = '加载中...') {
  wx.showLoading({ title, mask: true });
}

function hideLoading() {
  wx.hideLoading();
}

/**
 * 识别历史记录管理
 */
function getHistory() {
  return wx.getStorageSync('identify_history') || [];
}

function addHistory(record) {
  const history = getHistory();
  history.unshift({
    id: Date.now().toString(36) + Math.random().toString(36).substr(2, 6),
    ...record,
    timestamp: Date.now()
  });
  // 最多保留100条
  if (history.length > 100) history.pop();
  wx.setStorageSync('identify_history', history);
  return history;
}

function clearHistory() {
  wx.setStorageSync('identify_history', []);
}

function removeHistoryItem(id) {
  let history = getHistory();
  history = history.filter(item => item.id !== id);
  wx.setStorageSync('identify_history', history);
  return history;
}

/**
 * 收藏管理
 */
function getFavorites() {
  return wx.getStorageSync('favorites') || [];
}

function toggleFavorite(breedId) {
  let favorites = getFavorites();
  const index = favorites.indexOf(breedId);
  if (index > -1) {
    favorites.splice(index, 1);
    wx.setStorageSync('favorites', favorites);
    return { favorited: false, favorites };
  } else {
    favorites.push(breedId);
    wx.setStorageSync('favorites', favorites);
    return { favorited: true, favorites };
  }
}

function isFavorited(breedId) {
  return getFavorites().includes(breedId);
}

/**
 * 使用统计
 */
function getUsageStats() {
  const defaultStats = { total: 0, today: 0, date: '' };
  const stats = wx.getStorageSync('usage_stats') || defaultStats;
  const today = new Date().toDateString();
  if (stats.date !== today) {
    stats.today = 0;
    stats.date = today;
  }
  return stats;
}

function addUsageCount() {
  const stats = getUsageStats();
  stats.total++;
  stats.today++;
  stats.date = new Date().toDateString();
  wx.setStorageSync('usage_stats', stats);
  return stats;
}

/**
 * 剪贴板操作
 */
function copyToClipboard(text) {
  wx.setClipboardData({
    data: text,
    success() { showToast('已复制到剪贴板', 'success'); }
  });
}

/**
 * 页面跳转工具
 */
function navigateTo(url) {
  wx.navigateTo({ url, fail() { wx.switchTab({ url }); } });
}

/**
 * 生成唯一ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
}

module.exports = {
  formatDate,
  getRelativeTime,
  showToast,
  showConfirm,
  showLoading,
  hideLoading,
  getHistory,
  addHistory,
  clearHistory,
  removeHistoryItem,
  getFavorites,
  toggleFavorite,
  isFavorited,
  getUsageStats,
  addUsageCount,
  copyToClipboard,
  navigateTo,
  generateId
};
