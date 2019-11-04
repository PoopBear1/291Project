<template>
    <el-form :model="form"  label-width="150px" ref="form" @submit.native.prevent="submit">
        <el-form-item label="Registration #" prop="regno" :rules="required">
            <el-input v-model.trim="form.regno"></el-input>
        </el-form-item>
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
                regno : ""
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

            let r = await this.$api.post("renew_registration",this.form)

            if (r == 1){
                this.$message({
                    showClose: true,
                    message: "Registration Renewed",
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