<template>
  <div class="block">
    <!--      添加登录标题和表格-->
    <el-form ref="loginForm" :model="loginForm" status-icon :rules="loginRules" class="login-form" auto-complete="on"
             label-position="left">
      <div class="title-container">
        <h3 class="title">Spider 登录界面</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user"/>
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
        </span>
      </el-form-item>

      <el-form-item prop="email">
        <!--        <span class="svg-container">-->
        <!--          <i class="el-icon-message"></i>-->
        <!--        </span>-->
        <div class="email-container">
          <i class="el-icon-message"></i>
        </div>
        <el-input
          ref="email"
          v-model="loginForm.email"
          placeholder="QQ mail"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>
      <el-tooltip class="item" effect="dark" content="点击登录" placement="left">
        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
                   @click.native.prevent="handleLogin">Login
        </el-button>

      </el-tooltip>

      <div class="tips">
        <span style="margin-right:20px;">username: admin</span>
        <span> password: any</span>
      </div>

    </el-form>
    <!--    导入粒子特效控件,css设置所在位置和position-->
    <div class="lizi">
      <vue-particles
        color="#fff"
        :particleOpacity="0.7"
        :particlesNumber="60"
        shapeType="circle"
        :particleSize="4"
        linesColor="#fff"
        :linesWidth="1"
        :lineLinked="true"
        :lineOpacity="0.4"
        :linesDistance="150"
        :moveSpeed="2"
        :hoverEffect="true"
        hoverMode="grab"
        :clickEffect="true"
        clickMode="push"
      >
      </vue-particles>
    </div>

  </div>
</template>

<script>
  import {validUsername} from '@/utils/validate'

  export default {
    name: 'Login',
    data() {
      const validateUsername = (rule, value, callback) => {
        if (!validUsername(value)) {
          callback(new Error('Please enter the correct user name'))
        } else {
          callback()
        }
      }
      const validatePassword = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error('The password can not be less than 6 digits'))
        } else {
          callback()
        }
      }
      const validateEmail = (rule, value, callback) => {
        if (!validUsername(value)) {
          callback(new Error('Please enter the correct email'))
        } else {
          callback()
        }
      }
      return {
        loginForm: {
          username: '',
          password: '',
          email: ''
        },
        loginRules: {
          username: [{required: true, trigger: 'blur', validator: validateUsername}],
          password: [{required: true, trigger: 'blur', validator: validatePassword}],
          email: [
            {required: true, message: '请输入邮箱地址', trigger: 'blur'},
            {type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change']}
          ]
        },
        loading: false,
        passwordType: 'password',
        redirect: undefined,
        email: ''
      }
    },
    watch: {
      $route: {
        handler: function (route) {
          this.redirect = route.query && route.query.redirect
        },
        immediate: true
      }
    },
    methods: {
      showPwd() {
        if (this.passwordType === 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
        this.$nextTick(() => {
          this.$refs.password.focus()
        })
      },
      handleLogin() {
        this.$refs.loginForm.validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('user/login', this.loginForm).then(() => {
              this.$router.push({path: this.redirect || '/'})
              this.loading = false
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


<style lang="scss" scoped>
  /*添加fixed使得页面没有了垂直滚动条*/
  .block {
    background-repeat: no-repeat;
    background-size: 100% 100%;
    position: fixed;
    /*background-image: url("../../assets/login_images/indexbg.jpg");*/
    height: 100%;
    width: 100%;
  }

  /*添加的是粒子的设置,top和left使得不会被图片挤下去同时还需要设置position:fixed自适应*/
  .lizi {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("../../assets/login_images/indexbg.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    overflow: hidden;
  }

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
    background-size: cover;

    .title-container {
      position: relative;
    }

    .title {
      font-size: 26px;
      color: lightgray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    .svg-container {
      padding: 6px 5px 6px 15px;
      color: deepskyblue;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
    }

    .email-container {
      padding: 6px 5px 6px 15px;
      color: deepskyblue;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
      font-size: 20px;
    }

    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: darkgray;
      cursor: pointer;
      user-select: none;
    }

    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;
    }

  }


</style>
