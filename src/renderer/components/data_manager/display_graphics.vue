<template>
    <div>
        <el-dropdown class="select_graphics" @command="handleCommand">
            <el-button size="medium" icon="el-icon-bottom" >选择样式</el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="bar" >直方图</el-dropdown-item>
                <el-dropdown-item command="line" >折线图</el-dropdown-item>
                <el-dropdown-item command="pie" >圆饼图</el-dropdown-item>
                <el-dropdown-item command="scatter">散点图</el-dropdown-item>
            </el-dropdown-menu>        
        </el-dropdown>
        <el-button size="medium" icon="el-icon-pie-chart" @click="display_pic">显示图表</el-button>
        <!-- 统计图展示 -->
        <el-card shadow = "hover" >
            <div v-show="which_one_pic == '' ">暂无图表</div>
            <!-- 此处height控制了内层card的高度 -->
            <div ref="chart_bar" style="width: 100%;height: 520px;" v-show="which_one_pic == 'bar'"></div>
            <div ref="chart_line" style="width: 100%;height: 520px;" v-show="which_one_pic == 'line'"></div>
            <div ref="chart_pie" style="width: 100%;height: 520px;" v-show="which_one_pic == 'pie'"></div>
            <div ref="chart_scatter" style="width: 100%;height: 520px;" v-show="which_one_pic == 'scatter'"></div>
        </el-card>

        <!-- 属性面板展示,对话框形式 -->
        <el-dialog title="直方图属性面板" :visible.sync="isBar" width="50%" >
            <!-- dialog会自动调节高度，所以我们直接在标签内加一个一定高度的div即可实现对话框的高度调整 -->
            <div style="height: 200px">
                <div class="add_legend">
                    图例名: <el-input placeholder="请输入新加图例名" v-model="bar_legend" style="width: 25%"></el-input>
                </div>
                <div style="margin-top: 15px;">
                    <!-- margin表示的距离是指到父容器上下左右的距离！ -->
                    横轴变量名: <el-input placeholder="请按顺序输入新加横轴下标" v-model="bar_new_xAxis_name" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="bar_add_xAxis">
                    确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="item in bar_xAxis_name_list" :key="item">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px;">
                    手动输入该图例数据:  <el-input placeholder="请按顺序输入图例数据" v-model="bar_new_yAxis_data" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="bar_add_yAxis">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="(item,index) in bar_yAxis_data_list_tmp1" :key="index">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px; width: 100%">
                     <el-upload class="upload-demo" action="" :on-change="handleChange" :on-remove="handleRemove" :on-exceed="handleExceed" :limit="1" :auto-upload="false" accept=".xls,.xlsx">
                        导入图例数据文件: <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="bar_complite">确 定</el-button>
                <el-button @click="bar_cancel">取 消</el-button>
            </span>
        </el-dialog>

        <el-dialog title="折线图属性面板" :visible.sync="isLine" width="50%">
            <div style="height: 200px">
                <div class="add_legend">
                    图例名: <el-input placeholder="请输入新加图例名" v-model="line_legend" style="width: 25%"></el-input>
                </div>
                <div style="margin-top: 15px;">
                    横轴变量名: <el-input placeholder="请按顺序输入新加横轴下标" v-model="line_new_xAxis_name" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="line_add_xAxis">
                    确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="item in line_xAxis_name_list" :key="item">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px;">
                    手动输入该图例数据:  <el-input placeholder="请按顺序输入图例数据" v-model="line_new_yAxis_data" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="line_add_yAxis">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="(item,index) in line_yAxis_data_list_tmp1" :key="index">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px; width: 100%">
                     <el-upload class="upload-demo" action="" :on-change="handleChange_line" :on-remove="handleRemove" :on-exceed="handleExceed" :limit="1" :auto-upload="false" accept=".xls,.xlsx">
                        导入图例数据文件: <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="line_complite">确 定</el-button>
                <el-button @click="line_cancel">取 消</el-button>
            </span>

        </el-dialog>

        <el-dialog title="饼状图属性面板" :visible.sync="isPie" width="50%">
            <div style="height: 200px">
                手动输入图表数据
                <div style="margin-top: 15px;">
                    输入图例序列:  <el-input placeholder="请按顺序输入图例数据" v-model="pie_new_name" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="pie_add_name">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="item in pie_name" :key="item">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px;">
                    输入值序列:  <el-input placeholder="请按顺序输入值数据" v-model="pie_new_data" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="pie_add_data">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="(item,index) in pie_data" :key="index">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px; width: 100%">
                     <el-upload class="upload-demo" action="" :on-change="handleChange_pie" :on-remove="handleRemove" :on-exceed="handleExceed" :limit="1" :auto-upload="false" accept=".xls,.xlsx">
                        导入数据文件: <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="pie_complite">确 定</el-button>
                <el-button @click="pie_cancel">取 消</el-button>
            </span>
        </el-dialog>

        <el-dialog title="散点图属性面板" :visible.sync="isScatter" width="50%" >
            <div style="height: 200px">
                选择回归模式:<el-select v-model="regression_type" placeholder="请选择">
                                <el-option v-for="now_type in regression_types" :key="now_type.value" :label="now_type.label" :value="now_type.value"></el-option>
                            </el-select>
                <div style="margin-top: 15px;">
                    输入横坐标序列:  <el-input placeholder="请按顺序输入横坐标序列数据" v-model="scatter_new_x_data" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="scatter_add_x_data">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="(item,index) in scatter_x_data_list" :key="index">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px;">
                   
                    输入纵坐标序列:  <el-input placeholder="请按顺序输入纵坐标序列数据" v-model="scatter_new_y_data" style="width: 35%"></el-input>
                    <el-dropdown split-button type="primary" @click="scatter_add_y_data">
                        确认添加
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item v-for="(item,index) in scatter_y_data_list" :key="index">{{item}}</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <div style="margin-top: 15px; width: 100%">
                     <el-upload class="upload-demo" action="" :on-change="handleChange_scatter" :on-remove="handleRemove" :on-exceed="handleExceed" :limit="1" :auto-upload="false" accept=".xls,.xlsx">
                        导入数据文件: <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="scatter_complite">确 定</el-button>
                <el-button @click="scatter_cancel">取 消</el-button>
            </span>
        </el-dialog>
        
    </div>

