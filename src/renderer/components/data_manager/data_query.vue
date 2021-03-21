<template>
  <el-table class="tb-edit" highlight-current-row :data="tableData" height="600" border style="width: 100%">                	
	<template v-for="(col,index) in cols">                    
	<el-table-column :prop="col.prop" :label="col.label"></el-table-column>                
	</template>              
  </el-table>
</template>

<script>
  export default {
    data() {
      return {
	    cols : [],
        tableData: []
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

        }
    }
  }
</script>