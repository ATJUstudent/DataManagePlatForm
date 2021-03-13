<template>
  <div class="login_container">
    <div class="login_box">
      <el-form ref="loginFormRef" :model="loginform" :rules="login_rules" label-width="80px" class="login_form">
        <!-- IP地址 -->
        <el-form-item label="IP地址">
          <el-input v-model="loginform.IP" placeholder="请输入IP地址"></el-input>
        </el-form-item>
        <!-- 端口号 -->
        <el-form-item label="端口号">
          <el-input v-model="loginform.port" placeholder="请输入端口号"></el-input>
        </el-form-item>
        <!-- 用户名 -->
        <el-form-item label="用户名">
          <el-input v-model="loginform.username" placeholder="请输入用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item label="密码">
          <el-input v-model="loginform.password" placeholder="请输入密码" prefix-icon="el-icon-lock" type="password"></el-input>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item class="button_groups">
          <el-button type="primary" @click="login_load">确认连接</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
      loginform: {
        IP:'',
        port:'',
        username: '',
        password: ''
      },
      //表单验证规则
      login_rules:{
        username:[
          { required: true, message: "用户名不能为空",trigger:"blur"},
          { min: 3, max: 10, message: "长度在3到10个字符之间",trigger:"blur"}
        ],
        password:[
          { required: true, message: "密码不能为空",trigger:"blur"},
          { min: 5, max: 16, message: "长度在5到16个字符之间",trigger:"blur"}
        ]
      }
    }
  },
  methods: {
    login_load() {
      this.$refs.loginFormRef.validate(async (valid)=>{
        console.log(valid);
        if(!valid) return;
        //下面需要向服务器发起请求
        const  response=await this.$http.post("login",this.loginform);
        console.log(response['data']);
        if (response['status'] === 200) 
          this.$message.success('登录成功');
        else 
          return this.$message.error('用户名或密码错误');
        return this.$router.push("/main_page");
      });
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.login_container {
  background-color: #2b4b6b;
  height: 100%;
}
.login_box {
  width: 450px;
  height: 450px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top:  50%;
  transform: translate(-50%, -50%);
}

.button_groups {
  display: flex;
  justify-content: flex-end;
}

.login_form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 20px 20px;
  box-sizing: border-box;
}
</style>


