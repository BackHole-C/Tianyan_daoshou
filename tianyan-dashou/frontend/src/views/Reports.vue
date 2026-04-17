<template>
  <div class="reports-container">
    <el-card class="reports-card">
      <template #header>
        <div class="card-header">
          <span>报表管理</span>
          <el-button type="primary" @click="handleGenerateReport">
            <el-icon><component is="DocumentAdd" /></el-icon>
            生成周报
          </el-button>
        </div>
      </template>
      
      <!-- 报表筛选 -->
      <div class="filter-container">
        <el-date-picker
          v-model="reportDate"
          type="date"
          placeholder="选择日期"
          style="width: 200px; margin-right: 10px;"
        ></el-date-picker>
        <el-select v-model="reportType" placeholder="报表类型" style="width: 150px; margin-right: 10px;">
          <el-option label="周报" value="weekly"></el-option>
          <el-option label="月报" value="monthly"></el-option>
          <el-option label="季度报" value="quarterly"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">查询</el-button>
      </div>
      
      <!-- 报表列表 -->
      <el-table :data="reports" style="width: 100%" stripe>
        <el-table-column prop="report_id" label="报表ID" width="120"></el-table-column>
        <el-table-column prop="report_date" label="报表日期"></el-table-column>
        <el-table-column prop="report_type" label="报表类型" width="100">
          <template #default="scope">
            <el-tag>{{ getReportTypeText(scope.row.report_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_plots" label="地块总数" width="100"></el-table-column>
        <el-table-column prop="high_risk_plots" label="高风险地块" width="100"></el-table-column>
        <el-table-column prop="average_yield" label="平均产量" width="120"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleViewReport(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleDownloadReport(scope.row)">下载</el-button>
            <el-button size="small" type="danger" @click="handleDeleteReport(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { DocumentAdd } from '@element-plus/icons-vue'
import axios from 'axios'

const reportDate = ref('')
const reportType = ref('weekly')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const reports = ref([
  {
    report_id: 'REPORT_20260417',
    report_date: '2026-04-17',
    report_type: 'weekly',
    total_plots: 10,
    high_risk_plots: 2,
    average_yield: 520.5
  },
  {
    report_id: 'REPORT_20260410',
    report_date: '2026-04-10',
    report_type: 'weekly',
    total_plots: 10,
    high_risk_plots: 1,
    average_yield: 530.2
  }
])

total.value = reports.value.length

const getReportTypeText = (type) => {
  const map = {
    'weekly': '周报',
    'monthly': '月报',
    'quarterly': '季度报'
  }
  return map[type] || type
}

const handleGenerateReport = async () => {
  try {
    // 这里应该调用生成报表的API
    // const response = await axios.post('/api/analysis/generate-report', { type: reportType.value })
    // reports.value.unshift(response.data)
    console.log('生成报表:', reportType.value)
  } catch (error) {
    console.error('生成报表失败:', error)
  }
}

const handleViewReport = (row) => {
  // 这里应该跳转到报表详情页面
  console.log('查看报表:', row)
}

const handleDownloadReport = (row) => {
  // 这里应该调用下载报表的API
  console.log('下载报表:', row)
}

const handleDeleteReport = (row) => {
  // 这里应该调用删除报表的API
  console.log('删除报表:', row)
}

const handleSearch = () => {
  // 这里应该调用搜索报表的API
  console.log('搜索报表:', reportDate.value, reportType.value)
}

const handleSizeChange = (size) => {
  pageSize.value = size
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

onMounted(async () => {
  try {
    // 这里应该调用获取报表列表的API
    // const response = await axios.get('/api/analysis/reports')
    // reports.value = response.data
  } catch (error) {
    console.error('获取报表列表失败:', error)
  }
})
</script>

<style scoped>
.reports-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-container {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>