<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please enter a search term"
        v-model="query.queryMsg"
        style="width: 50%"
        v-if="!filterTrigger.clickT"
        clearable>
        <template #append>
          <!--router-link :to="'/result/'+selected+'/'+query"-->
          <el-button
            class="searchButton"
            @click="goSearchResult"
          >
            <img src="@/assets/svg/icons8-search.svg" alt="search">
          </el-button>
          <!-- <el-button :icon="Search" /> -->
        </template>
      </el-input>

      <el-button class='advanced' @click="() => toggleBotton('clickT')">
        ADVANCED SEARCH
      </el-button>
      <!--Advanced search panel-->
      <el-card class="card" v-if="filterTrigger.clickT">
        <template #header>
          <div class="card-header">
            <span>Search Filters</span>
          </div>
        </template>
        <el-scrollbar always>
          <!--form of additions information, includes categories, AND/NOT search, time filter and color filter-->
          <el-form :model="form" label-width="120px">
            <!--Basic query with a search category default is "By General"-->
            <el-form-item class="demonstration" label="Proximity Search">
              <el-switch v-model="query.proximity"/>
            </el-form-item>
            <el-form-item class="demonstration" label="Proximity Query" v-if="query.proximity">
              <el-col :span="1">
                <span class="text-gray-500">In</span>
              </el-col>
              <el-col :span="2">
                <el-select class="selectNot" v-model="query.by" placeholder="Any" style="width: 115px">
                    <el-option label="Any" value="any"/>
                    <el-option label="Title" value="title"/>
                    <el-option label="Keywords" value="keywords"/>
                    <el-option label="Genres" value="genre"/>
                </el-select>
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">First word</span>
              </el-col>
              <el-col :span="5">
                <el-input v-model="query.word1" placeholder="1st word" clearable />
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">Second word</span>
              </el-col>
              <el-col :span="5">
                <el-input v-model="query.word2" placeholder="2nd word" clearable />
              </el-col>
              <el-col :span="2" class="text-center">
                  <span class="text-gray-500">Distance</span>
              </el-col>
              <el-col :span="5">
                <el-input-number v-model="query.dist" placeholder="distance" :min="1" controls-position="right" />
              </el-col>
            </el-form-item>
            <el-form-item class="demonstration" label="Browse By" v-else>
              <el-input
                v-model="query.queryMsg"
                placeholder="Please enter a search term"
                class="input-with-select"
                clearable
              >
                <template #prepend>
                  <el-select class="selectNot" v-model="query.by" placeholder="Any" style="width: 115px">
                    <el-option label="Any" value="any"/>
                    <el-option label="Title" value="title"/>
                    <el-option label="Keywords" value="keywords"/>
                    <el-option label="Genres" value="genre"/>
                    <el-option label="Language" value="language"/>
                  </el-select>
                </template>
              </el-input>
            </el-form-item>

            <!--Additions and/not/or search or proximity search-->
            <div v-for="item in count" :key="item">
              <el-form-item class="demonstration" label="Alternatives">
                <el-switch v-model="additions[item-1].proximity" active-text="Proximity Search"/>
              </el-form-item>
              <el-form-item class="demonstration" label="Query" v-if="additions[item-1].proximity">
                <el-col :span="3">
                  <el-select class="selectNot" v-model="additions[item-1].type" placeholder="AND" style="width: 50%" >
                      <el-option label="AND" value="1" />
                      <el-option label="OR" value="2" />
                      <el-option label="NOT" value="3" />
                  </el-select>
                  <el-select class="selected" v-model="additions[item-1].by" placeholder="Any" style="width: 50%" >
                    <el-option label="Any" value="any"/>
                    <el-option label="Title" value="title"/>
                    <el-option label="Keywords" value="keywords"/>
                    <el-option label="Genres" value="genre"/>
                  </el-select>
                </el-col>
                <el-col :span="2" class="text-center">
                  <span class="text-gray-500">First</span>
                </el-col>
                <el-col :span="5">
                  <el-input v-model="additions[item-1].word1" placeholder="1st word" clearable>
                  </el-input>
                </el-col>
                <el-col :span="2" class="text-center">
                  <span class="text-gray-500">Last</span>
                </el-col>
                <el-col :span="5">
                  <el-input v-model="additions[item-1].word2" placeholder="2nd word" clearable>
                  </el-input>
                </el-col>
                <el-col :span="2" class="text-center">
                  <span class="text-gray-500">Distance</span>
                </el-col>
                <el-col :span="5">
                  <el-input-number v-model="additions[item-1].dist" :min="1" controls-position="right" />
                </el-col>
              </el-form-item>
              <el-form-item class="demonstration" label="Query" v-else>
                <el-input
                  v-model="additions[item-1].q"
                  placeholder="Please enter a search term"
                  class="input-with-select"
                  clearable
                >
                  <template #prepend>
                    <el-select class="selectNot" v-model="additions[item-1].type" placeholder="AND" style="width: 95px" >
                      <el-option label="AND" value="1" />
                      <el-option label="OR" value="2" />
                      <el-option label="NOT" value="3" />
                    </el-select>
                    <el-select class="selected" v-model="additions[item-1].by" placeholder="Any" style="width: 95px" >
                      <el-option label="Any" value="any"/>
                      <el-option label="Title" value="title"/>
                      <el-option label="Keywords" value="keywords"/>
                      <el-option label="Genres" value="genre"/>
                    </el-select>
                  </template>
                </el-input>
              </el-form-item>
            </div>

            <el-button class="AlterButton" @click="add" v-if="count<maxAdditionsNum">Add A New Request Line</el-button>
            <el-button class="AlterButton" @click="onDelete" v-if="count>0">Delete A Line</el-button>
            <el-form-item class="demonstration" label="Year Range">
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">From</span>
              </el-col>
              <el-col :span="10">
                <el-input-number
                  v-model="form.time.from"
                  placeholder="YYYY"
                  :min="0"
                  :max="2023"
                  controls-position="right"
                  style="width: 100%"
                  >
                </el-input-number>
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">TO</span>
              </el-col>
              <el-col :span="10">
                <el-input-number
                  v-model="form.time.to"
                  placeholder="YYYY"
                  :max="9999"
                  controls-position="right"
                  style="width: 100%"
                  >
                </el-input-number>
              </el-col>
            </el-form-item>
            <el-form-item class="demonstration" label="Film Color">
              <el-checkbox-group v-model="form.color">
                <el-checkbox label="Black/White" />
                <el-checkbox label="Colored" />
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button class="Advancedbutton" type="primary" @click="onSubmit">SEARCH</el-button>
              <el-button class="Advancedbutton" @click="resetForm" >CLEAR</el-button>
            </el-form-item>
          </el-form>
        </el-scrollbar>
      </el-card>
  </div>
