<template>
    <el-form :model="form"  label-width="150px" ref="form">
        <el-form-item label="Ticket #" prop="tno" :rules="required">
            <el-input v-model.trim="form.tno"></el-input>
        </el-form-item>

        <el-form-item label="Amount" prop="amount" :rules="[required,positiveNum]">
            <el-input type="number" v-model.trim.number="form.amount"></el-input>
        </el-form-item>
    
        <el-form-item>
            <el-button type="primary" @click="submit">Submit</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import {required,positiveNum} from "@/validators"
export default {
    data(){
        return {
            form : {
                tno : "",
                amount : ""
            },
            required, positiveNum
        }
    },
    methods : {
        async submit(){
            try{
                await this.$refs.form.validate();
            } catch {
                return
            }

            let r = await this.$api.post("process_payment",this.form)

            if (r.remain != null){
                this.$message({
                    showClose: true,
                    message: "Ticket processed" + (r.remain ? `, $${r.remain} remains` : ''),
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