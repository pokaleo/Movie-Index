<template>
    <div id="KeyWordsBar">
      <div class="footer">
        <div class="sidebar-content">
          <div class="sidebar-header">
            <p>Keywords <i class="count">{{ keywords.length }} Total</i></p>
          </div>
          <el-divider class="sidebar-divider"/>
          <div>

            <el-space class="sidebar-body" wrap>
              <el-button
                  class="tag"
                  v-for="keyword in collapse()"
                  :key="keyword"
                  color="#8794c0"
                  @click="jumpLink(keyword)"
                  round
              >
              {{keyword}}
              </el-button>
              <el-button 
                class="tag"
                color="#d2d5e9"
                v-if="keywords.length > 5"
                @click="showAll"
                round
              >{{ instruction() }}</el-button>
            </el-space>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { ElMessageBox} from 'element-plus'
import { useRouter } from "vue-router";
import {ref,computed} from "vue";
export default{
    name: "KeyWordsBar",
    props:['keywords'],
    setup(props){
      const router = useRouter()
      const leng = ref(5)
      const isShow = ref(false)
      const jumpLink=(keyword)=>{
        ElMessageBox.confirm(
          'Do you want to see all other movies including the keyword of "'+keyword+'" ?',
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
      const showAll=()=>{
        if (isShow.value){
          leng.value = 5
          isShow.value = false
        }
        else{
          leng.value = props.keywords.length
          isShow.value = true
        }
        console.log("Showall")
      }

      const collapse= computed(()=>{
        return function (){
          return props.keywords.slice(0,leng.value)
        }
      })

      const instruction= computed(()=>{
        return function (){
          if (props.keywords.length > 5 ){
            if( isShow.value)
              return 'Show Less'
            else
              return '+ '+ (props.keywords.length - leng.value)
          }
          return ""
        }
      })
      return{
        jumpLink,
        collapse,
        showAll,
        instruction
      }
    }
}
</script>

<style scoped>

.footer{
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    text-align: center;
}


.sidebar-body{
  justify-content: space-around;
  
}

.sidebar-body::after {
    content: '';
    flex: auto;  
}

p{
    font-style: oblique;
    font-size: x-large;
    font-weight:200;
}
.tag{
    margin-top: 2px;
    color: black;
    font-size: small;
}

.count{
  font-size: large;
}
</style>
