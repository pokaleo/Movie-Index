<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please enter a search term"
        v-model="query.queryMsg"
        style="width: 50%"
        v-if="!filterTrigger.clickT">
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
        <el-scrollbar max-height="300px">
          <!--form of additions information, includes categories, AND/NOT search, time filter and color filter-->
          <el-form :model="form" label-width="120px">
            <!--Basic query with a search category default is "By General"-->
            <el-form-item class="demonstration" label="Browse By">
              <el-input
                v-model="query.queryMsg"
                placeholder="Please enter a search term"
                class="input-with-select"
              >
                <template #prepend>
                  <el-select class="selectNot" v-model="query.by" placeholder="Any" style="width: 115px">
                    <el-option label="Any" value="any"/>
                    <el-option label="Title" value="title"/>
                    <el-option label="Keywords" value="keywords"/>
                    <el-option label="Genres" value="genres"/>
                  </el-select>
                </template>
              </el-input>
            </el-form-item>

            <!--Additions and/not/or search-->
            <el-form-item v-for="item in count" :key="item" class="demonstration" label="Alternatives">
              <el-input
                v-model="additions[item-1].q"
                placeholder="Please enter a search term"
                class="input-with-select"
              >
                <template #prepend>
                  <el-select class="selectNot" v-model="additions[item-1].type" placeholder="AND" style="width: 95px">
                    <el-option label="AND" value="1" />
                    <el-option label="OR" value="2" />
                    <el-option label="NOT" value="3" />
                  </el-select>
                  <el-select class="selected" v-model="additions[item-1].by" placeholder="Any" style="width: 95px">
                    <el-option label="Any" value="any"/>
                    <el-option label="Title" value="title"/>
                    <el-option label="Keywords" value="keywords"/>
                    <el-option label="Genres" value="genres"/>
                  </el-select>
                </template>
              </el-input>
            </el-form-item>
            <el-button class="AlterButton" @click="add" v-if="count<maxAdditionsNum">Add A New Request Line</el-button>
            <el-button class="AlterButton" @click="onDelete" v-if="count>0">Delete A Line</el-button>
            <el-form-item class="demonstration" label="Year Range">
              <el-col :span="11">
                <el-input
                v-model="form.time.from"
                placeholder="YYYY">
                <template #prefix>
                  <span class="range">From</span>
                </template>
                </el-input>
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">-</span>
              </el-col>
              <el-col :span="11">
                <el-input
                  v-model="form.time.to"
                  placeholder="YYYY">
                  <template #prefix>
                    <span class="range">To</span>
                  </template>
                </el-input>
              </el-col>
            </el-form-item>
            <el-form-item class="demonstration" label="Language">
              <el-select
                v-model="value3"
                multiple
                collapse-tags
                collapse-tags-tooltip
                clearable
                placeholder="Select"
                style="width: 240px"
              >
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item class="demonstration" label="Film Color">
              <el-checkbox-group v-model="form.color">
                <el-checkbox label="Black/White" />
                <el-checkbox label="Colored" />
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button class="Advancedbutton" type="primary" @click="onSubmit">SEARCH</el-button>
              <el-button class="Advancedbutton" clearable>CLEAR</el-button>
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
  },
  //emits: ["update:modelValue"],
  setup(props){
    const router = useRouter()

    var query = reactive({queryMsg:"", by:""})
    var additions = reactive([{type:"1", by:"any",q:""}])
    var form = reactive({color:[], 
      time:{from:"", to:""}})

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
      let additionalStr = []
      for(let i=0; i<additions.length; i++)
      {
        console.log(additions[i])
        if(additions[i].q != "")
          additionalStr.push([additions[i].type].concat([additions[i].by], [additions[i].q]))
      }
      console.log(additionalStr)
      const passedQuery = {q:query.queryMsg, 
        t:query.by, 
        from: form.time.from, 
        to: form.time.to,
        c:form.color, //array
        more: additionalStr} //array
      router.push({path:"/search",query:passedQuery})
    }
    const add = () => {
      if (count.value < maxAdditionsNum.value)
      {
        count.value++
        additions.push({type:"1",by:"any",q:""})
      }
    }
    const onDelete = () => {
      if (count.value > 0) {
        count.value--
        additions.pop()
      }
    }

    const value3 = ref([])
    const options = [
      {
        value: 'Option1',
        label: 'Option1',
      },
      {
        value: 'Option2',
        label: 'Option2',
      },
      {
        value: 'Option3',
        label: 'Option3',
      },
      {
        value: 'Option4',
        label: 'Option4',
      },
      {
        value: 'Option5',
        label: 'Option5',
      },
    ]
    
    function goSearchResult(){
      router.push({path:"/search",query:{q:query.queryMsg, t:"any"}})
    }

    onActivated(()=>{
      //const router = useRouter()
      query.queryMsg=props.q
      query.by=props.t
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
      maxAdditionsNum,
      value3,
      options
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

.selected{
  margin-left: 20px;
}


img{
  width: 20px;
}

.card{
  height: 400px;
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