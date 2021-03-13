<template>
    <el-container class="data_home_page">
        <el-header class="data_header">
            <h3>当前数据库: {{select_db_name}}</h3>
            <router-link :to="{path: '/main_page'}">
                <el-button>返回首页</el-button>
            </router-link>
        </el-header>
        <el-container>
            <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
            <el-submenu index="1">
                <template slot="title">
                <i class="el-icon-document" @click="fold_function"></i>
                <span slot="title">数据表</span>
                </template>
                <el-menu-item v-for="item in table_list" :key="item" index="item">
                    {{item}}
                    <!-- 在这里进行数据表选择 -->
                </el-menu-item>
            </el-submenu>
            </el-menu>
            <el-main>
                <el-tabs v-model="activeName" type="card">
                    <!-- 从上面el-submenu中的项选择指定的数据表进行操作 -->
                    <!-- 数据表的新建、删除、导入导出-->
                    <el-tab-pane label="数据表管理" name="first">数据表管理</el-tab-pane>
                    <!-- 数据的增删改查 -->
                    <el-tab-pane label="数据查询" name="second">数据查询</el-tab-pane>
                    <!-- 数据统计图展示 -->
                    <el-tab-pane label="统计图表" name="third">统计图表</el-tab-pane>
                    <el-tab-pane label="数据分析" name="fourth">数据分析</el-tab-pane>
                </el-tabs>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    data(){
        return {
            isCollapse: true,
            select_db_name:"",
            table_list: [],
            activeName: "first"
        }
    },
    created() {
        this.get_preparation()
    },
    methods: {
        async get_preparation(){
            this.select_db_name = this.$route.query.value;
            const {data:result} = await this.$http.get('/data_home',{params: {name: this.select_db_name}});
            var lists = JSON.parse(JSON.stringify(result));
            var len = lists.length;
            if (len == 0){
                this.table_list[0] = "暂无数据表";
            }else{
                this.table_list = lists;
            }

        },
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        fold_function() {
            this.isCollapse = ! this.isCollapse;
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.data_home_page {
    height: 100%;
}
.data_header {
    background-color:bisque;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color:indigo;
    font-size: 15px;
    > div {
        display: flex;
        align-items: center;
        span {
            margin-left: 15px;
        }
    }
}
.button {
    position:absolute;
    left: 0%;
    top: 100px;
}
.menu {
    position:absolute;
    left: 0%;
    top: 150px;
    height: 100%;
}

</style>