// pages/detail/detail.js
const BREEDS = require('../../utils/breeds.js');
const util = require('../../utils/util.js');

Page({
  data: {
    breedId: '',
    breed: null,
    isFav: false,
    error: ''
  },

  onLoad(options) {
    const breedId = options.breedId || '';
    this.setData({ breedId });
    this.loadBreed();
  },

  onShow() {
    if (this.data.breedId) {
      this.setData({ isFav: util.isFavorited(this.data.breedId) });
    }
  },

  loadBreed() {
    const breed = BREEDS.getBreedById(this.data.breedId);
    if (breed) {
      this.setData({
        breed,
        isFav: util.isFavorited(this.data.breedId),
        error: ''
      });
      wx.setNavigationBarTitle({ title: breed.name_zh });
    } else {
      this.setData({ error: '未找到该品种信息' });
    }
  },

  // 收藏/取消收藏
  toggleFav() {
    const result = util.toggleFavorite(this.data.breedId);
    this.setData({ isFav: result.favorited });
    util.showToast(result.favorited ? '已加入收藏' : '已取消收藏', 'success');
  },

  // 分享
  onShareAppMessage() {
    const breed = this.data.breed;
    if (!breed) return {};
    return {
      title: `来看看${breed.name_zh}（${breed.name_en}）的详细资料！`,
      path: `/pages/detail/detail?breedId=${this.data.breedId}`
    };
  }
});
