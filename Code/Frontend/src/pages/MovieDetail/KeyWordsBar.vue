<template>
    <div id="KeyWordsBar">
      <div class="sidebar">
        <div class="sidebar-content">
          <div class="sidebar-header">
            <p>Keywords</p>
          </div>
          {{ keywords.length }} Total
          <el-divider class="sidebar-divider"/>
          <div class="sidebar-body">
            <el-scrollbar height="450px" always>
            <el-space direction="vertical">
            <el-button
                class="tag"
                v-for="keyword in keywords"
                :key="keyword"
                color="BBEAFF"
                @click="jumpLink(keyword)"
                round
            >
            {{keyword}}
            </el-button>
          </el-space>
          </el-scrollbar>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { ElMessageBox} from 'element-plus'
import { useRouter } from "vue-router";
export default{
    name: "KeyWordsBar",
    props:['keywords'],
    setup(){
      const router = useRouter()
      const jumpLink=(keyword)=>{
        ElMessageBox.confirm(
          'Do you want to search results of "'+keyword+'"?',
          'Search',
          {
            confirmButtonText: 'YES',
            cancelButtonText: 'Cancel',
            type: 'info',
          })
          .then(()=>{
            router.push({path:"/search",query:{q:keyword, t:"keywords", pro:false, check:false}})
          })
          .catch(()=>{
            console.log("Jump Cancel!")
          })
      }
      return{
        jumpLink
      }
    }
}
</script>

<style scoped>

.sidebar{
    display: flex;
    flex-direction: column;
    width: 200px;
    justify-items: center;
    align-items: center;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    text-align: center;
}

p{
    font-style: oblique;
    font-size: x-large;
    font-weight:200;
}
.sidebar-body{
    flex-direction: column;
    flex-wrap: wrap;
}
.tag{
    margin-top: 10px;
    margin: 5px;
    color: black;
    font-size: small;
}
</style>