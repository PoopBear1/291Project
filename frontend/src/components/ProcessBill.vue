<template>
    <el-form :model="form"  label-width="150px" ref="form">
        <el-form-item label="VIN #" prop="vin" :rules="required">
            <el-input v-model.trim="form.vin"></el-input>
        </el-form-item>

        <el-form-item label="Plate" prop="plate" :rules="required">
            <el-input v-model.trim="form.plate"></el-input>
        </el-form-item>

        <template v-for="(p,type) in form">
            <fieldset  v-if="_.isObject(p)"  :key="type">
                <legend >{{_.upperFirst(type)}}</legend>
                <el-form-item label="First Name" :rules="required" :prop="`${type}.fname`">
                    <el-input v-model.trim="p.fname"></el-input>
                </el-form-item>
                <el-form-item label="Last Name" :rules="required" :prop="`${type}.lname`">
                    <el-input v-model.trim="p.lname"></el-input>
                </el-form-item>
            </fieldset>
        </template>
    
        <el-form-item>
            <el-button type="primary" @click="submit">Submit</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import {required} from "@/validators"
export default {
    data(){
        return {
            form : {
                seller : {
                    fname : "",
                    lname : ""
                },
                buyer : {
                    fname : "",
                    lname : ""
                },
                vin : "",
                plate : ""
            },
            required
        }
    },
    methods : {
        async submit(){
            try{
                await this.$refs.form.validate();
            } catch {
                return
            }

            let r = await this.$api.post("process_bill",this.form)

            if (r == 1){
                this.$message({
                    showClose: true,
                    message: "Bill Processed",
                    type: 'success'
                })
                this.$refs.form.resetFields()
            } else if (r.error){
                this.$message({
                    showClose: true,
                    message: r.error,
                    type: 'error'
                })
            } 
        }
    }
}
</script>