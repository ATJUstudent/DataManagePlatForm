<template>
  <div class="box">
      <div style="display:inline-block;"><el-button size="medium" icon="el-icon-circle-plus-outline" @click="add" class="add">添加数据</el-button></div>
      <div style="display:inline-block;">
        <download-excel class = "export-excel-wrapper" :data = "tableData.filter(data => !search || data[selected_col].toString().toLowerCase().includes(search.toString().toLowerCase()))" :fields = "fields" name = "filename.xls">
        <!-- 上面可以自定义自己的样式，还可以引用其他组件button -->
          <el-button icon="el-icon-download" size="medium">导出EXCEL</el-button>
        </download-excel>
      </div>
  <el-table class="tb-edit" highlight-current-row :data="tableData.filter(data => !search || data[selected_col].toString().toLowerCase().includes(search.toString().toLowerCase()))" height="600" border style="width: 100%">                	
	<template v-for="(col,index) in cols">                    
		<el-table-column :prop="col.prop" :label="col.label" :key="index"></el-table-column>                
	</template>              
	  <el-table-column
		  align="right">
		  <template slot="header" >
			<el-dropdown @command="handleCommand">
				<span class="el-dropdown-link">
				下拉菜单<i class="el-icon-arrow-down el-icon--right"></i>
				</span>
				<el-dropdown-menu slot="dropdown">
					<template >
						<el-dropdown-item v-for="(col,index) in cols" :key="index" :command="col.label">{{col.label}}</el-dropdown-item>
					</template>
				</el-dropdown-menu>
			</el-dropdown>

			<el-input v-model="search" size="mini" prefix-icon="el-icon-search" placeholder="输入关键字搜索"/>
		  </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
      </template>
    </el-table-column>
  </el-table>
  </div>
</template>

<script>
  export default {
    data() {
      return {
	    cols : [],
        tableData: [],
		search: '',
		selected_col: '',
		select_db_name: '',
		table_name: '',
		fields : {}
      }
    },
    created() {
        this.get_preparation()
    },
    methods: {
        async get_preparation(){
            this.select_db_name = this.$route.query.db_selected;
            this.table_name = this.$route.query.table_selected;
            const {data:result} = await this.$http.get('/data_home/data_query',{params: {db_selected: this.select_db_name, table_selected: this.table_name}});
            var res = JSON.parse(JSON.stringify(result));
            this.cols = res['cols']
            this.tableData = res['tableData']
			      this.fields = res['Fields']
        },
		handleEdit(index, row) {
			this.$router.push({path :'/data_update',query: {db_selected : this.select_db_name, table_selected : this.table_name, data : this.tableData[index], cols : this.cols}});
		},
      async handleDelete(index, row) {
      let ret = {};
      for(let key in this.tableData[index]){
        ret[key] = this.tableData[index][key];
      }
      var Ret = {'0' : ret};
      var Ret2 = {'json' : Ret, 'info' : {'db' : this.select_db_name, 'table' : this.table_name}};
      const response = await this.$http.post("data_delete",Ret2);
      if (response['status'] === 200) 
            this.$message.success('成功');

          console.log(index, row);
    },
	  handleCommand(command) {
      this.$message('click on item ' + command);
		  this.selected_col = command;
    },
	  add(){
		  this.$router.push({path :'/data_add',query: {db_selected : this.select_db_name, table_selected : this.table_name, cols : this.cols}});
	  }
  }
}
</script>

<style>
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>