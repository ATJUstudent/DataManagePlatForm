<template>
    <div>
        <div>
            <el-button  icon="el-icon-circle-plus-outline" @click="dialogVisible = true">添加数据表</el-button>
        </div>
        <div class="box">
            <div>为当前数据表导入数据: </div>
            <div class="box">
            <el-upload action="" :on-change="handleChange" :on-remove="handleRemove" :on-exceed="handleExceed" :limit="1" :auto-upload="false" accept=".xls,.xlsx">
                <el-button size="small" icon="el-icon-upload2">导入数据</el-button>
            </el-upload>
            </div>
            <el-button @click="display_and_send" size="medium" class="intput_button">确认导入</el-button>    
        </div>
        <el-dialog title="新建数据表" :visible.sync="dialogVisible" width="50%">
            <el-form :inline="true" :model="dynamicValidate" ref="dynamicValidate" label-width="100px">
            <el-form-item prop="tablename" label="表名" :rules="[{ required: true,  message: '请输入数据库名', trigger: 'blur' }]" >
                <el-input v-model="tablename"></el-input>
            </el-form-item>
            <div v-for="(item, index) in dynamicValidate.dynamicItem" :key="index" >
                <el-form-item label="属性" :prop="'dynamicItem.' + index + '.Field'" 
                :rules="{ required: true, message: 'field不能为空', trigger: 'blur', }">
                    <el-input v-model="item.Field"></el-input>
                </el-form-item>
                <el-form-item label="类型" :prop="'dynamicItem.' + index + '.Type'" 
                :rules="{ required: true, message: 'type不能为空', trigger: 'blur', }">
                    <el-input v-model="item.Type"></el-input>
                </el-form-item>
                <el-form-item  label="是否为空" :prop="'dynamicItem.' + index + '.Null'" 
                :rules="{ required: true, message: 'null不能为空', trigger: 'blur', }">
                        <el-input v-model="item.Null"></el-input>
                </el-form-item>
                <el-form-item label="是否为主键" :prop="'dynamicItem.' + index + '.Key'" 
                :rules="{ required: true, message: 'key不能为空', trigger: 'blur', }">
                        <el-input v-model="item.Key"></el-input>
                </el-form-item>
                <el-form-item label="默认值" :prop="'dynamicItem.' + index + '.Default'" 
                :rules="{ required: true, message: 'default不能为空', trigger: 'blur', }">
                        <el-input v-model="item.Default"></el-input>
                </el-form-item>
                <el-form-item>
                <i class="el-icon-delete" @click="deleteItem(item, index)" />
                </el-form-item>
            </div>
            <div>
            <el-button icon="el-icon-circle-plus-outline" @click="addItem">新增</el-button>                                                      
            <el-button icon="el-icon-refresh" @click="resetForm('dynamicValidate')" >重置</el-button>  
            <el-button icon="el-icon-circle-check" @click="create_table()" >提交</el-button>
            </div>                                              
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data(){
        return {
            isCollapse: true,
            select_db_name: "",
            activeName: "first",
            select_table_name: "",
            dialogVisible:false,
            tablename:'',
            dynamicValidate: {
                dynamicItem: []
            },
            data_form:[]
        }
    },
    created() {
        this.get_preparation()
    },
    methods: {
        async get_preparation(){
            this.select_db_name = this.$route.query.db_selected;
            this.select_table_name = this.$route.query.table_selected;
            console.log(this.select_db_name);
            console.log(this.select_table_name);
        },
        async send(){
            console.log("删除")
            console.log(JSON.stringify(this.select_table_name));
            //下面需要向服务器发起请求
            const response = await this.$http.post("delete_table_sql",{db : this.select_db_name, tb : this.select_table_name});
            if (response['status'] === 200) 
                this.$message.success('删除成功');
            else 
                return this.$message.error('删除错误');
            return this.$router.push("/main_page");
        },
        submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid) {
                alert('submit!');
            } 
            else {
                console.log('error submit!!');
                return false;
            }
        });
        },
        resetForm(formName){
            this.$refs[formName].resetFields();
        },
        deleteItem(item,index) {
            this.dynamicValidate.dynamicItem.splice(index, 1)
        },
        addItem() {
            this.dynamicValidate.dynamicItem.push({
                Field: '',
                Type:'',
                Null:'',
                Key:'',
                Default:'',
            });
        },
        async create_table(){
            console.log("新建数据表")
            console.log(JSON.stringify(this.tablename));
            console.log(JSON.stringify(this.dynamicValidate.dynamicItem));
            //下面需要向服务器发起请求
            const response = await this.$http.post("create_table_sql",{tb : this.tablename, attr : this.dynamicValidate.dynamicItem, db : this.select_db_name});
            if (response['status'] === 200) 
                this.$message.success('新建成功');
            else 
                return this.$message.error('新建错误');
            return this.$router.push("/main_page");
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
                this.importfile(this.fileTemp);
            } else {
                this.$message({
                    type:'warning',
                    message:'请上传附件！'
                })
            }
        },
        importfile(obj) {
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
                    _this.data_form.push(v);
                })
                // _this.reload();
                }
                reader.readAsArrayBuffer(f);
            }
                reader.readAsBinaryString(f);
        },
        async display_and_send(){
            console.log(this.data_form);
            const response = await this.$http.post("input_table_data",{db : this.select_db_name, tb : this.select_table_name, data_form: this.data_form});
            if (response['status'] === 200) 
                this.$message.success('数据导入成功，请自行查看导入结果');
            else 
                return this.$message.error('数据导入出错，请检查数据格式或再试一次');
            return this.$router.push({path :'/data_query',query: {db_selected : this.select_db_name, table_selected : this.select_table_name}});
        }
    }
}
</script>

<style>
.loginOut{
    position: relative;
    left:20px;
    top:5px;
    color: #e6a23c;
    font-weight: 600;
    font-size: 14px;
}
.box{
    position: relative;
    margin-top: 30px;
}
.button{
    position: relative;
    margin-top: 10px;
}
.input_button{
    position: absolute;
    margin-left: 30px;
    margin-top: 30px;
}
</style>