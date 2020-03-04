<template>
  <div class="handler-log">
    <el-table
      v-loading="listLoading"
      :data="tableData"
      border
      fit
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column fit="true" align="center" label="文件名">
        <template slot-scope="scope">
          <span>{{ scope.row.filename}}</span>
        </template>
      </el-table-column>

      <el-table-column fit="true" align="center" label="文件大小">
        <template slot-scope="scope">
          <span>{{ scope.row.filesize }}</span>
        </template>
      </el-table-column>

      <el-table-column fit="true" align="center" label="创建日期">
        <template slot-scope="scope">
          <span>{{ scope.row.maketime }}</span>
        </template>
      </el-table-column>

      <el-table-column fit="true" align="center" label="Actions">
        <template slot-scope="scope">
          <el-button
            type="primary"
            icon="el-icon-download"
            @click="download(scope.$index,scope.row)"
            circle
            plain
          ></el-button>
          <el-button
            type="danger"
            icon="el-icon-delete"
            @click="handledelete(scope.$index, scope.row)"
            circle
            plain
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { responsetips } from "../../utils/myaxios";
import { getStorageExpire } from "../../utils/mycookie";
import { Form } from "element-ui";
export default {
  name: "handler-log",
  data() {
    return {
      tableData: [],
      listLoading: false
    };
  },
  created() {
    this.get_fileslist_info();
  },
  methods: {
    download(index, row) {
      this.$axios("/").then(res => {
        this.$axios({
          method: "POST",
          url: "/download_logdb",
          data: {
            csrf_token: res.headers["csrf_token"],
            username: getStorageExpire("username"),
            filename: row.filename
          },
          responseType: "blob"
        }).then(resp => {
          responsetips(resp);
          if (resp.data.code != "-1") {
            if (resp.status === 200) {
              let url = window.URL.createObjectURL(resp.data);
              let link = document.createElement("a");
              link.style.display = "none";
              link.href = url;
              link.setAttribute("download", row.filename);
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link); // 创建完a标签后删除
            }
          }
        });
      });
    },
    handledelete(index, row) {
      this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          // 执行删除用户操作，如果没有删除成功则responsetips弹窗提示
          this.$axios.get("/").then(get_resp => {
            this.$axios
              .post("/handle_logdb", {
                username: getStorageExpire("username"),
                csrf_token: get_resp.headers["csrf_token"],
                filename: row.filename
              })
              .then(res => {
                if (res.data) {
                  // 根据请求的返回code进行对于弹窗提示
                  responsetips(res);
                  // 如果请求到用户列表数据的时候
                  if (res.data.code === "0") {
                    // 成功刷新列表
                    // 判断是否为服务日志,否则前端删掉这行数据
                    if (row.filename.indexOf(".txt") != -1) {
                      return;
                    } else {
                      this.tableData.splice(index, 1);
                    }
                  }
                }
              })
              .catch(err => {
                if (error.response) {
                  console.log(error.response.data);
                  console.log(error.response.status);
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
    get_fileslist_info() {
      this.$axios
        .get("/errlogs_db_info")
        .then(resp => {
          responsetips(resp);
          if (resp.data) {
            if (resp.data.code == "0") {
              this.listLoading = true;
              this.tableData = resp.data.data;
              this.listLoading = false;
            }
          }
        })
        .catch(err => {
          console.log("errlogs_db_info出错:", err);
          console.log(err.data);
        });
    }
  }
};
</script>

<style lang="scss"  scoped>
</style>