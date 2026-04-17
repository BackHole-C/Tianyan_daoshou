<template>
  <div class="users-container">
    <el-card class="users-card">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAddUser">
            <el-icon><component is="UserFilled" /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>
      
      <!-- 搜索 -->
      <div class="search-container">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名或邮箱"
          prefix-icon="Search"
          style="width: 300px; margin-right: 10px;"
        ></el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      
      <!-- 用户表格 -->
      <el-table :data="users" style="width: 100%" stripe>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="full_name" label="姓名"></el-table-column>
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag :type="getRoleTagType(scope.row.role)">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleViewUser(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEditUser(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDeleteUser(scope.row)">删除</el-button>
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
    
    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="!isAdd"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="userForm.full_name"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="用户" value="user"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="密码" :required="isAdd" prop="password">
          <el-input v-model="userForm.password" type="password" :placeholder="isAdd ? '请输入密码' : '留空表示不修改密码'"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveUser">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UserFilled, Search } from '@element-plus/icons-vue'
import axios from 'axios'

const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const isAdd = ref(true)
const userFormRef = ref(null)

const userForm = ref({
  username: '',
  email: '',
  full_name: '',
  role: 'user',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const users = ref([
  {
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    full_name: '管理员',
    role: 'admin',
    created_at: '2026-04-01 00:00:00'
  },
  {
    id: 2,
    username: 'user1',
    email: 'user1@example.com',
    full_name: '用户1',
    role: 'user',
    created_at: '2026-04-02 00:00:00'
  }
])

total.value = users.value.length

const getRoleTagType = (role) => {
  return role === 'admin' ? 'danger' : 'success'
}

const getRoleText = (role) => {
  return role === 'admin' ? '管理员' : '用户'
}

const handleAddUser = () => {
  isAdd.value = true
  dialogTitle.value = '新增用户'
  userForm.value = {
    username: '',
    email: '',
    full_name: '',
    role: 'user',
    password: ''
  }
  dialogVisible.value = true
}

const handleEditUser = (row) => {
  isAdd.value = false
  dialogTitle.value = '编辑用户'
  userForm.value = { ...row, password: '' }
  dialogVisible.value = true
}

const handleDeleteUser = (row) => {
  // 这里应该调用删除用户的API
  console.log('删除用户:', row)
}

const handleViewUser = (row) => {
  // 这里应该跳转到用户详情页面
  console.log('查看用户:', row)
}

const handleSaveUser = async () => {
  if (userFormRef.value) {
    await userFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          // 这里应该调用保存用户的API
          console.log('保存用户:', userForm.value)
          dialogVisible.value = false
        } catch (error) {
          console.error('保存失败:', error)
        }
      }
    })
  }
}

const handleSearch = () => {
  // 这里应该调用搜索用户的API
  console.log('搜索用户:', searchQuery.value)
}

const handleSizeChange = (size) => {
  pageSize.value = size
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

onMounted(async () => {
  try {
    // 这里应该调用获取用户列表的API
    // const response = await axios.get('/api/users')
    // users.value = response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
})
</script>

<style scoped>
.users-container {
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