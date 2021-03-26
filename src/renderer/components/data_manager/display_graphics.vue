<template>
    <div>
        <el-dropdown class="select_graphics" @command="handleCommand">
            <el-button type="primary" >选择样式</el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="bar">直方图</el-dropdown-item>
                <el-dropdown-item command="line">折线图</el-dropdown-item>
                <el-dropdown-item command="pie">圆饼图</el-dropdown-item>
                <el-dropdown-item command="scatter">散点图</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <el-card class="graphics_position" shadow = "hover">
            <div ref="chart" style="width: 100%;height: 400px">
            </div>
        </el-card>
        
    </div>
</template>


<script>
export default {
    data() {
        return {
            table_name: "",
            graphic_type: ""
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
            this.graphic_type = command;
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
</style>