<template>
  <div class="app-container">
    <!-- 主体表格部分 舍弃了 :span-method="mySpanMethod"合并单元格-->
    <el-table
      v-loading="listLoading"
      :data="tableData"
      style="width: 100%;margin-top:30px;"
      :cell-style="tableWholeStyle"
      fit
      :row-class-name="tableRowClassStyle"
      highlight-current-row
      border
    >
      <el-table-column fit="true" align="center" label="资源名称">
        <template v-slot="scope">{{scope.row.key}}</template>
      </el-table-column>
      <el-table-column fit="true" align="center" label="使用情况">
        <template v-slot="scope">{{scope.row.value}}</template>
      </el-table-column>
      <el-table-column fit="true" align="center" label="当前时间">
        <template v-slot="scope">{{scope.row.timestr}}</template>
      </el-table-column>
    </el-table>
    <div>{{timestr}}</div>
  </div>
</template>

<script>
import roleVue from "../permission/role.vue";
export default {
  data() {
    return {
      tableData: [],
      listLoading: false,
      mytimer: ""
    };
  },
  methods: {
    // 全局的字体和样式
    tableWholeStyle({ row, column, rowIndex, columnIndex }) {
      return "font-weight: 500;";
    },
    // 针对行的样式
    tableRowClassStyle({ row, rowIndex }) {
      if (rowIndex === 8) {
        return "other-row-color";
      } else if (rowIndex === 2) {
        return "warning-row";
      } else if (rowIndex === 3) {
        return "success-row";
      } else if (rowIndex === 5) {
        return "error-row";
      } else if (rowIndex === 0 || rowIndex === 1) {
        return "space-color";
      } else if (rowIndex === 6) {
        return "cpu-color";
      } else if (rowIndex === 7) {
        return "net-up-color";
      } else if (rowIndex === 4) {
        return "space-color";
      }
      return "";
    },
    currentTime() {
      // 每秒请求服务器获取信息(服务器会有一秒sleep测网速)
      this.mytimer = setInterval(this.getMachineInfo, 2000);
    },
    // 前端构造时间
    getDate: function() {
      var _this = this;
      let timeorigin = new Date();
      let year = timeorigin.getFullYear(); //年
      let month = timeorigin.getMonth() + 1; //月
      let day = timeorigin.getDate(); //日
      let time =
        timeorigin.getHours() +
        ":" +
        timeorigin.getMinutes() +
        ":" +
        timeorigin.getSeconds();
      _this.timestr = year + "年" + month + "月" + day + "日" + "  " + time;
    },
    getMachineInfo() {
      this.$axios.get("/machine_info").then(resp => {
        // 请求成功也不进行弹窗展示已经session缓存，避免造成打扰
        if (resp.data) {
          if (resp.data.code == "0") {
            this.listLoading = true;
            this.tableData = resp.data.data;
            this.listLoading = false;
          }
        }
      });
    }
  },
  create() {
    this.getMachineInfo();
  },
  mounted() {
    this.currentTime();
  },
  // 销毁定时器
  beforeDestroy: function() {
    clearInterval(this.mytimer); // 在Vue实例销毁前，清除时间定时器
  }
};
</script>

<style>
/* 如果需要设置表格行的样式需要在全局里面改掉el-table的样式*/
.el-table .other-row-color {
  background: #caf3ff;
}
.el-table .warning-row {
  background: oldlace;
}
.el-table .success-row {
  background: #f0f9eb;
}
.el-table .error-row {
  background: rgb(200, 173, 196);
}
.el-table .cpu-color {
  background: #a7a8bd;
}
.el-table .net-up-color {
  background: #b9dec9;
}
.el-table .space-color {
  background: rgb(245, 247, 250);
}
</style>

<style lang="scss" scoped>
.app-container {
  margin: 0 auto;
}
</style>