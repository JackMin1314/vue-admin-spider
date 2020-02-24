<template>
  <div class="block">
    <!--粒子特效-->
    <div class="lizi">
      <vue-particles
        color="#fff"
        :particle-opacity="0.7"
        :particles-number="60"
        shape-type="circle"
        :particle-size="4"
        lines-color="#fff"
        :lines-width="1"
        :line-linked="true"
        :line-opacity="0.4"
        :lines-distance="150"
        :move-speed="2"
        :hover-effect="true"
        hover-mode="grab"
        :click-effect="true"
        click-mode="push"
      />
    </div>
    <!--窗体容器-->
    <div class="login-container">
      <!--    主体登录窗口-->
      <el-form
        ref="loginForm"
        :model="loginForm"
        status-icon
        :rules="loginRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container">
          <h3 class="title">Spider 登录界面</h3>
        </div>
        <!--        prop一定必须要写在<el-form-item>上面，写在里面的input上或者其他任何地方都不行（el-form-item prop属性绑定）-->
        <el-form-item prop="username">
          <el-tooltip class="item" effect="dark" content="输入用户名" placement="left">
            <span class="svg-container">
              <svg-icon icon-class="user" />
            </span>
          </el-tooltip>
          <el-tooltip content="仅支持大小写字母、下划线、数字、- _ ? ! * @.中的字符命名" placement="right-start" effect="light" :hide-after="4000">
            <el-input
              ref="username"
              v-model="loginForm.username"
              placeholder="Username"
              name="username"
              type="text"
              tabindex="1"
              auto-complete="off"
            />
          </el-tooltip>
        </el-form-item>

        <el-form-item prop="password">

          <el-tooltip class="item" effect="dark" content="输入密码" placement="left">
            <span class="svg-container">
              <svg-icon icon-class="password" />
            </span>
          </el-tooltip>
          <el-tooltip content="仅支持大小写字母、下划线、数字、- _ ? ! * @.中的字符字符且长度6个或以上" placement="right-start" effect="light" :hide-after="4000">
            <el-input
              :key="passwordType"
              ref="password"
              v-model="loginForm.password"
              :type="passwordType"
              placeholder="Password"
              name="password"
              tabindex="2"
              auto-complete="off"
              @keyup.enter.native="handleLogin"
            />
          </el-tooltip>
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

        <!-- <el-form-item prop="email">
          <el-tooltip class="item" effect="dark" content="输入QQ邮箱" placement="left">
            <div class="email-container">
              <i class="el-icon-message" />
            </div>
          </el-tooltip>
          <el-tooltip content="目前仅支持QQ邮箱注册" placement="right-start" effect="light" :hide-after="4000">
            <el-input
              ref="email"
              v-model="loginForm.email"
              placeholder="QQ mail"
              name="username"
              type="text"
              tabindex="1"
              auto-complete="off"
            />
          </el-tooltip>
        </el-form-item> -->

        <el-tooltip class="item" effect="dark" content="点击登录" placement="left">
          <el-button
            :loading="loading"
            type="primary"
            style="width:100%;margin-bottom:30px;"
            @click.native.prevent="handleLogin"
          >Login
          </el-button>
        </el-tooltip>
        <!--        用户注册部分-->
        <div class="register">
          <span style="font-size: 15px; color: white">没有账号，立即
          <el-link type="primary" style="font-size: 15px" @click="open"><u>加入我们 </u><i class="el-icon-position" />
          </el-link>
          </span>
          <div class="drawer-class">
            <!--避免默认有遮罩,添加：modal="false"取消-->
            <el-drawer
              ref="drawer"
              title="我嵌套了 Form !"
              :with-header="false"
              :before-close="handleClose"
              :modal="false"
              :visible.sync="dialog"
              direction="rtl"
              custom-class="demo-drawer"
            >
              <div class="demo-drawer__content">
                <el-page-header content="" style="color:black" @back="cancelForm" />
                <!--              头部内容欢迎-->
                <div class="drawer-header">
                  <span style="font-size: 44px;color: black">
                    欢迎注册<strong>Spider</strong>
                  </span>
                  <p style="font-size:22px;color:#333333;">每一天，乐在使用。</p>
                </div>
                <!-- 注册部分用户名 -->
                <div class="register-input">
                  <i class="el-icon-user" style="font-size:16px;color: #2ac06d;padding-left: 20px" />
                  <!--登录表格部分-->
                  <el-tooltip content="用户密码不要包含中文、空格特殊字符等" placement="top-end" effect="light">
                  <el-input
                    v-model="regisForm.username"
                    placeholder="用户名"
                    clearable
                    @change="checkRegisUsername"
                  />
                  </el-tooltip>
                  <!-- 注册部分密码 -->
                  <i class="el-icon-key" style="font-size:16px;color: #2ac06d;padding-left: 20px" />
                  <el-input
                    :key="passwordType2"
                    v-model="regisForm.password"
                    placeholder="密码"
                    :type="passwordType2"
                    clearable
                    @change="checkRegisPassword"
                  />
                  <!-- 注册部分密码的展示 -->
                  <span class="show-regis-pwd" @click="showPwd2">
                    <svg-icon :icon-class="passwordType2 === 'password' ? 'eye' : 'eye-open'" />
                  </span>
                  <!-- 注册部分邮箱 -->
                  <i class="el-icon-message" style="font-size:16px;color: #2ac06d;padding-left: 20px" />
                  <el-tooltip content="当前仅支持QQ邮箱注册" placement="top-end" effect="light">
                  <el-input
                    v-model="regisForm.email"
                    placeholder="QQ邮箱"
                    clearable
                    @change="checkRegisEmail"
                  />
                  </el-tooltip>
                  <!-- 注册部分获取验证码 -->
                  <el-button type="primary" plain="plain" :disabled="isDisable" @click="sendcode">{{ buttonText }}</el-button>
                  <el-input
                    v-model="regisForm.capture"
                    placeholder="验证码"
                    :disabled="isEmailDisable"
                    clearable
                    class="input-capture"
                  />
                   <!-- 注册部分确认注册 -->
                  <div class="sure_button">
                   <el-button type="primary" icon="el-icon-thumb" round :disabled="isDisable" @click="handleRegis">确认注册</el-button>
                  </div>
                </div>
                <!--                底部图片-->
                <div class="demo-drawer__footer">
                  <img src="../../assets/avatar/panda.gif" style="margin-top:5px">
                </div>
              </div>
            </el-drawer>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
