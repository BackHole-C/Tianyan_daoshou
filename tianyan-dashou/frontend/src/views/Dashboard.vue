<template>
  <div class="dashboard-container">
    <el-card class="dashboard-card">
      <template #header>
        <div class="card-header">
          <span>仪表盘概览</span>
        </div>
      </template>
      
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ totalPlots }}</div>
            <div class="stat-label">总地块数</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ highRiskPlots }}</div>
            <div class="stat-label">高风险地块</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ averageYield.toFixed(1) }}</div>
            <div class="stat-label">平均预测产量(斤/亩)</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ diseaseRiskCount }}</div>
            <div class="stat-label">病虫害风险地块</div>
          </div>
        </el-card>
      </div>
      
      <!-- 图表区域 -->
      <div class="charts-container">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>产量预测趋势</span>
            </div>
          </template>
          <div class="chart-content">
            <!-- 这里可以集成ECharts -->
            <div class="chart-placeholder">产量预测趋势图</div>
          </div>
        </el-card>
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>风险分布</span>
            </div>
          </template>
          <div class="chart-content">
            <!-- 这里可以集成ECharts -->
            <div class="chart-placeholder">风险分布图</div>
          </div>
        </el-card>
      </div>
      
      <!-- 最近预警 -->
      <el-card class="alert-card">
        <template #header>
          <div class="card-header">
            <span>最近预警</span>
          </div>
        </template>
        <el-table :data="alerts" style="width: 100%">
          <el-table-column prop="plotName" label="地块名称" width="180"></el-table-column>
          <el-table-column prop="riskLevel" label="风险等级">
            <template #default="scope">
              <el-tag :type="getRiskTagType(scope.row.riskLevel)">
                {{ getRiskLevelText(scope.row.riskLevel) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="预警信息"></el-table-column>
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const totalPlots = ref(10)
const highRiskPlots = ref(2)
const averageYield = ref(520.5)
const diseaseRiskCount = ref(3)

const alerts = ref([
  {
    plotName: '王大哥-示范田',
    riskLevel: 3,
    message: 'NDVI值异常下降，可能存在病虫害风险',
    time: '2026-04-17 10:30'
  },
  {
    plotName: '李大姐-试验田',
    riskLevel: 2,
    message: '产量预测低于去年同期10%',
    time: '2026-04-16 14:20'
  }
])

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

onMounted(async () => {
  try {
    // 这里应该调用真实的API获取数据
    // const response = await axios.get('/api/analysis/weekly-report')
    // 现在使用模拟数据
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  overflow: hidden;
}

.stat-content {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #5470c6;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  height: 300px;
}

.chart-content {
  height: 250px;
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

.alert-card {
  margin-top: 20px;
}
</style>