<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户数据库设置</el-breadcrumb-item>
      <el-breadcrumb-item>数据库选择</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图区 -->
    <el-card>
      <el-table ref="singleTable" :data="namelist" highlight-current-row @current-change="handleCurrentChange" style="width: 100%">
      <el-table-column type="index" width="50"></el-table-column>
      <el-table-column property="database_name" label="数据库名称" style="width: 100%"></el-table-column>
      </el-table>
      <div style="margin-top: 20px">
        <router-link :to="{path: '/data_home', query: {value: this.currentRow}}">
          <el-button icon="el-icon-circle-check">确认选择</el-button>
        </router-link>
        <el-button icon="el-icon-circle-close" @click="cancel_select()">取消选择</el-button>
        <router-link :to="{path: '/main_page'}">
          <el-button icon="el-icon-s-home">返回首页</el-button>
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
    data() {
      return {
        activeName: 'first',
        queryInfo: {
          data_base_name: ""
        },
        namelist: [],
        currentRow: "default"
      };
    },
    created() {
      this.getDataBaseList()
    },
    methods: {
     async getDataBaseList() {
        this.namelist = this.$route.query.database_list;
        // console.log(this.namelist);
      },
      cancel_select() {
        this.currentRow = null;
      },
      handleCurrentChange(val) {
        this.currentRow = JSON.parse(JSON.stringify(val))['database_name'];
      }
    }
  };
</script>

<style rel="stylesheet/scss" lang="scss">

</style>