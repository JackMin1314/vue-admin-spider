(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-357ec460"],{"09cc":function(e,t,r){},8277:function(e,t,r){"use strict";var s=r("09cc"),a=r.n(s);a.a},e492:function(e,t,r){"use strict";r.r(t);var s=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"sendbug-main"},[r("div",{staticClass:"documentation-container"},[r("el-steps",{staticStyle:{"margin-top":"20px"},attrs:{active:e.active,aligin:"center",simple:""}},[r("el-step",{attrs:{title:"原始密码"}}),r("el-step",{attrs:{title:"新的密码",icon:"el-icon-edit"}}),r("el-step",{attrs:{title:"再次输入",icon:"el-icon-edit"}}),r("el-step",{attrs:{title:"提交",icon:"el-icon-upload"}})],1)],1),r("div",{staticClass:"changekey"},[r("el-form",{ref:"ruleForm",attrs:{model:e.ruleForm,"status-icon":"",rules:e.rules,"label-width":"100px"}},[r("el-form-item",{attrs:{label:"原始密码",prop:"prePass"}},[r("el-input",{attrs:{type:"password",autocomplete:"off","show-password":"",clearable:""},model:{value:e.ruleForm.prePass,callback:function(t){e.$set(e.ruleForm,"prePass",t)},expression:"ruleForm.prePass"}})],1),r("el-form-item",{attrs:{label:"新的密码",prop:"newPass"}},[r("el-input",{attrs:{type:"password",autocomplete:"off","show-password":"",clearable:""},model:{value:e.ruleForm.newPass,callback:function(t){e.$set(e.ruleForm,"newPass",t)},expression:"ruleForm.newPass"}})],1),r("el-form-item",{attrs:{label:"确认密码",prop:"checkPass"}},[r("el-input",{attrs:{type:"password",autocomplete:"off","show-password":"",clearable:""},model:{value:e.ruleForm.checkPass,callback:function(t){e.$set(e.ruleForm,"checkPass",t)},expression:"ruleForm.checkPass"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.submitForm("ruleForm")}}},[e._v("提交")]),r("el-button",{on:{click:function(t){return e.resetForm("ruleForm")}}},[e._v("重置")])],1)],1)],1)])},a=[],o=r("82af"),c=r("61f7"),l=r("b2a6"),n={name:"changekey",data:function(){var e=this,t=function(t,r,s){""===r?s(new Error("请输入原始密码")):Object(c["c"])(r)&&r.length>=6?(e.active=1,s()):(e.active=0,s(new Error("密码长度低于6位或含有特殊字符")))},r=function(t,r,s){""===r?(e.active=1,s(new Error("请输入新的密码"))):Object(c["c"])(r)&&r.length>=6?(e.active=2,s()):(e.active=1,s(new Error("密码长度低于6位或含有特殊字符")))},s=function(t,r,s){""===r?(e.active=2,s(new Error("请再次输入密码"))):r!==e.ruleForm.newPass?(e.active=2,s(new Error("两次输入密码不一致!"))):(e.active=3,s())};return{ruleForm:{prePass:"",newPass:"",checkPass:""},active:0,rules:{prePass:[{required:!0,validator:t,trigger:"blur"}],newPass:[{required:!0,validator:r,trigger:"blur"}],checkPass:[{required:!0,validator:s,trigger:"blur"}]}}},methods:{submitForm:function(e){var t=this;this.$refs[e].validate((function(e){if(!e)return console.log("error submit!!"),!1;t.$axios.get("/").then((function(e){t.$axios.post("/update_passwd",{csrf_token:e.headers["csrf_token"],username:Object(o["b"])("username"),old_passwd:Object(o["a"])(t.ruleForm.prePass),new_passwd:Object(o["a"])(t.ruleForm.newPass)}).then((function(e){t.resetForm("ruleForm"),Object(l["b"])(e),"0"===e.data.code&&(t.active=5,localStorage.clear(),setTimeout((function(){t.$router.push({path:"/"})}),1500))}))}))}))},resetForm:function(e){this.active=0,this.$refs[e].resetFields()}}},i=n,u=(r("8277"),r("2877")),p=Object(u["a"])(i,s,a,!1,null,"1c43bdec",null);t["default"]=p.exports}}]);