</template>


<script>
import ecStat from 'echarts-stat';

export default {
    data() {
        return {
            table_name: "",

            which_one_pic : "",
            isBar:      false,
            isLine:     false,
            isPie:      false,
            isScatter:  false,


            colors: ['#5470C6', '#91CC75', '#EE6666','#EE6888','#3bc420'],
            bar_legend: "",
            bar_legend_list: [],
            bar_new_xAxis_name: "",
            bar_xAxis_name_list: ['暂无数据'],  //横轴变量名
            bar_new_yAxis_data: "",
            bar_yAxis_data_list_tmp1: [],
            bar_yAxis_data_list_tmp2: [],
            bar_yAxis_data_list_final:[],
            bar_yAxis_data: [], //整体数据
            bar_serial_data: [],

            line_legend: "",
            line_legend_list: [],
            line_new_xAxis_name: "",
            line_xAxis_name_list: ['暂无数据'],  //横轴变量名
            line_new_yAxis_data: "",
            line_yAxis_data_list_tmp1: [],
            line_yAxis_data_list_tmp2: [],
            line_yAxis_data_list_final:[],
            line_yAxis_data: [], //整体数据
            line_serial_data: [],

            pie_new_name: "",
            pie_new_data: "",
            pie_name: [],
            pie_data: [],
            pie_name_and_data_from_file: [],
            pie_name_and_data_final:[],

            scatter_new_x_data: "",
            scatter_new_y_data: "",
            scatter_x_data_list: [],
            scatter_y_data_list: [],
            scatter_x_and_y_from_file: [],
            scatter_x_and_y_final:[],
            regression_type: "",
            regression_types: [{
                value: 'linear',
                label: '线性回归'
                }, {
                value: 'exponential',
                label: '指数回归'
                }, {
                value: 'polynomial',
                label: '多项式回归'
            }]
        }
    },
    created (){
        this.get_table_name();
    },
    methods: {
        drawBar(){
            if(this.bar_legend_list.length == this.bar_yAxis_data.length)
                return;
            if(this.bar_yAxis_data_list_final.length == 0)
                return;
            let myChart_bar = this.$echarts.init(this.$refs.chart_bar);
            var colors = this.colors;
            var legends = this.bar_legend_list;
            var xAxis_data = this.bar_xAxis_name_list;
            var minn = this.bar_yAxis_data_list_final[0];
            var maxx = this.bar_yAxis_data_list_final[0];
            for(var i=1;i<this.bar_yAxis_data_list_final.length;i++){
                maxx = Math.max(maxx,this.bar_yAxis_data_list_final[i]);
            }
            minn = minn- (maxx-minn) / 5;
            maxx = maxx+ (maxx-minn) / 5;
            let yAxis_obj = {}
            yAxis_obj.type = 'value';
            yAxis_obj.name = this.bar_legend;
            yAxis_obj.min  = 0
            yAxis_obj.max  = maxx
            yAxis_obj.position = 'right';
            yAxis_obj.offset = (legends.length-1) * 50;
            yAxis_obj.splitNumber = 5;
            yAxis_obj.interval = (maxx) / 5;
            yAxis_obj.axisLine = {show: true,lineStyle: {color: colors[legends.length-1]}};
            yAxis_obj.axisLabel= {formatter: '{value}'};
            this.bar_yAxis_data.push(yAxis_obj);
            var now_yAxis_data = this.bar_yAxis_data;

            let series_obj = {};
            series_obj.name = this.bar_legend;
            series_obj.type = 'bar';
            if(this.bar_serial_data.length != 0){
                series_obj.yAxisIndex = this.bar_serial_data.length;
            }
            series_obj.data = this.bar_yAxis_data_list_final;
            this.bar_serial_data.push(series_obj);
            var now_series_data = this.bar_serial_data;
                // 绘制图表
                myChart_bar.setOption({
                    // title: { text: '在Vue中使用echarts' },
                color: colors,
                tooltip: {trigger: 'axis', axisPointer: {type: 'cross'}},
                grid: {right: '20%'},
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                legend: {
                    data: legends
                },
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {
                            alignWithLabel: true
                        },
                        data: xAxis_data
                    }
                ],
                yAxis: now_yAxis_data,
                series: now_series_data
            });
            this.bar_legend = "";
            this.bar_yAxis_data_list_final = [];
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
        },
        bar_add_xAxis() {
            if(this.bar_xAxis_name_list[0] == '暂无数据'){
                this.bar_xAxis_name_list[0] = this.bar_new_xAxis_name;
            }else{
                this.bar_xAxis_name_list.push(this.bar_new_xAxis_name);
            }
            this.bar_new_xAxis_name = "";
        },
        bar_add_yAxis() {
            this.bar_yAxis_data_list_tmp1.push(this.bar_new_yAxis_data);
            this.bar_new_yAxis_data = "";
        },
        bar_complite() {
            this.which_one_pic = 'bar';
            this.isBar = false;
            if(this.bar_yAxis_data_list_tmp1.length != 0 && this.bar_yAxis_data_list_tmp2.length == 0)
                this.bar_yAxis_data_list_final = this.bar_yAxis_data_list_tmp1;
            else if(this.bar_yAxis_data_list_tmp1.length == 0 && this.bar_yAxis_data_list_tmp2.length != 0)
                this.bar_yAxis_data_list_final = this.bar_yAxis_data_list_tmp2;
            else if(this.bar_yAxis_data_list_tmp1.length != 0 && this.bar_yAxis_data_list_tmp2.length != 0){
                this.$message.error('数据导入方式不唯一');
            }
            console.log(this.bar_yAxis_data_list_tmp2);
            this.bar_yAxis_data_list_tmp1 = [];
            this.bar_yAxis_data_list_tmp2 = [];

            if(this.bar_legend != "")
                this.bar_legend_list.push(this.bar_legend);
        },
        bar_cancel() {
            this.isBar = false;
            this.bar_legend = "";
            this.bar_legend_list =  [];
            this.bar_new_xAxis_name = "";
            this.bar_xAxis_name_list = ['暂无数据'];  //横轴变量名
            this.bar_new_yAxis_data = "";
            this.bar_yAxis_data_list_tmp1 = [];
            this.bar_yAxis_data_list_tmp2 = [];
            this.bar_yAxis_data_list_final = [];
            
            this.which_one_pic = 'bar';
        },
        //超出最大上传文件数量时的处理方法
        handleExceed(){
            this.$message({
                type:'warning',
                message:'超出最大上传文件数量的限制！'
            })
            return;
        },
        //移除文件的操作方法
        handleRemove(file,fileList){
            this.fileTemp = null
        },
        //上传文件时处理方法  
        handleChange(file, fileList){
            this.fileTemp = file.raw;
            if(this.fileTemp){
                this.importfxx(this.fileTemp);
            } else {
                this.$message({
                    type:'warning',
                    message:'请上传附件！'
                })
            }
        },
        importfxx(obj) {
            let _this = this;
            this.file = event.currentTarget.files[0];  
            var rABS = false; //是否将文件读取为二进制字符串
            var f = this.file;
            var reader = new FileReader();
            FileReader.prototype.readAsBinaryString = function(f) {
            var binary = "";
            var wb; //读取完成的数据
            var outdata;
            var reader = new FileReader();
            reader.onload = function(e) {
                var bytes = new Uint8Array(reader.result);
                var length = bytes.byteLength;
                for(var i = 0; i < length; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                var XLSX = require('xlsx');
                wb = XLSX.read(binary, {
                    type: 'binary'
                });
                outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]); 
                outdata.map(v => {
                    let obj = v['num']
                    _this.bar_yAxis_data_list_tmp2.push(obj)
                })
                // _this.reload();
                }
                reader.readAsArrayBuffer(f);
            }
                reader.readAsBinaryString(f);
                this.bar_yAxis_data_list_final = this.bar_yAxis_data_list_tmp2;
        },
        line_add_xAxis() {
            if(this.line_xAxis_name_list[0] == '暂无数据'){
                this.line_xAxis_name_list[0] = this.line_new_xAxis_name;
            }else{
                this.line_xAxis_name_list.push(this.line_new_xAxis_name);
            }
            this.line_new_xAxis_name = "";
        },
        line_add_yAxis() {
            this.line_yAxis_data_list_tmp1.push(this.line_new_yAxis_data);
            this.line_new_yAxis_data = "";
        },
        line_complite() {
            this.which_one_pic = 'line';
            this.isLine = false;
            if(this.line_yAxis_data_list_tmp1.length != 0 && this.line_yAxis_data_list_tmp2.length == 0)
                this.line_yAxis_data_list_final = this.line_yAxis_data_list_tmp1;
            else if(this.line_yAxis_data_list_tmp1.length == 0 && this.line_yAxis_data_list_tmp2.length != 0)
                this.line_yAxis_data_list_final = this.line_yAxis_data_list_tmp2;
            else if(this.line_yAxis_data_list_tmp1.length != 0 && this.line_yAxis_data_list_tmp2.length != 0){
                this.$message.error('数据导入方式不唯一');
            }
            console.log(this.line_yAxis_data_list_final);
            this.line_yAxis_data_list_tmp1 = [];
            this.line_yAxis_data_list_tmp2 = [];

            if(this.line_legend != "")
                this.line_legend_list.push(this.line_legend);
        },
        line_cancel() {
            this.isLine = false;
            this.line_legend = "";
            this.line_legend_list =  [];
            this.line_new_xAxis_name = "";
            this.line_xAxis_name_list = ['暂无数据'];  //横轴变量名
            this.line_new_yAxis_data = "";
            this.line_yAxis_data_list_tmp1 = [];
            this.line_yAxis_data_list_tmp2 = [];
            this.line_yAxis_data_list_final = [];
            
            this.which_one_pic = 'line';
        },
        handleChange_line(file, fileList){
            this.fileTemp = file.raw;
            if(this.fileTemp){
                this.importfxx_line(this.fileTemp);
            } else {
                this.$message({
                    type:'warning',
                    message:'请上传附件！'
                })
            }
        },
        importfxx_line(obj) {
            let _this = this;
            this.file = event.currentTarget.files[0];  
            var rABS = false; //是否将文件读取为二进制字符串
            var f = this.file;
            var reader = new FileReader();
            FileReader.prototype.readAsBinaryString = function(f) {
            var binary = "";
            var wb; //读取完成的数据
            var outdata;
            var reader = new FileReader();
            reader.onload = function(e) {
                var bytes = new Uint8Array(reader.result);
                var length = bytes.byteLength;
                for(var i = 0; i < length; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                var XLSX = require('xlsx');
                wb = XLSX.read(binary, {
                    type: 'binary'
                });
                outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]); 
                outdata.map(v => {
                    let obj = v['num']
                    _this.line_yAxis_data_list_tmp2.push(obj)
                })
                }
                reader.readAsArrayBuffer(f);
            }
                reader.readAsBinaryString(f);
                this.line_yAxis_data_list_final = this.line_yAxis_data_list_tmp2;
        },
        drawLine() {
            if(this.line_legend_list.length == this.line_yAxis_data.length)
                return;
            if(this.line_yAxis_data_list_final.length == 0)
                return;
            // this.$refs.chart_line.display = 'block';
            let myChart_line = this.$echarts.init(this.$refs.chart_line);
            var legends = this.line_legend_list;
            var xAxis_data = this.line_xAxis_name_list;
            
            let series_obj = {};
            series_obj.name = this.line_legend;
            series_obj.type = 'line';
            // series_obj.stack = '总量';
            series_obj.data = this.line_yAxis_data_list_final;
            this.line_serial_data.push(series_obj);
            console.log(this.line_serial_data);
            var now_series_data = this.line_serial_data;
                // 绘制图表
            myChart_line.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: legends
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: xAxis_data
                },
                yAxis: {
                    type: 'value'
                },
                series: now_series_data
            });
            this.line_legend = "";
            this.line_yAxis_data_list_final = [];
        },
        pie_add_name() {
            if(this.pie_new_name!="")
                this.pie_name.push(this.pie_new_name);
            this.pie_new_name = "";
        },
        pie_add_data() {
            if(this.pie_new_data!="")
                this.pie_data.push(this.pie_new_data);
            this.pie_new_data = "";
        },
        handleChange_pie(file, fileList) {
            this.fileTemp = file.raw;
            if(this.fileTemp){
                this.importfxx_pie(this.fileTemp);
            } else {
                this.$message({
                    type:'warning',
                    message:'请上传附件！'
                })
            }
        },
        importfxx_pie(obj){
            let _this = this;
            this.file = event.currentTarget.files[0];  
            var rABS = false; //是否将文件读取为二进制字符串
            var f = this.file;
            var reader = new FileReader();
            FileReader.prototype.readAsBinaryString = function(f) {
            var binary = "";
            var wb; //读取完成的数据
            var outdata;
            var reader = new FileReader();
            reader.onload = function(e) {
                var bytes = new Uint8Array(reader.result);
                var length = bytes.byteLength;
                for(var i = 0; i < length; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                var XLSX = require('xlsx');
                wb = XLSX.read(binary, {
                    type: 'binary'
                });
                outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]); 
                outdata.map(v => {
                    let obj = {}
                    obj.value = v['value']
                    obj.name  = v['name']
                    _this.pie_name_and_data_from_file.push(obj)
                })
                }
                reader.readAsArrayBuffer(f);
            }
                reader.readAsBinaryString(f);
                // this.pie_name_and_data_final = this.pie_name_and_data_from_file;
        },
        pie_complite() {
            this.which_one_pic = 'pie';
            this.isPie = false;

            if(this.pie_name.length != this.pie_data.length)
                this.$message.error('图例个数与对应值个数不匹配');
            else if(this.pie_name_and_data_from_file.length != 0 && this.pie_name.length != 0)
                this.$message.error('数据导入方式冲突');
            else if(this.pie_name_and_data_from_file.length == 0 && this.pie_name.length != 0){
                var now_data = [];
                for(var i=0;i<this.pie_name.length;i++){
                    let obj = {};
                    obj.value = this.pie_data[i];
                    obj.name  = this.pie_name[i];
                    now_data.push(obj);
                }
                this.pie_name_and_data_final = now_data;
            }else if(this.pie_name_and_data_from_file.length != 0 && this.pie_name.length == 0){
                this.pie_name_and_data_final = this.pie_name_and_data_from_file;
                console.log(this.pie_name_and_data_from_file);
            }
                
            this.pie_name_and_data_from_file = [];
            this.pie_name = [];
            this.pie_data = [];

        },
        drawPie() {
            // this.$refs.chart_line.display = 'block';
            let myChart_pie = this.$echarts.init(this.$refs.chart_pie);
            var now_series_data = this.pie_name_and_data_final;
                // 绘制图表
            myChart_pie.setOption({
                legend: {
                    top: 'bottom'
                },
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                series: [
                    {
                        name: '面积模式',
                        type: 'pie',
                        radius: [50, 250],
                        center: ['50%', '50%'],
                        roseType: 'area',
                        itemStyle: {
                            borderRadius: 8
                        },
                        data: now_series_data
                    }
                ]
            });
        },
        pie_cancel() {
            this.isPie = false;
            this.pie_new_name = "";
            this.pie_new_data = "";
            this.pie_name = [];
            this.pie_data = [];
            this.pie_name_and_data_from_file = [];
            this.pie_name_and_data_final = [];
            this.which_one_pic = 'pie';
        },
        scatter_add_x_data() {
            if(this.scatter_new_x_data != "")
                this.scatter_x_data_list.push(this.scatter_new_x_data);
            this.scatter_new_x_data = "";
        },
        scatter_add_y_data() {
            if(this.scatter_new_y_data != "")
                this.scatter_y_data_list.push(this.scatter_new_y_data);
            this.scatter_new_y_data = "";
        },
        handleChange_scatter(file, fileList){
            this.fileTemp = file.raw;
            if(this.fileTemp){
                this.importfxx_scatter(this.fileTemp);
            } else {
                this.$message({
                    type:'warning',
                    message:'请上传附件！'
                })
            }
        },
        importfxx_scatter(obj){
            let _this = this;
            this.file = event.currentTarget.files[0];  
            var rABS = false; //是否将文件读取为二进制字符串
            var f = this.file;
            var reader = new FileReader();
            FileReader.prototype.readAsBinaryString = function(f) {
            var binary = "";
            var wb; //读取完成的数据
            var outdata;
            var reader = new FileReader();
            reader.onload = function(e) {
                var bytes = new Uint8Array(reader.result);
                var length = bytes.byteLength;
                for(var i = 0; i < length; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                var XLSX = require('xlsx');
                wb = XLSX.read(binary, {
                    type: 'binary'
                });
                outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]); 
                outdata.map(v => {
                    let obj = []
                    obj.push(v['x'])
                    obj.push(v['y'])
                    _this.scatter_x_and_y_from_file.push(obj)
                })
                }
                reader.readAsArrayBuffer(f);
            }
                reader.readAsBinaryString(f);
                // this.pie_name_and_data_final = this.pie_name_and_data_from_file;
        },
        drawScatter() {
            var ecStat = require('echarts-stat');
            let myChart_scatter = this.$echarts.init(this.$refs.chart_scatter);
            var now_series_data = this.scatter_x_and_y_final;
                // 绘制图表
            var myRegression = ecStat.regression(this.regression_type, now_series_data);

            myRegression.points.sort(function(a, b) {
                return a[0] - b[0];
            });

            myChart_scatter.setOption({
                title: {
                    text: 'Linear Regression',
                    subtext: 'By ecStat.regression',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                xAxis: {
                    type: 'value',
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    },
                },
                yAxis: {
                    type: 'value',
                    min: 1.5,
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    },
                },
                series: [{
                    name: 'scatter',
                    type: 'scatter',
                    emphasis: {
                        label: {
                            show: true,
                            position: 'left',
                            color: 'blue',
                            fontSize: 16
                        }
                    },
                    data: now_series_data
                }, {
                    name: 'line',
                    type: 'line',
                    showSymbol: false,
                    data: myRegression.points,
                    markPoint: {
                        itemStyle: {
                            color: 'transparent'
                        },
                        label: {
                            show: true,
                            position: 'left',
                            formatter: myRegression.expression,
                            color: '#333',
                            fontSize: 14
                        },
                        data: [{
                            coord: myRegression.points[myRegression.points.length - 1]
                        }]
                    }
                }]
            });
        },
        scatter_complite() {
            this.which_one_pic = 'scatter';
            this.isScatter = false;

            if(this.scatter_x_data_list.length != this.scatter_y_data_list.length)
                this.$message.error('图例个数与对应值个数不匹配');
            else if(this.scatter_x_and_y_from_file.length != 0 && this.scatter_x_data_list.length != 0)
                this.$message.error('数据导入方式冲突');
            else if(this.scatter_x_and_y_from_file.length == 0 && this.scatter_x_data_list.length != 0){
                var now_data = [];
                for(var i=0;i<this.scatter_x_data_list.length;i++){
                    let obj = [];
                    obj.push(this.scatter_x_data_list[i]);
                    obj.push(this.scatter_y_data_list[i]);
                    now_data.push(obj);
                }
                this.scatter_x_and_y_final = now_data;
                
            }else if(this.scatter_x_and_y_from_file.length != 0 && this.scatter_x_data_list.length == 0){
                this.scatter_x_and_y_final = this.scatter_x_and_y_from_file;
                
            }
            this.scatter_x_and_y_from_file = [];
            this.scatter_x_data_list = [];
            this.scatter_y_data_list = [];
        },
        scatter_cancel() {
            this.isScatter = false;
            this.scatter_new_x_data = "";
            this.scatter_new_y_data = "";
            this.scatter_x_data_list = [];
            this.scatter_y_data_list = [];
            this.scatter_x_and_y_from_file = [];
            this.scatter_x_and_y_final = [];
            this.which_one_pic = 'scatter';
        },
        display_pic() {
            console.log(this.which_one_pic);
            if(this.which_one_pic == 'bar')
                this.drawBar();
            else if(this.which_one_pic == 'line')
                this.drawLine();
            else if(this.which_one_pic == 'pie')
                this.drawPie();
            else if(this.which_one_pic == 'scatter')
                this.drawScatter(); 
        }
        
    }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.select_graphics {
    position: absolute;
    left: 0;
}

.add_legend {
    display: inline;
    // background-color: #3bc420;
}
.bar_input_data {
    display: inline;
}
</style>


