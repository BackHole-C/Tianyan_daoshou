<template>
  <div class="plots-container">
    <el-card class="plots-card">
      <template #header>
        <div class="card-header">
          <span>地块管理</span>
          <el-button type="primary" @click="handleAddPlot">
            <el-icon><component is="Plus" /></el-icon>
            新增地块
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-container">
        <el-input
          v-model="searchQuery"
          placeholder="搜索地块名称或ID"
          prefix-icon="Search"
          style="width: 300px; margin-right: 10px;"
        ></el-input>
        <el-select v-model="cropType" placeholder="筛选作物类型" style="width: 150px; margin-right: 10px;">
          <el-option label="水稻" value="rice"></el-option>
          <el-option label="小麦" value="wheat"></el-option>
          <el-option label="玉米" value="corn"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      
      <!-- 地块表格 -->
      <el-table :data="plots" style="width: 100%" stripe>
        <el-table-column prop="plot_id" label="地块ID" width="120"></el-table-column>
        <el-table-column prop="plot_name" label="地块名称"></el-table-column>
        <el-table-column prop="area_mu" label="面积(亩)" width="100"></el-table-column>
        <el-table-column prop="crop_type" label="作物类型" width="100"></el-table-column>
        <el-table-column prop="variety" label="品种" width="120"></el-table-column>
        <el-table-column prop="owner_name" label="负责人" width="120"></el-table-column>
        <el-table-column prop="risk_level" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskTagType(scope.row.risk_level)">
              {{ getRiskLevelText(scope.row.risk_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleViewPlot(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEditPlot(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDeletePlot(scope.row)">删除</el-button>
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
    
    <!-- 新增/编辑地块对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form :model="plotForm" :rules="rules" ref="plotFormRef" label-width="100px">
        <el-form-item label="地块ID" prop="plot_id">
          <el-input v-model="plotForm.plot_id" :disabled="!isAdd"></el-input>
        </el-form-item>
        <el-form-item label="地块名称" prop="plot_name">
          <el-input v-model="plotForm.plot_name"></el-input>
        </el-form-item>
        <el-form-item label="面积(亩)" prop="area_mu">
          <el-input v-model.number="plotForm.area_mu" type="number"></el-input>
        </el-form-item>
        <el-form-item label="作物类型" prop="crop_type">
          <el-select v-model="plotForm.crop_type">
            <el-option label="水稻" value="rice"></el-option>
            <el-option label="小麦" value="wheat"></el-option>
            <el-option label="玉米" value="corn"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="品种" prop="variety">
          <el-input v-model="plotForm.variety"></el-input>
        </el-form-item>
        <el-form-item label="负责人" prop="owner_name">
          <el-input v-model="plotForm.owner_name"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="owner_phone">
          <el-input v-model="plotForm.owner_phone"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSavePlot">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Search } from '@element-plus/icons-vue'
import axios from 'axios'

const searchQuery = ref('')
const cropType = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('新增地块')
const isAdd = ref(true)
const plotFormRef = ref(null)

const plotForm = ref({
  plot_id: '',
  plot_name: '',
  area_mu: '',
  crop_type: 'rice',
  variety: '',
  owner_name: '',
  owner_phone: ''
})

const rules = {
  plot_id: [
    { required: true, message: '请输入地块ID', trigger: 'blur' }
  ],
  plot_name: [
    { required: true, message: '请输入地块名称', trigger: 'blur' }
  ],
  area_mu: [
    { required: true, message: '请输入面积', trigger: 'blur' }
  ]
}

const plots = ref([
  {
    plot_id: 'PLOT_001',
    plot_name: '王大哥-示范田',
    area_mu: 50.5,
    crop_type: 'rice',
    variety: '杂交稻',
    owner_name: '王大哥',
    owner_phone: '13800138001',
    risk_level: 3
  },
  {
    plot_id: 'PLOT_002',
    plot_name: '李大姐-试验田',
    area_mu: 30.0,
    crop_type: 'rice',
    variety: '常规稻',
    owner_name: '李大姐',
    owner_phone: '13900139002',
    risk_level: 2
  }
])

total.value = plots.value.length

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

const handleAddPlot = () => {
  isAdd.value = true
  dialogTitle.value = '新增地块'
  plotForm.value = {
    plot_id: '',
    plot_name: '',
    area_mu: '',
    crop_type: 'rice',
    variety: '',
    owner_name: '',
    owner_phone: ''
  }
  dialogVisible.value = true
}

const handleEditPlot = (row) => {
  isAdd.value = false
  dialogTitle.value = '编辑地块'
  plotForm.value = { ...row }
  dialogVisible.value = true
}

const handleDeletePlot = (row) => {
  // 这里应该调用删除API
  console.log('删除地块:', row)
}

const handleViewPlot = (row) => {
  // 这里应该跳转到地块详情页面
  console.log('查看地块:', row)
}

const handleSavePlot = async () => {
  if (plotFormRef.value) {
    await plotFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          // 这里应该调用保存API
          console.log('保存地块:', plotForm.value)
          dialogVisible.value = false
        } catch (error) {
          console.error('保存失败:', error)
        }
      }
    })
  }
}

const handleSearch = () => {
  // 这里应该调用搜索API
  console.log('搜索:', searchQuery.value, cropType.value)
}

const handleSizeChange = (size) => {
  pageSize.value = size
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

onMounted(async () => {
  try {
    // 这里应该调用获取地块列表的API
    // const response = await axios.get('/api/plots')
    // plots.value = response.data
  } catch (error) {
    console.error('获取地块列表失败:', error)
  }
})
</script>

<style scoped>
.plots-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-container {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>