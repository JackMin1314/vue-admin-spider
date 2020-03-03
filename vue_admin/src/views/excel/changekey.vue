<template>
  <div class="sendbug-main">
    <div class="documentation-container">
      <el-steps :active="active" aligin="center" simple style="margin-top: 20px">
        <el-step title="原始密码"></el-step>
        <el-step title="新的密码" icon="el-icon-edit"></el-step>
        <el-step title="再次输入" icon="el-icon-edit"></el-step>
        <el-step title="提交" icon="el-icon-upload"></el-step>
      </el-steps>
    </div>
    <div class="changekey">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="原始密码" prop="prePass">
          <el-input
            type="password"
            v-model="ruleForm.prePass"
            autocomplete="off"
            show-password
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="新的密码" prop="newPass">
          <el-input
            type="password"
            v-model="ruleForm.newPass"
            autocomplete="off"
            show-password
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input
            type="password"
            v-model="ruleForm.checkPass"
            autocomplete="off"
            show-password
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { AESEncrypt, getStorageExpire } from "../../utils/mycookie";
import { validUsername } from "../../utils/validate";
import { responsetips } from "../../utils/myaxios";
export default {
  name: "changekey",
  data() {
    // 原始密码校验
    const validate_prePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入原始密码"));
      } // validUsername只是一个输入的正则检测，符合为true，不符合为false
      else if (validUsername(value) && value.length >= 6) {
        // 验证成功
        this.active = 1;
        callback();
      } else {
        this.active = 0;
        callback(new Error("密码长度低于6位或含有特殊字符"));
      }
    };
    // 新密码校验
    const validate_newPass = (rule, value, callback) => {
      if (value === "") {
        this.active = 1;
        callback(new Error("请输入新的密码"));
      } // validUsername只是一个输入的正则检测，符合为true，不符合为false
      else if (validUsername(value) && value.length >= 6) {
        // 验证成功
        this.active = 2;
        callback();
      } else {
        this.active = 1;
        callback(new Error("密码长度低于6位或含有特殊字符"));
      }
    };
    // 再次输入新密码校验
    const validate_checkPass = (rule, value, callback) => {
      if (value === "") {
        this.active = 2;
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.newPass) {
        this.active = 2;
        callback(new Error("两次输入密码不一致!"));
      } else {
        this.active = 3;
        callback();
      }
    };
    return {
      ruleForm: {
        prePass: "",
        newPass: "",
        checkPass: ""
      },
      active: 0,
      // 表单验证规则
      rules: {
        prePass: [
          { required: true, validator: validate_prePass, trigger: "blur" }
        ],
        newPass: [
          { required: true, validator: validate_newPass, trigger: "blur" }
        ],
        checkPass: [
          { required: true, validator: validate_checkPass, trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    // 提交事件按钮
    submitForm(formName) {
      // 当所有的表单都正确输入的时候
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$axios.get("/").then(res => {
            this.$axios
              .post("/update_passwd", {
                csrf_token: res.headers["csrf_token"],
                username: getStorageExpire("username"),
                old_passwd: AESEncrypt(this.ruleForm.prePass),
                new_passwd: AESEncrypt(this.ruleForm.newPass)
              })
              .then(resp => {
                // 清空输入表单
                this.resetForm("ruleForm");
                responsetips(resp);
                if (resp.data.code === "0") {
                  this.active = 5;
                  // 修改成功后服务端清楚了原始密码和登陆记录，因而要立即退出，用新密码重新登录。故清楚本地localstorage数据
                  localStorage.clear();
                  setTimeout(() => {
                    this.$router.push({
                      path: "/"
                    });
                  }, 1500);
                }
              });
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 重置事件按钮,参数是绑定的表单名称
    resetForm(formName) {
      this.active = 0;
      this.$refs[formName].resetFields();
    }
  }
};
</script>


<style lang="scss" scoped>
.documentation-container {
  width: 800px;
  margin: 0 auto;
}
.changekey {
  position: relative;
  width: 500px;
  max-width: 100%;
  padding: 40px 35px 0;
  margin: 0 auto;
  overflow: hidden;
}
</style>
