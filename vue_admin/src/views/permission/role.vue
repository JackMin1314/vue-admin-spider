<template>
  <div class="app-container">
    <div class="search-input">
      <el-input
        v-model="search"
        placeholder="输入查询"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleEdit"
      />
      <el-button
        class="search-btn el-button--infoSearch"
        icon="el-icon-search"
        @click="submitSearch()"
      ></el-button>
      <el-button :loading="isloading" type="primary" @click="refreshData" icon="el-icon-refresh">刷新</el-button>
    </div>
    <el-table :data="tableData" style="width: 100%;margin-top:30px;" border>
      <el-table-column align="center" label="用户名称" width="150">
        <template v-slot="scope">{{ scope.row.date }}</template>
      </el-table-column>
      <el-table-column align="center" label="用户类型" width="80">
        <template v-slot="scope">
          <!-- {{ scope.row.type }} -->
          <el-tag
            :type="scope.row.type === 'user' ? 'primary' : 'success'"
            disable-transitions
          >{{scope.row.type}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="锁定类型" width="100">
        <template v-slot="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column align="center" label="用户密码" width="300">
        <template v-slot="scope">{{ scope.row.address }}</template>
      </el-table-column>
      <el-table-column align="center" label="用户邮箱" width="180">
        <template v-slot="scope">{{ scope.row.addresss }}</template>
      </el-table-column>
      <el-table-column align="center" label="修改日期" width="180">
        <template v-slot="scope">{{ scope.row.date }}</template>
      </el-table-column>
      <el-table-column align="center" label="账户锁定" width="200">
        <template v-slot="scope">
          <el-switch
            style="margin-right:10px;"
            v-model="scope.row.on"
            active-color="#ff4949"
            inactive-color="#13ce66"
            :active-value="1"
            :inactive-value="0"
            active-text="锁定"
            inactive-text="不锁定"
            @change="changeSwitch($event, scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column align="center" label="相关操作">
        <template v-slot="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope)" icon="el-icon-edit">修改</el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope)"
            icon="el-icon-delete"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { responsetips } from "../../utils/myaxios";

export default {
  data() {
    return {
      tableData: [],
      search: "",
      isloading: false,
      switchvalue: true
    };
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    refreshData() {
      this.isloading = !this.isloading;
      setTimeout(() => {
        this.isloading = false;
        this.clearTable();
      }, 1500);
      this.tableData = [
        {
          type: "admin",
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
          on: "0"
        },
        {
          type: "user",
          date: "2016-05-04",
          name: "Allen",
          address: "上海市普陀区金沙江路 1517 弄",
          on: "1"
        },
        {
          type: "user",
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄",
          on: "0"
        },
        {
          type: "super",
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
          on: "0"
        }
      ];
    },
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
          if (
            item.name.toLowerCase().indexOf(sstring) != -1 ||
            item.name.indexOf(sstring) != -1
          ) {
            // 因为用户名唯一所以通过用户名查找
            rightlist.push(item);
            continue;
          }
          if (item.type.indexOf(sstring) != -1) {
            // 因为用户名唯一所以通过用户名查找
            rightlist.push(item);
            continue;
          }
          if (item.date.indexOf(sstring) != -1) {
            // 因为用户名唯一所以通过用户名查找
            rightlist.push(item);
            continue;
          }
          if (item.address.indexOf(sstring) != -1) {
            // 因为用户名唯一所以通过用户名查找
            rightlist.push(item);
            continue;
          }
        }
        return rightlist;
      } else {
        return "";
      }
    },

    changeSwitch($event, row) {
      // 如果设定状态为锁定那么$event值为1
      if ($event === row.on) {
        console.log($event, row.on);
        if ($event === 1) {
          this.$message({
            showClose: true,
            message: "锁定 " + row.name + " 用户将致其失去核心数据业务",
            type: "warning",
            duration: 3000
          });
          console.log($event);
        }
        if ($event === 0) {
          this.$message({
            showClose: true,
            message: "已解除对 " + row.name + " 用户的锁定",
            type: "success",
            duration: 2500
          });
          console.log($event);
        }
      }
    },

    clearTable() {
      this.tableData.type = "";
      this.tableData.name = "";
      this.tableData.date = "";
      this.tableData.address = "";
    }
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
</style>>