<template>
    <el-container class="main-container">
        <el-header>
            <div>
                <!-- <img src="../assets/logo_main.jpeg" alt=""> -->
                <span>数据分析管理平台</span>
            </div>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <!-- 设置左侧菜单 -->
                <el-menu :unique-opened="false" :router="true">
                    <!-- 用户信息以及数据库设置 -->
                    <el-submenu index="1">
                        <!-- 一定要设置index，不然全部子菜单同时展开或折叠 -->
                        <template slot="title">
                            <i class="el-icon-setting"></i>
                            <span>用户数据库设置</span>
                        </template>
                            <el-menu-item-group>
                                <el-menu-item index="/welcome2">新建数据库</el-menu-item>
                                <el-menu-item index="/select-database">数据库选择</el-menu-item>
                            </el-menu-item-group>
                    </el-submenu>
                    <!-- 数据管理——增删改查 -->
                    <el-submenu index="2">
                        <template slot="title">
                            <i class="el-icon-tickets"></i>
                            <span>用户数据管理</span>
                        </template>
                         <el-menu-item-group>
                                <el-menu-item index="2-1">功能一</el-menu-item>
                                <el-menu-item index="2-2">功能二</el-menu-item>
                        </el-menu-item-group>
                    </el-submenu>
                </el-menu>
            </el-aside>
            <el-main>
                <!-- 形成子路径：welcome路径是在main_page路径之后的，即/mian_page/welcome -->
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
}
</script>

<style rel="stylesheet/scss" lang="scss">
.el-header {
    background-color: #373d43;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 20px;
    > div {
        display: flex;
        align-items: center;
        span {
            margin-left: 15px;
        }
    }
}
.el-aside {
    background-color: #373d41;
}
.el-main {
    background-color: ghostwhite;
}
.main-container {
    height: 100%;
}

</style>