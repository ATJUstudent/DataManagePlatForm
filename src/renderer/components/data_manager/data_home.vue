<template>
    <div>
        <h3>data---home!!!</h3>
        <router-link :to="{path: '/', query: {value: 'world'}}">
          <el-button>返回</el-button>
        </router-link>
    </div>

</template>

<script>
export default {
    data(){
        return {
            select_db_name:""
        }
    },
    created() {
        this.get_preparation()
    },
    methods: {
        get_preparation(){
            this.select_db_name = this.$route.query.value;
        }
    }
}
</script>