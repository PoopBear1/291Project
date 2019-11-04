<template>
    <div>
        <el-form :model="form"  label-width="150px" ref="form">
            <el-form-item v-for="field in _.keys(form)" :key="field" :prop="field" :label="_.upperFirst(field)">
                <el-input v-model.trim="form[field]"></el-input>
            </el-form-item>
        
            <el-form-item>
                <el-button type="primary" @click="submit">Search</el-button>
            </el-form-item>
        </el-form>
        <el-table v-if="this.matches" :data="this.matches">
            <el-table-column v-for="field in _.keys(form)" :key="field" :label="_.upperFirst(field)" :prop="field"></el-table-column>

            <el-table-column v-if="_.size(this.matches) > 4" >
                <template slot-scope="{row}">
                    <el-button type="primary" @click="openDetail(row)">See Detail</el-button>
                </template>
            </el-table-column>
            <template v-else>
                <el-table-column v-for="field in extra" :key="field" 
                    :label="field == 'regdate' ? 'Latest Registration Date' : _.upperFirst(field)" 
                    :prop="field">
                </el-table-column>
            </template>
        </el-table>
        <el-dialog title="Detail" :visible.sync="visible">
            <el-form  label-width="300px">
                <el-form-item v-for="field in _.keys(form)" :key="field" :label="_.upperFirst(field)">
                    <el-divider direction="vertical"></el-divider>
                    {{row[field]}}
                </el-form-item>
                <el-form-item v-for="field in extra" :key="field" 
                    :label="field == 'regdate' ? 'Latest Registration Date' : _.upperFirst(field)">
                    <el-divider direction="vertical"></el-divider>
                    {{row[field]}}
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data(){
        return {
            form : {
                make : "",
                model : "",
                year : "",
                color : "",
                plate : ""
            },
            row : {},
            visible : false,
            extra : ["regdate","expiry","owner"],
            matches : null
        }
    },
    methods : {
        async submit(){
            if (this._.every(this.form,(value)=>value == "")){
                if (this.msg) this.msg.close()
                this.msg = this.$message({
                    showClose: true,
                    message: "Need at least one field to search",
                    type: 'error'
                })
                return
            }
            this.matches = await this.$api.post("find_car_owner",this.form)
        },
        async openDetail(row){
            this.row = row
            this.visible = true
        }
    }
}
</script>
