<template>
  <div class="app-container">
    <el-container style="height: 100vh;">
      <!-- 侧边栏 -->
      <el-aside width="200px" style="background-color: #5470c6; color: white;">
        <div class="logo" style="padding: 20px; text-align: center; font-size: 18px; font-weight: bold;">
          天眼稻守
        </div>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-vertical-demo"
          background-color="#5470c6"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><component is="House" /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="plots">
            <el-icon><component is="Location" /></el-icon>
            <span>地块管理</span>
          </el-menu-item>
          <el-menu-item index="analysis">
            <el-icon><component is="DataAnalysis" /></el-icon>
            <span>数据分析</span>
          </el-menu-item>
          <el-menu-item index="reports">
            <el-icon><component is="Document" /></el-icon>
            <span>报表管理</span>
          </el-menu-item>
          <el-menu-item index="users">
            <el-icon><component is="User" /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header style="background-color: #f5f7fa; padding: 0 20px; line-height: 60px; border-bottom: 1px solid #e4e7ed;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>智能农业病虫害检测与产量预测平台</div>
            <div style="display: flex; align-items: center; gap: 20px;">
              <el-dropdown>
                <span class="el-dropdown-link">
                  {{ userInfo.username || '未登录' }}
                  <el-icon class="el-icon--right"><component is="ArrowDown" /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        
        <!-- 内容区域 -->
        <el-main style="padding: 20px;">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { House, Location, DataAnalysis, Document, User, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const activeIndex = ref('dashboard')
const userInfo = ref({})

// 处理菜单选择
const handleMenuSelect = (key) => {
  activeIndex.value = key
  router.push(`/${key}`)
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

// 初始化
onMounted(() => {
  // 从localStorage获取用户信息
  const token = localStorage.getItem('token')
  if (token) {
    // 这里应该从API获取用户信息，现在使用模拟数据
    userInfo.value = { username: 'admin' }
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
}

.el-menu {
  border-right: none;
}
</style>