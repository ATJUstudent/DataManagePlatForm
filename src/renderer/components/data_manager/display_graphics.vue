<template>
    <div>
        <el-dropdown class="select_graphics" @command="handleCommand">
            <el-button type="primary" >选择样式</el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="bar" >直方图</el-dropdown-item>
                <el-dropdown-item command="line" >折线图</el-dropdown-item>
                <el-dropdown-item command="pie" >圆饼图</el-dropdown-item>
                <el-dropdown-item command="scatter">散点图</el-dropdown-item>
            </el-dropdown-menu>
                
        </el-dropdown>
        <!-- 统计图展示 -->
        <el-card class="graphics_position" shadow = "hover">
            <div ref="chart" style="width: 100%;height: 400px">
            </div>
        </el-card>

        <!-- 属性面板展示,对话框形式 -->
        <el-dialog title="直方图属性面板" :visible.sync="isBar" width="50%">
            <!-- dialog会自动调节高度，所以我们直接在标签内加一个一定高度的div即可实现对话框的高度调整 -->
            <div style="height: 200px"></div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isBar = false">取 消</el-button>
                <el-button type="primary" @click="isBar = false">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="折线图属性面板" :visible.sync="isLine" width="30%">
            <span>这是一段信息</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isLine = false">取 消</el-button>
                <el-button type="primary" @click="isLine = false">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="饼状图属性面板" :visible.sync="isPie" width="30%">
            <span>这是一段信息</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isPie = false">取 消</el-button>
                <el-button type="primary" @click="isPie = false">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="散点图属性面板" :visible.sync="isScatter" width="30%" >
            <span>这是一段信息</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isScatter = false">取 消</el-button>
                <el-button type="primary" @click="isScatter = false">确 定</el-button>
            </span>
        </el-dialog>
        
    </div>

</template>


<script>
export default {
    data() {
        return {
            table_name: "",
            isBar:      false,
            isLine:     false,
            isPie:      false,
            isScatter:  false
        }
    },
    created (){
        this.get_table_name();
    },
    mounted(){
        this.drawLine();
    },
    methods: {
        drawLine(){
            let myChart = this.$echarts.init(this.$refs.chart);
                // 绘制图表
                myChart.setOption({
                    // title: { text: '在Vue中使用echarts' },
                    tooltip: {},
                    xAxis: {
                        data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                    },
                    yAxis: {},
                    series: [{
                        name: '销量',
                        type: 'bar',
                        data: [5, 20, 36, 10, 10, 20]
                }]
            });

        },
        get_table_name(){
            this.table_name = this.$route.query.table_selected; //页面之间传参最好使用query而不是params，params用于页面与服务器传参
            // console.log(this.table_name);
        },
        handleCommand(command) {
            if(command == "bar")
                this.isBar = true;
            else if(command == "line")
                this.isLine = true;
            else if(command == "pie")
                this.isPie  = true;
            else if(command == "scatter")
                this.isScatter = true;
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.select_graphics {
    position: absolute;
    left: 0;
}
.graphics_position {
    position: relative;
    left: 0%;
    top: 5px;
    width: 100%;
    height: 400px;

}