// 引入需要添加的

import { validUsername } from '../../utils/validate'
import { responsetips } from '../../utils/myaxios'
import { AESEncrypt, setStorageExpire } from '../../utils/mycookie'
// import { getCookie } from '../../utils/mycookie'
export default {
  name: 'Login',
  data() {
    // 自定义的验证函数一定要执行得到callback，if,else都需要添加callback()函数。
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('用户名为空或含有空格、特殊字符'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      // validUsername只是一个输入的正则检测，符合为true，不符合为false
      if (validUsername(value) && value.length >= 6) {
        // 验证成功可以
        callback()
      } else {
        callback(new Error('密码长度低于6位或含有特殊字符'))
      }
    }

    return {
      loginForm: {
        username: '',
        password: '',
        email: ''
      },
      regisForm: {
        username: '',
        password: '',
        email: '',
        capture: '',
        isEmail: false,
        isUsername: false,
        isPassword: false
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
        // email: [
        //   { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        //   { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        // ]
      },
      buttonText: '发送验证码',
      loading: false,
      passwordType: 'password',
      passwordType2: 'password',
      redirect: undefined,
      isDisable: true,  // 验证码按钮是否disable，true为按钮失效
      isEmailDisable: true,
      csrf_token: '',
      // add for register  panel
      dialog: false,
      timer: null
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
   // 函数部分
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
    showPwd2() {
      if (this.passwordType2 === 'password') {
        this.passwordType2 = ''
      } else {
        this.passwordType2 = 'password'
      }
      // 注册功能输入框并没有绑定到ref。点击展示按钮时候会触发原有的登录验证
      this.$nextTick(() => {
        //this.$refs.password.focus()
      })
    },
    checkRegisUsername() {
      var value = this.regisForm.username
      if(!value){
        this.regisForm.isUsername = false
         this.$notify({
          message: '用户名不能为空，请重新输入',
          type: 'error',
          duration: 2500
        })
      }
      if(value){
        this.regisForm.isUsername = validUsername(value)
        if(!this.regisForm.isUsername)
        {
          this.$notify({
          message: '用户名不合法，请重新输入',
          type: 'error',
          duration: 2500
        })
        }
      }
      },
    checkRegisPassword() {
      var myvalue = this.regisForm.password
      // 密码为空则为长度小于6
      if(myvalue.length<6){
        this.regisForm.isPassword = false
         this.$notify({
          message: '密码长度小于6位',
          type: 'error',
          duration: 2500
        })
        return
      }
      // 当密码长度大于6进行验证
      if(myvalue){
        this.regisForm.isPassword = validUsername(myvalue)
        if(!this.regisForm.isPassword) {
          this.$notify({
          message: '密码不合法，请重新输入',
          type: 'error',
          duration: 2500
          })
        }
        }
      },
    checkRegisEmail() {
      var value = this.regisForm.email
      if (!value) {
        this.regisForm.isEmail = false
        this.isDisable = true
        this.buttonText = '发送验证码'
        this.regisForm.isEmailDisable = true
      }
      if (value) {
        setTimeout(() => {
          var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
          if (!reg.test(value)) {
            // this.$message('请输入有效的电子邮箱！')
             this.$notify({
              message: '请输入有效的电子邮箱！',
              type: 'error',
              duration: 2500
            })
            this.regisForm.isEmail = false
            this.isDisable = true
            this.regisForm.isEmailDisable = true
          } else {
            this.isDisable = false
            console.log('right')
            this.regisForm.isEmail = true
          }
        }, 500)
      }
    },
    // 登录请求
    getcsrf_login() {
      // axios默认会返回Promise实例，成功fulfilled状态调用.then，失败rejected状态时then方法捕捉到Promise的状态为rejected，调用.catch
      // 对于Promise对象成功的时候可以一直调用.then只要保证上一个状态时fulfilled就行。。
      // then 是回调函数，因而在上一个请求成功后会调用.then然后结束返回promise对象。
      // 为了保证get请求成功，this.csrf_token任然不变,应该立即执行post。都结束时候get的promise对象才会返回

      this.$axios.get('/').then((res) => {
        if (res.data) {
          console.log('get resp_data:', res.data)
          // console.log('get res.header.csrf:', res.headers['csrf_token'])
          this.csrf_token = res.headers['csrf_token']
          console.log(this.csrf_token)
        } else {
          console.log('get / 请求结果为空...')
        }
        const cpwd = AESEncrypt(this.loginForm.password)
        // 在 获取到csrf_token立即执行post
        this.$axios.post('/login', {
          'csrf_token': this.csrf_token,
          'username': this.loginForm.username,
          // 这里添加了加密后的密码，然后发给后端
          'passwd': cpwd
        }).then(res => {
          if (res.data) {
            console.log('post resp_data:', res.data)
            // 根据请求的返回code进行对于弹窗提示
            responsetips(res)
            // 请求成功通过
            if (res.data.code === '0') {
              this.loading = true
              // 这里进行了请求拦截，参考permission.js
              this.$router.push({
                path: this.redirect || '/dashboard'
              })
              this.loading = false
              // 本地保存相关数据包括加密的数据
              setStorageExpire('username', this.loginForm.username, 24)
              setStorageExpire('password', cpwd, 24)
            }
          } else {
            console.log('post login 请求结果为空...')
          }
        }).catch(error => {
          if (error.response) {
            console.log(error.response.data)
            console.log(error.response.status)
            console.log(error.response.headers)
          } else {
            console.log('err:', error.message)
          }
          console.log(error.config)
        })
      })
    },
    // 注册请求
    getcsrf_regis() {
      this.$axios.get('/').then((res) => {
        if (res.data) {
          console.log('get resp_data:', res.data)
          // console.log('get res.header.csrf:', res.headers['csrf_token'])
          this.csrf_token = res.headers['csrf_token']
          console.log(this.csrf_token)
        } else {
          console.log('get / 请求结果为空...')
        }
        const cpwd = AESEncrypt(this.regisForm.password)
        // 在 获取到csrf_token立即执行post
        this.$axios.post('/register', {
          'email': this.regisForm.email,
          'csrf_token': this.csrf_token,
          'username': this.regisForm.username,
          // 这里添加了加密后的密码，然后发给后端
          'passwd': cpwd,
          'capture': this.regisForm.capture
        }).then(res => {
          if (res.data) {
            console.log('post resp_data:', res.data)
            // 根据请求的返回code进行对于弹窗提示
            responsetips(res)
            // 请求成功通过
            if (res.data.code === '0') {
              this.loading = true
              // 这里进行了请求拦截，参考permission.js
              // 本地保存相关数据包括加密的数据
              setStorageExpire('username', this.regisForm.username, 24)
              setStorageExpire('password', cpwd, 24)
              this.$router.push({
                path: this.redirect || '/dashboard'
              })
              this.loading = false
            } else {
              // 没通过的话清空前端的storage
              localStorage.removeItem('username')
              localStorage.removeItem('password')
            }
          } else {
            console.log('post register 请求结果为空...')
          }
        }).catch(error => {
          if (error.response) {
            console.log(error.response.data)
            console.log(error.response.status)
            console.log(error.response.headers)
          } else {
            console.log('err:', error.message)
          }
          console.log(error.config)
        })
      })
    },
    // 登录事件
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 如果表单数据校验通过,axios请求后端接口
          this.getcsrf_login()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 注册事件
    handleRegis() {
      console.log(this.regisForm.isUsername, this.regisForm.isPassword, this.regisForm.isEmail, this.regisForm.capture)
      if (this.regisForm.isUsername && this.regisForm.isPassword && 
      this.regisForm.isEmail && this.regisForm.capture) {
        // 均符合要求的时候可以注册
        this.getcsrf_regis()
      } else {
        
      }
    },
    // add for register panel
    handleClose(done) {
      if (this.loading) {
        return
      }
      this.$confirm('确定要提交表单吗？')
        .then(_ => {
          //this.loading = true
          this.timer = setTimeout(() => {
            done()
            // 动画关闭需要一定的时间
            setTimeout(() => {
              this.loading = false
            }, 400)
          }, 2000)
        })
        .catch(_ => {
        })
    },
    cancelForm() {
      this.loading = false
      this.dialog = false

      clearTimeout(this.timer)
      this.loading = false
    },
    // add for pannel  register message trips
    open() {
      this.$message({
        showClose: true,
        message: '欢迎新用户注册',
        type: 'success',
        duration: 2000
      })
      this.dialog = true
    },
    // 请求发送邮箱验证码前提邮箱通过验证
    getcsrf_regis_emailCode() {
      this.$axios.get('/get_capture', {
          params:{'email': this.regisForm.email}
        }).then(res => {
          if (res.data) {

            console.log('post resp_data:', res.data)
            // 根据请求的返回code进行对于弹窗提示
            responsetips(res)
          } else {
            console.log('post register 请求结果为空...')
          }
        }).catch(error => {
          if (error.response) {
            console.log(error.response.data)
            console.log(error.response.status)
            console.log(error.response.headers)
          } else {
            console.log('err:', error.message)
          }
          console.log(error.config)
        })
    },
    // 邮箱验证码事件
    sendcode() {
      this.checkRegisEmail()
      if (this.regisForm.isEmail && this.regisForm.email !== '') {
        console.log('email is ok')
        this.$notify({
          title: '发送成功',
          message: '请尽快前往' + this.regisForm.email + '邮箱查收!',
          type: 'success',
          duration: 2500
        })
        this.buttonText = '已发送'
        this.isDisable = true
        this.isEmailDisable = false
        // 请求发送验证码
        this.getcsrf_regis_emailCode()
      } else {
        this.buttonText = '发送验证码'
        this.isEmailDisable = true
        console.log('email error')
      }
    }
  }
}
</script>

<style lang="scss">
  /* 修复input 背景不协调 和光标变色 */
  /* 修改第三方全局样式必须在全局的style修改（不含scope），修改特定组件需要定位到具体可区分的位置*/
  /* 下面的代码会覆盖上面的代码，局部代码会覆盖全局代码；实际开发过程中，遵循先处理全局的样式，在修改局部样式*/

  $bg: #283443;
  $light_gray: #fff;
  $cursor: #fff;

  /* reset 全局的 element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 40px;
      width: 85%;

      input {
        background: transparent;
        -webkit-appearance: none;
        border-radius: 0;
        color: $light_gray;
        border: none;
      }
    }

    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.3);
      border-radius: 8px;
      color: #454545;
    }

  }

  /*修改局部的样式*/
  .register {
    .el-input {
      input {
        color: black;
        padding-left: 15px;
        background: transparent;
        border-radius: 43px;
      }
    }
  }

</style>

<style lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;
  /*在scope里面更改element-ui的样式解析时候任然会被element-ui全局样式替换掉*/

  .block {
    background-repeat: no-repeat;
    background-size: 100% 100%;
    position: fixed;
    height: 100%;
    width: 100%;
    /* 粒子特效style*/
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

    .login-container {
      min-height: 100%;
      width: 100%;
      overflow: hidden;

      .login-form {
        position: relative;
        width: 520px;
        max-width: 100%;
        padding: 160px 35px 0;
        margin: 0 auto;
        overflow: hidden;
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

      .title-container {
        position: relative;

        .title {
          font-size: 26px;
          color: $light_gray;
          margin: 0 auto 40px auto;
          text-align: center;
          font-weight: bold;
        }
      }

      .show-pwd {
        position: absolute;
        right: 10px;
        top: 7px;
        font-size: 16px;
        color: black;
        cursor: pointer;
        user-select: none;
      }
    }

    .register {
      font-size: 14px;
      margin-bottom: 10px;

      /*登录下面的注册提示文字*/
      .tips {
        font-size: 14px;
        color: #fff;
        margin-bottom: 10px;
      }

      span {
        color: white;
        position: relative;
      }

      /* 抽屉div*/
      .drawer-class {
        width: 100%;
        height: 100%;
        position: absolute;
        background: transparent;

        /* 抽屉主体部分div*/
        .demo-drawer__content {
          margin-top: 10px;

          margin-left: 20px;
          position: fixed;
          padding-top: 15px;

          /* 头部欢迎文字*/
          .drawer-header {
            margin-top: 30px;
            margin-left: 20px;
            background: transparent;

          }

          /* 下方的图片img标签样式*/
          img {
            background: transparent;
            position: relative;
            width: auto;
            height: auto;
            max-width: 100%;
            max-height: 100%;
            padding-left: 40px;
            background-size: auto;
            background-repeat: no-repeat;
            // 这里添加的是为了解决下方图片将确认注册按钮遮住导致点击失败
            pointer-events:none;
          }

        }

      }

      .regis-form {
        position: relative;
        width: 520px;
        max-width: 100%;
        padding: 160px 35px 0;
        margin: 0 auto;
        overflow: hidden;
      }

      .show-regis-pwd {
        position: absolute;
        right: 80px;
        font-size: 16px;
        padding-top: 18px;
        color: black;
        cursor: pointer;
        user-select: none;
      }
      .sure_button {
        position: absolute;
        padding-top: 10px;
        right: 60px;
      }
    }
  }
</style>
