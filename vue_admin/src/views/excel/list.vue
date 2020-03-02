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
    <el-table
      v-loading="listLoading"
      :data="tableData"
      border
      fit
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column fit="true" align="center" label="用户">
        <template slot-scope="scope">
          <span>{{ scope.row.username }}</span>
        </template>
      </el-table-column>

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
    <!-- 添加回到顶部按钮 -->
    <BackToTop />
    <!-- <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />-->
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"; // Secondary package based on el-pagination
import BackToTop from "@/components/BackToTop";
import { getStorageExpire, setStorageExpire } from "../../utils/mycookie";
import { responsetips } from "../../utils/myaxios";
export default {
  name: "ArticleList",
  components: { Pagination, BackToTop },
  data() {
    return {
      tableData: [],
      total: 0,
      listLoading: false,
      isloading: false,
      search: "",
      listQuery: {
        page: 1,
        limit: 20
      }
    };
  },
  created() {
    if (sessionStorage.getItem("userlistInfo")) {
      this.tableData = JSON.parse(sessionStorage.getItem("userlistInfo"));
    } else {
      this.get_fileslist_info();
    }

    //在页面刷新时将vuex里的信息保存到sessionStorage里

    window.addEventListener("beforeunload", () => {
      sessionStorage.setItem("userlistInfo", JSON.stringify(this.tableData));
    });
  },
  methods: {
    // getList() {
    //   this.listLoading = true;
    //   fetchList(this.listQuery).then(response => {
    //     this.list = response.data.items;
    //     this.total = response.data.total;
    //     this.listLoading = false;
    //   });
    // }
    download(index, row) {
      // 前端进行转义避免后端解析的时候将文件名解析成其他的字符例如: ”我的C++学习笔记.md“变成了”我的C 学习笔记.md“丢失了空格
      // 因为+在url中会被转义成空格
      var url =
        "/download_file?username=" +
        getStorageExpire("username") +
        "&filename=" +
        encodeURIComponent(row.filename);
      this.$axios({
        method: "get",
        url: url,
        responseType: "blob" //binary large object 二进制大对象
      }).then(resp => {
        // 这里要处理的是对于已经删除的文件，浏览器缓存访问可能导致返回404。直接跳到写好的404页面
        // if (resp.status == 404) {
        //   this.$router.push({
        //     path: "/404"
        //   });
        // }
        //因为修改了axios的拦截器，不用再每个组件请求后面判断一次了。统一由响应拦截器进行判断404、401
        // 解决每次请求的时候都响应了，但是没出现下载页面，下到了network里面.
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
      });
    },
    handledelete(idnex, row) {},
    // 刷新按钮事件
    refreshData() {
      this.isloading = true;
      this.listLoading = true;
      this.get_fileslist_info();
      this.isloading = false;
      // setStorageExpire("fetched", "1", 0.05);
      sessionStorage.setItem("userlistInfo", JSON.stringify(this.tableData));
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
            item.username.toLowerCase().indexOf(sstring) != -1 ||
            item.username.indexOf(sstring) != -1
          ) {
            rightlist.push(item);
            continue;
          }
          // 文件名匹配
          if (item.filename.indexOf(sstring) != -1) {
            rightlist.push(item);
            continue;
          }
          // 创建时间匹配
          if (item.maketime.indexOf(sstring) != -1) {
            rightlist.push(item);
            continue;
          }
        }
        return rightlist;
      } else {
        return "";
      }
    },
    get_fileslist_info() {
      this.$axios
        .get("/user_files_info", {
          params: { username: getStorageExpire("username") }
        })
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
          console.log("get_fileslist_info出错:", err);
          console.log(err.data);
        });
    }
  }
};
</script>

<style scoped>
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>
