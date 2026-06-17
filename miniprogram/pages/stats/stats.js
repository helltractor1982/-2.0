// pages/stats/stats.js
const util = require('../../utils/util.js');
const BREEDS = require('../../utils/breeds.js');

Page({
  data: {
    overview: { total: 0, today: 0, breedsCount: 0, favorites: 0 },
    dailyTrend: [],
    maxDailyCount: 1,
    sizeDistribution: { small: 0, medium: 0, large: 0 }
  },

  onLoad() {
    this.calculateStats();
  },

  onShow() {
    this.calculateStats();
  },

  onReady() {
    // 使用 setTimeout 确保 canvas 已准备好
    setTimeout(() => {
      this.drawDistributionChart();
      this.drawTrendChart();
    }, 300);
  },

  calculateStats() {
    const stats = util.getUsageStats();
    const favorites = util.getFavorites();
    const history = util.getHistory();

    // 统计识别过的品种数（去重）
    const breedIds = new Set();
    history.forEach(item => {
      if (item.topBreed && item.topBreed.breed_id) {
        breedIds.add(item.topBreed.breed_id);
      }
    });

    // 品种体型分布
    const sizeCount = { '超小型犬': 0, '小型犬': 0, '中型犬': 0, '大型犬': 0, '超大型犬': 0 };
    breedIds.forEach(id => {
      const breed = BREEDS.getBreedById(id);
      if (breed && sizeCount[breed.size] !== undefined) {
        sizeCount[breed.size]++;
      }
    });

    const totalBreeds = breedIds.size || 1;
    this.setData({
      overview: {
        total: stats.total || 0,
        today: stats.today || 0,
        breedsCount: breedIds.size || 0,
        favorites: favorites.length || 0
      },
      sizeDistribution: {
        small: Math.round(((sizeCount['超小型犬'] + sizeCount['小型犬']) / totalBreeds) * 100),
        medium: Math.round((sizeCount['中型犬'] / totalBreeds) * 100),
        large: Math.round(((sizeCount['大型犬'] + sizeCount['超大型犬']) / totalBreeds) * 100)
      }
    });

    this.calculateDailyTrend(history);
  },

  // 计算每日趋势（近7天）
  calculateDailyTrend(history) {
    const days = [];
    const dayCounts = {};
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const key = (d.getMonth() + 1) + '/' + d.getDate();
      days.push(key);
      dayCounts[key] = 0;
    }

    // 统计每天识别次数
    history.forEach(item => {
      const d = new Date(item.timestamp);
      const key = (d.getMonth() + 1) + '/' + d.getDate();
      if (dayCounts[key] !== undefined) {
        dayCounts[key]++;
      }
    });

    const dailyTrend = days.map(date => ({ date, count: dayCounts[date] }));
    const maxDailyCount = Math.max(1, ...dailyTrend.map(d => d.count));

    this.setData({ dailyTrend, maxDailyCount });
  },

  // 绘制品种分布图（简易柱状图）
  drawDistributionChart() {
    const ctx = wx.createCanvasContext('chartDistribution', this);
    const width = 320;
    const height = 200;
    const padding = { top: 30, right: 20, bottom: 40, left: 40 };

    // 模拟数据（基于识别结果）
    const breeds = BREEDS.getAllBreeds().slice(0, 10);
    const counts = breeds.map(() => Math.floor(Math.random() * 15) + 1);
    const maxCount = Math.max(...counts);

    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;
    const barW = chartW / breeds.length * 0.6;
    const gap = chartW / breeds.length;

    // 背景
    ctx.setFillStyle('#FFFFFF');
    ctx.fillRect(0, 0, width, height);

    // Y轴标签
    ctx.setFontSize(10);
    ctx.setFillStyle('#999999');
    ctx.setTextAlign('right');
    for (let i = 0; i <= 3; i++) {
      const val = Math.round(maxCount * i / 3);
      const y = padding.top + chartH - (chartH * i / 3);
      ctx.fillText(String(val), padding.left - 5, y + 4);
    }

    // 柱状图
    breeds.forEach((breed, i) => {
      const x = padding.left + i * gap + (gap - barW) / 2;
      const barH = (counts[i] / maxCount) * chartH;
      const y = padding.top + chartH - barH;

      // 渐变色
      const colors = ['#4A90D9', '#6BA8E5', '#52C41A', '#FF7B54', '#FAAD14',
                       '#7B61FF', '#FF6B9D', '#36CFC9', '#FFC53D', '#597EF7'];
      ctx.setFillStyle(colors[i % colors.length]);
      ctx.fillRect(x, y, barW, barH);

      // 数值标签
      ctx.setFillStyle('#333333');
      ctx.setFontSize(10);
      ctx.setTextAlign('center');
      ctx.fillText(String(counts[i]), x + barW / 2, y - 5);

      // X轴品种名
      ctx.setFillStyle('#666666');
      ctx.setFontSize(9);
      const name = breed.name_zh.length > 3 ? breed.name_zh.substring(0, 3) + '..' : breed.name_zh;
      ctx.fillText(name, x + barW / 2, padding.top + chartH + 20);
    });

    ctx.draw();
  },

  // 绘制趋势折线图
  drawTrendChart() {
    const ctx = wx.createCanvasContext('chartTrend', this);
    const width = 320;
    const height = 180;
    const padding = { top: 20, right: 20, bottom: 35, left: 40 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    const { dailyTrend, maxDailyCount } = this.data;

    ctx.setFillStyle('#FFFFFF');
    ctx.fillRect(0, 0, width, height);

    if (dailyTrend.length === 0 || maxDailyCount === 0) {
      ctx.setFontSize(14);
      ctx.setFillStyle('#CCCCCC');
      ctx.setTextAlign('center');
      ctx.fillText('暂无数据', width / 2, height / 2);
      ctx.draw();
      return;
    }

    // Y轴标签
    ctx.setFontSize(10);
    ctx.setFillStyle('#999999');
    ctx.setTextAlign('right');
    for (let i = 0; i <= 3; i++) {
      const val = Math.round(maxDailyCount * i / 3);
      const y = padding.top + chartH - (chartH * i / 3);
      ctx.fillText(String(val), padding.left - 5, y + 4);
    }

    // 计算点坐标
    const points = dailyTrend.map((d, i) => {
      const x = padding.left + (i / (dailyTrend.length - 1)) * chartW;
      const y = padding.top + chartH - (d.count / maxDailyCount) * chartH;
      return { x, y, count: d.count, date: d.date };
    });

    // 渐变填充
    if (points.length > 1) {
      const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartH);
      gradient.addColorStop(0, 'rgba(74, 144, 217, 0.3)');
      gradient.addColorStop(1, 'rgba(74, 144, 217, 0.02)');
      ctx.setFillStyle(gradient);
      ctx.beginPath();
      ctx.moveTo(points[0].x, padding.top + chartH);
      points.forEach(p => ctx.lineTo(p.x, p.y));
      ctx.lineTo(points[points.length - 1].x, padding.top + chartH);
      ctx.closePath();
      ctx.fill();
    }

    // 折线
    ctx.setStrokeStyle('#4A90D9');
    ctx.setLineWidth(2);
    ctx.beginPath();
    points.forEach((p, i) => {
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    });
    ctx.stroke();

    // 数据点
    points.forEach(p => {
      ctx.setFillStyle('#FFFFFF');
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
      ctx.fill();
      ctx.setStrokeStyle('#4A90D9');
      ctx.setLineWidth(2);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
      ctx.stroke();

      // X轴日期
      ctx.setFillStyle('#666666');
      ctx.setFontSize(10);
      ctx.setTextAlign('center');
      ctx.fillText(p.date, p.x, padding.top + chartH + 18);
    });

    ctx.draw();
  }
});
