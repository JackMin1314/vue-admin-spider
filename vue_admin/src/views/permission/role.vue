<template>
  <div class="app-container">
    <!-- 头部输入框和刷新按钮 -->
    <div class="search-input">
      <el-input v-model="search" placeholder="输入查询" style="width: 300px;" class="filter-item" />
      <el-button
        class="search-btn el-button--infoSearch"
        icon="el-icon-search"
        @click="submitSearch"
      ></el-button>
      <el-button :loading="isloading" type="primary" @click="refreshData" icon="el-icon-refresh">刷新</el-button>
    </div>
    <!-- 主体表格部分 舍弃了 :span-method="mySpanMethod"合并单元格-->
    <el-table
      v-loading="listLoading"
      :data="tableData"
      style="width: 100%;margin-top:30px;"
      cell-style="font-weight: 600;"
      fit
      highlight-current-row
      border
    >
      <el-table-column fixed align="center" label="用户名称" width="150">
        <template v-slot="scope">{{ scope.row.USER_NAME }}</template>
      </el-table-column>
      <el-table-column align="center" label="用户类型" width="80">
        <template v-slot="scope">
          <el-tag
            :type="scope.row.USER_TYPE | typeFilter"
            disable-transitions
          >{{scope.row.USER_TYPE}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="锁定类型" width="100">
        <template v-slot="scope">{{ scope.row.USER_LOCK }}</template>
      </el-table-column>

      <el-table-column align="center" label="用户邮箱" width="180">
        <template v-slot="scope">{{ scope.row.USER_MAIL }}</template>
      </el-table-column>
      <el-table-column align="center" label="修改日期" width="180">
        <template v-slot="scope">{{ scope.row.SUBMISSION_DATE }}</template>
      </el-table-column>
      <!-- switch锁定按钮部分 -->
      <el-table-column align="center" label="账户锁定" width="200">
        <template v-slot="scope">
          <el-switch
            style="margin-right:10px;"
            v-model="scope.row.USER_LOCK"
            :active-value="1"
            :inactive-value="0"
            active-color="#ff4949"
            inactive-color="#13ce66"
            active-text="锁定"
            inactive-text="不锁定"
            @change="changeSwitch($event, scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <!-- 修改和删除部分 -->
      <el-table-column align="center" label="相关操作" width="300">
        <template v-slot="scope">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(scope.$index,scope.row)"
            icon="el-icon-edit"
          >修改</el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.$index,scope.row)"
            icon="el-icon-delete"
          >删除</el-button>
          <!-- 修改按钮的dialog弹窗内容 -->
          <el-dialog title="修改" align="left" :visible.sync="dialogFormVisible" :modal="false">
            <el-form :model="dialog_obj">
              <el-form-item label="用户名称" :label-width="'120px'">
                <el-input v-model="dialog_obj.USER_NAME" size="small" :disabled="true"></el-input>
              </el-form-item>
              <!-- dialog弹窗用户类型部分 -->
              <el-form-item label="用户类型" align="left" :label-width="'120px'">
                <el-select v-model="dialog_obj.USER_TYPE" placeholder="请选择用户类型">
                  <el-option label="普通用户" value="user"></el-option>
                  <el-option label="管理员" value="admin"></el-option>
                </el-select>
              </el-form-item>
              <!-- dialog弹窗锁定类型部分 -->
              <el-form-item label="锁定类型" :label-width="'120px'">
                <el-select v-model="dialog_obj.USER_LOCK" placeholder="请选择锁定类型">
                  <el-option label="未锁定" :value="0"></el-option>
                  <el-option label="锁定" :value="1"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="用户邮箱" :label-width="'120px'">
                <el-input v-model="dialog_obj.USER_MAIL" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="修改日期" :label-width="'120px'">
                <el-input v-model="dialog_obj.SUBMISSION_DATE" size="small" :disabled="true"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="changeRole(dialog_obj)">提 交</el-button>
            </div>
          </el-dialog>
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">高权限用户才可以修改低权用户</el-table-column>
    </el-table>
  </div>
</template>

<script>
import { responsetips } from "../../utils/myaxios";
import { getStorageExpire, setStorageExpire } from "../../utils/mycookie";

