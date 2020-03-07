<template>
  <div class="dashboard-container">
    <div class="table-main">
      <el-card shadow="hover" :body-style="{ height:'600px'  }">
        <div class="input-class">
          <el-tooltip class="item" effect="dark" content="IT之家的网址url" placement="bottom-start">
            <el-input
              v-model="searchURL"
              placeholder="请输入IT之家的网址"
              :clearable="true"
              size="medium"
              style="width: 90%;margin: 0  auto"
              suffix-icon="el-icon-edit"
              @change="validateinput"
            >
              <!-- <template slot="prepend">URL:</template> -->
            </el-input>
          </el-tooltip>
          <el-button type="primary" plain circle style="margin-left:5px;" @click="postSpider">
            <svg-icon icon-class="search" />
          </el-button>
        </div>
        <div class="button-download">
          <el-button
            type="primary"
            :loading="isloading"
            :disabled="isdisable"
            round
            style="margin:0 auto;"
            @click="downloadfile"
          >
            <i class="el-icon-upload"></i>文件下载
          </el-button>
        </div>
        <div class="progress-main">
          <el-progress
            :text-inside="true"
            :stroke-width="24"
            :percentage="percentnum"
            :color="colors"
          ></el-progress>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { validIthomeURL } from "../../utils/validate";
import { getStorageExpire } from "../../utils/mycookie";
import { responsetips } from "../../utils/myaxios";
export default {
  name: "Dashboard",
  data() {
    return {
      searchURL: "",
      url_status: false,
      spider_file_name: "",
      isloading: false,
      isdisable: true,
      percentnum: 0,
      task_id: "",
      timer: null,
      colors: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#6f7ad3", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#5cb87a", percentage: 100 }
      ]
    };
  },
  methods: {
    validateinput() {
      const result = validIthomeURL(this.searchURL);
      if (result) {
        this.url_status = true;
        this.$message({
          message: "IT之家URL监测通过",
          type: "success",
          duration: 1500
        });
      } else {
        this.url_status = false;
        this.searchURL = "";
        this.$message({
          message: "请检查输入URL是否正确",
          type: "warning",
          duration: 1500
        });
      }
    },
    postSpider() {
      this.$axios
        .get("/")
        .then(res => {
          this.isloading = true;
          // 这段请求响应时间很长会导致超时，首次采用请求后端，后端根据url hash为一个值作为任务id，存在session中，id值返回给前端。
          // 前端异步轮询另一个接口判断任务后端id是否完成，如果后端任务id完成，session['hash的id']==True；然后前端在执行download
          this.$message({
            message: "爬取时间较长，请稍等...",
            type: "warning",
            duration: 1500
          });
          // 请求获取耗时的任务id
          this.$axios
            .post("/it_spider", {
              csrf_token: res.headers["csrf_token"],
              username: getStorageExpire("username"),
              spiderurl: this.searchURL
            })
            .then(resp => {
              responsetips(resp);
              if (resp.data.code == "0") {
                this.task_id = resp.data.data;
                console.log("spider task_id is:", this.task_id);
                this.isloading = true;
                this.isdisable = true;
                //
                this.timer = setInterval(this.spiderStatus, 5000);
              }
            });
        })
        .catch(err => {
          this.isloading = false;
          this.isdisable = true;
          console.log(err);
        });
    },
    spiderStatus() {
      // 请求后端数据是否准备好了
      console.log("下载按钮isloading状态", this.isloading);
      if (this.isloading) {
        this.$axios
          .get("/spider_status", {
            params: { task_id: this.task_id }
          })
          .then(resp => {
            // 数据准备好了，可拿到文件名
            if (resp.data.code == "0") {
              responsetips(resp);
              this.spider_file_name = resp.data.data;
              this.isloading = false;
              this.isdisable = false;
            } else {
              this.isdisable = true;
              this.isloading = true;
            }
          });
      }
    },
    downloadfile() {
      if (this.spider_file_name) {
        const url =
          "/download_file?username=" +
          getStorageExpire("username") +
          "&" +
          "filename=" +
          encodeURIComponent(this.spider_file_name);
        this.$axios({
          methods: "get",
          url: url,
          responseType: "blob",
          onDownloadProgress: progress => {
            // 计算已经下载和总大小的百分比，保留两位小数.箭头函数可以使用this.正常的函数参数传递那种就不能使用this.了
            if (progress.lengthComputable) {
              this.percentnum =
                (progress.loaded / progress.total) * (100).toFixed(2);
              console.log(this.percentnum);
            }
          }
        })
          .then(resp => {
            responsetips(resp);

            if (resp.status === 200) {
              let url = window.URL.createObjectURL(resp.data);
              let link = document.createElement("a");
              link.style.display = "none";
              link.href = url;
              link.setAttribute("download", this.spider_file_name);
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link); // 创建完a标签后删除
              //
              clearInterval(this.timer);
            }
          })
          .catch(err => {
            console.log(err);
            console.log(err.data);
          });
      } else {
        this.$message({
          message: "数据还没有准备好,请稍等",
          type: "warning",
          duration: 1500
        });
      }
    }
  },
  // mounted() {
  //   this.timer = setInterval(this.spiderStatus, 5000);
  // },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>

<style lang="scss" scoped>
.table-main {
  width: 75%;
  margin: 0 auto;
  margin-top: 30px;
  position: relative;
}
.input-class {
  margin-left: 10%;
}
.progress-main {
  margin: 0 auto;
  width: 60%;
  margin-top: 50px;
  position: relative;
}
.button-download {
  width: 30%;
  margin-top: 40px;
  margin-left: 40%;
  margin-bottom: 10px;
}
</style>
