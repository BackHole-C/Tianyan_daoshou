<template>
  <div class="analysis-container">
    <el-card class="analysis-card">
      <template #header>
        <div class="card-header">
          <span>数据分析</span>
        </div>
      </template>
      
      <!-- 地块选择 -->
      <div class="plot-selector">
        <el-select v-model="selectedPlotId" placeholder="选择地块" style="width: 300px;" @change="handlePlotChange">
          <el-option
            v-for="plot in plots"
            :key="plot.plot_id"
            :label="plot.plot_name"
            :value="plot.plot_id"
          ></el-option>
        </el-select>
      </div>
      
      <!-- 分析结果 -->
      <div v-if="selectedPlot" class="analysis-content">
        <!-- 基本信息 -->
        <el-card class="info-card">
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">地块名称</div>
              <div class="info-value">{{ selectedPlot.plot_name }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">面积</div>
              <div class="info-value">{{ selectedPlot.area_mu }} 亩</div>
            </div>
            <div class="info-item">
              <div class="info-label">作物类型</div>
              <div class="info-value">{{ getCropTypeText(selectedPlot.crop_type) }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">品种</div>
              <div class="info-value">{{ selectedPlot.variety }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">当前风险等级</div>
              <div class="info-value">
                <el-tag :type="getRiskTagType(selectedPlot.risk_level)">
                  {{ getRiskLevelText(selectedPlot.risk_level) }}
                </el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="info-label">预测产量</div>
              <div class="info-value">{{ selectedPlot.predicted_yield || 'N/A' }} 斤/亩</div>
            </div>
          </div>
        </el-card>
        
        <!-- NDVI时序图 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>NDVI时序变化</span>
            </div>
          </template>
          <div class="chart-content">
            <!-- 这里可以集成ECharts -->
            <div class="chart-placeholder">NDVI时序图</div>
          </div>
        </el-card>
        
        <!-- 产量预测 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>产量预测</span>
            </div>
          </template>
          <div class="chart-content">
            <!-- 这里可以集成ECharts -->
            <div class="chart-placeholder">产量预测图</div>
          </div>
        </el-card>
        
        <!-- 病虫害风险 -->
        <el-card class="risk-card">
          <template #header>
            <div class="card-header">
              <span>病虫害风险评估</span>
            </div>
          </template>
          <div class="risk-content">
            <el-table :data="diseaseRisks" style="width: 100%">
              <el-table-column prop="disease_type" label="病虫害类型"></el-table-column>
              <el-table-column prop="risk_level" label="风险等级">
                <template #default="scope">
                  <el-tag :type="getRiskTagType(scope.row.risk_level)">
                    {{ getRiskLevelText(scope.row.risk_level) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="confidence" label="置信度"></el-table-column>
              <el-table-column prop="affected_area" label="受影响面积%"></el-table-column>
              <el-table-column prop="recommendation" label="建议措施"></el-table-column>
            </el-table>
          </div>
        </el-card>
      </div>
      <div v-else class="empty-state">
        <el-empty description="请选择一个地块进行分析" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const selectedPlotId = ref('')
const selectedPlot = ref(null)

const plots = ref([
  {
    plot_id: 'PLOT_001',
    plot_name: '王大哥-示范田',
    area_mu: 50.5,
    crop_type: 'rice',
    variety: '杂交稻',
    risk_level: 3,
    predicted_yield: 420.5
  },
  {
    plot_id: 'PLOT_002',
    plot_name: '李大姐-试验田',
    area_mu: 30.0,
    crop_type: 'rice',
    variety: '常规稻',
    risk_level: 2,
    predicted_yield: 580.0
  }
])

const diseaseRisks = ref([
  {
    disease_type: '稻瘟病',
    risk_level: 3,
    confidence: 0.85,
    affected_area: 30,
    recommendation: '立即喷施杀菌剂'
  },
  {
    disease_type: '纹枯病',
    risk_level: 2,
    confidence: 0.75,
    affected_area: 15,
    recommendation: '加强田间管理'
  }
])

const getCropTypeText = (type) => {
  const map = {
    'rice': '水稻',
    'wheat': '小麦',
    'corn': '玉米'
  }
  return map[type] || type
}

const getRiskTagType = (level) => {
  switch (level) {
    case 1: return 'success'
    case 2: return 'warning'
    case 3: return 'danger'
    case 4: return 'danger'
    default: return 'info'
  }
}

const getRiskLevelText = (level) => {
  switch (level) {
    case 1: return '正常'
    case 2: return '关注'
    case 3: return '警告'
    case 4: return '危险'
    default: return '未知'
  }
}

const handlePlotChange = async (plotId) => {
  try {
    // 这里应该调用获取地块分析数据的API
    // const response = await axios.get(`/api/analysis/plot/${plotId}`)
    // selectedPlot.value = response.data
    
    // 现在使用模拟数据
    selectedPlot.value = plots.value.find(p => p.plot_id === plotId)
  } catch (error) {
    console.error('获取地块分析数据失败:', error)
  }
}

onMounted(async () => {
  try {
    // 这里应该调用获取地块列表的API
    // const response = await axios.get('/api/plots')
    // plots.value = response.data
    
    // 默认选择第一个地块
    if (plots.value.length > 0) {
      selectedPlotId.value = plots.value[0].plot_id
      handlePlotChange(selectedPlotId.value)
    }
  } catch (error) {
    console.error('获取地块列表失败:', error)
  }
})
</script>

<style scoped>
.analysis-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plot-selector {
  margin-bottom: 20px;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-content {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
  border-radius: 4px;
}

.chart-placeholder {
  color: #999;
  font-size: 16px;
}

.risk-card {
  margin-bottom: 20px;
}

.empty-state {
  padding: 40px;
  text-align: center;
}
</style>