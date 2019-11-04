<template>
    <el-form :model="form"  label-width="150px" ref="form">
        <fieldset v-for="(p,type) in form" :key="type">
            <legend >{{_.upperFirst(type)}}</legend>
            <el-form-item label="First Name" :rules="required" :prop="`${type}.fname`">
                <el-input v-model.trim="p.fname"></el-input>
            </el-form-item>
            <el-form-item label="Last Name" :rules="required" :prop="`${type}.lname`">
                <el-input v-model.trim="p.lname"></el-input>
            </el-form-item>

            <el-form-item v-if="type=='child'" label="Gender" :rules="required" :prop="`${type}.gender`">
                <el-radio-group v-model.trim="p.gender">
                    <el-radio-button label="m">Male</el-radio-button>
                    <el-radio-button label="f">Female</el-radio-button>
                </el-radio-group>
            </el-form-item>


            <template v-if="type == 'child' || p.more_info">
                <el-form-item label="Birth Date" :rules="type == 'child' ? [required,notInFuture] : null" :prop="`${type}.bdate`">
                    <el-date-picker v-model.trim="p.bdate" value-format="yyyy-MM-dd"></el-date-picker>
                </el-form-item>
                <el-form-item label="Birth Place" :rules="type == 'child' ? required : null" :prop="`${type}.bplace`">
                    <el-input v-model.trim="p.bplace"></el-input>
                </el-form-item>
            </template>

            <tempalte v-if="p.more_info">
                <el-form-item label="Address" :prop="`${type}.address`">
                    <el-input v-model.trim="p.address"></el-input>
                </el-form-item>
                <el-form-item label="Phone #" :prop="`${type}.phone`">
                    <el-input v-model.trim="p.phone"></el-input>
                </el-form-item>
            </tempalte>
        </fieldset>
    
        <el-form-item>
            <el-button type="primary" @click="submit">Submit</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import {required,notInFuture} from "@/validators"
export default {
    data(){
        return {
            form : {
                child : {
                    fname : "",
                    lname : "",
                    bplace : "",
                    bdate : "",
                    gender : ""
                },
                father : {
                    fname : "",
                    lname : "",
                    bplace : "",
                    bdate : "",
                    phone : "",
                    address : "",
                    more_info : false
                },
                mother : {
                    fname : "",
                    lname : "",
                    bplace : "",
                    bdate : "",
                    phone : "",
                    address : "",
                    more_info : false
                }
            },
            required,notInFuture
        }
    },
    methods : {
        async submit(){
            try{
                await this.$refs.form.validate();
            } catch {
                return
            }

            let r = await this.$api.post("register_birth",this.form)

            if (r == 1){
                this.$message({
                    showClose: true,
                    message: "Birth Registered",
                    type: 'success'
                })
                this.$refs.form.resetFields()
                this.form.father.more_info = false
                this.form.mother.more_info = false
            } else if (r.error){
                this.$message({
                    showClose: true,
                    message: r.error,
                    type: 'error'
                })
            } else if (r.more_info_required){
                this._.each(r.more_info_required,type=>{
                    this.form[type].more_info = true
                })
                this.$message({
                    showClose: true,
                    message: "Need more info about" + this._.join(r.more_info_required," & "),
                    type: 'warning'
                })
            }
        }
    }
}
</script>