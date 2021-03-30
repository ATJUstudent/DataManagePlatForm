<template>
<el-form ref="form" :model="form" label-width="80px">
	<template v-for="col in cols">                    
		<el-form-item label=col.label>
			<el-input v-model="form[col.label]"></el-input>
		</el-form-item>        
	</template>   
  <el-form-item>
    <el-button type="primary" @click="onSubmit">修改</el-button>
    <el-button @click="back">返回</el-button>
  </el-form-item>
</el-form>
</template>
<script>
  export default {
    data() {
      return {
		select_db_name : '',
		table_name : '',
		cols : [],
        form : {},
		data_orign : {}
      }
    },
	created(){
		this.get_preparation();
	},
    methods: {
	  get_preparation(){
        this.select_db_name = this.$route.query.db_selected;
        this.table_name = this.$route.query.table_selected;
		this.cols = this.$route.query.cols;
		this.form = this.$route.query.data;
		for(let key in this.form){
			this.data_orign[key] = this.form[key];
		}
    },
      async onSubmit() {
		let ret = {};
		for(let key in this.form){
			ret[key] = this.form[key];
		}
		var array = [];
		for(let key in this.form){
			if(this.form[key] !== this.data_orign[key]){
				array.push(key);
			}
		}
		ret['update'] = array;
		var Ret = {'0' : ret};
		var Ret2 = {'json' : Ret, 'info' : {'db' : this.select_db_name, 'table' : this.table_name}};
		const response = await this.$http.post("data_update",Ret2);
		if (response['status'] === 200) 
          this.$message.success('成功');
        console.log('submit!');
      },
	  back(){
		this.$router.push({path :'/data_query',query: {db_selected : this.select_db_name, table_selected : this.table_name}});
	  }
    }
  }
</script>