<template>
  <div class="register-container">
    <el-form class="register-form" :model="registerForm" :rules="registerRules" ref="registerForm" label-position="left">
      <h3 class="title">用户注册</h3>
      <el-form-item prop="username">
        <span class="svg-container svg-container_register">
          <svg-icon icon-class="user" />
        </span>
        <el-input name="username" type="text" v-model="registerForm.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password"></svg-icon>
        </span>
        <el-input name="password" :type="pwdType" v-model="registerForm.password"
          placeholder="请输入密码" />
          <span class="show-pwd" @click="showPwd"><svg-icon icon-class="eye" /></span>
      </el-form-item>
      <el-form-item prop="password2">
        <span class="svg-container">
          <svg-icon icon-class="password"></svg-icon>
        </span>
        <el-input name="password2" :type="pwdType2" v-model="registerForm.password2"
          placeholder="请再次输入密码" />
          <span class="show-pwd" @click="showPwd2"><svg-icon icon-class="eye" /></span>
      </el-form-item>
      <el-form-item prop="realname">
        <span class="svg-container svg-container_register">
          <svg-icon icon-class="user" />
        </span>
        <el-input name="realname" type="text" v-model="registerForm.realname" placeholder="请输入真实姓名" />
      </el-form-item>
      <el-form-item prop="telephone">
        <span class="svg-container svg-container_register">
          <svg-icon icon-class="telephone" />
        </span>
        <el-input name="telephone" type="text" v-model="registerForm.telephone" placeholder="请输入手机号" />
      </el-form-item>
      <el-form-item prop="email">
        <span class="svg-container svg-container_register">
          <svg-icon icon-class="email" />
        </span>
        <el-input name="email" type="text" v-model="registerForm.email" placeholder="请输入电子邮箱" />
      </el-form-item>
      <div class="tips">
        <el-checkbox v-model="agreement"></el-checkbox>
        <span>我已经阅读并同意遵守</span>
        <el-button type="text" @click="agreementVisible = true">《服务条款》</el-button>
      </div>
      <div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-button type="success" style="width:100%;" :loading="loading" :disabled="!actived" @click.native.prevent="handleRegister">
              注册
            </el-button>
          </el-col>
          <el-col :span=12>
            <el-button type="info" style="width:100%;" :loading="loading" @click.native.prevent="cancel">
              取消
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-form>
    <el-dialog :visible.sync="agreementVisible" title="服务条款" :modal-append-to-body='false'>
      <span>服务条款</span>
    </el-dialog>
  </div>
</template>

<script>
import { remote } from '@/assets/api'

export default {
  name: 'register',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 5) {
        callback(new Error('用户名不能小于5位'))
      } else if (value.length > 15) {
        callback(new Error('用户名不能大于15位'))
      } else {
        callback()
      }
    }
    const validatePass = (rule, value, callback) => {
      if (value.length < 5 || value.length > 15) {
        callback(new Error('请确保密码长度为5-15位'))
      } else {
        callback()
      }
    }
    const validateRealname = (rule, value, callback) => {
      if (value.length < 2 || value.length > 10) {
        callback(new Error('请填写真实姓名'))
      } else {
        callback()
      }
    }
    const validateTelephone = (rule, value, callback) => {
      if (!value.match(/^1[0-9]{10}$/)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      if (!value.match(/^\w+@\w+\.\w+$/)) {
        callback(new Error('请输入正确的电子邮箱'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {},
      registerRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        realname: [{ required: true, trigger: 'blur', validator: validateRealname }],
        password: [{ required: true, trigger: 'blur', validator: validatePass }],
        telephone: [{ required: true, trigger: 'blur', validator: validateTelephone }],
        email: [{ required: true, trigger: 'blur', validator: validateEmail }],
        password2: [{ required: true, trigger: 'blur', validator: this.validatePass2 }]
      },
      loading: false,
      pwdType: 'password',
      pwdType2: 'password',
      agreement: false,
      agreementVisible: false
    }
  },
  computed: {
    actived() {
      if (!this.registerForm.username) { return false }
      if (!this.registerForm.password) { return false }
      if (!this.registerForm.realname) { return false }
      if (!this.registerForm.telephone) { return false }
      if (!this.registerForm.email) { return false }
      if (!this.registerForm.password2) { return false }
      return this.agreement
    }
  },
  methods: {
    showPwd() {
      if (this.pwdType === 'password') {
        this.pwdType = ''
      } else {
        this.pwdType = 'password'
      }
    },
    showPwd2() {
      if (this.pwdType2 === 'password') {
        this.pwdType2 = ''
      } else {
        this.pwdType2 = 'password'
      }
    },
    validatePass2(rule, value, callback) {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    },
    cancel() {
      this.$router.push({ path: '/login' })
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid && this.agreement) {
          this.loading = true
          remote('/user/register', this.registerForm).then((data) => {
            this.loading = false
            this.$message({
              message: data.message,
              type: 'success'
            })
            this.$router.push({ path: '/login' })
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
$dark_gray:#ccc;
$light_gray:#eee;
register-container {
    position: fixed;
    height: 100%;
    width: 100%;
    // background: url(../../assets/images/login-bg.png) no-repeat center top;
    // background-size: 100%;
    overflow-y: auto;
    .register-form {
        position: absolute;
        left: 0;
        right: 0;
        width: 520px;
        padding: 35px 35px 15px 35px;
        margin: 50px auto;
    }
    .tips {
        font-size: 14px;
        color: #fff;
        margin-top: -10px;
        margin-bottom: 10px;
        background: rgba(0, 0, 0, 0.4);
        .el-checkbox {
            padding: 10px;
        }
        .el-button {
            color: #fff;
        }
    }
    .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        width: 30px;
        display: inline-block;
        &_register {
            font-size: 20px;
        }
    }
    .title {
        font-size: 26px;
        font-weight: 400;
        color: $light_gray;
        margin: 0px auto 30px auto;
        text-align: center;
        font-weight: bold;
    }
    .show-pwd {
        position: absolute;
        right: 10px;
        top: 7px;
        font-size: 16px;
        color: $dark_gray;
        cursor: pointer;
        user-select: none;
    }
}
</style>