export default {
  filters: {
    typeFilter(type) {
      const typeMap = {
        super: "warning",
        admin: "success",
        user: "primary"
      };
      return typeMap[type];
    }
  },
  data() {
    return {
      tableData: [],
      search: "",
      isloading: false,
      switchvalue: true,
      dialogFormVisible: false,
      listLoading: false,
      dialog_obj: {
        type: "",
        date: "",
        name: "",
        email: "",
        on: ""
      }
    };
  },
  created() {
    //在页面加载时读取sessionStorage里的状态信息

    if (sessionStorage.getItem("userlistMsg")) {
      this.tableData = JSON.parse(sessionStorage.getItem("userlistMsg"));
    }

    //在页面刷新时将vuex里的信息保存到sessionStorage里

    window.addEventListener("beforeunload", () => {
      sessionStorage.setItem("userlistMsg", JSON.stringify(this.tableData));
    });
  },
  methods: {
    // 修改按钮事件
    handleEdit(index, row) {
      this.dialogFormVisible = true;
      let _row = row;
      this.dialog_obj = _row; // 将当前行数据获取并传给dialog的table里面
      console.log(index, row);
    },
    // 删除按钮事件
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该用户, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          // 执行删除用户操作，如果没有删除成功则responsetips弹窗提示
          this.$axios.get("/").then(get_resp => {
            this.$axios
              .post("/delete_user", {
                username: getStorageExpire("username"),
                csrf_token: get_resp.headers["csrf_token"],
                othername: row.USER_NAME,
                otheremail: row.USER_MAIL
              })
              .then(res => {
                if (res.data) {
                  // res是响应对象,里面data字段会保存后端返回的json数据
                  console.log("post change_role_data:", res.data);
                  // 根据请求的返回code进行对于弹窗提示
                  responsetips(res);
                  // 如果请求到用户列表数据的时候
                  if (res.data.code === "0") {
                    // 成功刷新列表
                    // 前端删掉这行数据
                    this.tableData.splice(index, 1);
                    setTimeout(() => {
                      this.fetch_userList();
                    }, 1500);
                  }
                } else {
                  console.log("post chagnerole用户列表请求结果为空...");
                }
              })
              .catch(err => {
                if (error.response) {
                  console.log(error.response.data);
                  console.log(error.response.status);
                  console.log(error.response.headers);
                } else {
                  console.log("err:", error.message);
                }
                console.log(error.config);
              });
          });

          // 删除失败则不经行任何操作responsetips弹窗提示
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    // 刷新按钮事件
    refreshData() {
      this.isloading = true;
      this.listLoading = true;
      this.fetch_userList();
      this.isloading = false;
      // setStorageExpire("fetched", "1", 0.05);
    },
    // 搜索按钮事件
    submitSearch() {
      var result;
      result = this.searchFromData(this.search);

      if (result.length > 0) {
        this.isloading = false;
        this.tableData = result;
      } else {
        this.$message({
          showClose: true,
          message: "未查询到相关信息，请刷新后重试",
          duration: 1500
        });
      }
    },
    // 重新修改了，支持字符串匹配
    searchFromData(sstring) {
      if (sstring) {
        var item;
        var rightlist = [];
        for (let index = 0; index < this.tableData.length; index++) {
          item = this.tableData[index];
          // 用户名称匹配
          if (
            item.name.toLowerCase().indexOf(sstring) != -1 ||
            item.name.indexOf(sstring) != -1
          ) {
            rightlist.push(item);
            continue;
          }
          // 用户类型匹配
          if (item.type.indexOf(sstring) != -1) {
            rightlist.push(item);
            continue;
          }
          // 锁定类型匹配
          if (item.on == sstring) {
            rightlist.push(item);
            continue;
          }
          // 用户邮箱匹配
          if (item.email.indexOf(sstring) != -1) {
            rightlist.push(item);
            continue;
          }
          // 用户修改日期匹配
          if (item.date.indexOf(sstring) != -1) {
            rightlist.push(item);
            continue;
          }
        }
        return rightlist;
      } else {
        return "";
      }
    },
    // 按钮改变的时触发的实践
    changeSwitch($event, row) {
      // 如果设定状态为锁定那么$event值为1
      if ($event === row.USER_LOCK) {
        console.log($event, row.USER_LOCK);
        if ($event === 1) {
          this.$message({
            showClose: true,
            message: "锁定 " + row.USER_NAME + " 用户将致其失去核心数据业务",
            type: "warning",
            duration: 3000
          });
          console.log($event);
        }
        if ($event === 0) {
          this.$message({
            showClose: true,
            message: "已解除对 " + row.USER_NAME + " 用户的锁定",
            type: "success",
            duration: 2500
          });
          console.log($event);
        }
      }
    },
    // 修改了用户的数据后提交
    changeRole(dialog_obj) {
      this.dialogFormVisible = false;
      this.$axios.get("/").then(get_resp => {
        this.$axios
          .post("/change_role", {
            username: getStorageExpire("username"),
            csrf_token: get_resp.headers["csrf_token"],
            othername: dialog_obj.USER_NAME,
            new_othertype: dialog_obj.USER_TYPE,
            new_otherlock: dialog_obj.USER_LOCK
          })
          .then(res => {
            if (res.data) {
              // res是响应对象,里面data字段会保存后端返回的json数据
              console.log("post change_role_data:", res.data);
              // 根据请求的返回code进行对于弹窗提示
              responsetips(res);
              // 如果请求到用户列表数据的时候
              if (res.data.code === "0") {
                // 成功刷新列表
                this.fetch_userList();
              }
            } else {
              console.log("post chagnerole用户列表请求结果为空...");
            }
          })
          .catch(err => {
            if (error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else {
              console.log("err:", error.message);
            }
            console.log(error.config);
          });
      });
    },
    // 清空表格
    clearTable() {
      this.tableData.type = "";
      this.tableData.name = "";
      this.tableData.date = "";
      this.tableData.address = "";
    },
    // post请求后端获取用户列表
    fetch_userList() {
      this.$axios.get("/").then(get_resp => {
        this.$axios
          .post("/user_list", {
            username: getStorageExpire("username"),
            csrf_token: get_resp.headers["csrf_token"]
          })
          .then(res => {
            if (res.data) {
              // res是响应对象,里面data字段会保存后端返回的json数据
              console.log("post resp_data:", res.data);
              // 根据请求的返回code进行对于弹窗提示
              responsetips(res);
              // 如果请求到用户列表数据的时候
              if (res.data.code === "0") {
                this.listLoading = true;
                this.tableData = res.data.data;
                this.listLoading = false;
                this.$store.commit("set_userlistMsg", this.tableData); //修改保存数据
              }
            } else {
              console.log("post 用户列表请求结果为空...");
            }
          })
          .catch(err => {
            if (error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else {
              console.log("err:", error.message);
            }
            console.log(error.config);
          });
      });
    }
    // 合并最后一列单元格
    // mySpanMethod({ rowIndex, columnIndex }) {
    //   // 定位到最后一列（备注部分）
    //   if (columnIndex === 7) {
    //     // 第0行是字段部分
    //     return {
    //       rolspan: rowIndex,
    //       colspan: 1
    //     };
    //   }
    // },
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  .roles-table {
    margin-top: 30px;
  }
  .permission-tree {
    margin-bottom: 30px;
  }
}
</style>