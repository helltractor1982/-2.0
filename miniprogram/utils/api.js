// utils/api.js - API 服务
const BREEDS = require('./breeds.js');

const app = getApp();
const API_BASE = 'http://localhost:8000/api';

// 通用请求方法
function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: API_BASE + url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      timeout: options.timeout || 15000,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject({ code: res.statusCode, message: res.data.detail || '请求失败' });
        }
      },
      fail(err) {
        console.error('[API] 请求失败:', err);
        reject({ code: -1, message: '网络连接失败，请检查网络' });
      }
    });
  });
}

// 图片识别 - 上传图片进行品种识别
async function identifyBreed(imagePath, topK = 3) {
  try {
    // 读取图片并转换为 base64
    const fs = wx.getFileSystemManager();
    const base64 = fs.readFileSync(imagePath, 'base64');

    const result = await request('/identify', {
      method: 'POST',
      data: { image_base64: base64.toString(), top_k: topK }
    });
    return result;
  } catch (err) {
    console.warn('[API] 后端不可用，使用本地模拟识别');
    return localMockIdentify(imagePath, topK);
  }
}

// ====== 本地模拟识别（当后端不可用时） ======
function localMockIdentify(imagePath, topK = 3) {
  const allBreeds = BREEDS.getAllBreeds();

  // 使用确定性随机（同一张图片返回一致结果）
  let seed = 0;
  try {
    const fs = wx.getFileSystemManager();
    const buffer = fs.readFileSync(imagePath);
    // 取前100字节计算hash
    for (let i = 0; i < Math.min(buffer.length, 100); i++) {
      seed = ((seed << 5) - seed) + buffer[i];
      seed |= 0;
    }
  } catch (e) {
    seed = Date.now();
  }

  const seededRandom = () => {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  };

  const shuffled = [...allBreeds].sort(() => seededRandom() - 0.5);
  const selected = shuffled.slice(0, Math.min(topK, allBreeds.length));

  const results = selected.map((breed, index) => {
    let confidence;
    if (index === 0) confidence = 0.7 + seededRandom() * 0.25;
    else confidence = (1 - confidence + 0.05) * seededRandom();
    confidence = Math.min(0.99, Math.max(0.1, confidence));

    return {
      breed_id: breed.breed_id,
      name_zh: breed.name_zh,
      name_en: breed.name_en,
      confidence: parseFloat(confidence.toFixed(4))
    };
  });

  results.sort((a, b) => b.confidence - a.confidence);

  return {
    success: true,
    results: results,
    top_result: results[0],
    mock: true
  };
}

// 获取品种列表
async function getBreeds(params = {}) {
  try {
    return await request('/breeds', { data: params });
  } catch (err) {
    console.warn('[API] 后端不可用，使用本地数据');
    return { breeds: BREEDS.filterBreeds(params) };
  }
}

// 获取品种详情
async function getBreedDetail(breedId) {
  try {
    return await request('/breeds/' + breedId);
  } catch (err) {
    console.warn('[API] 后端不可用，使用本地数据');
    const breed = BREEDS.getBreedById(breedId);
    if (!breed) throw { code: 404, message: '品种不存在' };
    return { breed: breed };
  }
}

// 随机推荐品种
async function getRandomBreed(count = 3) {
  try {
    return await request('/breeds/random', { data: { count } });
  } catch (err) {
    return { breeds: BREEDS.getRandomBreeds(count) };
  }
}

// 对比多个品种
async function compareBreedsApi(breedIds) {
  try {
    return await request('/breeds/compare/' + breedIds.join(','));
  } catch (err) {
    return { breeds: BREEDS.compareBreeds(breedIds) };
  }
}

// 获取统计数据
async function getStats() {
  try {
    return await request('/stats/overview');
  } catch (err) {
    return { mock: true };
  }
}

// 健康检查
async function healthCheck() {
  try {
    const result = await request('/health', { timeout: 3000 });
    return result.status === 'healthy';
  } catch (err) {
    return false;
  }
}

module.exports = {
  identifyBreed,
  getBreeds,
  getBreedDetail,
  getRandomBreed,
  compareBreedsApi,
  getStats,
  healthCheck
};
