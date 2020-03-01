<template>
<div class="sendbug-main">

  <div class="documentation-container">
   <el-card class="box-card">
   <el-tabs v-model="activeName">
      <el-tab-pane label="Contact with QQ" name="directly">
        <svg-icon icon-class="qq" style="width: 20px;display: inline-block;"/>
        <el-input v-model="inputQQ" :disabled="true" placeholder="Please input" style="width:400px;max-width:100%;padding-left:10px;" />
        <el-button type="primary" icon="el-icon-document" @click="handleCopy(inputQQ,$event)">
          复制
        </el-button>
      </el-tab-pane>
      <el-tab-pane label="Contact with WeChat" name="v-directive">
        <svg-icon icon-class="wechat" style="width: 20px;display: inline-block;"/>
        <el-input v-model="inputWeChat" :disabled="true" placeholder="Please input" style="width:400px;max-width:100%;padding-left:10px" />
         <el-button type="primary" icon="el-icon-document" @click="handleCopy(inputWeChat,$event)">
          复制
        </el-button>
      </el-tab-pane>
    </el-tabs>
   </el-card>
   </div>
   
   <div class="git-issue">
     <!-- <el-card class="box-card" shadow="hover">   -->
       <div class="svg-class">
            <svg-icon icon-class="github"/>
       </div>
          <div class="component-item">
             <a href="https://github.com/JackMin1314/vue-admin-spider/issues" class="link-mallki">
              <strong>去Github提个issue吧</strong>
              <strong>
                <span data-letters="去Github提个issue吧"></span>
                <span data-letters="去Github提个issue吧"></span>
              </strong>
              </a>
            </div>
        <!-- </el-card> -->
  </div>
</div>
</template>

<script>
import clip from '@/utils/clipboard'
export default {
  name: 'Documentation',
  data() {
    return {
      activeName: 'directly',
      inputQQ: '1416825008',
      inputWeChat: 'll520828116',
    }
  },
  methods: {
     handleCopy(text, event) {
      clip(text, event)
    },
    clipboardSuccess() {
      this.$message({
        message: 'Copy successfully',
        type: 'success',
        duration: 1500
      })
    }
  }
}
</script>




<style lang="scss" scoped>

.git-issue {
  height: 50px;
  margin: 0 auto;
  width: 250px;
}
.sendbug-main {
   background-color: #f0f2f5;
  padding-top: 20px;
  min-height: calc(100vh - 84px);
}
.documentation-container {
  margin: 100px;
  margin-bottom: 50px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;

}




a {
  display: inline-block;
  font-size: 20px;
  margin: 10px 0 20px;
  }

        [class*="link-"] {
            outline: none;
            text-decoration: none;
            position: relative;
            line-height: 1;
            display: inline-block;
        }

        .link-mallki {
            color:rgb(48, 49, 54);
            -webkit-transition: color 0.5s 0.25s;
            transition: color 0.5s 0.35s;
            overflow: hidden;
        }

        .link-mallki:hover {
            -webkit-transition: none;
            transition: none;
            color: transparent;
        }

        .link-mallki::before {
            content: '';
            width: 100%;
            height: 2px;
            margin: -3px 0 0 0;
            background: lightgreen;
            position: absolute;
            left: 0;
            top: 50%;
            -webkit-transform: translate3d(-100%, 0, 0);
            transform: translate3d(-100%, 0, 0);
            -webkit-transition: -webkit-transform 0.4s;
            transition: transform 0.4s;
            -webkit-transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
            transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
        }

        .link-mallki:hover::before {
            -webkit-transform: translate3d(100%, 0, 0);
            transform: translate3d(100%, 0, 0);
        }

        .link-mallki span {
            position: absolute;
            height: 50%;
            width: 100%;
            left: 0;
            top: 0;
            overflow: hidden;
        }

        .link-mallki span::before {
            content: attr(data-letters);
            position: absolute;
            left: 0;
            width: 100%;
            color: deepskyblue;
            -webkit-transition: -webkit-transform 0.5s;
            transition: transform 0.3s;
        }

        .link-mallki span:nth-child(2) {
            top: 50%;
        }

        .link-mallki span:first-child::before {
            top: 0;
            -webkit-transform: translate3d(0, 100%, 0);
            transform: translate3d(0, 100%, 0);
        }

        .link-mallki span:nth-child(2)::before {
            bottom: 0;
            -webkit-transform: translate3d(0, -100%, 0);
            transform: translate3d(0, -100%, 0);
        }

        .link-mallki:hover span::before {
            -webkit-transition-delay: 0.3s;
            transition-delay: 0.3s;
            -webkit-transform: translate3d(0, 0, 0);
            transform: translate3d(0, 0, 0);
            -webkit-transition-timing-function: cubic-bezier(0.2, 1, 0.3, 1);
            transition-timing-function: cubic-bezier(0.2, 1, 0.3, 1);
        }
</style>
