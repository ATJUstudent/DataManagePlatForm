<template>
  <el-tabs v-model="activeName">
    <el-tab-pane label="新建数据库" name="first">
       <el-form :model="createdb" :rules="rules" ref="createdb_Form" label-width="100px">
          <el-form-item label="数据库名称" prop="name">
             <el-input v-model="createdb.name" prefix-icon="el-icon-edit"></el-input>
          </el-form-item>
          <el-form-item label="编码类型">
             <el-input v-model="createdb.codetype" prefix-icon="el-icon-edit"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-circle-check" @click="create_db()">提交</el-button>
            <router-link :to="{path: '/main_page'}">
              <el-button icon="el-icon-s-home">返回</el-button>
            </router-link>
          </el-form-item>
        </el-form>
    </el-tab-pane>
    <el-tab-pane label="导入数据库" name="third">
        <el-form :model="createdb" :rules="rules" ref="createdb_Form" label-width="100px">
          <el-form-item label="数据库名称" prop="name">
             <el-input v-model="createdb.name" prefix-icon="el-icon-edit"></el-input>
          </el-form-item>
          <el-form-item label="编码类型">
             <el-input v-model="createdb.codetype" prefix-icon="el-icon-edit"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-circle-check" @click="create_db()">提交</el-button>
          </el-form-item>
        </el-form>
        <el-upload
          action='/upload_xlsx'
          :limit="1">
          <el-button size="small" icon="el-icon-upload2">点击上传</el-button>
        </el-upload>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import XLSX from 'xlsx'
  export default {
    props: {
    dialogVisible: Boolean
    },
    data() {
      return {
        activeName: 'first',
        createdb: {
            name:"",
            codetype:""
        },
        rules: {
          name: [
            { required: true, message: '请输入数据库名称', trigger: 'blur' }
          ],
        },
		    excelJson : {
          name:"",
          data:[]
        }
      }
    },
    methods: {
	  handleUpload (file,fileList) {
    this.excelJson.name = file.name;
		alert(file.name);
		const types = file.name.split('.')[1];
	  const fileType = [
		'xlsx', 'xlc', 'xlm', 'xls', 'xlt', 'xlw', 'csv'
	  ].some(item => item == types);
	  if (!fileType) {
		alert('格式错误！请重新选择');
		return
	  }

	  const reader = new FileReader();
	  let result = [];
	  reader.onload = function(e) {
		const data = e.target.result;
		const wb = XLSX.read(data, {
		  type: 'binary'
		});
		wb.SheetNames.forEach((sheetName) => {
		  result.push({
			sheetName: sheetName,
			sheet: XLSX.utils.sheet_to_json(wb.Sheets[sheetName])
		  })
		});
	  };
	  reader.readAsBinaryString(file.raw)
	  this.excelJson.data = result;
	  },
	  async aa(){
		    // console.log(JSON.stringify(this.excelJson));
        //  const response = await this.$http.post("upload_xlsx", this.excelJson);
        //  if (response['status'] === 200) 
        //         this.$message.success('提交成功');
        //   else 
        //         return this.$message.error('提交错误');
	  },
    async create_db(){
            console.log("新建数据库")
            console.log(JSON.stringify(this.createdb.name));
            console.log(JSON.stringify(this.createdb.codetype));
            //下面需要向服务器发起请求
            const response = await this.$http.post("create_database_sql",{db : this.createdb.name, tb : this.createdb.codetype});
            if (response['status'] === 200) 
                this.$message.success('新建成功');
            else 
                return this.$message.error('新建错误');
            return this.$router.push("/main_page");
        }
    }
  }
</script>