</template>

<script>
import { defineComponent,ref,reactive, onActivated} from 'vue';
import { useRouter } from "vue-router";

//import { getJson } from "serpapi";

export default defineComponent({
  name: "SearchBar",
  props: {
    q: String,
    t: String,
    pro:Boolean
  },
  //emits: ["update:modelValue"],
  setup(props){
    const router = useRouter()

    var query = reactive({
      queryMsg:null, by:"any", 
      proximity:false, word1:null, word2:null, dist:1})

    var additions = reactive([{
      type:"1", by:"any",q:"",
      proximity:false, word1:"", word2:"", dist:1
    }])

    var form = reactive({color:[], 
      time:{from:null, to:null}})
    
    const maxAdditionsNum = ref(5)

    const filterTrigger = ref({
      clickT: false
    })
    //const select = ref(1)
    const toggleBotton = (trigger) => {
      filterTrigger.value[trigger] = !filterTrigger.value[trigger]
    }
    const count = ref(1)

    const onSubmit = () => {
      console.log('submit!')
      console.log(query)
      console.log(additions)
      console.log(form)
      if(query.proximity){
        query.queryMsg = ([query.word1,query.word2,query.dist]).join('+')
      }
      let additionalStr = []
      for(let i=0; i<additions.length; i++){
        console.log(additions[i])
        if(additions[i].proximity){
          if(additions[i].word1 !="" && additions[i].word2 != "" && additions[i].dist != "")
            additionalStr.push([additions[i].type].concat([additions[i].proximity],
                                                          [additions[i].by],
                                                          [([additions[i].word1,additions[i].word2,additions[i].dist]).join('+')]))
        }
        else if(additions[i].q != "") 
          additionalStr.push([additions[i].type].concat([additions[i].by], [additions[i].q]))
      }
      console.log(additionalStr)
      const passedQuery = {
        q:query.queryMsg, 
        t:query.by, 
        from: form.time.from, 
        to: form.time.to,
        c:form.color, //array
        more: additionalStr,
        pro: query.proximity
      } //array
      router.push({path:"/search",
        query:passedQuery, 
        params:
          {w1:query.word1,
          w2:query.word2,
          d:query.dist,}})
    }

    const add = () => {
      if (count.value < maxAdditionsNum.value)
      {
        count.value++
        additions.push({type:"1",by:"any",q:"",
                        proximity:false, word1:"", word2:"", dist:1})
      }
    }
    const onDelete = () => {
      if (count.value > 0) {
        count.value--
        additions.pop()
      }
    }

    const resetForm = () => {
      query.queryMsg = null
      query.by = "any"
      query.proximity=false
      query.word1=null
      query.word2=null
      query.dist=null

      while(count.value > 0){
        onDelete()
      }
      add()
      form.color=[]
      form.time.from=null
      form.time.to=null
    }
    
    function goSearchResult(){
      router.push({path:"/search",query:{q:query.queryMsg, t:"any", pro:false}})
    }

    onActivated(()=>{
      query.queryMsg=props.q
      query.by=props.t
      query.proximity=props.pro
    })

    return{
      query,
      additions,
      goSearchResult,
      filterTrigger,
      toggleBotton,
      count,
      add,
      onDelete,
      form,
      onSubmit,
      resetForm,
      maxAdditionsNum,
    }

    
  }
});
</script>

<style lang="scss" scoped>
.text{
  width: 60%;
  height: 45px;
  outline: hidden;
  margin: auto;
  //border: 1px solid rgb(67, 66, 66);
  background: white;
}
.searchButton{
  background: white;
  height: 45px;
  width: 60px;
}


img{
  width: 20px;
}

.card{
  background-color: white;
}

.demonstration{
  font-size: 18px;
  font-style: oblique;
  font-weight: bold;
  margin-right: 10px;
}

.AlterButton{
  margin-bottom: 10px;
  font-style: italic;
}

.range{
  font-size: 15px;
  font-style: italic;
}

.advanced{
  height: 45px;
  font-weight: bold;
}
.card-header {
  font-size: 20px;
  font-style: oblique;
  font-weight: bold;
  margin-left: 100px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.Advancedbutton{
  width: 200px;
  height: 45px;
  margin-right: 120px;
  font-size: 15px;
  font-style:oblique;
  font-weight: bold;
}


</style>
